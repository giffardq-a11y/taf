// Rejoue le solveur hors navigateur et écrit sur la sortie standard le plan d'occupation,
// en JSON, tel que `planning_cible.py` l'attend.
//
//   node planning_runner.js <classeur.xlsx> [date-de-référence] [options...]
//
// Options : --variante=N  --sans-optimiseur  --flux-tendu  --en-cours-de-cycle
//           --sans-staggering  --budget=ms
//
// Le noyau du solveur est extrait de `index.html` tel quel, entre ses deux marqueurs : le
// planning exporté est donc calculé par le même code que l'interface, jamais par une copie.
const fs = require('fs'), vm = require('vm'), path = require('path');
const XLSX = require('xlsx');

const args = process.argv.slice(2);
const positionnels = args.filter(a => !a.startsWith('--'));
const option = (nom, defaut) => {
  const a = args.find(x => x === `--${nom}` || x.startsWith(`--${nom}=`));
  if (!a) return defaut;
  return a.includes('=') ? a.split('=').slice(1).join('=') : true;
};

const classeur = positionnels[0];
if (!classeur) { console.error('usage : node planning_runner.js <classeur.xlsx> [date-réf] [options]'); process.exit(2); }
const dateRef = positionnels[1] || new Date().toISOString().slice(0, 10);

const source = fs.readFileSync(path.join(__dirname, 'index.html'), 'utf8');
const noyau = source.match(/\/\* ==== SOLVEUR-CORE-DEBUT ====[\s\S]*?\/\* ==== SOLVEUR-CORE-FIN ==== \*\//);
if (!noyau) { console.error('noyau du solveur introuvable dans index.html'); process.exit(3); }

const bac = {
  console: {log(){}, warn(){}, error(){}}, Date, Math, Object, Array, Map, Set, Number, String,
  JSON, RegExp, isNaN, parseFloat, parseInt, Infinity, NaN, XLSX,
  document: {getElementById: () => null},
};
bac.globalThis = bac;
vm.createContext(bac);
vm.runInContext(noyau[0] + `;globalThis.__api = {
  set wb(v){ wb = v }, get elements(){ return elements }, get speConfig(){ return speConfig },
  get sequencesInputs(){ return sequencesInputs }, get lastJournal(){ return lastJournal },
  get lastChangements(){ return lastChangements }, get lastRetards(){ return lastRetards },
  get lastKPI(){ return lastKPI }, set sequenceChoisie(v){ sequenceChoisie = v },
  parseWorkbook, runSimulation, optimiserSequence, sequenceCourante, STAGGER, REGLES,
};`, bac);
const api = bac.__api;

api.STAGGER.actif = !option('sans-staggering', false);
api.wb = XLSX.read(fs.readFileSync(classeur), {type: 'buffer', cellDates: true});
api.sequenceChoisie = parseInt(option('variante', '1'), 10) - 1;
api.parseWorkbook(dateRef);

// Mêmes réglages que la page de restitution : sans cela le « meilleur scénario » exporté ici
// ne serait pas celui que l'utilisateur voit à l'écran.
const params = {
  dateRef: new Date(dateRef),
  seuilParkingSem: 4, floatUpSem: 1, hookupSem: 0.5, ballastSem: 1, placesStockageSPE: 1,
  arretAuPlusTot: !option('flux-tendu', false),
  accelererEnCoursCycle: !option('sans-accel-cycle', false),
  vacances: !option('sans-vacances', false),
  floatUpUnique: !option('sans-porte-unique', false),
  jourCoulage: !option('sans-jour-coulage', false),
  bassinLibre: !option('sans-bassin-libre', false),
};

if (option('sans-optimiseur', false)) {
  api.runSimulation({...params, silencieux: true});
} else {
  api.optimiserSequence(params, {budgetMs: parseInt(option('budget', '12000'), 10)});
  api.runSimulation({...params, silencieux: true});
}

const iso = d => d ? new Date(d).toISOString().slice(0, 10) : null;
const NOM = {1: 'PL-1', 2: 'PL-2', 3: 'PL-3', 4: 'PL-4', 5: 'PL-5', 6: 'SPE'};
const sortie = {
  classeur: path.basename(classeur),
  dateRef,
  parametres: {
    variante: api.sequenceChoisie + 1,
    optimiseur: !option('sans-optimiseur', false),
    arretAuPlusTot: params.arretAuPlusTot,
    accelererEnCoursCycle: params.accelererEnCoursCycle,
    vacances: params.vacances, jourCoulage: params.jourCoulage,
    bassinLibre: params.bassinLibre, floatUpUnique: params.floatUpUnique,
    staggering: api.STAGGER.actif,
  },
  zonesSPE: api.speConfig.map(z => ({nom: z.nom, beton: z.estBeton})),
  kpi: {
    retards: api.lastKPI.nbRetards, retardMax: api.lastKPI.retardMax,
    retardTotal: api.lastKPI.retardTotal, bloques: api.lastKPI.nonImmerges,
    changements: api.lastKPI.nbChangements, finProduction: iso(api.lastKPI.finProduction),
  },
  retards: api.lastRetards.map(r => ({id: r.id, jours: r.retardJours})),
  changements: api.lastChangements.map(c => ({ligne: c.ligne, date: iso(c.date), de: c.from, vers: c.to})),
  elements: api.elements.map(e => ({
    id: e.id, ligne: e.ligne, nomLigne: NOM[e.ligne], ordre: e.ordreSeq, rythme: e.rythme,
    rang: isFinite(e.rangImmersion) ? e.rangImmersion : null,
    beton: [iso(e.dateDebutBeton), iso(e.dateFinBeton)],
    outfitting: [iso(e.dateDebutOut), iso(e.dateFinOut)],
    floatUp: [iso(e.dateDebutFU), iso(e.dateFinFU)],
    basin: [iso(e.dateDebutBasin), iso(e.dateDebutParking) || iso(e.dateBallast)],
    basinNum: e.basinNum, basinPlace: e.basinPlace,
    hookup: [iso(e.dateDebutBasin), iso(e.dateFinBasin)],
    parking: [iso(e.dateDebutParking), iso(e.dateBallast)], parkingNum: e.parkingNum,
    stockageSPE: [iso(e.dateDebutStockageSPE), iso(e.dateBallast)], stockageSPENum: e.stockageSPENum,
    ballast: [iso(e.dateBallast), iso(e.dateFinBallast)],
    immersionCible: iso(e.dateImmersion), immersion: iso(e.dateImmersionReelle),
    // Passages de zone de la ligne SPE, tels que la simulation les a réellement produits.
    zones: e.passagesSim
      ? Object.fromEntries(Object.entries(e.passagesSim).map(([z, d]) => [z, iso(d)]))
      : null,
  })),
};
process.stdout.write(JSON.stringify(sortie, null, 1));
