# 2. Cahier des charges fonctionnel

Ce document reconstruit, à partir du code et de `README.md`, ce qui tient lieu de
cahier des charges du projet — il n'a pas existé en tant que document séparé avant le
code : les exigences ont été formulées et affinées au fil de l'eau, chaque règle étant
implémentée puis mesurée sur un classeur réel avant validation.

## 2.1 Fonctionnalités

### Cœur : calcul de cadence et simulation

- Calculer, pour chaque ligne de production PL-1 à PL-5, le **rythme** (en semaines
  par segment béton) à appliquer à chaque nouvel élément lancé, parmi un ensemble
  discret de rythmes autorisés (1,0 / 1,5 / 2,0 / 2,5 / 3,0 / 3,5 / 4,0
  semaines/segment).
- Respecter simultanément, pour le choix d'un rythme : la pente d'accélération
  maximale tenable (1 semaine de variation de cadence par tranche de 4 mois), les
  dates d'immersion de **tous** les éléments restants de la ligne (pas seulement du
  suivant), et la synchronisation de cadence avec la ligne jumelle de la même halle.
- Ne jamais relâcher une cadence une fois atteinte (option de dérogation
  disponible, désactivée par défaut, avec chiffrage de son coût).
- Deux stratégies d'arrêt d'usine sélectionnables : « au plus tôt » (chaque ligne
  tourne à la cadence la plus rapide tenable et s'arrête dès sa file épuisée) ou
  « à flux tendu » (cadence la plus lente qui tienne les dates, l'usine tourne
  jusqu'au dernier élément).
- Rejouer, **jour par jour**, le cheminement complet de chaque élément à travers
  toutes les ressources partagées du site : zone de coulée béton (par segment),
  zone d'équipement (*outfitting*), mise à flot (*float-up*, une seule paire de
  portes actives à la fois par défaut), bassin (3 bassins × 2 places,
  paramétrable), sortie vers parking (5 places + 1 place de réserve), quai de
  ballastage (*Ballast Jetty*, un seul élément ballasté à la fois), immersion.
- Traiter la ligne spéciale SPE selon un cheminement dédié piloté par les dates de
  passage de zone lues dans le planning directeur (7 zones : CPA, CP1, CP2, CP3,
  UB1, UB2, UB3), avec gestion du jalon d'étanchéité provisoire/critique et d'une
  zone de stockage tampon dédiée pour absorber les conflits d'ordre d'immersion
  avec les éléments standards du Basin C.
- Appliquer un déphasage de démarrage (*staggering*) entre les halles de coulée,
  contraignant à cadence rapide, simple préférence sinon.
- Appliquer les arrêts annuels de l'usine (vacances de fin d'année, semaine
  sainte), qui allongent la durée de coulée d'un élément dont la coulée les
  chevauche, sans décaler le reste de la chaîne aval.
- Prendre en compte un état d'avancement réel (« as-built ») du chantier à une
  date de référence donnée, saisi soit dans le classeur d'entrée, soit directement
  à l'écran.

### Optimisation

- Optimiser l'**ordre de production** sur chaque ligne pour supprimer les
  inversions entre l'ordre de production et l'ordre d'immersion imposé (critère
  premier), puis minimiser le nombre d'éléments en retard, le retard cumulé, le
  retard maximal, éventuellement la date de fin de production, et le nombre de
  changements de cadence (critères suivants, dans cet ordre lexicographique).
- Optimiser également la **répartition des éléments entre les 5 lignes
  standards** (interchangeables entre elles), en réaffectant un à un les éléments
  en retard vers les lignes les moins chargées.
- Comparer automatiquement plusieurs séquences de production candidates (issues
  du classeur d'entrée) et retenir la meilleure, ou laisser l'utilisateur choisir
  une séquence précise.
- Fournir un mode de calcul « automatique » qui explore toutes les séquences
  disponibles et retient la meilleure selon les mêmes critères.

### Interface et visualisation

- Interface web en une page, entièrement en français, sans étape serveur.
- Chargement d'un classeur Excel (`.xlsx` ou `.xlsm`, macros préservées) et d'une
  image de fond de plan (JPG/PNG).
- Visualisation animée du mouvement des éléments sur le plan réel du site
  (positions calées sur le plan d'installation générale), avec curseur temporel
  et lecture automatique.
- Coupe longitudinale du tunnel montrant la pose progressive des éléments.
- Gantt de production par ligne, avec numérotation des segments de coulée et
  compteurs hebdomadaires/mensuels de coulées.
- Planning d'occupation du site, imprimable, au format du *Target schedule* utilisé
  sur le chantier.
- Fiche détaillée par élément (dates de chaque phase), accessible par clic.
- Édition à l'écran de l'état as-built (sans modifier le classeur source).
- Édition à l'écran de toutes les règles du modèle (`REGLES`), avec un bouton de
  retour aux valeurs de référence.
- **Dates pilotes déplaçables** : glisser une barre de coulée ou d'immersion dans
  le Gantt impose une nouvelle date et relance automatiquement tout le calcul ; un
  rapport de « conséquences » compare alors le résultat au calcul de référence
  (sans date imposée).
- Comparatif visuel entre séquence du classeur et séquence optimisée (jetons qui
  glissent d'une position à l'autre).
- Relevé exhaustif et commenté de toutes les contraintes actives du modèle,
  classées par famille, avec leur origine (donnée du planning P6, règle réglable,
  règle figée) et leur statut.
- Journal de calcul commenté (avertissements, décisions prises, coûts mesurés).

### Exports

- Génération d'un classeur modèle vide (structure attendue en entrée).
- Export CSV/JSON du rapport de cadence.
- Export d'un planning d'occupation au format *Target schedule* (`planning_cible.py`),
  pouvant intégrer les travaux marins et les finitions extraits du planning P6
  (`extraire_p6.py`).
- Génération d'un planning de post-tension au format Dywidag, dérivé directement
  des dates de coulée du meilleur scénario calculé (`post_tension.py`), présenté
  en Gantt classique (dates début/fin par opération, numéros d'éléments en clair).
- Génération d'un classeur d'entrée réduit à ce que le solveur lit réellement
  (`reduire_classeur.py`), pour en simplifier la relecture.

### Outils d'audit du planning directeur (indépendants du solveur)

- Lecture générique et économe en mémoire d'un export XER de Primavera P6
  (`lire_xer.py`), quelle que soit sa taille.
- Audit de qualité du planning selon une grille inspirée de la méthode DCMA-14
  (`auditer_xer.py`) : extrémités ouvertes, types de liens, décalages,
  contraintes dures, marges, durées, cohérence des dates, ressources,
  calendriers, arborescence WBS, chemin déterminant.
- Extraction des règles répétées du planning (rôles d'activités, enchaînements,
  durées et calendriers typiques) par repérage de motifs dans les noms
  d'activités (`regles_p6.py`), utile pour proposer des accélérations sans casser
  la logique du planning.

## 2.2 Cas d'usage

1. **Calcul de cadence hebdomadaire** — le planificateur charge le dernier état
   d'avancement, lance le calcul, communique aux équipes le rythme à tenir sur
   chaque ligne pour la semaine à venir.
2. **Test d'une hypothèse de production** — le planificateur impose une nouvelle
   date de coulée ou d'immersion sur un élément (glisser-déposer), et lit
   immédiatement le rapport de conséquences pour savoir si le reste du planning
   tient toujours.
3. **Comparaison de séquences** — avant de figer l'ordre de production d'une
   nouvelle campagne, comparer plusieurs séquences candidates et visualiser ce que
   chacune déplace par rapport à l'ordre du classeur.
4. **Diagnostic d'un retard constaté sur le terrain** — désactiver une à une les
   règles du modèle (staggering, jour de coulage, pente d'inertie…) pour isoler
   la cause d'un retard ou d'un blocage, et chiffrer le coût de chaque règle.
5. **Préparation de la réunion de planning** — exporter le planning d'occupation
   imprimable et le comparatif de séquences pour présentation.
6. **Dérivation d'un planning de sous-traitant** — générer le planning de
   post-tension Dywidag directement à partir du meilleur scénario de coulée,
   sans ressaisie manuelle.
7. **Audit ponctuel du planning directeur P6** — après une nouvelle publication
   du planning par le bureau d'études, faire tourner l'audit DCMA-14 et
   l'extraction de règles pour repérer les anomalies et les gisements
   d'accélération, avant d'en discuter avec le planificateur responsable.

## 2.3 Contraintes

- **L'ordre d'immersion est une donnée d'entrée du planning P6, jamais modifiée
  par le programme.** C'est la contrainte la plus structurante du projet : tout
  calcul qui optimise, réordonne ou impose une date le fait *sous* cette
  contrainte, jamais contre elle. Une imposition d'une nouvelle date d'immersion
  reste possible, mais c'est une décision explicite de l'utilisateur, jamais une
  initiative du solveur.
- **Aucune donnée ne doit être envoyée à un serveur.** L'outil principal
  (`index.html`) et la page de restitution (`rapport.html`) tournent
  entièrement dans le navigateur ; le calcul et la lecture du classeur s'y font
  sur place.
- **Le cœur du solveur doit rester une implémentation unique**, partagée entre
  l'outil de développement (`index.html`), la page de restitution publiée
  (assemblée par `build_report.py`) et l'exécution en ligne de commande
  (`planning_runner.js`). Techniquement imposé par extraction de code source
  entre deux marqueurs (voir `03_architecture.md`).
- **Compatibilité avec le classeur existant du chantier** : structure des onglets
  `Inputs`, `Immersion`, `Config_Cycles`, `Config_SPE` héritée du classeur Excel
  historique piloté par macro VBA, reprise telle quelle en entrée (voir
  `06_documentation_technique.md` pour le détail des colonnes).
- **Langue** : interface, documentation et commentaires de code en français ;
  messages de commit Git en anglais (convention adoptée en cours de projet, sans
  incidence fonctionnelle).
- **Aucune dépendance à un service externe au moment de l'usage** : la
  bibliothèque de lecture Excel (SheetJS) est intégrée (« inlinée ») dans la page
  de restitution au moment de sa génération, pas chargée depuis un CDN à
  l'exécution.

## 2.4 Exigences

### Fonctionnelles

- Le calcul doit être **déterministe** : mêmes données d'entrée et mêmes
  paramètres ⇒ même résultat, à chaque exécution.
- La lecture de l'état as-built doit être **tolérante** (fautes de frappe,
  variantes de séparateurs, synonymes français acceptés) — voir le format détaillé
  dans `06_documentation_technique.md`.
- Le programme doit **journaliser** toute décision non triviale prise
  automatiquement (avertissement, correction, écart mesuré), pour qu'un résultat
  inattendu reste explicable sans relire le code.
- Une date imposée manuellement doit rester **non destructive** : elle est
  réappliquée à chaque recalcul par-dessus les données du classeur, jamais
  écrite dedans, et peut être annulée sans perte d'information.
- Le rapport de « conséquences » d'une imposition doit détecter si la comparaison
  reste valide (mêmes paramètres, même effet d'optimiseur) et avertir sinon.

### Non fonctionnelles

- **Performance** : l'audit d'un export XER de 67 000 activités et 107 000 liens
  doit s'exécuter en quelques secondes, indépendamment de la taille du fichier
  (mesuré : ~4 secondes sur un export de 86 Mo).
- **Portabilité** : l'outil principal doit s'ouvrir par double-clic sur
  `index.html`, sans installation, sur n'importe quel navigateur moderne.
- **Autonomie de la page de restitution** : `rapport.html`, une fois généré, ne
  dépend d'aucune ressource réseau pour fonctionner.
- **Lisibilité du code pour un tiers** : commentaires en français expliquant le
  *pourquoi* de chaque règle, pas seulement le *quoi* — convention tenue tout au
  long du projet et visible dans `index.html`.

## 2.5 Hypothèses

Les hypothèses de conception détaillées (structurelles, métier, données) sont
regroupées dans `10_hypotheses.md`, pour éviter la duplication. Les plus
structurantes, résumées ici :

- Le nombre d'éléments (89 sur le classeur de référence : 79 éléments standards +
  10 SPE), leur répartition sur 5 lignes + 1 ligne spéciale, et la topologie du
  site (3 bassins de 2 places, 5 places de parking + 1 réserve) sont ceux du
  chantier Fehmarnbelt à Rødbyhavn ; le modèle n'a pas été généralisé à un autre
  site.
- Le planning directeur (Primavera P6) est la source de vérité pour les dates
  d'immersion, l'ordre d'immersion, les dates de passage de zone de la ligne SPE
  et les durées de ballast par élément ; toute donnée absente du P6 retombe sur
  une valeur de repli interne, clairement signalée comme telle.
