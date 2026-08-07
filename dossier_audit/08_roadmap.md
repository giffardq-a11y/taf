# 8. Roadmap

Il n'existe pas de roadmap formelle antérieure au code : ce document reconstruit
l'état « terminé / à faire » à partir de `README.md` (section « À venir » et
« Limites connues »), de `SUITE.md` et de l'historique Git, et y ajoute les
priorités déduites de l'analyse de risques (`05_analyse_risques.md`).

## 8.1 Terminé

### Calcul de cadence et simulation

- [x] Solveur de cadence par ligne (choix parmi 7 rythmes discrets, pente
  d'inertie, cadence jamais relâchée par défaut).
- [x] Simulation jour par jour du cheminement complet d'un élément (coulée,
  outfitting, float-up, bassin, parking, ballast, immersion).
- [x] Ligne SPE pilotée par les dates réelles de passage de zone du planning P6.
- [x] Deux stratégies d'arrêt d'usine (au plus tôt / flux tendu).
- [x] Arrêts annuels de l'usine (vacances de fin d'année, semaine sainte).
- [x] État *as-built* pris en compte à une date de référence, saisi dans le
  classeur ou directement à l'écran.
- [x] Déphasage (staggering) entre halles, dur ou souple selon la cadence.
- [x] Étanchéité SPE en cascade à trois niveaux, négociable par dichotomie.
- [x] Zone de stockage tampon dédiée à la ligne SPE.
- [x] Règle « un jour de coulage par ligne », désormais désactivée
  automatiquement aux cadences intermédiaires.
- [x] Règle de sortie du bassin vers le parking corrigée (sortie dès qu'une
  place est libre, sauf dispense courte et non bloquante).
- [x] Blocage du float-up vers un bassin occupé.
- [x] Correction du double comptage de la durée de hook-up contre la date
  réelle de ballast ; suppression des paramètres de durée de hook-up et de
  ballast au profit des données réelles du planning P6.
- [x] Accélération en cours de cycle (revue quotidienne, sans attendre le
  prochain départ béton) et date de décision d'accélérer, paramétrables.

### Optimisation

- [x] Optimiseur de séquence (zéro inversion puis minimisation des retards,
  ordre lexicographique de critères).
- [x] Réaffectation optimisée des éléments entre les 5 lignes standards.
- [x] Comparaison automatique de plusieurs séquences candidates, mode
  automatique.
- [x] Bouton de comparaison séquence du classeur / séquence optimisée, avec
  visualisation du mouvement des jetons.

### Interface et visualisation

- [x] Plan animé du site, calé sur le plan d'installation générale réel, avec
  curseur temporel et lecture automatique.
- [x] Coupe longitudinale du tunnel (positions provisoires, basées sur l'ordre
  de pose, pas encore sur les abscisses réelles).
- [x] Gantt de production avec numérotation des segments et compteurs de
  coulées hebdomadaires/mensuels.
- [x] Planning d'occupation du site imprimable.
- [x] Fiche détaillée par élément, icônes de statut.
- [x] Édition à l'écran de l'état *as-built* et des règles du modèle
  (`REGLES`), avec retour aux valeurs par défaut.
- [x] Dates pilotes (coulée, immersion) déplaçables par glisser-déposer,
  relançant automatiquement le calcul complet.
- [x] Rapport de conséquences d'une date imposée, contre une référence
  capturée avant toute imposition.
- [x] Relevé exhaustif et commenté de toutes les contraintes actives du
  modèle.
- [x] Correction géométrique : coulée démarrant 4 segments à l'intérieur des
  halles (élimination de tous les chevauchements visuels concrete/outfitting).
- [x] Affichage de la ligne SPE dans les zones CPA/CP1-3 (pas seulement Upper
  Basin), basé sur les dates de passage de zone P6.

### Exports et plannings dérivés

- [x] Génération d'un classeur modèle vide.
- [x] Export CSV/JSON du rapport de cadence.
- [x] Export du planning d'occupation au format *Target schedule*, avec
  intégration optionnelle des travaux marins et des finitions.
- [x] Génération du planning de post-tension (Gantt classique, dates
  début/fin par opération, numéros d'éléments en clair, ligne SPE exclue —
  confirmé par l'utilisateur).
- [x] Génération d'un classeur d'entrée réduit.

### Audit du planning directeur (P6)

- [x] Lecteur XER générique et économe en mémoire (validé sur un export réel
  de 86 Mo, 67 000 activités, 107 000 liens — traité en ~4 secondes).
- [x] Audit de qualité selon une grille inspirée de DCMA-14, étendue (détection
  d'anomalies de calendrier à capacité identique mais durée journalière
  différente).
- [x] Extraction des règles et motifs répétés du planning (aide au repérage de
  candidats à l'accélération).

## 8.2 À faire

### Priorité haute (dette technique et fiabilité — voir `05_analyse_risques.md`)

- [ ] Ajouter `package.json` et `requirements.txt` à la racine du dépôt.
- [ ] Committer une suite de tests minimale versionnée (santé de page,
  non-régression de KPI sur le classeur de référence, vérification de
  l'extraction du bloc `SOLVEUR-CORE`).
- [ ] Mettre en place une intégration continue exécutant cette suite à chaque
  modification.
- [ ] Clarifier et harmoniser le statut Git des fichiers générés
  (`__pycache__/`, `Post_tension.xlsx`, `donnees_p6.txt`).
- [ ] Verrouiller par un test la synchronisation des valeurs par défaut entre
  `report_template.html` et `planning_runner.js` (ADR-018 dans
  `04_journal_decisions_ADR.md`).

### Priorité métier (attend un arbitrage ou une donnée externe — voir `09_questions_ouvertes.md`)

- [ ] Trancher la question des calendriers des activités marines (8 h vs
  10 h/jour) — explicitement en attente d'une discussion entre l'utilisateur et
  le planificateur responsable de ce périmètre.
- [ ] Obtenir les durées réelles des opérations de post-tension (enfilage, mise
  en tension, injection) auprès du sous-traitant Dywidag, pour remplacer les
  valeurs par défaut actuelles.
- [ ] Confirmer l'interprétation de la règle de délai de post-tension (« deux
  jours après le **démarrage** de la coulée de l'élément suivant »).
- [ ] Obtenir le nombre d'équipes de post-tension disponibles, pour contraindre
  le planning généré (actuellement supposé en parallélisme illimité).
- [ ] Recalibrer les coordonnées extrapolées de la zone de stockage SPE et du
  quai de ballastage sur un plan officiel, quand il sera disponible.
- [ ] Obtenir le plan de coupe réel du tunnel, pour remplacer l'ordre de pose
  (actuellement utilisé comme position provisoire) par les abscisses réelles.

### Améliorations fonctionnelles identifiées, non urgentes

- [ ] Modéliser des pentes de changement de cadence progressives (un
  changement de rythme se fait graduellement sur le terrain, pas d'un jour à
  l'autre — limite notée dans `README.md`, section « À venir »).
- [ ] Étendre `Config_Cycles` au-delà de 3 emplacements de changement de
  cadence par ligne, ou documenter plus visiblement le repli actuel (liste
  complète disponible ailleurs).
- [ ] Envisager de faire modéliser au solveur de cadence, dès son estimation
  prospective de faisabilité (pas seulement dans la simulation aval), les
  portes du Basin C et le déphasage entre halles — actuellement source
  d'oscillations de cadence supplémentaires évitables sur PL-5 (limite notée
  dans `README.md`).
- [ ] Icônes par élément directement sur le plan de production (déjà présentes
  dans le tableau *as-built* et sur la coupe, pas encore sur le plan lui-même).

## 8.3 Prochaines étapes recommandées, par ordre

1. Corriger la dette technique de priorité haute (section 8.2), qui ne dépend
   d'aucun arbitrage externe et sécurise tout développement futur.
2. Relancer la discussion sur les calendriers marins avec le planificateur
   responsable, seul point métier réellement bloquant identifié.
3. Obtenir les données manquantes du sous-traitant Dywidag (durées, règle
   d'interprétation, nombre d'équipes) pour finaliser le planning de
   post-tension.
4. Traiter les améliorations fonctionnelles non urgentes selon la disponibilité
   des données externes qu'elles requièrent (plan de coupe réel, plan officiel
   pour la zone de stockage SPE et le Ballast Jetty).
