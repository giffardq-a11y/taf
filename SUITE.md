# État des lieux et prochaines étapes

Note de reprise. Les règles métier et leur justification sont dans `README.md` ;
ce document ne couvre que ce qui reste à faire et les décisions en attente.

## Résultat courant, sur `target_schedule_programme.xlsm`

Date de référence 05/08/2026, cadence de départ 3 semaines/segment (confirmée), staggering
actif, ligne SPE sur planning P6, séquence automatique :

**Aucun retard. Les 89 éléments s'immergent à leur date cible, au jour près.** Aucun bloqué,
aucune inversion sur les lignes PL, une seule fermeture provisoire de SPE à programmer.
Répartition retenue : 17/17/17/17/11 sur les lignes PL, en mode « arrêt de l'usine au plus
tôt » (18/17/17/17/10 à flux tendu).

L'usine s'éteint ligne par ligne, la dernière halle libérée le **11/07/2029** : PL-5 le
22/09/2028, PL-1 et PL-2 le 17/04/2029, SPE le 10/07/2029, PL-3 et PL-4 le 11/07/2029 —
**292 jours** d'extinction étalée. À flux tendu, mêmes zéro retard mais la dernière halle ne
se libère que le 14/10/2029 et l'étalement tombe à 180 jours. Le prix de l'arrêt anticipé est
du stockage à flot : 208 jours d'avance moyenne sur l'immersion contre 187, et un changement
de cadence de plus (15 contre 14).

Cinq corrections y ont conduit, toutes mesurées :

| | Retards | Retard max | Retard cumulé |
|---|---|---|---|
| Ligne SPE estimée, cadence relâchée | 18 | 133 j | 774 j |
| + ligne SPE sur planning P6 | 8 | 12 j | 34 j |
| + cadence jamais relâchée, lignes rééquilibrées | 4 | 12 j | 29 j |
| + ballast au planning, aucun pour les SPE | 2 | 5 j | 6 j |
| + plus de durée inventée en fin de chaîne SPE | **0** | **0** | **0** |

## Sortie de chaîne SPE : plus aucune durée inventée

Le planning ne date pas la sortie de la dernière zone qu'il couvre — la section `FI3` ne
contient de groupe que pour 2 SPE sur 10. Le solveur y appliquait la durée fixe d'UB3 de
`Config_SPE`, 3 semaines, ce qui rendait `SPE-06` en retard de 5 jours. Cette règle datait
d'avant l'exploitation du planning détaillé et **inventait un délai que le planning ne
contient pas** : elle est supprimée. Un SPE que le planning pilote est désormais prêt dès
qu'il atteint sa dernière zone datée.

Les durées fixes de `Config_SPE` ne servent plus qu'à un SPE dont le planning ne dit rien.

**À venir** : les dates *ready for float up*, c'est-à-dire le moment où un SPE est prêt à être
immergé — indépendamment de la zone UB où il se trouve. Le raccord est en place : dès que ces
activités figurent dans l'onglet `Immersion`, elles commandent la sortie de chaîne à la place
de tout le reste.

**Correspondance des zones — tranchée.** Le planning nomme trois zones d'aménagement :
`FI1 - Fit Out in Outfitting Buffer Area`, `FI2 - Fit Out in Upper Basin 1`,
`FI3 - Fit Out in Upper Basin 2`, là où `Config_SPE` déclare UB1, UB2, UB3. **L'aire tampon
est bien dans le Basin C** (confirmé) : la correspondance FI1→UB1, FI2→UB2, FI3→UB3 est la
bonne, et un SPE qui s'y trouve ferme à juste titre la porte d'inondation. Rien à changer.

Les retards d'arrondi ont disparu avec la durée de ballast lue au planning : elle vaut 4 ou
5 jours selon l'élément, non 7, et les cibles espacées de 6 ou 7 jours ne se télescopent plus.

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

| Variante | Inversions PL | Bloqués | Retards | Retard max | Retard cumulé |
|---|---|---|---|---|---|
| 1 (classeur) | 3 | 0 | 33 | 141 j | 1999 j |
| **1 optimisée** | **0** | **0** | **19** | **141 j** | **888 j** |
| 2 (classeur) | 1 | 5 | 36 | 141 j | 1761 j |
| 2 optimisée | 0 | 0 | 33 | 141 j | 1367 j |
| 3 (classeur) | 5 | 51 | 13 | 71 j | 559 j |
| 3 optimisée | 0 | 0 | 43 | 71 j | 1352 j |

C'est la **variante 1 optimisée** que retient le mode automatique. Deux pièges de lecture
qu'elle illustre :

- la variante 3 *au classeur* paraît la meilleure sur *Retards* (13) parce que 51 de ses
  éléments ne sortent jamais et ne comptent donc pas comme retardataires. C'est l'inverse
  d'un bon plan, et c'est pourquoi *Bloqués* passe avant *Retards* dans les critères ;
- une fois toutes débloquées, c'est la variante 1 qui l'emporte nettement (19 retards,
  888 j) — l'ordre du classeur n'était pas prédictif de l'ordre après optimisation.

Chaque variante garde une inversion sur la ligne SPE (`SPE-02`/`SPE-06`), sauf la 3. Elle
ne se corrige plus par la séquence — `SPE-02` est déjà en zone CP1 à la date de référence —
et n'a plus à l'être : le stockage l'absorbe.

## Pourquoi les dates d'immersion ne sont pas tenues — analyse de sensibilité

La question a été posée : le planning P6 prouve que ces dates sont tenables, pourquoi le
solveur n'y arrive-t-il pas ? Réponse mesurée, en désactivant les règles une à une
(variante 1, staggering actif) :

Mesures refaites une fois la ligne SPE pilotée par le planning P6, sur la séquence du
classeur :

| Configuration | Retards | Retard max | Retard cumulé |
|---|---|---|---|
| Référence | 22 | 104 j | 1145 j |
| Sans staggering | 24 | 128 j | 1509 j |
| Sans ordre d'immersion imposé | 3 | 104 j | 170 j |
| Ancre de cadence à 1 sem/segment | 23 | 65 j | 761 j |
| Toutes règles levées | 3 | 49 j | 69 j |

Deux enseignements :

1. **L'ordre d'immersion imposé est le premier amplificateur** : à lui seul il fait passer le
   retard cumulé de 170 à 1145 jours. Il ne crée presque aucun retard, il les propage — un
   élément retenu bloque tous ceux qui le suivent, même prêts. Ce n'est donc pas la séquence
   de production qui pèche : la réordonner ne change pas la cause. C'est une donnée d'entrée
   P6, non modifiable, et le programme ne la modifie pas : la ligne ci-dessus est un
   diagnostic, pas une proposition.
2. **L'ancre de cadence est bien de 3 semaines/segment** — confirmé par l'utilisateur, c'est
   la valeur de `Config_Cycles` et le solveur l'utilise déjà. La ligne « ancre à 1 sem » du
   tableau n'est donc qu'un point de comparaison : elle chiffre ce que coûte la montée en
   cadence (8 mois pour passer de 3 à 1 semaine, à raison d'1 semaine par 4 mois), non un
   réglage à changer. Ce coût est structurel et se paie en début de programme.

Le staggering, lui, ne coûte rien : il *réduit* les retards (1145 j contre 1509 sans lui).

**Le relâchement de cadence coûte cher.** Le solveur atteignait la cadence d'1 semaine/segment
le 30/05/2027, puis **remontait volontairement à 1,5** en février 2028 : c'est l'exception
« relâcher une fois en fin de programme », censée être économique. Mais le test de faisabilité
du solveur de cadence ignore l'aval — bassins, parking, ordre d'immersion — et conclut qu'un
rythme plus lent tient alors qu'il ne tient pas. Mesure, à séquence du classeur :

| | Retards | Retard max | Retard cumulé | Changements de cadence |
|---|---|---|---|---|
| Relâchement autorisé | 22 | 104 j | 1145 j | 18 |
| **Relâchement interdit** | **14** | **19 j** | **113 j** | **14** |

Il coûte donc des retards *et* des changements de cadence supplémentaires. La règle première
du `README` — « une cadence atteinte n'est jamais relâchée » — est désormais le comportement
par défaut ; l'exception reste accessible par une case de l'interface.

**Le planning est tenable — mesuré.** Avec la séquence automatique et l'étanchéité avancée
de 42 semaines : **5 éléments en retard, 1 jour au maximum, 5 jours de cumul**, aucun bloqué.
C'est bien ce que le planning P6 laissait attendre. Il fallait pour cela trois choses, aucune
n'étant l'ordre de production : corriger la mesure des retards, laisser le solveur choisir la
séquence et les lignes, et avancer l'étanchéité.

Sur ce dernier point, les paliers intermédiaires ne rapportent rien : 11, 21 ou 32 semaines
d'avance laissent les 19 retards inchangés, et seul le palier de 42 semaines fait basculer à 5.
La porte est fermée par le SPE présent en UB à l'instant considéré ; tant qu'il reste un SPE
non étanche, avancer les autres ne change rien. C'est un tout ou rien, et la boîte de dialogue
le montre.

**Règle corrigée, en cascade** (précisée par l'utilisateur) : le clamping P6 *est* l'étanchéité
— la fermeture définitive. Quand il tombe trop tard pour le planning, une **fermeture
provisoire** le remplace, possible au plus tôt 12 semaines après la **sortie de CP3**, et
descendable à 8 semaines au prix d'un planning critique. La position du SPE dans la chaîne UB
n'entre pas en compte : les travaux peuvent commencer en UB1 et s'achever en UB2. Une fois le
seuil franchi, le SPE ne bloque plus jamais — il est rouvert puis refermé à la demande.

**La ligne SPE suit désormais le planning P6**, qui date chaque passage de zone (activités de
skidding sous les niveaux CPA / CP1 / CP2 / CP3 / FI1 / FI2 / FI3). Elle n'est plus estimée
par les durées fixes de `Config_SPE`, qui ne servent que de repli. C'est ce qui manquait :

| | Retards | Retard max | Retard cumulé |
|---|---|---|---|
| SPE estimée à 5 sem/zone, séquence classeur | 32 | 133 j | 1885 j |
| SPE estimée, séquence optimisée | 18 | 133 j | 774 j |
| **SPE sur planning P6, séquence classeur** | 22 | 104 j | 1145 j |
| **SPE sur planning P6, séquence optimisée** | **8** | **12 j** | **34 j** |

Et **aucune fermeture provisoire n'est nécessaire** : les dates de clamping tombent assez tôt,
le niveau 1 de la cascade suffit partout. Les sept premiers SPE tiennent leur date exactement ;
seuls `SPE-06` (+12 j), `SPE-03` et `SPE-04` glissent.

**Question ouverte, chiffrée** : le classeur laisse la colonne G de `Config_SPE` vide, donc
chaque zone UB dure 5 semaines. Un SPE entre alors en UB1 tous les 35 jours alors qu'il lui
faut 84 jours pour être provisoirement étanche : **2,4 SPE sont en permanence non étanches**,
et le bassin n'est presque jamais inondable. Renseigner la colonne G à 12 semaines rétablit la
cohérence et change le résultat du tout au tout :

| Durée des zones UB | Séquence classeur | Séquence optimisée |
|---|---|---|
| 5 sem (classeur, colonne G vide) | 32 retards, 133 j max, 1885 j | 18 retards, 133 j max, 774 j |
| 12 sem (colonne G renseignée) | 24 retards, 104 j max, 1231 j | **18 retards, 53 j max, 276 j** |

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

### 5. Étanchéité SPE négociable — fait

La contrainte reste stricte ; c'est la durée pour l'atteindre qui devient un paramètre. Après
chaque calcul, le solveur chiffre ce que la porte du Basin C coûte, cherche par dichotomie le
gain minimal qui l'annule, mesure des paliers intermédiaires, et ouvre une boîte de dialogue
où l'utilisateur choisit le niveau d'accélération — ou le refuse. La page de rapport porte le
même champ et signale le gain possible dans son journal.

### 6. Interface entièrement paramétrable — commencée

**Fait** : les règles du modèle sont sorties du code. Elles vivaient en constantes
(`RYTHMES`, pente d'inertie, segments, déphasages, seuils d'étanchéité, parking) ; elles sont
maintenant dans un objet `REGLES` unique, exposé à l'étape 6 de l'interface avec un libellé
métier par règle, et un bouton de retour aux valeurs de référence. Modifier une règle change
le calcul : porter la pente d'inertie de 4 à 2 mois fait passer de 4 à 9 retards.

**Fait aussi** : l'**état as-built se règle à l'écran** (étape 3). Une ligne par élément, le
statut dans une liste adaptée à la ligne — segments béton, outfitting, bassin, parking… pour
une PL, les sept zones pour la SPE — avec sa date de début et un filtre. Le classeur remplit
le tableau au chargement ; la saisie écran prime ensuite, y compris quand le classeur est relu
(changement de séquence, mode automatique), ce qui demandait de porter la surcharge dans le
moteur et non dans la page.

**Fait aussi** : la **capacité des bassins** est paramétrable — nombre de bassins et places
par bassin — comme le reste des règles. Plus rien du dimensionnement n'est en dur.

**Fait aussi** : la **coupe du tunnel**, sous la vue en plan. Les 89 éléments côte à côte,
`STE-01` à gauche, `STE-79` à droite, la pose progressant avec le même curseur temporel que
la production. Positions provisoires — l'ordre est juste, les distances non — à reprendre du
plan de coupe quand il sera disponible.

**Reste** : les icônes par élément sur le plan de production lui-même ; le tableau as-built
et la coupe en portent déjà une par statut.

### 6bis. Interface — spécification d'origine

Demandé par l'utilisateur : une interface HTML où l'**état actuel se définit à l'écran** au
lieu d'être saisi dans le classeur (colonnes as-built de `Inputs`), avec des **icônes par
élément portant leur statut**, et où **toutes les règles du modèle sont visibles et
modifiables** — cadences autorisées, pente d'inertie, staggering, seuils d'étanchéité, places
de bassin et de parking, durées de float-up et de ballast. Aujourd'hui une partie de ces
règles est dans le classeur, une autre en constantes du code (`RYTHMES`, `SLOPE_*`, `STAGGER`,
`SEUIL_ETANCHE_*`, `GEO`) : les remonter dans l'interface est le chantier suivant.

### 7. Coupe des éléments immergés — faite, positions provisoires

Les 89 éléments côte à côte dans l'ordre de pose, `STE-01` à gauche et `STE-79` à droite,
dans **les deux pages** : sous la vue en plan de `index.html`, et dans la page de restitution
où elle suit le curseur du plan animé. Elle n'existait d'abord que dans `index.html`, ce qui
la rendait invisible depuis le rapport publié — corrigé.

Reste l'attente initiale : le PDF de coupe, pour remplacer l'ordre de pose par les abscisses
réelles. Le rendu ne changera pas, seulement l'échelle horizontale.

### 8. Arrêt progressif de l'usine — fait

Règle `REGLES.arretAuPlusTot`, cochée par défaut, exposée dans les deux pages. Elle inverse
l'économie du solveur : au lieu de tenir la cadence la plus lente qui respecte les dates, la
ligne prend la plus rapide que la pente autorise et s'arrête dès sa file vidée. Le critère
« fin de production » entre aussi dans l'ordre lexicographique de l'optimiseur, entre les
retards et le nombre de changements de cadence.

Le stockage aval reste la limite physique : un élément sans place attend en halle et la ligne
ralentit d'elle-même. C'est pourquoi le gain est de trois mois et non davantage.

### 9. Accélération en cours de cycle et date de décision — fait

Une cadence ne pouvait changer qu'au lancement d'un élément : la pente s'ouvrait et rien ne se
passait jusqu'au prochain départ béton, 35 à 84 jours plus tard. Deux leviers ajoutés, tous
deux facultatifs et sans effet sur le résultat de référence quand ils sont laissés au repos :

- **Accélérer en cours de cycle** — revue quotidienne des cadences, et l'élément en coulée
  finit ses segments restants au nouveau rythme (le segment entamé se termine à l'ancien).
  Les cinq lignes PL s'éteignent sept semaines plus tôt, à zéro retard. La date d'arrêt du
  site ne bouge pas pour autant : c'est la ligne SPE, réglée par le planning P6, qui devient
  contraignante.
- **Date de décision d'accélérer** — point de départ de la pente. Vide, comportement
  inchangé. Le chiffrage du retard de décision est dans `README.md` : un an de retard à
  décider coûte 63 éléments en retard.

Reste ouvert : la montée en cadence réelle est continue, ce modèle s'arrête au segment. Si la
granularité fine devient nécessaire, c'est `raccourcirEnCours` qu'il faudra reprendre.

### 10. Relevé exhaustif des contraintes — fait

74 contraintes en 12 familles dans la page de restitution, avec seuil, origine et statut
(réglable / donnée / figé / à trancher). Tenu à la main d'après le solveur, avec les seuils lus
dans `REGLES` et `PARAMS`. Les deux points sortis de l'audit sont réglés :

- **Doublon** — la date d'entrée au Ballast Jetty était écrite quatre fois à l'identique ;
  tout passe désormais par `dateDebutBallastDe`. Résultat de référence inchangé.
- **Règle morte** — `Config_Outfitting` (6 phases × 2 séquences) était lu et journalisé sans
  entrer dans aucun calcul. Sur décision de l'utilisateur, l'onglet est retiré : lecture,
  valeurs par défaut, génération du modèle et date `Seq2_Debut` de `Inputs` avec. Le calcul
  est inchangé, par construction — la durée d'outfitting vaut `segmentsOutfitting × rythme × 7 j`.

Trois autres points relevés, sans conséquence pour l'instant mais à garder en tête :

### 11. Départage des lignes concurrentes, icônes et fiche d'élément — fait

Le départage se fait par **rang d'immersion** puis ordre de production, au lieu de l'ordre du
tableau : sur la séquence brute du classeur, la variante 1 passe de 18 bloqués à 0 et la
variante 2 de 7 retards à 0. Avec l'optimiseur, le résultat était déjà à zéro et le reste.

Les éléments portent leur **icône de statut** sur les deux vues en plan, avec légende, et
l'icône subsiste quand l'élément devient trop court pour son identifiant. Dans la page de
restitution, **tout élément représenté ouvre sa fiche au clic** — grille de séquence, coupe du
tunnel, plan animé : toutes ses dates, ses places de bassin et de parking, son écart à la cible.

**Reste sur la partie graphique** (repoussé par l'utilisateur) : la vue en plan et la coupe
demandent encore du travail de fond — position réelle du Ballast Jetty et de la zone de
stockage SPE, abscisses de la coupe, et un rendu des éléments plus proche du plan réel.

### 12. Arrêts annuels de l'usine — fait

Règle `REGLES.vacances`, cochée par défaut, avec `noelSemaines` (2) et `paquesSemaines` (1)
réglables. Deux semaines dès le lundi de la semaine du 25 décembre, une semaine sainte (Pâques
calculé par l'algorithme grégorien). Les durées de béton et d'outfitting s'étirent sur les
arrêts, aucun élément ne démarre pendant, et le test de faisabilité du solveur en tient compte.

Conséquence mesurée : les arrêts rendent **l'accélération en cours de cycle nécessaire**. Sans
elle, 24 retards ; avec elle, retour à zéro. Sur la séquence brute du classeur, les arrêts font
passer de 4 retards à 66 éléments jamais immergés.

**Non couvert volontairement** : les arrêts ne s'appliquent qu'à la production (béton,
outfitting). Le float-up, les bassins, le ballast et l'immersion suivent le planning P6, qui
porte son propre calendrier. Si les opérations marines s'arrêtent aussi, c'est à ajouter.

### 13. Planning imprimable — fait

Section « Planning d'occupation du site » dans la page de restitution : mêmes 48 ressources et
mêmes couleurs que l'export Excel, découpée en tranches de 3, 6 ou 12 mois. Chaque tranche
porte ses libellés et part sur sa propre feuille à l'impression (A3 paysage). Arrêts de l'usine
hachurés, lignes non modélisées en gris et masquables, barres cliquables vers la fiche.

Piège rencontré, à retenir : le rapport utilisait déjà `#gantt` et le préfixe de classe `g-`
pour l'écoulement de production, et cet identifiant figure dans la liste des conteneurs vidés à
chaque rendu. Le nouveau planning se faisait donc effacer juste après avoir été construit. Il
porte désormais `#planning` et le préfixe `pl-`.

**Envisagé, non fait** : l'éditeur à blocs déplaçables qui rejouerait la simulation après un
décalage saisi à la main. C'est la suite naturelle de cette section si le besoin se confirme.

## Points relevés, sans conséquence aujourd'hui

- `REGLES.basins` est réglable, mais `groupeId` fige à 3 le nombre de groupes de lignes :
  réduire le nombre de bassins n'affecte que la soupape de stockage croisé, pas l'affectation.
- Le budget de recherche de l'optimiseur (8 s), la fenêtre de déplacement (±4) et le nombre de
  lignes d'accueil essayées (5) ne sont pas exposés.
- L'horizon de simulation (6 ans) et la tolérance de phase du staggering (0,5 j) non plus.

## Onglets du classeur devenus caducs

`Recap_Dates` est le résultat de l'ancienne macro, pas une donnée d'entrée : il n'a plus lieu
d'être et le solveur ne le lit pas. J'en avais tiré à tort que la cadence réelle était d'une
semaine par segment contre les 3 semaines déclarées dans `Config_Cycles` — c'était lire le
résultat d'un calcul, pas le chantier. La cadence de 3 semaines est confirmée.

## Défauts corrigés au passage

**Un SPE placé par son statut as-built ignorait sa date de clamping P6.** `placerEnZoneSPE`
recalculait le jalon théorique au lieu de passer par `dateEtancheDe`, court-circuitant à la
fois la règle documentée (« la date P6 prime sur le jalon de la colonne F ») et le gain
d'étanchéité. Sur ce classeur, `SPE-08` était réputé étanche le 28/10/2026 au lieu du
06/05/2026.

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
