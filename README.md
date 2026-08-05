# Lolland Master Planner — Solveur de cadence & visualisation de planning

Outil web autonome (un seul fichier `index.html`, tout tourne dans le navigateur —
aucune donnée n'est envoyée sur un serveur) qui :

1. **calcule** les rythmes de production à appliquer sur chaque ligne (PL-1..PL-5),
   en partant du rythme actuel et de l'état d'avancement réel du chantier ;
2. **rejoue** la simulation jour par jour du flux complet ;
3. **affiche** le résultat visuellement sur le plan du site, avec un curseur temporel.

## Utilisation

1. Ouvrir `index.html` dans un navigateur (double-clic, ou glisser dans un onglet).
2. **Étape 1** — Charger l'image du plan du site. L'image reste locale.
3. **Étape 2** — Charger le classeur (`.xlsx` ou `.xlsm`, macros préservées).
4. **Étape 3** — Vérifier la date de référence (par défaut : aujourd'hui). C'est le
   « présent » du solveur : tout ce qui est renseigné comme en cours l'est à cette date.
5. **Étape 4** — Ajuster les durées fixes si besoin.
6. **Étape 5** — Choisir la séquence de production du classeur, activer ou non le staggering
   et l'optimiseur de séquence, puis **LANCER LE SOLVEUR**. Le bouton *Comparer* met les
   deux séquences en regard sans avoir à relancer soi-même.
7. Parcourir le planning avec le curseur ou le bouton ▶, et exporter le résultat.

## Ce que fait le solveur

Pour chaque élément au moment où il entre en zone béton, le solveur teste les rythmes
autorisés **du plus lent (économique) au plus rapide** et retient le premier qui respecte
simultanément :

- **la pente d'inertie de la ligne** — 1 semaine de variation par tranche de 4 mois
  maximum, mesurée depuis le dernier changement réellement appliqué sur la paire ;
- **les dates d'immersion de tout le reste de la file**, pas seulement celle de
  l'élément courant ;
- **la cadence de la ligne jumelle** : les deux lignes d'une paire partagent un même
  rythme et basculent ensemble. Leurs éléments doivent sortir de l'outfitting en même
  temps, donc accélérer une ligne sans l'autre créerait un blocage au transfert vers le
  bassin.

**Une cadence atteinte n'est jamais relâchée.** Le solveur ne peut qu'accélérer, dans la
limite de la pente. Remonter puis redescendre coûterait deux réinstallations, sans commune
mesure avec l'économie d'un cycle plus lent, et le moindre retard qui en découlerait se
paierait en pénalités.

Une case de l'interface autorise malgré tout un relâchement unique par paire, en fin de
programme. Elle est décochée par défaut, et la mesure explique pourquoi : le test de
faisabilité du solveur ignore l'aval (bassins, parking, ordre d'immersion), donc il juge
parfois tenable un rythme plus lent qui ne l'est pas. Sur le classeur de référence, l'autoriser
coûte 8 retards, 1032 jours de retard cumulé et 4 changements de cadence supplémentaires.

Ce second point est essentiel : ralentir un élément repousse mécaniquement tous ceux
qui attendent derrière lui. Regarder toute la file évite au solveur d'osciller
(accélérer / ralentir / réaccélérer) et divise par ~4 le nombre de changements de
cadence à faire appliquer aux opérateurs.

Rythmes autorisés : **1,0 / 1,5 / 2,0 / 2,5 / 3,0 / 3,5 / 4,0** semaines par segment.
Le rythme d'un élément est fixé à son lancement et ne change plus jusqu'à sa sortie.

Quand aucun rythme conforme à la pente ne permet de tenir les délais, le solveur retient
le plus rapide autorisé et émet une **alerte de délai** dans le rapport.

## Staggering entre halls

Le hall A (PL-1/PL-2) et le hall B (PL-3/PL-4) partagent les mêmes moyens : ils ne doivent
pas attaquer un élément au même moment du cycle. Le solveur décale donc le départ du béton :

- **3 segments entre A et B** — PL-3 et PL-4 démarrent quand PL-1 et PL-2 sont à leur
  segment 4. La contrainte est **dure dès que la cadence atteint 1 semaine/segment**, et
  reste une simple préférence en deçà.
- **7 segments pour PL-5** — préférence seulement, jamais bloquante : sa cadence varie
  librement.
- **Aucun déphasage à l'intérieur d'un hall.**

La phase se mesure sur le dernier départ de béton du hall A, modulo le takt de la ligne.
Sous contrainte dure, la ligne patiente jusqu'au segment visé quel qu'en soit le prix : au
plus un cycle, et une seule fois — les takts étant égaux, la phase se conserve ensuite
d'elle-même. Écourter cette attente reviendrait à la reproduire à chaque cycle sans jamais
rattraper la phase. Sous simple préférence, la ligne ne patiente que si l'attente est
gratuite, c'est-à-dire si toute sa file restante tient encore ses dates après décalage.

Deux cas lèvent le déphasage, tous deux signalés dans le journal :

1. **Cadences de halls différentes.** Un déphasage ne se conserve qu'entre halls de même
   cadence ; sinon la phase dérive d'un cycle à l'autre et la tenir reviendrait à brider le
   hall le plus rapide. Il est suspendu le temps que les cadences se rejoignent — elles ne
   divergent qu'entre deux bascules. PL-5 n'est pas concerné, son écart n'étant qu'une
   préférence.
2. **Hall A vidé.** Sa dernière date de départ n'est plus une phase, juste un souvenir : il
   n'y a plus rien à déphaser, et attendre bloquerait la fin de programme pour rien.

Le staggering se désactive depuis l'interface.

## Optimiseur de séquence

Le solveur de cadence prend la séquence de l'onglet `Inputs` telle quelle. L'optimiseur,
lui, choisit **l'ordre des éléments sur chaque ligne** et, si on le lui demande, **la ligne
sur laquelle produire chaque élément**. Objectif, dans cet ordre :

1. **zéro inversion** entre séquence de production et ordre d'immersion ;
2. **minimisation des retards** : éléments bloqués, puis éléments en retard, puis retard
   cumulé, puis retard maximum, puis nombre de changements de cadence.

Le premier critère détermine presque tout : une file sans inversion est une file triée par
date d'immersion, **ordre unique aux ex æquo près**. Le second critère ne s'exerce donc que
là où le premier laisse le choix — les éléments sans date d'immersion, qui n'imposent rien,
et ceux qui partagent la même date. L'optimiseur explore ces cas par descente locale, chaque
candidat étant évalué par une simulation complète, sous budget de temps borné.

**Affectation aux lignes.** Les cinq lignes PL sont interchangeables : un élément standard se
produit sur n'importe laquelle. La ligne SPE, elle, ne produit que ses éléments spéciaux — sa
chaîne de 7 zones ne convient à rien d'autre — et rien d'autre ne s'y produit. L'optimiseur
part d'une répartition par ordonnancement de liste (chaque élément sur la ligne dont le
créneau se libère le plus tôt), puis déplace un à un les éléments qui posent problème —
bloqués ou en retard — vers les lignes les moins chargées. Chaque candidat étant évalué par
une simulation complète, le voisinage exploré est ciblé plutôt qu'énuméré.

Un élément déjà engagé — statut as-built saisi, ou date d'immersion déjà passée — garde sa
place et sa ligne : sa production est commencée. Et l'optimiseur ne rend jamais un plan pire
que celui de l'utilisateur : à égalité, la séquence du classeur est conservée.

La séquence retenue est celle que l'on peut recopier dans `Inputs` : la simuler donne
exactement ce que donnerait le même ordre saisi dans le classeur. Elle est exportée telle
quelle dans l'onglet `Sequence_Solveur`.

## Structure du classeur

| Onglet | Rôle |
|---|---|
| `Inputs` | Séquences de production. Colonnes B/D/F/H/J/L = PL-1..PL-5, SPE ; colonne A = ordre. Colonnes **C/E/G/I/K/M = statut as-built** (voir ci-dessous). Cellule `Seq2_Debut` en ligne 1/2 = bascule de séquence outfitting. |
| `Immersion` | `ID Element` / `Date Immersion` — les dates cibles que le solveur doit tenir, et **l'ordre d'immersion**, qui est une donnée d'entrée P6 que le programme ne modifie jamais. Les colonnes `Activity Name` / `Start` / `Finish` portent le planning P6 détaillé : dates d'immersion, activités de clamping, et **passages de zone de la ligne SPE** (voir ci-dessous). |
| `Config_Cycles` | **Colonnes B/C (Date Seuil 1 / Cycle 1) = le rythme actuel**, saisi par vous. Les colonnes D à I (Seuils 2-4 / Cycles 2-4) sont **ignorées en entrée** : c'est le solveur qui les calcule et les réinjecte à l'export. |
| `Config_SPE` | Les 7 zones de la ligne SPE (CPA→CP3 béton, UB1→UB3 outfitting). **Colonne F** = jalon d'étanchéité, en semaines après l'entrée en UB1, saisi sur chaque zone UB. **Colonne G** (optionnelle) = rythme SPE long, en semaines, remplaçant la durée standard de la colonne D dans les zones UB. |
| `Config_Outfitting` | Sans effet sur le calendrier : la durée d'outfitting est dérivée de la production (voir ci-dessous). L'onglet ne fournit plus que les noms des phases. |

### Format des statuts as-built (colonnes C/E/G/I/K/M de `Inputs`)

Le statut va dans la cellule **immédiatement à droite** de l'ID de l'élément, sur la
même ligne. Un élément sans statut est considéré comme non démarré (le solveur le
lancera quand la ligne se libère), **sauf** si sa date d'immersion est déjà passée :
il est alors déduit comme terminé.

La lecture est tolérante : séparateur deux-points **ou espace**, accents et casse
ignorés, synonymes français acceptés. `Beton 7`, `Beton:7`, `Bassin`, `immergé` et
`UB2` sont tous compris.

| Code | Signification |
|---|---|
| `Beton:N` | En zone béton, au segment N (1 à 9). Lignes PL uniquement. |
| `Outfitting` | En zone outfitting. Lignes PL uniquement. |
| `Zone:N` | Ligne SPE uniquement : dans la zone N (1=CPA … 7=UB3). Si N est une zone UB, l'entrée en UB1 — et donc le jalon d'étanchéité — est recalée en remontant les durées des zones UB déjà traversées. |
| `FloatUp` | En cours de float-up. |
| `Basin` | En Lower Basin (hook-up en cours). |
| `Parking` ou `Parking:N` | Au parking (place N si connue, sinon première libre). |
| `Ballast` | Au Ballast Jetty. |
| `Done` | Déjà immergé (synonymes : `immerge`, `termine`, `fini`). |

Suffixe de date optionnel pour préciser le début réel de la phase :
`Beton:5:2026-06-15`. Sans date, la phase est réputée avoir commencé à la date de
référence. Un code non reconnu est signalé dans le journal et l'élément est traité
comme non démarré.

## Page de restitution autonome

`report_template.html` + `build_report.py` produisent une page de rapport indépendante,
qui embarque le solveur et SheetJS : on y charge un classeur et le calcul est relancé
sur place, sans aucune ressource externe.

```bash
python3 build_report.py -o rapport.html
```

Le solveur n'y est jamais recopié : il est prélevé entre les marqueurs
`SOLVEUR-CORE-DEBUT` / `SOLVEUR-CORE-FIN` de `index.html`, qui reste la seule
implémentation. C'est le build **mini** de SheetJS qui est inliné — suffisant pour du
`.xlsx`/`.xlsm`, là où le build *full* embarque les tables de pages de code héritées.

La page affiche le mouvement des éléments sur un schéma reconstruit d'après les
coordonnées du dossier de référence, superposé au plan d'installation générale.
La ligne SPE y est découpée en 7 aires successives d'est en ouest — cpa, cp1, cp2, cp3,
ub1, ub2, ub3 — chacune à son emplacement propre.

## La ligne SPE suit le planning P6

Le planning P6 collé dans l'onglet `Immersion` est hiérarchique : un niveau par zone
(`CPA`, `CP1`, `CP2`, `CP3`, puis `FI1`, `FI2`, `FI3` — les trois Upper Basin), et sous
chaque zone, un groupe par SPE dont l'activité de *skidding* date sa sortie. Le solveur en
tire les **dates de passage de zone de chaque SPE** : la ligne SPE est donc une donnée
d'entrée, comme l'ordre d'immersion, et non un résultat estimé par des durées fixes.

Les durées de `Config_SPE` (colonne D, et colonne G pour le rythme long en UB) ne servent
plus que de repli, pour un SPE dont le planning ne donne pas les passages.

La **sortie de CP3** ainsi datée est la référence du jalon d'étanchéité provisoire.

## Étanchéité SPE : trois niveaux en cascade

Un SPE non étanche interdit d'inonder le Basin C, donc d'en évacuer un élément normal. La
contrainte ne se lève jamais. Ce qui se négocie, c'est **comment** l'étanchéité est obtenue,
dans cet ordre :

1. **Clamping** — la fermeture définitive, datée par les activités du planning P6 lues dans
   l'onglet `Immersion`. S'il tombe assez tôt, rien d'autre n'est nécessaire.
2. **Fermeture provisoire à 12 semaines** — quand le clamping tombe trop tard, le SPE est
   fermé provisoirement pour permettre l'inondation, puis rouvert pour finir l'aménagement, et
   refermable à la demande. Possible au plus tôt 12 semaines après la **sortie de CP3**
   (colonne F de `Config_SPE`). C'est l'avancement des travaux qui compte, pas la zone où ils
   se font : ils peuvent commencer en UB1 et s'achever en UB2.
3. **Seuil critique à 8 semaines** — faisable, mais le planning passe en tension. Ce niveau
   n'est employé que si l'utilisateur l'autorise, et **chaque recours est signalé** dans le
   journal et le rapport.

Le solveur ne descend pas seul au niveau 3. Après chaque calcul, il mesure ce que le seuil
critique rapporterait et **ouvre une boîte de dialogue** : retards obtenus de part et d'autre,
et liste des fermetures concernées avec leur date, leur ancienneté après CP3 et l'élément
qu'elles débloquent. Refuser laisse le plan tel quel ; accepter coche l'autorisation et
relance le calcul.

Les fermetures provisoires nécessaires sont listées dans tous les cas : ce sont des opérations
à programmer, le plan ne peut pas les demander sans le dire.

## Séquence automatique

Le menu de séquence propose, en plus des variantes du classeur, une entrée **« Automatique —
le solveur choisit »** : chaque séquence empilée dans `Inputs` est optimisée, et celle qui
donne le meilleur plan est retenue. Une variante peut sembler bonne telle quelle parce que ses
éléments bloqués ne comptent pas comme retards — les comparer une fois optimisées évite ce
piège.

Les critères sont comparés dans cet ordre : éléments bloqués, inversions des lignes PL,
éléments en retard, retard cumulé, retard maximum, changements de cadence. Les bloqués passent
en tête parce que c'est le seul résultat dont on ne se relève pas. Les inversions de la ligne
SPE ne comptent pas : la zone de stockage les absorbe, et les ranger au même niveau ferait
préférer une variante sans inversion SPE mais bien plus en retard.

## Sorties

- **Rapport de cadence (CSV)** — une ligne par changement de rythme (ligne, date de
  bascule, ancien → nouveau rythme, élément déclencheur), suivi des alertes de délai
  et de la liste des éléments ratant leur date cible.
- **Classeur complet** — le fichier d'origine avec `Config_Cycles` mis à jour (les
  changements calculés réinjectés dans les slots 2 à 4), un onglet `Solver_Report` et un
  onglet `Sequence_Solveur` donnant la séquence réellement simulée, ligne par ligne.
  L'onglet `Inputs` n'est jamais réécrit : ses colonnes de statut as-built appartiennent à
  l'utilisateur. Les macros VBA sont préservées si l'entrée était un `.xlsm`.
- **KPI à l'écran** — éléments bloqués, inversions restantes, nombre d'éléments ratant leur
  date d'immersion, retard maximum, fin de projet estimée, rythme courant par ligne.
- **Comparatif à l'écran** — séquence du classeur contre séquence optimisée, sur les mêmes
  indicateurs : inversions, bloqués, éléments en retard, retard maximum, retard cumulé,
  changements de cadence.

## Logique de production simulée

**Cadence de ligne et flux tendu.** Le segment 1 d'un élément ne démarre qu'une fois le
segment 9 du précédent terminé : le takt d'une ligne vaut donc 9 × R semaines. L'outfitting
d'un élément démarre quand ses 9 segments sont poussés et s'achève quand l'élément suivant
a terminé son **7e segment** — soit 7 × R semaines. Plus court que le béton, le battement
de 2 segments absorbant les deux transferts (béton → outfitting, puis outfitting → bassin).
Un seul élément occupe l'outfitting à la fois. Tant que le suivant n'a pas démarré son
béton, l'élément en outfitting garde sa place.

`Béton (1 place/ligne)` → `Outfitting (1 place/ligne)` → `Float-up couplé
(PL1+2 / PL3+4 / PL5+SPE)` → `Lower Basin (3 bassins × 2 places, hook-up sur place)` →
`Parking (5 places + 1 réserve)` → `Ballast Jetty` → `Immersion`.

**Séjour en bassin et parking.** Un élément reste dans son bassin tant que sa place n'est
pas réclamée par la production : le déplacer plus tôt ne ferait que consommer une place de
parking. Dès qu'un autre élément du groupe attend le bassin, il en sort. Le **seuil de
parking** n'est pas une contrainte de flux mais une économie de mouvement : quand
l'immersion est assez proche, on évite le détour par le parking — sauf si la place est
réclamée, auquel cas la production prime.

**Hook-up** : 24 h, sur place, juste avant le Ballast Jetty.

**Parking** : 5 places sans limite de durée, plus une 6e réservée au déblocage ponctuel,
ouverte seulement si les autres sont pleines et si l'élément repart dans le mois.

**Stockage croisé** : parking saturé, un élément peut être garé dans une place de bassin
libre — mais jamais dans le bassin d'un groupe ayant encore des éléments en amont, sous
peine de bloquer ce groupe. C'est une soupape de déblocage, comptabilisée dans le journal.

**Ordre d'immersion imposé.** Les éléments s'immergent dans l'ordre des lignes de
l'onglet `Immersion`. Un élément qui n'est pas prêt bloque tous ceux qui le suivent,
même s'ils le sont. La porte est posée à l'entrée du **Ballast Jetty** : seul
l'élément en tête de file peut être ballasté, et l'immersion suit directement la fin
du ballast. Un seul élément est donc ballasté à la fois. Les éléments prêts mais
retenus par un prédécesseur sont comptés et signalés dans le journal.

La ligne SPE suit une chaîne de 7 zones bloquantes avant de rejoindre le float-up
avec PL-5.

**Couplage du float-up** : pour PL1+2 et PL3+4, les deux lignes sortent de l'outfitting
ensemble, le plus rapide attendant le plus lent. L'élément qui vient d'entrer en
outfitting derrière la paire appartient au cycle suivant et n'est pas bloquant —
l'exiger rendrait le float-up quasi impossible, la place d'outfitting étant reprise
dès qu'elle se libère.

**Float-up et entrée en bassin sans partenaire** : les files des deux lignes d'un
groupe n'ont pas la même longueur (PL-5 compte 15 éléments, SPE 10). Quand la ligne
jumelle est épuisée, les derniers éléments partent seuls — sans cette règle ils
resteraient bloqués indéfiniment. Ces départs solo sont signalés dans le journal.

## Géométrie du plan (coordonnées relatives %, "pixel perfect")

| Repère | Valeur |
|---|---|
| Épaisseur (Y) | 2,21 % |
| Longueur standard (PL1-5) / spéciale (SPE) | 7,42 % / 1,66 % |
| X entrée (Est) → fin de halle → fin outfitting → bassin (Ouest) | 58,40 → 50,98 → 42,68 → 37,01 |
| Y PL-1 / PL-2 / PL-3 / PL-4 / PL-5 / SPE | 71,71 / 69,29 / 60,66 / 58,38 / 51,83 / 48,23 |
| Parking (épi -75°) | de [16,31 ; 80,97] à [10,25 ; 47,13] |

## Règles spécifiques au Basin C (paire PL-5 / SPE)

Ce groupe ne fonctionne pas comme les deux autres. Les zones UB1-3 étant dans le
Basin C, le SPE en construction y séjourne longtemps pendant que les éléments
normaux de PL-5 défilent.

1. **Jalon d'étanchéité provisoire** (colonne F de `Config_SPE`). Ce qui commande
   l'inondation du bassin est l'étanchéité **provisoire**, pas la fin des travaux : un SPE
   passe par une phase d'étanchéité provisoire pour permettre le float-up, puis il est
   rouvert pour finir les travaux intérieurs, et peut être refermé à la demande. Une fois le
   jalon franchi, il ne bloque donc plus jamais. Le délai minimal court depuis l'entrée en
   UB1 — de l'ordre de 8 à 12 semaines sur ce chantier. La valeur est saisie **sur chaque
   zone UB**, non parce qu'elle diffère d'une zone à l'autre, mais pour pouvoir suivre
   indépendamment plusieurs SPE présents simultanément dans les UB.
2. **Rythme SPE long en UB** (colonne G, optionnelle). Dans les zones UB1/UB2/UB3, le SPE
   peut suivre un rythme propre, bien plus long que les durées standard de la colonne D.
   Cette valeur doit être cohérente avec le jalon d'étanchéité : si un SPE ne reste que
   5 semaines en UB1 alors qu'il lui en faut 12 pour être provisoirement étanche, un nouveau
   SPE non étanche entre en UB1 avant que le précédent n'ait franchi son jalon, et le bassin
   n'est presque jamais inondable.

**Le clamping du planning P6 ne commande pas la porte.** Les activités *clamping* lues dans
l'onglet `Immersion` (colonnes `Activity Name` / `Start` / `Finish`) datent la **fin des
travaux intérieurs**, huit à quinze mois après l'entrée en UB1 sur le classeur de référence.
Les prendre pour l'étanchéité qui commande le bassin le fermait des mois durant. Elles sont
lues et reportées au journal, à titre d'information.

3. **Le SPE n'est évacué qu'avant son utilisation finale** : il reste en Basin C
   jusqu'au démarrage de son Ballast Jetty (date d'immersion − durée Ballast), bien
   au-delà de la fin de son hook-up. **Sauf s'il retient un SPE qui doit s'immerger avant
   lui** : la place SPE du Basin C étant unique, l'attendre bloquerait toute la file
   d'immersion. Il part alors en **zone de stockage SPE** — dédiée aux éléments spéciaux,
   distincte du parking, et d'**une seule place** — d'où il revient pour son propre ballast. Sortir du Basin C imposant
   de l'inonder, l'évacuation attend que tout SPE encore en zone UB soit étanche. Chaque
   évacuation anticipée est signalée dans le journal.
4. **Les éléments normaux sont évacués au fur et à mesure**, sans attendre le SPE.
5. **Porte outfitting** : un élément normal ne passe en outfitting que si celui-ci
   sera terminé avant l'évacuation du SPE suivant.
6. **Porte étanchéité** : évacuer un élément normal impose d'inonder le bassin, donc
   d'attendre que tout SPE présent en zone UB ait franchi son jalon d'étanchéité.

**Conséquence assumée** : le float-up couplé et l'entrée en bassin par paire, qui
restent la règle pour PL1+2 et PL3+4, sont **abandonnés pour PL-5 / SPE**. Un SPE
stationnant des mois en Basin C pendant que les éléments normaux défilent, une
synchronisation par paire bloquerait la ligne. Les six règles ci-dessus la remplacent.
Les deux places du Basin C sont donc gérées indépendamment (place 1 = PL-5,
place 2 = SPE).

## À venir

- **Pentes progressives de cadence.** Un changement de rythme se fait graduellement dans la
  réalité, pas d'un jour à l'autre.

## Limites connues

- **Position de la zone de stockage SPE estimée.** Sa capacité (une place) est celle du
  chantier ; ses coordonnées sur le plan, elles, sont extrapolées à l'ouest du Basin C
  (`GEO.stockageSPE` dans `index.html`). A recalibrer.
- **Position du Ballast Jetty estimée.** Elle n'était pas fournie dans le cahier des
  charges ; elle est extrapolée depuis l'axe du parking (`GEO.ballast` dans
  `index.html`). À recalibrer si vous avez la position réelle.
- **`Config_Cycles` n'a que 3 slots de changement par ligne.** Si le solveur en produit
  davantage, les changements au-delà ne sont pas réinjectés dans cet onglet (un
  avertissement le signale) ; la liste complète reste dans `Solver_Report` et le CSV.
- **Le solveur est glouton, pas optimal au sens strict.** Il décide ligne par ligne au
  fil de l'eau, sans arbitrage global entre lignes concurrentes pour les ressources
  partagées (bassins, parking). C'est ce que décrit le cahier des charges, et cela
  suffit à produire un plan de cadence exploitable, mais ce n'est pas une optimisation
  sous contraintes au sens mathématique.
- **Le solveur ne modélise pas le staggering quand il choisit la cadence.** Comme pour les
  portes du Basin C, le décalage de phase imposé au départ n'entre pas dans son estimation
  de délai : elle reste optimiste sur PL-3, PL-4 et PL-5. La simulation, elle, applique bien
  le déphasage — les dates affichées et les retards signalés sont justes.
- **L'optimiseur n'a que peu de marge sur son second objectif.** Une file sans inversion est
  une file triée par date d'immersion : l'ordre est unique aux ex æquo près. Sur un classeur
  où toutes les dates d'immersion sont distinctes et renseignées, l'optimiseur se réduit donc
  à ce tri, et l'affinage sur les retards ne trouve rien à déplacer. Ce n'est pas une limite
  d'implémentation mais du degré de liberté disponible : le levier suivant est l'affectation
  des éléments aux lignes.
- **Le solveur ne modélise pas les portes du Basin C.** Quand il choisit un rythme pour
  PL-5, il ignore que la porte outfitting ou la porte étanchéité pourront retarder
  l'élément. Ses estimations de délai sont donc optimistes sur cette ligne, ce qui peut
  provoquer quelques allers-retours de cadence supplémentaires sur PL-5. La simulation,
  elle, applique bien les portes : les dates affichées et les retards signalés sont
  justes.
