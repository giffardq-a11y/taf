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

## Bassin libre avant float-up

Un float-up fait passer l'élément de l'Upper Basin au Lower Basin : le mouvement suppose les
deux bassins au même niveau, donc **le bassin d'arrivée doit être libre**. Le solveur lançait
pourtant le mouvement vers un bassin encore occupé par la paire précédente, et l'élément se
retrouvait à flot sans poste — un état qui n'existe pas sur le chantier, et qui se voyait à
l'écran : deux éléments en bassin, deux autres en float-up vers le même bassin.

Le contrôle reprend exactement celui de l'entrée en bassin : bassin **entièrement libre** pour
les groupes A et B, dont les deux lignes entrent par paire ; **poste par poste** pour le Basin C,
où PL-5 et la ligne SPE sont indépendants.

Une conséquence non évidente a dû être corrigée en même temps. Un élément ne quitte son poste
que si quelqu'un le réclame, et cette réclamation se lisait sur les éléments en attente de
bassin. La file ne se formant plus à flot mais en amont, en fin d'outfitting, il fallait l'y
lire : sans cela plus personne ne réclamait, le bassin ne se vidait jamais et tout se bloquait —
62 éléments jamais immergés au premier essai.

**Le prix est lourd et il faut le savoir.** Ce n'est pas la règle qui coûte, c'est ce qu'elle
révèle : le planning ne tenait qu'en s'autorisant un mouvement impossible. Le journal dit où —
sur le classeur de référence, **2 015 jours** où un float-up a été repoussé faute de poste libre.
La case permet de revenir à l'ancien comportement pour comparer.

## Le bassin n'est pas un lieu de stationnement

Hook-up terminé, un élément **gagne un parking dès qu'une place est libre**. Une seule dispense :
un séjour de moins de `seuilParkingSem` semaines — quatre par défaut — **et** à condition qu'il
ne retienne aucun float-up de son propre bassin. Bouger un élément pour trois semaines coûte
deux manœuvres et ne libère rien d'utile.

C'est l'inverse de la règle précédente, qui ne le faisait sortir que si quelqu'un réclamait sa
place. Le bassin se vidait alors au dernier moment, et le nombre de places de parking n'avait
presque aucun effet sur le résultat — ce qui n'est pas ce que le chantier observe.

Avec la bonne règle, l'effet apparaît, mesuré avec l'optimiseur (5 places plus la réserve étant
la configuration nominale) :

| Places de parking | En retard | Retard max | Cumulé | Bloqués |
|---|---|---|---|---|
| 3 | — | — | — | **62** |
| 4 à 6 | 9 | 46 j | 161 j | 0 |
| 8 | 4 | 18 j | 40 j | 0 |
| 10 | **0** | — | — | 0 |

La règle corrigée améliore d'ailleurs nettement le cas nominal : le retard cumulé passe de
993 à **161 jours**.

Le mécanisme, mesuré en jours-élément sur le séjour en bassin : **5 810** jours où aucune place
de parking n'était libre, **3 908** où l'élément était retenu par celui qui fait face à la sortie.
Quand le parking est plein, la soupape range l'élément dans **un autre bassin** — et ce poste-là
retient à son tour un float-up. La saturation du parking remonte ainsi jusqu'à l'usine. Le
journal l'écrit à chaque calcul.

## Une seule paire de portes

Le site n'a qu'une paire de portes : **un seul float-up à la fois**. Le groupe dont l'élément
est le plus urgent passe d'abord, au sens du rang d'immersion — le même départage que pour les
places de bassin et de parking.

Cette règle a été ajoutée après vérification, non par principe. L'hypothèse de départ était que
le staggering suffisait à l'assurer : **il ne suffit pas**. Le staggering décale les *départs
béton*, pas les *sorties d'outfitting*. Mesuré avant la règle, sur la séquence brute du
classeur : **28 float-ups de groupes différents se chevauchaient** dans le temps, et sur la
séquence optimisée deux jours demandaient à deux ou trois bassins de se remplir ensemble —
le 24/12/2026 (PL-5, hall A et hall B le même jour) et le 09/03/2027.

Après la règle : **zéro chevauchement**, et elle ne coûte rien — zéro retard, zéro bloqué, même
date d'arrêt de l'usine. L'optimiseur trouve une séquence qui la respecte sans perdre un jour.

## Arrêts annuels de l'usine

Deux périodes par an, activables et réglables : **deux semaines à partir du lundi de la semaine
du 25 décembre** — ce qui couvre Noël et le jour de l'an — et **une semaine sainte**, celle qui
précède Pâques, dont la date est calculée chaque année.

Les arrêts ne décalent pas le travail, ils l'**étirent** : un élément dont la coulée traverse un
arrêt met d'autant plus de jours à sortir, et **rien ne démarre** pendant. Le test de
faisabilité du solveur en tient compte, sans quoi il jugerait tenable un rythme qui ne l'est
pas et découvrirait le retard une fois l'élément lancé. L'aval — float-up, bassin, ballast,
immersion — n'est pas concerné : ses dates viennent du planning P6, qui porte déjà son propre
calendrier.

**Ce que les arrêts coûtent, mesuré** (séquence optimisée, arrêt au plus tôt) :

| | Retards | Bloqués | Arrêt de l'usine |
|---|---|---|---|
| Sans arrêts | 0 | 0 | 11/07/2029 |
| Avec arrêts | **24** (43 j max, 547 j cumulés) | 0 | 18/01/2030 |
| Avec arrêts + accélération en cours de cycle | **0** | 0 | 27/09/2029 |

Trois semaines de production perdues par an ne se rattrapent pas toutes seules : avec les
arrêts, **l'accélération en cours de cycle cesse d'être une option et devient nécessaire** pour
tenir les dates d'immersion.

Sur la séquence **brute** du classeur, c'est plus net encore : sans arrêts elle donne 4 retards,
avec arrêts elle donne 0 retard mais **66 éléments qui ne s'immergent jamais** — le piège de
lecture habituel, un élément bloqué ne compte pas comme retardataire. L'optimiseur de séquence
n'est plus facultatif dès lors que les arrêts sont pris en compte.

Allonger les arrêts ne dégrade pas régulièrement le résultat : l'optimiseur redistribue les
éléments entre les lignes et retrouve souvent une solution à zéro retard. Ne lisez donc pas ces
variantes comme une courbe — chacune est un plan différent.

## Un jour de coulage par ligne

Cinq lignes qui démarrent le même jour, ce sont cinq premières coulées le même jour : centrale
à béton, grue et équipe de coffrage saturées en début de semaine puis désœuvrées ensuite. Chaque
ligne PL reçoit donc **son jour de la semaine** — PL-1 le lundi, PL-2 le mardi, … PL-5 le
vendredi par défaut, réglable ligne par ligne à l'étape 6 — et n'y lance un élément que ce
jour-là. La règle est activable ; elle l'est par défaut. La ligne SPE n'est pas concernée : ses
passages de zone viennent du planning P6.

Le reste du cycle suit. À cadence entière, les neuf coulées de segment d'un élément tombent
toutes ce même jour de semaine ; à cadence demi-entière (3,5 ou 2,5 ou 1,5 sem/segment) elles
alternent entre deux jours — c'est le rythme qui l'impose, pas la règle.

**Cette règle et le staggering se battaient.** Reporter un départ sur son jour de coulage laisse
la phase de la ligne en retard de ce même écart ; le solveur y lisait « cible franchie » et lui
faisait attendre un takt entier, à chaque cycle. Le dernier départ béton de PL-3 et PL-4 passait
de juin 2029 à mars 2031. Deux corrections : la cible de phase du staggering est elle-même
reportée sur le jour de coulage de la ligne, et la comparaison de phase tolère les quelques
jours de retard que ce report crée.

### Le prix de la règle, et d'où il vient

Mesuré sur le classeur de référence avec l'optimiseur de séquence : **4 éléments en retard,
17 jours au pire, 41 jours cumulés**, contre zéro sans la règle.

Ce prix n'est pas dû au choix des jours — six répartitions différentes, y compris en groupant
les deux lignes d'un hall sur le même jour, donnent toutes le même résultat. Il vient de la
**quantification à la semaine**.

Le cycle d'un élément dure `R × 7 × 9` jours. Tant que ce takt est un multiple de 7, le départ
retombe de lui-même sur le jour de la ligne et la règle ne coûte rien. Une cadence en
demi-semaines donne un takt qui ne l'est pas — 1,5 sem/segment fait 94,5 jours, soit 13,5
semaines — et le jour de semaine dérive à chaque élément. Il faut le rattraper, et le rattrapage
tombe sur les éléments les plus rapides, ceux de la fin de programme, qui n'ont plus de marge.

Vérifié par l'expérience : en retirant les cadences en demi-semaines de la liste des rythmes
(4 / 3 / 2 / 1 au lieu de 4 / 3,5 / 3 / 2,5 / 2 / 1,5 / 1), **la règle devient gratuite** —
zéro élément en retard, avec ou sans elle. Sur le classeur de référence, seuls 5 éléments
tournaient à 1,5 sem/segment ; ce sont eux qui portaient tout le coût.

**La règle se désactive donc d'elle-même à cadence intermédiaire**, et ne s'applique qu'aux
rythmes entiers (4, 3, 2, 1 sem/segment) où elle ne coûte rien — plutôt que de rattraper un
dérapage qui n'a de sens qu'au bénéfice de l'atelier, jamais à son détriment. Une ligne qui
passe d'un rythme entier à un rythme intermédiaire perd sa contrainte de jour le temps de la
cadence intermédiaire, et la retrouve dès qu'elle revient à un rythme entier — sans
intervention. Le journal le signale, avec les cadences concernées et le nombre d'éléments qui
en profitent : sans ce repère, un jour de coulage manquant en fin de programme passerait pour
un oubli plutôt que pour la règle qui s'applique.

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

### Dans la page de restitution : le profil réel, avec la descente

La coupe du rapport n'est plus ordinale : c'est le **profil en long**, chaque élément à son
**chaînage et à son niveau de pose réels**, relevés sur `TUX-DWG-ITP-GE-GE-GEN-COW-042012-B`.
Les deux bandes du dessin ont été calées séparément sur leurs axes — chaînage R² > 0,998,
niveaux R² = 1,000 — et donnent la **même échelle verticale**, ce qui les valide l'une par
l'autre. L'échelle verticale est exagérée d'environ 40 fois, comme sur le dessin d'origine.

Les SPE, dont le profil ne porte pas d'étiquette exploitable, sont placés au milieu de
l'intervalle laissé entre deux standard : **un tous les huit**, après TE-03, TE-11, … TE-75.
Deux sources indépendantes concordent — les écarts de chaînage anormalement larges tombent aux
mêmes endroits, et l'ordre du graphique « Tunnel Progress » donne la même intercalation.

**L'animation de descente** : chaque élément a un emplacement vide dessiné à sa position finale,
et son caisson descend verticalement à sa place dans les six jours qui précèdent son immersion.
La position est une **fonction de la date du curseur**, pas une transition déclenchée : le
curseur se déplace donc dans les deux sens sans désynchroniser l'animation, et une date donnée
redonne toujours la même image.

Les gabarits — 217 m pour un standard, 39 m pour un spécial, 9 m de hauteur — sont ceux du
programme, le profil ne les porte pas. C'est indiqué sous la coupe.

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

**Le découpage de l'après-coulée est tranché.** Les *repairs* et l'*integrated outfitting* se
font **en temps masqué pendant la coulée**, et s'achèvent pendant l'*Outfitting UB* : ils
n'occupent aucune zone à eux, donc leur ligne du planning reste vide. La phase d'outfitting du
solveur est l'**Outfitting UB** — l'élément y est transféré une fois sa coulée finie, et **y
reste statique** jusqu'au float-up. C'est exactement ce que le moteur fait déjà ; seule la vue
en plan a dû être corrigée, elle faisait glisser l'élément à travers la zone au lieu de l'y
laisser stationner.

**Approximation assumée** : deux occupations d'une même ressource qui se suivent à moins d'une
demi-semaine ne peuvent pas partager une colonne. La seconde est alors rognée d'une colonne —
174 barres sur 559 dans l'export de référence. Quand deux occupations sont réellement
simultanées, ce qui arrive au hook-up puisque les deux lignes d'une paire entrent en bassin
ensemble, les deux étiquettes sont accolées dans la même barre plutôt que d'en perdre une. Le
script annonce les deux chiffres à chaque exécution.

## Planning imprimable, dans la page de restitution

La même lecture que l'export Excel, mais dans le rapport : section **« Planning d'occupation du
site »**, une ligne par ressource, les 48 mêmes ressources, les mêmes couleurs.

Ce qui la rend imprimable est le **découpage en tranches de temps** : la page se coupe en
tranches de 3, 6 ou 12 mois, chacune portant ses propres libellés de ressource. À l'impression
chaque tranche part sur sa feuille — il n'y a rien à recoller, et aucun bandeau de libellés ne
manque. Le bouton *Imprimer le planning* masque le reste du rapport le temps du tirage, puis le
rétablit ; la mise en page vise l'A3 paysage.

Les arrêts annuels de l'usine sont hachurés en travers de toutes les lignes, les ressources non
modélisées gardent leur ligne en gris, et **chaque barre ouvre la fiche de l'élément** au clic.
Une case permet de masquer les lignes non modélisées pour un tirage plus dense.

### Les coulées, segment par segment

Une barre de coulée porte ses **neuf segments numérotés**. Les dates viennent du solveur — c'est
`datesSegments()` qui les calcule, arrêts d'usine compris, et le rapport ne les recalcule pas :
les deux vues ne peuvent donc pas diverger. Un segment dure une à quatre semaines et ne ferait
que quelques pixels sur un planning de six ans : son bloc reçoit une **largeur minimale** pour
que le numéro reste lisible. L'élément garde ses vraies dates, seul l'affichage est élargi. Le
numéro d'élément reste épinglé à gauche de la barre.

### Compteurs de coulées

Deux rangs au-dessus du planning, alignés sur la règle de temps : le nombre de coulées de
segment **par semaine** et **par mois**, toutes lignes confondues. C'est ce que voit la centrale
à béton. Une semaine qui dépasse une coulée par ligne se signale en rouge — c'est exactement la
charge que la règle du jour de coulage cherche à lisser, et le compteur permet de vérifier
qu'elle y parvient.

### Cheminement des éléments

Une case, décochée par défaut, relie les barres d'un même élément d'une ressource à la suivante :
béton, outfitting, bassin, parking, ballast, immersion. Le tracé est une courbe en S terminée
par une pointe, ramenée au bord de la tranche quand le saut en sort — un cheminement qui quitte
la page reste lisible comme tel. Quatre-vingt-neuf éléments font beaucoup de traits : le faisceau
est donc très pâle, et **survoler une barre isole le trajet de son élément**.

### Retouches manuelles

Une case *Ajuster à la main* rend les barres déplaçables : **de gauche à droite pour décaler les
dates au jour près, de haut en bas pour changer de ressource**. Le solveur n'est pas rejoué — les
retouches sont une couche par-dessus son résultat, ce qui permet de discuter une hypothèse (un
arrêt technique, une immersion repoussée) sans perdre le reste du calcul.

Chaque retouche est listée dans un bandeau au-dessus du planning, avec de quoi l'annuler pièce
par pièce ou d'un coup, et la barre déplacée se borde d'orange. Sans ce relevé, une barre
déplacée par mégarde se confondrait avec un résultat de calcul. Les compteurs de coulées se
recalculent sur le planning retouché.

### Deux barres pilotent vraiment le calcul

Toutes les barres se déplacent, mais **deux seulement sont des entrées du modèle** : la coulée
béton et l'immersion. Les glisser à l'horizontale **impose la date et relance le solveur** ;
tout le reste du planning en découle. Elles se distinguent à l'œil (curseur de redimensionnement,
soulignement bleu) parce qu'une barre qu'on croit pilotante alors qu'elle est calculée est pire
que pas de glisser-déposer du tout.

Les autres — outfitting, bassin, parking, ballast — sont des **sorties** des règles d'occupation.
Les imposer n'aurait pas de sens tant que le solveur ne sait pas raisonner sur des dates
contraintes ; elles restent donc de simples retouches d'affichage.

Deux précisions de sémantique, toutes deux visibles dans le journal :

- **un départ béton imposé est un « au plus tôt », jamais un « au plus tard »** : on peut
  retarder le lancement d'un élément, on ne peut pas rendre la halle libre plus tôt qu'elle ne
  l'est. Quand la halle, le déphasage ou l'ordre d'immersion repoussent encore le départ, le
  journal le dit, élément par élément, avec l'écart ;
- **déplacer une date d'immersion touche à une donnée du planning P6** et peut changer l'ordre
  d'immersion — précisément ce que le programme ne modifie jamais de lui-même. C'est une
  décision de l'utilisateur, appliquée telle quelle, et le journal signale en rouge les
  éléments dont le rang a changé.

Les impositions sont **non destructives** : chaque simulation repart des valeurs du classeur
avant de les réappliquer. Sans cette remise à zéro, retirer une imposition ne la retirerait pas
— la valeur forcée resterait écrite dans l'élément d'une simulation à l'autre, et le solveur
mentirait silencieusement. Le bandeau les liste et permet de rendre un élément, ou tous, au
solveur.

Mesuré sur le classeur de référence : repousser la coulée de STE-42 de deux mois fait passer les
retards de 4 à 13, le pire de 17 à 84 jours, et bloque 27 éléments. L'annulation restitue
exactement l'état initial.

### Le rapport de conséquences

Forcer une date rejoue tout : la séquence est réoptimisée, les retards et les blocages
recalculés, le planning d'occupation redessiné. Un tableau de bord dont les chiffres changent
n'apprend pourtant rien sans point de comparaison — d'où la section **« Conséquences des dates
imposées »**, qui apparaît dès qu'une date est forcée et se referme quand on la rend au solveur.

Elle donne l'écart contre **le dernier calcul sans aucune date forcée** : éléments en retard,
retard maximum et cumulé, éléments bloqués, date d'arrêt de l'usine, dernière immersion. Puis
l'onde de choc : combien d'autres éléments ont vu leur départ béton se déplacer et de combien,
lesquels manquent désormais leur date d'immersion sans la manquer avant, lesquels au contraire
la tiennent maintenant, lesquels ne sont plus immergés dans l'horizon.

Deux précautions y sont écrites plutôt que tues :

- **la séquence a été rejouée.** Quand l'optimiseur est actif il en choisit une nouvelle, et les
  déplacements affichés mêlent alors l'effet de la date forcée et celui de ce nouveau choix. Le
  panneau dit combien d'éléments ont changé de place et de ligne, et invite à décocher
  l'optimiseur pour isoler le seul effet de la date. Sans cela on attribuerait à un glissement
  d'un jour des décalages d'un an ;
- **la référence peut vieillir.** Elle est prise à la volée, au dernier calcul sans imposition,
  plutôt qu'en rejouant une simulation de contrôle à chaque geste — deux passages de l'optimiseur
  par glissement rendraient l'outil inutilisable. Si un paramètre change entre-temps, sa signature
  ne correspond plus et le panneau le signale en rouge.

Rien de tout cela ne remonte dans l'export : le format du planning peut donc continuer d'évoluer
sans casser les retouches, qui ne dépendent que du couple *(élément, ressource, date d'origine)*.

## Travaux marins et finitions, repris du planning P6

`extraire_p6.py` lit l'export P6 `TUXERev2LinkedActivities.xlsx` et en tire les seules
activités qui remplissent des lignes du Gantt que le solveur laissait vides :

```bash
python3 extraire_p6.py TUXERev2LinkedActivities.xlsx donnees_p6.txt
python3 planning_cible.py plan.json Target_schedule_solveur.xlsx donnees_p6.txt
```

**Le solveur n'en voit rien.** Ces dates ne servent qu'à l'affichage : le plan de production
reste entièrement calculé, et aucune de ces activités n'entre dans une contrainte. C'est une
consigne explicite, et elle vaut aussi pour les dates *ready for float-up*, dont le raccord
existe pourtant dans le parseur.

Dix familles, à la maille de WBS demandée — une ligne par famille, non une par élément, ce qui
en ferait 79 :

| Ligne du Gantt | Source dans le P6 | Éléments |
|---|---|---|
| Trench rectification (leveling layer) | activités « Leveling Layer Installation » | 12 |
| Gravel bed | « Gravel Bed » | 89 |
| Locking fill & Backfill | « Locking fill » et « Backfill » | 89 |
| Immersion joint removal (bulkheads) | WBS `Immersion Joint Removal` | 87 |
| Immersion joint infill concrete | WBS `Immersion Joint infill Concrete` | 87 |
| Omega seal installation | WBS `Omega seal installation` | 87 |
| Removal of TE system | WBS `Removal of TE System` | 79 |
| Drainage installation | WBS `Drainage Installation` | 89 |
| Walkways | WBS `Walkways` | 89 |
| Element ready for float-up (SPE) | « Element ready for floatup » | 10 |

Ces lignes portent des **teintes sourdes** et pas d'étiquette : elles se lisent comme une bande
d'activité, non comme une suite de barres. C'est délibéré — les finitions de 89 éléments se
recouvrent largement, et une ligne unique ne peut pas les empiler. On voit d'un coup d'œil ce
que le solveur calcule et ce qu'il ne fait que recopier.

`Trench verification` a été retirée : le P6 n'a aucune activité sous ce nom.

## Avancement des finitions

Une vue à part du planning, avec **son propre curseur** — les finitions courent jusqu'en mai
2030, bien au-delà de la fin de production. Le même profil en long que la coupe, mais rempli
par les finitions plutôt que par la pose : chaque élément porte **six bandes empilées** dans
leur ordre d'exécution — dépose des bulkheads au joint, béton de remplissage du joint, joint
Omega, dépose du système TE, drainage, passerelles — et chacune se remplit au prorata de
l'avancement de sa tâche récapitulative.

Les travaux de joint portent deux numéros dans le P6 (`77-78`). Ils sont attribués au **second
élément** du joint, celui qui vient d'être posé et que le joint raccorde.

Le rendu retrouve la lecture du graphique *Tunnel Progress* du chantier : les finitions
progressent depuis les deux rives vers le milieu. Le compteur donne le nombre d'éléments
terminés et en cours à la date affichée — 8 terminés en juillet 2027, 46 en octobre 2028, 89 en
mai 2030.

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

## Audit d'un planning P6 (`auditer_xer.py`)

`lire_xer.py` lit un export XER — le format tabulé de Primavera — sans jamais charger le fichier
entier : seules les tables et colonnes demandées sont gardées. Un champ mémo pouvant contenir
des retours à la ligne, une ligne qui ne commence pas par un jeton `%` est traitée comme la
suite de l'enregistrement précédent, et non comme un nouvel enregistrement.

`auditer_xer.py` en tire un rapport : volumétrie, options de calcul, types de liens, décalages,
extrémités ouvertes, contraintes, marges, durées, cohérence des dates, ressources, calendriers,
WBS, chemin déterminant. Les seuils cités sont ceux de l'évaluation DCMA en 14 points — un
repère, pas un verdict.

    python3 auditer_xer.py planning.xer -o audit.txt

Sur l'export de référence — 86 Mo, 67 000 activités, 107 000 liens, 108 calendriers — le
rapport sort en **4 secondes**. Le coût ne dépend pas de la taille du fichier : c'est le script
qui le lit, pas l'analyste.

## Planning de post-tension (`post_tension.py`)

Dérive un planning de post-tension du meilleur scénario de coulée calculé par le solveur,
au format Dywidag : la post-tension d'un élément commence **deux jours après le démarrage
de la coulée de l'élément suivant sur la même ligne** (règle du modèle Dywidag, cellule
E31) — le temps que le poussage l'ait dégagé et que le suivant soit engagé. Pour le dernier
élément d'une ligne, faute de suivant, le départ se prend sur sa propre fin de coulée.

```bash
node planning_runner.js classeur.xlsx 2026-08-05 > plan.json
python3 post_tension.py plan.json Post_tension.xlsx --threading 6 --stressing 4 --grouting 2
```

Sortie en Gantt classique — une ligne par élément, dates de début/fin par opération
(enfilage, mise en tension, injection), numéro d'élément en clair, plus un graphique en
barres empilées horizontal. La ligne SPE reste hors tableau : le solveur ne date pas la
coulée d'un élément spécial, il n'en suit que les passages d'aire — y lire un départ de
post-tension serait une donnée fabriquée. Les durées par opération (en postes D/N,
demi-journées) sont des paramètres de ligne de commande, pas des constantes du chantier :
les valeurs par défaut sont des repères à remplacer par celles de Dywidag.

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

La page affiche le mouvement des éléments sur le plan d'installation générale lui-même.
Elle ne redéfinit pas la géométrie du site : elle reprend le bloc `GEO` du solveur et le
convertit dans le repère du dessin, ce qui interdit toute dérive entre les deux vues. La
ligne SPE y occupe les sept aires repérées sur le plan, d'est en ouest — cpa, cp1, cp2, cp3,
ub1, ub2, ub3 — et les portes y sont animées.

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
planning P6, propre à chaque élément (4, 5 ou 25 jours sur le classeur de référence). Sans
cette donnée pour un élément, le solveur retombe sur `REGLES.ballastJoursDefaut` (7 jours) —
un repli interne, plus un paramètre de l'interface : il ne s'ajoute à aucune durée réelle
déjà connue.

**Les SPE n'ont pas de phase de ballast.** Ils ne figurent pas dans les activités de float-out :
un SPE passe du bassin à l'immersion, sans passer par le Ballast Jetty.

**Hook-up** : 24 h, sur place, juste avant le Ballast Jetty — tenues dans la durée de ballast
déjà comptée à rebours depuis l'immersion cible, pas une durée en plus. Une version antérieure
imposait, en plus de cette date réelle, une attente forfaitaire *depuis l'entrée en bassin* :
un élément déjà tendu sur sa date de ballast pouvait ainsi être retardé une seconde fois par
un jour de coulage sans rapport avec la contrainte physique. Corrigé : la sortie du bassin ne
dépend plus que de la date de ballast réelle (et des règles d'ordre, d'étanchéité SPE et de
sortie bloquée), plus d'aucune durée de hook-up réglable.

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

## Géométrie du plan (coordonnées relatives %, relevées sur le plan général)

Toutes les cotes sont mesurées sur le plan d'installation générale lui-même
(`vendor_plan.png`, 2000 × 991 px du plan TUX-DWG-PFA-AL-AL-GEN-FLC-002005-9A), soit par
lecture des ouvrages dessinés, soit par report des rectangles bleus tracés sur le PDF et
calés sur le fond par corrélation d'image (rapport 0,990, décalage 135 / 999 points).
Conversion : `x% = px / 20`, `y% = px / 9,91`.

| Repère | Valeur |
|---|---|
| Largeur d'un élément (Y) | 4,44 % (44 px) |
| Longueur standard (PL1-5) / spéciale (SPE) | 12,10 % (242 px = 217 m) / 2,20 % (44 px = 39 m) |
| X station de coulée → porte coulissante → travée outfitting → bassin | 90,48 → 76,85 → 64,75 → 55,75 |
| Y PL-1 / PL-2 / PL-3 / PL-4 / PL-5 / SPE | 70,53 / 64,73 / 44,75 / 39,00 / 18,97 / 12,76 |
| Parkings (6 places relevées une à une) | môle nord [14,60 ; 17,46] et [11,70 ; 25,63] à 0° ; môle sud [16,98 ; 73,03], [20,54 ; 79,02], [24,11 ; 85,02] à −50° ; réserve [43,22 ; 87,82] à 90° |
| Ballast Jetty (un seul poste, dans l'axe du quai) | [41,55 ; 20,69] à 90° |
| Postes en bassin (un par ligne, dans son axe) | A : 70,53 / 64,73 — B : 44,75 / 39,00 — C : 18,97 / 12,76, tous à x = 55,75 |
| Stockage SPE (angle nord-ouest du Basin C) | [52,50 ; 10,09] |
| Aires de la ligne SPE, d'est en ouest | 89,80 / 86,65 / 83,10 / 79,70 / 75,55 / 72,20 / 67,05 |
| Porte flottante | souille [46,55 ; 39,35] ; fermeture à x = 47,90, sur l'axe du bassin concerné |
| Porte coulissante (une par ligne PL) | x = 77,50 |
| Aire d'attente à flot | x = 33,00, quatre places visibles par bassin puis un compteur |

La station de coulée n'est pas au bord de halle relevé sur le fond (1702 px) mais **quatre
segments plus à l'est** (1810 px) : les quatre premiers segments d'un élément sont coulés à
l'intérieur des halles. Sans ce report, un élément en fin de coulée empiétait sur la travée
d'outfitting, ce qui ne se peut pas — le décalage supprime les 3 239 chevauchements que la
simulation produisait entre un béton et un outfitting de la même ligne.

Deux positions ne se lisent pas sur le plan parce qu'elles ne correspondent à aucun ouvrage :
l'aire d'attente à flot (un élément dont le float-up est fait mais dont le poste en bassin
n'est pas libre est au mouillage, sans emplacement dessiné) et l'écart en ordonnée appliqué
quand deux éléments d'une même ligne occupent la même travée — le modèle raisonne en zones
d'occupation, pas en mètres linéaires, et tolère une situation que la longueur réelle de la
ligne n'autorise pas toujours. Plutôt que de la masquer, la vue écarte les deux bandes.

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
