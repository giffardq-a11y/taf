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

## Le blocage de départ est levé

Aucune des trois séquences de production du classeur n'était réalisable : chacune contient
des inversions — un élément produit avant un autre qu'il doit immerger après — et les places
en aval étant uniques, la ligne se bloque.

| Variante | Inversions | Bloqués | Retards | Retard max |
|---|---|---|---|---|
| 1 (originale) | 4 | 38 | 47 | 140 j |
| 2 | 2 | 38 | 47 | 140 j |
| 3 | 6 | 51 | 34 | 70 j |

Inversions de la variante 1, signalées au chargement :
PL-3 `STE-12`/`STE-47`, PL-4 `STE-11`/`STE-48`, PL-5 `STE-29`/`STE-34`,
SPE `SPE-02`/`SPE-06`.

L'optimiseur les résout sans intervention : cocher *Optimiser la séquence* remet chaque
ligne dans l'ordre d'immersion. Le comparatif chiffre l'écart sur les indicateurs
ci-dessus. **Ces trois lignes sont à réétablir sur le classeur réel** — elles datent
d'avant l'optimiseur, et les colonnes *Bloqués/Retards/Retard max* ont été mesurées sur un
moteur qui contenait le défaut d'ordre corrigé depuis (voir plus bas).

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

### 2. Optimiseur de séquence — fait

Objectif respecté : zéro inversion d'abord, retards ensuite, staggering en contrainte dure
à 1 semaine. Activable et désactivable depuis l'interface, comme le staggering.

**Constat à connaître avant d'y retoucher** : une file sans inversion est une file triée par
date d'immersion — l'ordre est **unique aux ex æquo près**. Le second objectif ne s'exerce
donc que là où le premier laisse le choix : éléments sans date d'immersion, et dates
partagées. Sur un classeur où toutes les dates sont renseignées et distinctes, l'optimiseur
se réduit au tri et l'affinage ne trouve rien à déplacer — ce n'est pas un défaut
d'implémentation, c'est le degré de liberté disponible. Le vrai levier suivant sur les
retards est l'**affectation des éléments aux lignes**, aujourd'hui figée par le classeur.

### 3. Comparatif — fait

Bouton *Comparer* : séquence du classeur contre séquence optimisée, sur inversions,
bloqués, éléments en retard, retard max, retard cumulé et changements de cadence. La
séquence gagnante reste appliquée et affichée à l'écran.

**Lecture du tableau** : lever les inversions débloque des éléments, et un élément débloqué
qui arrive en retard bascule de la colonne *bloqués* vers la colonne *retards*. Le nombre de
retards peut donc augmenter alors que le plan s'améliore. C'est pour cela que les deux
colonnes figurent côte à côte, et que les critères sont comparés dans cet ordre.

### 4. Coupe des éléments immergés — à faire

Inchangé : l'utilisateur fournira un PDF de coupe avec le positionnement des éléments. À
remplir au fil des immersions, comme le plan d'installation l'est déjà pour le mouvement en
surface.

## Défaut corrigé au passage

Quand deux éléments d'une même ligne attendaient ensemble — l'outfitting peut se libérer
avant que le float-up n'ait eu lieu — le moteur prenait **le premier du tableau `elements`,
c'est-à-dire l'ordre des lignes du classeur**, et non le plus ancien de la file. Même
séquence, résultats différents selon la disposition des lignes dans `Inputs` : sur le jeu
d'essai, 53 éléments bloqués contre 6 pour un ordre de production pourtant identique.
Le choix se fait désormais sur `ordreSeq` (`premierDeLigne` dans `index.html`), ce qui rend
la simulation indépendante de la disposition du classeur — condition pour que la séquence
proposée par l'optimiseur, une fois recopiée dans `Inputs`, donne exactement le même plan.

## Évolutions notées, non planifiées

- **Affectation des éléments aux lignes** par le solveur (cf. ci-dessus).
- **Pentes progressives de cadence.** Un changement de rythme se fait
  graduellement dans la réalité, pas d'un jour à l'autre.
- **Évacuation anticipée d'un SPE**, qui peut laisser deux éléments non étanches
  simultanément dans les UB. La colonne F de `Config_SPE` est saisie par zone
  précisément pour permettre ce cas.

## Réserves connues

- Les 7 aires SPE sont réparties uniformément entre l'entrée est et les bassins,
  faute de leurs abscisses exactes. L'ordre et la séparation sont justes, les
  largeurs approchées.
- Le solveur ne modélise ni les deux portes du Basin C ni le déphasage entre halls quand il
  choisit la cadence : ses estimations de délai restent optimistes sur PL-3, PL-4 et PL-5.
  La simulation, elle, applique les deux.
- L'affinage de l'optimiseur tourne sous budget de temps (5 s par défaut, chaque candidat
  coûtant une simulation complète). Sur un très gros classeur il peut s'arrêter avant
  d'avoir épuisé le voisinage ; la meilleure séquence trouvée est alors retenue.
- `Config_Outfitting` ne pilote plus le calendrier ; l'onglet ne sert plus qu'aux
  noms de phases. Il est conservé pour ne pas casser les classeurs existants.
