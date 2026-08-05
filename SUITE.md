# État des lieux et prochaines étapes

Note de reprise. Les règles métier et leur justification sont dans `README.md` ;
ce document ne couvre que ce qui reste à faire et les décisions en attente.

## Où en est le modèle

Toutes les règles arrêtées sont implémentées et vérifiées sur le classeur réel :
flux tendu au 7ᵉ segment du suivant, cliquet de cadence, ordre d'immersion imposé,
étanchéité SPE datée par les activités de clamping, ordre de sortie des bassins,
stockage croisé, parking 5 places + 1 réserve.

S'y ajoutent désormais le **staggering entre halls**, l'**optimiseur de séquence** et le
**comparatif** — les trois points ci-dessous étaient à construire, ils sont faits. Le
solveur de cadence et l'optimiseur de séquence se pilotent séparément depuis l'étape 5 de
l'interface, et le choix de la séquence du classeur y est exposé.

## Le blocage de départ : diagnostic et levée

Mesures faites sur `target_schedule_programme.xlsm`, date de référence 05/08/2026,
staggering actif, 1 place de stockage SPE.

Les 38 éléments bloqués de la variante 1 ne venaient **pas** des inversions de séquence.
Ils tenaient à un seul verrou physique : `SPE-06` doit s'immerger le 16/10/2028, `SPE-02`
le 30/11/2028, mais `SPE-02` est produit avant et occupait la place SPE du Basin C jusqu'à
son propre ballast. `SPE-06` finissait sa chaîne dès mars 2027 sans jamais pouvoir entrer,
et l'ordre d'immersion imposé gelait derrière lui 37 éléments pourtant tous prêts.

Vérifié par l'expérience : corriger les trois inversions des lignes PL ne changeait rien
(38 bloqués) ; échanger les deux dates d'immersion débloquait tout (0 bloqué).

**La zone de stockage SPE lève ce verrou**, sans toucher aux dates : `SPE-02` part en
stockage quatre jours après son hook-up, `SPE-06` prend la place et s'immerge, `SPE-02`
revient pour son ballast. Le chantier n'en compte qu'**une seule place** (confirmé), et elle
suffit : en essayer deux ne change rien.

| Variante | Inversions | Bloqués | Retards | Retard max | Retard cumulé |
|---|---|---|---|---|---|
| 1 (classeur) | 4 | 0 | 85 | 140 j | 1993 j |
| 1 optimisée | 1 | 0 | 85 | 140 j | **896 j** |
| 2 (classeur) | 2 | 5 | 80 | 140 j | 1751 j |
| 2 optimisée | 1 | 0 | 85 | 140 j | **935 j** |
| 3 (classeur) | 6 | 51 | 34 | 70 j | 559 j |
| 3 optimisée | 0 | 0 | 85 | 70 j | 609 j |

Lecture : la variante 3 paraît meilleure sur *Retards* parce que 51 de ses éléments ne
sortent jamais et ne comptent donc pas comme retardataires. C'est l'inverse d'un bon plan,
et c'est pourquoi *Bloqués* passe avant *Retards* dans les critères.

L'inversion résiduelle est `SPE-02`/`SPE-06` : elle ne se corrige plus par la séquence —
`SPE-02` est déjà en zone CP1 à la date de référence — et n'a plus à l'être, le stockage
l'absorbe. Le journal la distingue désormais des inversions de lignes PL, qui, elles,
bloquent vraiment.

## Pourquoi les dates d'immersion ne sont pas tenues — analyse de sensibilité

La question a été posée : le planning P6 prouve que ces dates sont tenables, pourquoi le
solveur n'y arrive-t-il pas ? Réponse mesurée, en désactivant les règles une à une
(variante 1, staggering actif) :

| Configuration | Retards | Retard max | Retard cumulé |
|---|---|---|---|
| Référence | 33 | 141 j | 1999 j |
| Sans porte d'étanchéité du Basin C | 19 | 104 j | 1116 j |
| Ancre de cadence à 1 sem/segment | 26 | 141 j | 1218 j |
| Étanchéité levée + ancre 1 sem | 12 | 65 j | 335 j |
| Sans ordre d'immersion imposé | 5 | 141 j | 314 j |
| Toutes règles levées | 3 | 49 j | 69 j |

Trois enseignements :

1. **L'ordre d'immersion imposé est le premier amplificateur** : à lui seul il fait passer le
   retard cumulé de 314 à 1999 jours. Il ne crée presque aucun retard, il les propage — un
   élément retenu bloque tous ceux qui le suivent, même prêts. Ce n'est donc pas la séquence
   de production qui pèche : la réordonner ne change pas la cause.
2. **La porte d'étanchéité du Basin C est le premier générateur.** `STE-70`, 141 jours de
   retard, est en bassin dès la date de référence et n'en sort qu'en juillet 2027 : évacuer
   un élément normal impose d'inonder, donc d'attendre l'étanchéité du SPE présent en UB.
3. **L'ancre de cadence du classeur contredit le classeur lui-même.** `Config_Cycles`
   déclare 3 semaines/segment ; l'onglet `Recap_Dates`, produit à partir du même planning,
   montre 7 jours par segment sur tous les éléments — soit 1 semaine. Avec la pente d'inertie
   (1 semaine de variation par 4 mois), partir de 3 coûte 8 mois avant d'atteindre 1. Corriger
   cette seule saisie fait passer le cumul de 1999 à 1218 jours.

**Faut-il itérer entre séquence et cadence, essayer toutes les combinaisons ?** Non, et pas
par manque de moyens : l'espace des affectations seul vaut 5^79. Surtout, la mesure ci-dessus
montre que la séquence n'est pas la contrainte active — les retards viennent de trois règles
du modèle, pas de l'ordre de production. Le solveur explore déjà conjointement séquence et
cadence, puisque chaque séquence candidate est évaluée par une simulation complète où le
solveur de cadence tourne. Ce qui reste à trancher est métier, pas algorithmique : la porte
d'étanchéité est-elle aussi stricte en réalité, et quelle est la cadence de départ ?

## Ce qui a été construit

### 1. Staggering entre halls — fait

Conforme à la règle confirmée : 3 segments entre hall A et hall B, dur à partir de la
cadence de 1 semaine/segment et simple préférence en deçà ; 7 segments pour PL-5, jamais
bloquant ; aucun déphasage intra-hall. Détail dans `README.md`.

**Point tranché** — que faire quand les deux halls ne tournent pas à la même cadence :
le déphasage est **suspendu** le temps qu'elles se rejoignent, plutôt que de brider le hall
le plus rapide. Une phase ne se conserve qu'entre takts égaux ; la tenir sur des cadences
différentes coûterait une attente à chaque cycle sans jamais la rattraper. Le cas est porté
au journal quand il se produit. La décision se change en une ligne (`hallsMemeCadence`
dans `index.html`) si l'arbitrage inverse est préféré.

Deux points de conception qui ne sont pas des réglages arbitraires :

- Sous contrainte dure, la ligne patiente **jusqu'au segment visé, sans plafond**. Une
  attente écourtée se reproduirait à chaque cycle : les takts étant égaux, une phase ratée
  ne se rattrape jamais toute seule. Payée une fois, elle se conserve ensuite d'elle-même.
- Le déphasage cesse de s'appliquer dès que le **hall A n'a plus rien à lancer** : sans
  départ à venir il n'y a plus de phase, et attendre bloquerait la fin de programme.

### 2. Optimiseur de séquence — fait, affectation aux lignes comprise

Objectif respecté : zéro inversion d'abord, retards ensuite, staggering en contrainte dure
à 1 semaine. Activable et désactivable depuis l'interface, comme le staggering.

**Constat qui a guidé la suite** : une file sans inversion est une file triée par date
d'immersion — l'ordre est **unique aux ex æquo près**. Or les 89 éléments du classeur ont
tous une date d'immersion, toutes distinctes, toutes issues du planning P6 : aucun élément
sans date, aucun ex æquo (vérifié). L'ordre sans inversion est donc entièrement déterminé,
et l'affinage à l'intérieur d'une ligne n'a rien à déplacer. À lignes figées, l'optimiseur
se réduisait au tri. D'où l'affectation aux lignes, qui est le seul vrai levier.

Les mouvements internes à une ligne (éléments sans date, dates partagées) restent codés :
le moteur tolère un onglet `Immersion` incomplet et le signale. Sur ce classeur-ci ils ne
s'appliquent jamais.

**Affectation aux lignes** : les 5 lignes PL sont interchangeables, la ligne SPE non. Le
classeur porte 17/17/17/17/11 éléments. L'optimiseur essaie une répartition équilibrée par
ordonnancement de liste, puis déplace un à un les éléments en retard vers les lignes les
moins chargées. Sur la variante 1, le rééquilibrage global n'a pas battu la répartition du
classeur, mais **un seul déplacement ciblé** (`STE-04` : PL-3 → PL-5) fait passer le retard
cumulé de 1365 à 896 jours. Sur la variante 2, 7 déplacements font 1751 → 935 j.

### 3. Comparatif — fait

Bouton *Comparer* : séquence du classeur contre séquence optimisée, sur inversions,
bloqués, éléments en retard, retard max, retard cumulé et changements de cadence. La
séquence gagnante reste appliquée et affichée à l'écran.

**Lecture du tableau** : lever les inversions débloque des éléments, et un élément débloqué
qui arrive en retard bascule de la colonne *bloqués* vers la colonne *retards*. Le nombre de
retards peut donc augmenter alors que le plan s'améliore. C'est pour cela que les deux
colonnes figurent côte à côte, et que les critères sont comparés dans cet ordre.

### 4. Séquence automatique, grille et animation — fait

Le menu de séquence porte une entrée **« Automatique — le solveur choisit »** : chaque
séquence du classeur est optimisée, et la meilleure l'emporte. Sur ce classeur, la 1 gagne
(19 retards, 888 j de cumul) devant la 2 (33, 1367 j) et la 3 (43, 1352 j).

La page de rapport dessine la séquence comme l'onglet `Inputs` : une colonne par ligne, un
jeton par élément dans l'ordre de production. Le bouton *Classeur / Optimisée* fait glisser
les jetons d'une séquence à l'autre, ceux qui bougent s'allumant à l'accent. Le mouvement
se lit d'un coup d'œil, sans comparer deux tableaux.

### 5. Coupe des éléments immergés — à faire

Inchangé : l'utilisateur fournira un PDF de coupe avec le positionnement des éléments. À
remplir au fil des immersions, comme le plan d'installation l'est déjà pour le mouvement en
surface.

## Défauts corrigés au passage

**53 des 85 « retards » n'existaient pas.** Les dates cibles du planning P6 portent une heure
— 17:00, 20:00, 22:00, 09:00 selon l'élément — alors que le moteur avance d'un jour entier et
date ses immersions à minuit. Un élément immergé le bon jour était compté en retard d'un jour.
Toute date lue est désormais ramenée au jour (`jourSeul` dans `index.html`). Le décompte passe
de 85 à 33 retards réels, dont 26 dépassent le mois.

**Un jalon d'étanchéité non renseigné fermait la porte pour toujours.** `speNonEtancheEnUB`
traitait « pas de date d'étanchéité » comme « pas encore étanche », donc bloquait l'évacuation
du Basin C indéfiniment — l'inverse de ce que le README annonce (« la contrainte est
inactive »). Sans jalon, il n'y a rien à attendre : la porte reste ouverte.

**Les inversions de la ligne SPE faussaient le choix entre variantes.** Elles comptaient au
même rang que celles des lignes PL alors que la zone de stockage les absorbe. Le critère les
sépare : les éléments bloqués passent en tête, puis les inversions des seules lignes PL. Sans
cette correction, l'automatique retenait la variante 3 (43 retards) au motif qu'elle n'avait
aucune inversion SPE, contre la variante 1 (19 retards).

Quand deux éléments d'une même ligne attendaient ensemble — l'outfitting peut se libérer
avant que le float-up n'ait eu lieu — le moteur prenait **le premier du tableau `elements`,
c'est-à-dire l'ordre des lignes du classeur**, et non le plus ancien de la file. Même
séquence, résultats différents selon la disposition des lignes dans `Inputs` : sur le jeu
d'essai, 53 éléments bloqués contre 6 pour un ordre de production pourtant identique.
Le choix se fait désormais sur `ordreSeq` (`premierDeLigne` dans `index.html`), ce qui rend
la simulation indépendante de la disposition du classeur — condition pour que la séquence
proposée par l'optimiseur, une fois recopiée dans `Inputs`, donne exactement le même plan.

**Une simulation modifiait ses propres données d'entrée.** Un élément sans date d'immersion
s'en voyait attribuer une au ballast, et cette date survivait à l'exécution : deux essais de
la même séquence ne partaient donc pas des mêmes données. L'optimiseur comparait des
candidats évalués sur des bases différentes, et comptait comme inversions des couples dont
la date avait été inventée par la simulation elle-même. La date cible est désormais
restaurée à chaque exécution, et tout ce qui décide de la séquence passe par `dateCible()`,
qui ne lit que la donnée d'entrée.

**Le rang de production lu ne valait pas le rang renuméroté.** `ordreSeq` reprenait le numéro
de ligne du classeur, qui saute dès qu'une colonne est vide, alors que l'optimiseur
renumérote de 1 à n par ligne. Les deux donnaient des plans légèrement différents (1,6 % sur
le retard cumulé), l'ordre du tableau départageant les lignes qui se disputent une place de
parking le même jour. La lecture normalise désormais comme l'optimiseur.

## Évolutions notées, non planifiées

- **Départage des lignes concurrentes.** Quand deux lignes se disputent la même place de
  parking ou de bassin le même jour, c'est l'ordre du tableau des éléments qui tranche, non
  l'urgence. Départager par rang d'immersion serait plus juste — et rendrait le plan
  totalement indépendant de la disposition du classeur.
- **Pentes progressives de cadence.** Un changement de rythme se fait
  graduellement dans la réalité, pas d'un jour à l'autre.
- **Position de la zone de stockage SPE** sur le plan : extrapolée à l'ouest du Basin C,
  à recalibrer. Sa capacité, elle, est connue — une place.

## Réserves connues

- Les 7 aires SPE sont réparties uniformément entre l'entrée est et les bassins,
  faute de leurs abscisses exactes. L'ordre et la séparation sont justes, les
  largeurs approchées.
- Le solveur ne modélise ni les deux portes du Basin C ni le déphasage entre halls quand il
  choisit la cadence : ses estimations de délai restent optimistes sur PL-3, PL-4 et PL-5.
  La simulation, elle, applique les deux.
- L'optimiseur tourne sous budget de temps (8 s par défaut, chaque candidat coûtant une
  simulation complète — environ 100 candidats sur le classeur réel). Il peut s'arrêter avant
  d'avoir épuisé le voisinage ; la meilleure séquence trouvée est alors retenue.
- `Config_Outfitting` ne pilote plus le calendrier ; l'onglet ne sert plus qu'aux
  noms de phases. Il est conservé pour ne pas casser les classeurs existants.
