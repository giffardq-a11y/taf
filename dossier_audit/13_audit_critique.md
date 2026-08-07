# 13. Audit critique

Auto-évaluation honnête du projet, écrite du point de vue de l'assistant IA qui a
construit l'essentiel du code, en dialogue continu avec un unique interlocuteur
métier. Cette section assume des jugements de valeur — c'est son objet — et ne
cherche pas à minimiser les faiblesses réelles du projet.

## 13.1 Points forts

- **Discipline de mesure.** Chaque règle métier ajoutée au modèle a été validée
  par une mesure chiffrée avant/après sur un classeur réel, jamais acceptée sur
  la seule base d'un raisonnement intuitif. Cette discipline a évité plusieurs
  erreurs qui auraient été difficiles à détecter autrement — le cas le plus
  clair étant la règle de sortie du bassin vers le parking (ADR-016) : sans
  mesure de sensibilité, une règle *fonctionnellement plausible* mais
  *quantitativement fausse* serait restée en production, contredisant
  l'observation directe du chantier.
- **Traçabilité du raisonnement.** Le code est commenté de façon dense, en
  expliquant systématiquement le *pourquoi* d'une règle et pas seulement son
  fonctionnement. Combiné à des messages de commit descriptifs et à `README.md`,
  cela a permis de reconstruire ce dossier d'audit sans avoir besoin de
  deviner l'intention derrière la plupart des décisions.
- **Séparation propre entre données d'entrée intangibles et sorties
  calculées.** La distinction stricte entre ce qui est une vraie donnée du
  planning P6 (ordre d'immersion, dates cibles, durées de ballast réelles) et
  ce qui est une sortie du solveur (toutes les autres dates) est appliquée avec
  constance — c'est ce qui rend le système d'impositions manuelles (ADR-013)
  cohérent, et c'est ce qui a permis de diagnostiquer correctement le bug de
  double comptage du hook-up (ADR-019) : la question à se poser était toujours
  « cette date est-elle une entrée ou une sortie ? ».
- **Réactivité aux signaux du terrain.** Plusieurs corrections importantes
  (géométrie de coulée dans les halles, règle de sortie du bassin, chevauchement
  visuel de bassins) sont directement issues d'observations concrètes du
  chantier rapportées par l'utilisateur, et ont été traitées en révisant le
  modèle plutôt qu'en défendant l'implémentation existante.
- **Confidentialité par construction.** L'absence totale de communication
  réseau à l'exécution (ADR-002) n'est pas un ajout tardif mais une contrainte
  posée dès le premier commit — elle structure toute l'architecture plutôt que
  d'être une couche de sécurité rajoutée après coup.
- **Boîte à outils d'audit P6 performante et généraliste.** `lire_xer.py` traite
  un export de 86 Mo, 67 000 activités et 107 000 liens en quelques secondes,
  sans dépendance externe, avec une architecture (lecture par table/colonnes
  demandées) qui resterait valable sur un export bien plus gros.

## 13.2 Points faibles

- **Aucun test automatisé versionné.** C'est la faiblesse la plus sérieuse du
  projet du point de vue d'un audit externe. Des tests de bout en bout et de
  non-régression ont bien été écrits et exécutés à de nombreuses reprises en
  cours de développement — mais dans un répertoire de travail temporaire, jamais
  intégrés au dépôt. Un tiers qui reprend ce projet aujourd'hui hérite d'un code
  fonctionnellement validé *au moment de sa dernière modification*, sans aucun
  filet pour la suite.
- **Absence de fichiers de dépendances.** Un détail en apparence mineur, mais
  qui illustre un relâchement de rigueur d'ingénierie logicielle standard : sur
  un projet qui utilise deux écosystèmes (Node.js et Python), ne pas déclarer
  les dépendances à la racine est une omission qui aurait dû être corrigée dès
  la première utilisation de `planning_runner.js` ou de `post_tension.py`, pas
  laissée pour plus tard.
- **Housekeeping Git incohérent.** `rapport.html` est exclu du suivi avec une
  justification écrite explicite ; `Post_tension.xlsx`, `donnees_p6.txt` et
  `__pycache__/` sont, eux, suivis, sans qu'aucune règle explicite ne le
  justifie — vraisemblablement un oubli au moment de leur premier commit,
  jamais corrigé depuis.
- **Fichier `index.html` devenu très volumineux et à double rôle.** Porter à la
  fois le solveur (censé être une source unique, réutilisée ailleurs) et
  l'interface de développement dans le même fichier de ~4000 lignes est un
  compromis qui a bien fonctionné jusqu'ici, mais qui rend chaque lecture du
  fichier plus coûteuse qu'elle ne devrait l'être — un tiers doit d'abord
  localiser les marqueurs de périmètre avant de savoir si une portion de code
  est partagée ou locale.
- **Le mécanisme d'extraction par marqueurs de commentaire est fragile par
  construction**, même si son usage réel ne l'a jamais mis en défaut à ce jour.
  Une expression régulière sur du texte, sans aucune vérification structurelle
  du JavaScript extrait (pas de linting, pas de vérification de syntaxe
  post-extraction au-delà de ce que `build_report.py` fait), est un point
  d'ingénierie que je referais différemment si je recommençais (voir §13.6).
- **Des interactions en cascade entre règles ont, à plusieurs reprises,
  nécessité une seconde correction après la première** (voir ADR-016/ADR-016bis
  dans `04_journal_decisions_ADR.md` ; voir aussi le cas limite non totalement
  résolu de ADR-015, section 9.7 de `09_questions_ouvertes.md`). Ce n'est pas
  en soi anormal dans un système à règles multiples et interdépendantes, mais
  cela révèle que le modèle n'a pas de représentation explicite de ses propres
  dépendances internes — chaque interaction est découverte par l'usage, pas
  anticipée par construction.
- **Un scénario testé pendant la validation d'un correctif récent (ADR-015) a
  révélé une dégradation mesurable dans une configuration synthétique
  spécifique**, non totalement expliquée avant la clôture du travail (voir
  `09_questions_ouvertes.md`, §9.7). Le choix a été de vérifier que le chemin
  réel de l'interface n'était pas affecté puis de documenter le cas limite
  plutôt que de creuser jusqu'au bout — un compromis défendable sous contrainte
  de temps, mais qui laisse une zone d'ombre non refermée.

## 13.3 Compromis assumés

- **Simulation gloutonne plutôt qu'optimisation globale prouvée** (ADR-004) —
  choix délibéré, documenté, dont la contrepartie (absence de garantie
  d'optimalité) est explicitement écrite dans `README.md` plutôt que cachée.
- **Extraction de code par marqueurs plutôt que module partagé** (ADR-003) —
  privilégie la simplicité de distribution de l'outil interactif au prix d'une
  solution non idiomatique. Assumé et documenté, pas un aveuglement.
- **Boîte à outils d'audit P6 tenue séparée du solveur** (ADR-020) — limite le
  risque de régression croisée au prix d'un lien manuel entre constat d'audit et
  correction de modèle. Choix défendable, mais qui repose entièrement sur la
  vigilance humaine pour être suivi d'effet.
- **Un seul jeu de données de validation** (le classeur de référence) pour
  toutes les mesures citées dans ce projet. Un compromis de temps et de moyens
  raisonnable au stade actuel, mais qui limite la confiance qu'on peut accorder
  aux chiffres cités en dehors de ce contexte précis.

## 13.4 Limites actuelles

Reprises et complétées de `README.md` (section « Limites connues ») :

- Le solveur ne modélise pas, au moment où il choisit une cadence, les portes du
  Basin C ni le déphasage entre halles — il les applique correctement dans la
  simulation aval, mais son estimation prospective de faisabilité reste
  optimiste sur PL-3, PL-4 et PL-5, ce qui peut provoquer des changements de
  cadence évitables.
- Les coordonnées de la zone de stockage SPE et du Ballast Jetty sont
  extrapolées, pas mesurées.
- `Config_Cycles` ne porte que 3 emplacements de changement de cadence par
  ligne ; au-delà, l'export vers cet onglet est tronqué (avec avertissement).
- Aucune source de durée réelle par élément n'existe encore pour le float-up
  (contrairement au ballast, corrigé en ADR-019) — un traitement asymétrique
  documenté mais pas résolu.
- Le planning de post-tension repose sur des durées d'opération non confirmées
  et ne modélise aucune contrainte de nombre d'équipes.

## 13.5 Améliorations possibles, par ordre d'impact estimé

1. **Committer une suite de tests minimale et une intégration continue** — le
   changement isolé qui réduirait le plus le risque pris à chaque nouvelle
   modification, pour un coût de mise en œuvre faible au regard du bénéfice.
2. **Ajouter les fichiers de dépendances** (`package.json`,
   `requirements.txt`) — coût minimal, corrige un vrai obstacle à la reprise du
   projet par un tiers.
3. **Faire modéliser au solveur, dès le choix de cadence, les contraintes qu'il
   applique déjà en aval** (portes du Basin C, déphasage) — réduirait les
   changements de cadence évitables sur PL-3/PL-4/PL-5, un gain mesurable
   probable au vu des mesures déjà faites sur des limites voisines.
4. **Séparer `index.html`** en au moins deux fichiers distincts (solveur d'un
   côté, interface de développement de l'autre), avec un chargement explicite
   plutôt qu'une extraction par marqueurs — gain de lisibilité et de robustesse
   pour un coût de refonte non négligeable, à ne faire qu'après avoir sécurisé
   le filet de tests (point 1), pour ne pas refondre sans garde-fou.
5. **Clore le cas limite documenté en `09_questions_ouvertes.md` §9.7** —
   investigation ciblée pour déterminer s'il est atteignable en usage réel.

## 13.6 Ce qui serait fait différemment en recommençant aujourd'hui

- **Committer un test de non-régression dès le premier commit**, même
  minimal (charger le classeur de référence, vérifier zéro erreur JavaScript
  et un jeu d'indicateurs de référence), plutôt que d'attendre — ce test aurait
  dû exister avant la dixième règle métier ajoutée, pas être considéré comme un
  chantier à part, repoussé indéfiniment.
- **Déclarer les dépendances dès leur première utilisation** (`npm install
  xlsx --save` avec un `package.json` commité dès `planning_runner.js`;
  `requirements.txt` dès le premier script `openpyxl`), au lieu de laisser
  cette dette s'accumuler silencieusement pendant tout le projet.
- **Séparer plus tôt le solveur de l'interface de développement** dans deux
  fichiers distincts, avant que `index.html` n'atteigne 4000 lignes — le coût de
  cette séparation croît avec la taille du fichier, et il aurait été
  nettement plus faible réalisé tôt.
- **Faire modéliser au solveur de cadence, dès sa conception initiale, les
  contraintes aval qu'il finit par simuler correctement mais sans les
  anticiper** (portes, déphasage) — plutôt que de découvrir a posteriori que
  cette asymétrie coûte des changements de cadence évitables.
- **Tenir, dès le début, un tableau de correspondance explicite entre chaque
  règle du modèle et son test de validation**, plutôt que de mesurer chaque
  règle une fois puis de laisser cette mesure devenir un fait historique
  documenté en prose (`README.md`, `SUITE.md`) sans qu'aucune exécution
  automatisée ne la revérifie jamais.
- **Adopter, dès le début, la convention de housekeeping Git appliquée à
  `rapport.html`** (fichier généré → jamais versionné) pour tous les artefacts
  de sortie des scripts, plutôt que de la découvrir a posteriori incohérente sur
  trois autres fichiers.

Rien de ce qui précède ne remet en cause le choix fondamental d'un outil web
autonome sans serveur (ADR-001/ADR-002) ni celui d'une simulation gloutonne
plutôt qu'un solveur de contraintes global (ADR-004) : ces deux décisions
restent, avec le recul, adaptées au problème posé. Les regrets exprimés ici
portent sur la **rigueur d'ingénierie logicielle** (tests, dépendances,
organisation des fichiers), pas sur les choix de conception métier eux-mêmes.
