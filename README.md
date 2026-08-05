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
5. **Étape 4** — Ajuster les durées fixes si besoin, puis **LANCER LE SOLVEUR**.
6. Parcourir le planning avec le curseur ou le bouton ▶, et exporter le résultat.

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

Ce second point est essentiel : ralentir un élément repousse mécaniquement tous ceux
qui attendent derrière lui. Regarder toute la file évite au solveur d'osciller
(accélérer / ralentir / réaccélérer) et divise par ~4 le nombre de changements de
cadence à faire appliquer aux opérateurs.

Rythmes autorisés : **1,0 / 1,5 / 2,0 / 2,5 / 3,0 / 3,5 / 4,0** semaines par segment.
Le rythme d'un élément est fixé à son lancement et ne change plus jusqu'à sa sortie.

Quand aucun rythme conforme à la pente ne permet de tenir les délais, le solveur retient
le plus rapide autorisé et émet une **alerte de délai** dans le rapport.

## Structure du classeur

| Onglet | Rôle |
|---|---|
| `Inputs` | Séquences de production. Colonnes B/D/F/H/J/L = PL-1..PL-5, SPE ; colonne A = ordre. Colonnes **C/E/G/I/K/M = statut as-built** (voir ci-dessous). Cellule `Seq2_Debut` en ligne 1/2 = bascule de séquence outfitting. |
| `Immersion` | `ID Element` / `Date Immersion` — les dates cibles que le solveur doit tenir. |
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

## Sorties

- **Rapport de cadence (CSV)** — une ligne par changement de rythme (ligne, date de
  bascule, ancien → nouveau rythme, élément déclencheur), suivi des alertes de délai
  et de la liste des éléments ratant leur date cible.
- **Classeur complet** — le fichier d'origine avec `Config_Cycles` mis à jour (les
  changements calculés réinjectés dans les slots 2 à 4) et un nouvel onglet
  `Solver_Report`. Les macros VBA sont préservées si l'entrée était un `.xlsm`.
- **KPI à l'écran** — nombre d'éléments ratant leur date d'immersion, retard maximum,
  fin de projet estimée, rythme courant par ligne.

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

1. **Jalon d'étanchéité** (colonne F de `Config_SPE`). Le SPE devient étanche N semaines
   après son entrée en UB1. La valeur est saisie **sur chaque zone UB** — non pas parce
   qu'elle diffère d'une zone à l'autre en régime normal, mais pour pouvoir suivre
   indépendamment plusieurs SPE présents simultanément dans les UB.
2. **Rythme SPE long en UB** (colonne G, optionnelle). Dans les zones UB1/UB2/UB3, le SPE
   peut suivre un rythme propre, bien plus long que les durées standard de la colonne D.
**Étanchéité datée.** Si l'onglet `Immersion` contient les activités *clamping* du planning
P6 (colonnes `Activity Name` / `Start` / `Finish`), un SPE est réputé étanche à la dernière
fin de clamping le concernant. Cette date réelle prime sur le jalon théorique de la
colonne F.

3. **Le SPE n'est évacué qu'avant son utilisation finale** : il reste en Basin C
   jusqu'au démarrage de son Ballast Jetty (date d'immersion − durée Ballast), bien
   au-delà de la fin de son hook-up.
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

- **Optimisation de la séquence de production.** La séquence de l'onglet `Inputs` est
  prise telle quelle : le solveur choisit les cadences, pas l'ordre des éléments sur
  les lignes. La faire optimiser par le solveur est une évolution possible.
- **Évacuation anticipée d'un SPE.** Si un SPE doit quitter le Basin C avant son immersion,
  deux éléments non étanches peuvent se retrouver simultanément dans les zones UB. Ce cas
  reste exceptionnel et n'est pas modélisé ; la structure par zone de la colonne F le
  permettra une fois la règle spécifiée.

## Limites connues

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
- **Le solveur ne modélise pas les portes du Basin C.** Quand il choisit un rythme pour
  PL-5, il ignore que la porte outfitting ou la porte étanchéité pourront retarder
  l'élément. Ses estimations de délai sont donc optimistes sur cette ligne, ce qui peut
  provoquer quelques allers-retours de cadence supplémentaires sur PL-5. La simulation,
  elle, applique bien les portes : les dates affichées et les retards signalés sont
  justes.
