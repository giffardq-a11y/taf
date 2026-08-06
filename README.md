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

Deux économies possibles, choisies par la case **« Arrêt de l'usine au plus tôt »** :

- **Cochée (défaut)** — chaque ligne tourne au **rythme le plus rapide** que la pente
  d'inertie autorise et **s'éteint dès sa file vidée**, quitte à produire des éléments
  longtemps avant leur immersion. Les halles se libèrent au plus tôt, l'une après l'autre.
- **Décochée** — production à flux tendu : le solveur retient la **cadence la plus lente**
  qui tienne les dates, et l'usine tourne jusqu'au dernier élément.

Sur le classeur de référence, séquence optimisée dans les deux cas et **zéro retard des deux
côtés** : l'arrêt au plus tôt libère la dernière halle le **11/07/2029** contre le
**14/10/2029** à flux tendu — trois mois de moins — et l'extinction s'étale sur **292 jours**
(PL-5 le 22/09/2028, PL-1/PL-2 le 17/04/2029, SPE et PL-3/PL-4 en juillet 2029) au lieu de
180. Le prix est du stockage à flot : **208 jours** d'avance moyenne entre la sortie
d'outfitting et l'immersion, contre 187, et un changement de cadence de plus.

Le stockage aval reste la limite : un élément qui n'a pas où aller attend en halle et la ligne
ralentit d'elle-même. Le mode « au plus tôt » ne peut donc pas produire n'importe quand.

Pour chaque élément au moment où il entre en zone béton, le solveur teste les rythmes
autorisés — **du plus lent (économique) au plus rapide** à flux tendu, en prenant directement
le plus rapide autorisé en mode « arrêt au plus tôt » — et retient celui qui respecte
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

## Quand une accélération prend effet

Par défaut, le rythme d'un élément est **fixé à son lancement** et ne change plus jusqu'à sa
sortie : une accélération s'applique au prochain départ béton de la ligne, pas à l'élément qui
coule. La contrainte effective est donc le maximum de deux choses — la pente d'inertie, et la
date du prochain lancement. Sur le classeur de référence, cela coûtait 37 jours d'attente sur
la bascule 2,5 → 1,5 et 35 sur la bascule 1,5 → 1,0.

La case **« Accélérer en cours de cycle »** lève cette attente : la ligne accélère le jour où
la pente l'autorise, et l'élément déjà en coulée termine ses segments restants au nouveau
rythme. **Le segment entamé se termine à l'ancien** — un segment ne se coule pas à deux
vitesses. La vraie montée en cadence est progressive sur le chantier ; ce modèle-ci s'arrête au
segment, c'est la granularité que la simulation sait tenir.

Effet mesuré, séquence optimisée, arrêt au plus tôt, **zéro retard dans les deux cas** :

| | Sans | En cours de cycle |
|---|---|---|
| Cadence maximale atteinte le | 30/05/2027 | **02/03/2027** |
| PL-5 éteinte | 22/09/2028 | **04/08/2028** |
| PL-1 / PL-2 éteintes | 17/04/2029 | **27/02/2029** |
| PL-3 / PL-4 éteintes | 11/07/2029 | **23/05/2029** |
| Coulées raccourcies | — | 14, soit 231 j gagnés |
| Bascules de cadence | 15 | 20 |

Les cinq lignes PL gagnent donc **sept semaines chacune**. La date d'arrêt du site, elle, ne
bouge presque pas (11/07/2029 → 10/07/2029) : c'est la **ligne SPE** qui devient contraignante,
et ses durées viennent du planning P6, pas du solveur de cadence. Le prix est double : cinq
bascules de plus à faire appliquer aux opérateurs (la pente ouvre un demi-palier tous les deux
mois, et l'option le prend dès qu'il s'ouvre), et 247 jours d'avance moyenne sur l'immersion au
lieu de 208.

## Date de décision

Le champ **« Date de décision d'accélérer »** fixe le point de départ de la pente d'inertie :
une fois la décision prise, la rampe court, et la durée est réduite dès que la pente le permet.
Laissé vide, la pente court depuis le dernier changement de cadence réellement appliqué —
c'est-à-dire qu'il n'y a rien à décider, la ligne est déjà en régime.

C'est le lever le plus sensible du modèle. Toujours sur le classeur de référence, en cours de
cycle et arrêt au plus tôt :

| Décision | Retards | Arrêt de l'usine |
|---|---|---|
| Aucune (rampe déjà en cours) | **0** | 10/07/2029 |
| 01/01/2027 | 1 | 26/08/2029 |
| 01/01/2028 | **63** | 19/03/2030 |

Décider un an trop tard ne se rattrape pas : la pente ne rend pas les mois perdus.

Quand aucun rythme conforme à la pente ne permet de tenir les délais, le solveur retient
le plus rapide autorisé et émet une **alerte de délai** dans le rapport.

**L'alerte tient compte des accélérations à venir.** Le test qui décide d'accélérer fige le
rythme courant sur toute la file restante : c'est ce qu'il faut pour trancher aujourd'hui,
mais pas pour alerter, puisque la pente autorisera une nouvelle accélération dans quatre mois,
puis quatre mois plus tard. Le drapeau d'alerte rejoue donc la file en accélérant dès que la
pente le permet, et ne retient que ce qui reste hors d'atteinte quoi qu'il arrive. Sur le
classeur de référence, les 15 bascules passaient toutes en rouge alors que le plan final ne
compte aucun retard ; il n'en reste aucune. Brider la pente à 1 semaine par 12 mois les fait
toutes revenir, avec 63 retards à la clé — l'alerte parle quand elle a lieu de parler.

Cette alerte ne porte que sur la **cadence**. Un retard causé par l'aval — bassin plein,
parking saturé, ordre d'immersion — ne la déclenche pas : c'est l'indicateur « éléments en
retard » qui le montre.

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

## Coupe du tunnel

Sous la vue en plan, une bande montre les 89 éléments côte à côte, `STE-01` à gauche et
`STE-79` à droite, et la pose qui progresse avec le **même curseur temporel** que la
production : un élément s'allume quand il est immergé, se distingue pendant son ballast, et
porte un liseré rouge s'il a manqué sa date. Le compteur donne le nombre d'éléments posés à la
date affichée. Sur le classeur de référence, on y voit le tunnel se fermer par ses deux
extrémités vers le milieu — c'est ce que fait l'ordre d'immersion.

Les éléments standard se rangent par numéro ; les SPE, qui n'ont pas de numéro comparable,
se glissent à la place que leur donne l'ordre d'immersion, juste derrière l'élément standard
qui les précède. **Les positions sont donc provisoires** : l'ordre est juste, les distances
non. Elles seront reprises du plan de coupe quand il sera disponible.

La coupe figure dans les **deux** pages : l'outil `index.html`, sous la vue en plan, et la
page de restitution, où elle suit le curseur du plan animé.

## Arrêt de l'usine

Le panneau de statistiques et la page de restitution donnent, ligne par ligne, la date du
**dernier départ béton**, celle où la **halle se libère** pour de bon, et l'**avance moyenne**
de la ligne — le temps qu'un élément y passe entre sa sortie d'outfitting et son immersion.
L'écart entre la première et la dernière extinction mesure si l'arrêt s'étale ou s'il est
brutal : un arrêt étalé rend les moyens au fur et à mesure, un arrêt groupé les immobilise
tous jusqu'au dernier jour.

En mode « arrêt au plus tôt », vider les halles tôt devient aussi un **critère de
l'optimiseur** : il s'intercale après les retards et avant le nombre de changements de
cadence. À flux tendu il n'y figure pas — produire tôt y est un coût, pas un gain.

## État as-built, réglé à l'écran

L'étape 3 affiche un tableau d'une ligne par élément : son identifiant, sa ligne de
production, son statut choisi dans une liste, et la date de début de phase. Les statuts
proposés dépendent de la ligne — segments béton, outfitting, float-up, bassin, parking,
ballast, immergé pour une ligne PL ; les sept zones CPA→UB3 pour la ligne SPE. Un champ de
filtre permet de retrouver un élément par son identifiant, sa ligne ou son statut.

Le classeur reste la source de départ : le tableau est rempli à son chargement, et les
statuts écrits librement (`Bassin`, `Beton 7`, `immergé`) y apparaissent tels que le solveur
les a compris, pas tels qu'ils sont écrits. Ce qui est réglé à l'écran **prime ensuite sur les
colonnes de `Inputs`**, y compris lorsque le classeur est relu — changement de séquence, mode
automatique. Deux boutons permettent de revenir aux statuts du classeur ou de tout vider.

## Règles du modèle, visibles et modifiables

Tout ce qui était figé dans le code est regroupé dans l'objet `REGLES` et exposé à l'étape 6
de l'interface, sous son libellé métier : segments béton par élément, segment de fin
d'outfitting, pente d'inertie (variation autorisée et période), déphasages du hall B et de
PL-5 et cadence à partir de laquelle ils deviennent contraignants, seuils d'étanchéité normal
et critique, nombre de bassins et de places par bassin, places de parking et délai d'ouverture
de la réserve, et la liste des rythmes autorisés. Les valeurs saisies s'appliquent au lancement suivant ; un bouton rétablit les
valeurs de référence.

C'est la première étape de l'interface entièrement paramétrable : les règles sont sorties du
code. Restent à y remonter l'état as-built, aujourd'hui saisi dans les colonnes de `Inputs`,
et la capacité des bassins.

## Icônes de statut et fiche d'un élément

Sur la vue en plan, chaque élément porte l'**icône de son statut** — ▣ béton, ◆ outfitting,
≈ float-up, ● bassin, ▪ parking, ▼ Ballast Jetty, ▤ béton fini en attente, ○ attente de place,
★ zone de stockage SPE — avec une légende sous le plan. L'icône survit au rétrécissement de
l'élément : à cadence rapide, une coulée naissante ne fait que quelques pixels et son
identifiant ne tient plus, mais son symbole reste lisible.

Dans la page de restitution, **tout élément représenté est cliquable** — jeton de la grille de
séquence, bloc de la coupe du tunnel, élément sur le plan animé. Le clic ouvre sa **fiche** :
rythme appliqué, dates de début et de fin de béton et d'outfitting avec leurs durées, float-up,
entrée en bassin avec son numéro et sa place, fin de hook-up, zone de stockage SPE le cas
échéant, entrée au parking et place occupée, hook-up de jetée, ballast, immersion cible et
simulée, écart à la cible, date d'étanchéité pour un SPE, et l'avance entre la sortie
d'outfitting et l'immersion.

## Départage des lignes concurrentes

Quand deux lignes se disputent la même place de bassin ou de parking le même jour, c'est
l'élément traité en premier qui l'emporte. Le départage se fait par **rang d'immersion** — le
plus urgent d'abord — puis par ordre de production à rang égal. Auparavant c'était l'ordre du
tableau des éléments, c'est-à-dire la disposition du classeur.

Le gain est net sur la séquence brute du classeur, à séquence et paramètres identiques :
la variante 1 passe de **18 éléments bloqués à 0**, et la variante 2 de 7 retards à 0. Avec
l'optimiseur, le résultat était déjà à zéro et le reste. Le plan ne dépend donc plus de la
mise en page du classeur, et la priorité va à qui en a besoin.

## Planning d'occupation, à la forme du Target schedule

Le solveur sait produire le planning dans la forme utilisée sur le chantier : une ligne par
ressource, une colonne par demi-semaine, une barre par occupation.

```bash
node planning_runner.js target_schedule_reduit.xlsx 2026-08-05 > plan.json
python3 planning_cible.py plan.json Target_schedule_solveur.xlsx
```

`planning_runner.js` extrait le noyau du solveur de `index.html` entre ses deux marqueurs et le
rejoue hors navigateur : le planning exporté vient donc du même code que l'interface, jamais
d'une copie. Options : `--variante=N`, `--sans-optimiseur`, `--flux-tendu`,
`--en-cours-de-cycle`, `--sans-staggering`, `--budget=ms`.

**Ce que le solveur remplit** — casting par ligne, outfitting, la chaîne SPE zone par zone
(Cage Prefabrication Area = CPA, Casting Pit 1 à 3 = CP1 à CP3, Outfitting buffer area = UB1,
Upper Basin 1 et 2 = UB2 et UB3), les 6 places de Lower basin, le stockage SPE, les 6 places de
Harbour Parking, le hook-up, le Ballast Jetty et l'immersion.

**Ce qu'il ne remplit pas**, et qui garde sa ligne, vide et grisée : `STE Repairs + Integrated
out` et `Outfitting UB`, `MPP Repair`, `Trench verification`, `Trench rectification`,
`Gravel bed`, `Locking fill & Backfill`. Le tableau reste ainsi superposable à celui du
chantier, et ce qui manque se voit au lieu de se deviner.

**Une question de découpage reste ouverte.** Le chantier sépare l'après-coulée en deux lignes —
« Repairs + Integrated outfitting » puis « Outfitting UB ». Le solveur n'a qu'une seule phase
d'outfitting, de `segmentsOutfitting × rythme` semaines. Laquelle des deux elle recouvre, ou
comment elle se répartit entre les deux, est une décision de chantier : la barre est donc
tracée sur sa propre ligne, `Outfitting (solveur, phase unique)`, et les deux lignes d'origine
restent vides. Le jour où le découpage est arrêté, il suffit de rebrancher la source.

**Approximation assumée** : deux occupations d'une même ressource qui se suivent à moins d'une
demi-semaine ne peuvent pas partager une colonne. La seconde est alors rognée d'une colonne —
174 barres sur 559 dans l'export de référence. Quand deux occupations sont réellement
simultanées, ce qui arrive au hook-up puisque les deux lignes d'une paire entrent en bassin
ensemble, les deux étiquettes sont accolées dans la même barre plutôt que d'en perdre une. Le
script annonce les deux chiffres à chaque exécution.

## Relevé des contraintes

La page de restitution porte un relevé complet de ce que le solveur applique : **74 contraintes**
en 12 familles — données d'entrée, cadence, staggering, occupation des zones, float-up, bassins,
parking, Basin C et ligne SPE, étanchéité, ballast et immersion, optimiseur, cadre de la
simulation. Chaque ligne donne son seuil, son origine, et son statut :

| Statut | Sens | Nombre |
|---|---|---|
| **Réglable** | modifiable depuis l'interface | 26 |
| **Donnée** | vient du classeur ou du planning P6 | 10 |
| **Figé** | structurel, ou codé en dur et non exposé | 37 |
| **À trancher** | incohérence relevée à l'audit | 0 |

Le relevé est **tenu à la main** d'après le solveur : c'est une relecture du code, pas une
extraction. C'est précisément ce qui lui permet de servir de contrôle — une extraction
automatique ne pourrait pas signaler qu'une règle lue n'est jamais appliquée. Les seuils
affichés, eux, sont lus dans `REGLES` et `PARAMS` : le tableau ne peut pas mentir sur les
valeurs réellement en vigueur.

### Ce que l'audit a relevé

Les deux points sont réglés.

- **Doublon corrigé.** La date d'entrée au Ballast Jetty (date d'immersion cible moins la durée
  de ballast) était réécrite à **quatre endroits** : évacuation d'un SPE du Basin C, ouverture
  de la réserve de parking, départ depuis le parking, et la fonction dédiée. Les quatre sont
  ramenées à `dateDebutBallastDe`. Résultat de référence inchangé, vérifié.
- **Règle lue mais jamais appliquée, retirée.** `Config_Outfitting` fournissait 6 phases ×
  2 séquences que le solveur lisait, journalisait, et n'utilisait pas — la durée d'outfitting
  vaut `segmentsOutfitting × rythme × 7 j`. L'onglet, sa lecture, ses valeurs par défaut et la
  date `Seq2_Debut` de `Inputs` sont supprimés. Le calcul est inchangé, par construction.

## Classeur réduit

`reduire_classeur.py` produit un classeur ne contenant que ce que le solveur lit :

```bash
python3 reduire_classeur.py target_schedule_programme.xlsm target_schedule_reduit.xlsx
```

Ce qui reste — 4 onglets :

| Onglet | Conservé | Retiré |
|---|---|---|
| `Inputs` | 51 lignes, 13 colonnes (n° d'ordre + identifiant et statut par ligne) | les colonnes de mise en forme |
| `Immersion` | 405 lignes, 5 colonnes (`ID Element`, `Date Immersion`, `Activity Name`, `Start`, `Finish`) | 11 colonnes, et les activités du P6 qui n'entrent dans aucun calcul |
| `Config_Cycles` | 5 lignes, 3 colonnes (ligne, date seuil 1, cycle 1) | les seuils 2 à 4, que le solveur détermine lui-même |
| `Config_SPE` | les 7 zones, 7 colonnes | — |

Ce qui disparaît entièrement : `Feuil1`, `Planning_Final`, `Dashboard`, `Recap_Dates` (sortie de
l'ancienne macro) et `Config_Outfitting` (retiré du modèle). Le fichier passe de **149 Ko à
24 Ko**, et n'a plus besoin d'être un `.xlsm` : la macro n'existe plus.

**Équivalence vérifiée**, pas supposée : les deux classeurs ont été simulés côte à côte sur les
**3 variantes de séquence** de `Inputs`, et comparés élément par élément sur 13 champs — ligne,
rang, rythme, début et fin de béton, fin d'outfitting, entrée bassin, entrée parking, ballast,
immersion cible, immersion réelle, date d'étanchéité, état final. **Zéro écart sur les 89
éléments, dans les 3 variantes.**

## Structure du classeur

| Onglet | Rôle |
|---|---|
| `Inputs` | Séquences de production. Colonnes B/D/F/H/J/L = PL-1..PL-5, SPE ; colonne A = ordre. Colonnes **C/E/G/I/K/M = statut as-built** (voir ci-dessous). |
| `Immersion` | `ID Element` / `Date Immersion` — les dates cibles que le solveur doit tenir, et **l'ordre d'immersion**, qui est une donnée d'entrée P6 que le programme ne modifie jamais. Les colonnes `Activity Name` / `Start` / `Finish` portent le planning P6 détaillé : dates d'immersion, activités de clamping, et **passages de zone de la ligne SPE** (voir ci-dessous). |
| `Config_Cycles` | **Colonnes B/C (Date Seuil 1 / Cycle 1) = le rythme actuel**, saisi par vous. Les colonnes D à I (Seuils 2-4 / Cycles 2-4) sont **ignorées en entrée** : c'est le solveur qui les calcule et les réinjecte à l'export. |
| `Config_SPE` | Les 7 zones de la ligne SPE (CPA→CP3 béton, UB1→UB3 outfitting). **Colonne F** = jalon d'étanchéité, en semaines après l'entrée en UB1, saisi sur chaque zone UB. **Colonne G** (optionnelle) = rythme SPE long, en semaines, remplaçant la durée standard de la colonne D dans les zones UB. |

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

Les trois zones d'aménagement du planning correspondent aux trois zones UB de `Config_SPE` :
`FI1 - Fit Out in Outfitting Buffer Area` → UB1, `FI2 - Upper Basin 1` → UB2,
`FI3 - Upper Basin 2` → UB3. L'aire tampon fait partie du Basin C : un SPE qui s'y trouve
compte donc pour la porte d'inondation, au même titre que dans les deux bassins.

La **sortie de CP3** ainsi datée est la référence du jalon d'étanchéité provisoire.

**Sortie de chaîne.** Le planning ne date pas la sortie de la dernière zone qu'il couvre. Le
solveur n'y applique aucune durée de remplacement : un SPE que le planning pilote est prêt
pour le float-up dès qu'il atteint sa dernière zone datée. Inventer un délai absent du
planning ne ferait que produire des retards fictifs. Les durées de `Config_SPE` ne servent
qu'à un SPE dont le planning ne dit rien.

Quand l'onglet `Immersion` contient des activités **« ready for float up »**, c'est cette date
qui commande la sortie de chaîne — elle marque le moment où le SPE est prêt à être immergé,
quelle que soit la zone UB où il se trouve.

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

**Ballast** : sa durée est celle de l'activité *Floatout, 1st Phase Ballast Concrete* du
planning P6, propre à chaque élément (4, 5 ou 25 jours sur le classeur de référence). Le
paramètre *Durée Ballast* de l'interface ne sert que de repli, pour un élément absent du
planning.

**Les SPE n'ont pas de phase de ballast.** Ils ne figurent pas dans les activités de float-out :
un SPE passe du bassin à l'immersion, sans passer par le Ballast Jetty.

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
