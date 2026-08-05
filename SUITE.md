# État des lieux et prochaines étapes

Note de reprise. Les règles métier et leur justification sont dans `README.md` ;
ce document ne couvre que ce qui reste à faire et les décisions en attente.

## Où en est le modèle

Toutes les règles arrêtées sont implémentées et vérifiées sur le classeur réel :
flux tendu au 7ᵉ segment du suivant, cliquet de cadence, ordre d'immersion imposé,
étanchéité SPE datée par les activités de clamping, ordre de sortie des bassins,
stockage croisé, parking 5 places + 1 réserve.

Le solveur de cadence fonctionne. Ce qui manque, c'est l'optimiseur de **séquence**.

## Le blocage actuel n'est pas dans l'outil

Aucune des trois séquences de production du classeur n'est réalisable. Chacune
contient des inversions — un élément produit avant un autre qu'il doit immerger
après — et les places en aval étant uniques, la ligne se bloque.

| Variante | Inversions | Bloqués | Retards | Retard max |
|---|---|---|---|---|
| 1 (originale) | 4 | 38 | 47 | 140 j |
| 2 | 2 | 38 | 47 | 140 j |
| 3 | 6 | 51 | 34 | 70 j |

Inversions de la variante 1, signalées au chargement :
PL-3 `STE-12`/`STE-47`, PL-4 `STE-11`/`STE-48`, PL-5 `STE-29`/`STE-34`,
SPE `SPE-02`/`SPE-06`.

Corriger ces quatre permutations à la main suffirait à débloquer les 38 éléments,
sans attendre l'optimiseur.

## À construire

### 1. Staggering entre halls

Règle confirmée par l'utilisateur :

- **Déphasage A↔B de 3 segments** — PL-3 et PL-4 au segment 4 quand PL-1 et PL-2
  sont au segment 1. Contrainte **dure** dès que la cadence atteint 1 semaine,
  simple préférence avant.
- **PL-5 à 7 segments d'écart** : préférence, jamais bloquant, sa cadence variant
  librement.
- Aucun déphasage à l'intérieur d'un hall.

Point non tranché : le déphasage ne se conserve que si les deux halls tournent à la
même cadence. Si un jour A passe à 1 semaine et B reste à 1,5, il faudra choisir
entre brider A et lever le staggering. Le cas ne s'est présenté dans aucun essai —
les deux halls atteignent 1 semaine ensemble.

### 2. Optimiseur de séquence

Objectif, dans cet ordre : zéro inversion, puis minimisation des retards, avec le
staggering en contrainte dure à 1 semaine. Activable et désactivable depuis
l'interface.

L'onglet `Inputs` accepte déjà plusieurs séquences empilées — chaque retour du
compteur à 1 ouvre une variante. `sequenceChoisie` sélectionne celle qui est
calculée ; l'interface doit exposer ce choix.

### 3. Comparatif

Opposer la séquence de l'utilisateur à celle proposée, sur les mêmes indicateurs
que le tableau ci-dessus.

### 4. Coupe des éléments immergés

L'utilisateur fournira un PDF de coupe avec le positionnement des éléments. À
remplir au fil des immersions, comme le plan d'installation l'est déjà pour le
mouvement en surface.

## Évolutions notées, non planifiées

- **Pentes progressives de cadence.** Un changement de rythme se fait
  graduellement dans la réalité, pas d'un jour à l'autre.
- **Évacuation anticipée d'un SPE**, qui peut laisser deux éléments non étanches
  simultanément dans les UB. La colonne F de `Config_SPE` est saisie par zone
  précisément pour permettre ce cas.

## Réserves connues

- Les 7 aires SPE sont réparties uniformément entre l'entrée est et les bassins,
  faute de leurs abscisses exactes. L'ordre et la séparation sont justes, les
  largeurs approchées.
- Le solveur ne modélise pas les deux portes du Basin C quand il choisit la cadence
  de PL-5 : ses estimations restent optimistes sur cette ligne. La simulation, elle,
  les applique.
- `Config_Outfitting` ne pilote plus le calendrier ; l'onglet ne sert plus qu'aux
  noms de phases. Il est conservé pour ne pas casser les classeurs existants.
