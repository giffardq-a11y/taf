# Structure du moteur — état au démarrage

Ce document explique comment le moteur est construit, pourquoi il commence par cette
capacité précise plutôt qu'une autre, et ce qui est délibérément laissé de côté en
attendant que des questions encore ouvertes (`tempo/DONNEES.md` §4) soient tranchées.
Comme pour le reste du dépôt : rien n'est deviné pour combler un trou, un trou reste un
trou tant qu'il n'est pas comblé par une vraie donnée.

## Ce que le moteur sait faire aujourd'hui

**Calculer la charge de ressource agrégée, jour par jour, sur les 5 lignes en même
temps, et repérer où elle dépasse la capacité disponible.**

C'est le sous-ensemble directement disponible avec les données reçues à ce jour, et il
répond à deux des quatre objectifs posés au départ : détecter les goulots
d'étranglement, et vérifier que la cadence retenue est tenable avec les ressources
réelles. Les deux autres (générer un planning détaillé équipe par équipe, dimensionner
les ressources) en découlent directement une fois cette première brique posée — mais pas
avant, parce qu'un planning détaillé suppose de savoir **ordonnancer** les tâches
(dans quel ordre, avec quelle marge), et ça, on ne l'a pas encore construit (cf. plus
bas, "Ce qui n'est pas encore construit").

### Le principe

Le classeur N3 décrit, tâche par tâche, la charge horaire d'**un seul élément
générique** traversant les zones du site (colonne Élément = En/En-1/En+1, jamais liée à
une ligne précise — vérifié en lisant `lire_tempo.lire_taches_n3`). Le classeur N1 donne
le **déphasage** entre les 5 lignes : chaque ligne démarre son cycle à un jour tempo
absolu différent (`L1-T1`, `L2-T3`, `L3-T23`, `L4-T25`, `L5-T49`, lu dans
`lire_n1(...)['demarrage']`).

Le moteur recopie donc le même gabarit de tâches N3 sur les 5 lignes, en décalant
chacune de son déphasage, puis additionne la demande en ressource (effectif, heures de
grue) de toutes les lignes sur chaque jour calendaire absolu. Là où la somme dépasse la
capacité déclarée d'une ressource, c'est un goulot — daté, chiffré, et pointé vers les
tâches et lignes qui le causent, pas seulement signalé en bloc.

### Deux hypothèses posées ici, à confirmer avant de leur faire confiance sur un vrai cas

1. **Le jour tempo (« Ti ») est un jour calendaire, pas un poste.** Déduit du fait que le
   cycle complet dure 70 jours calendaires pour 140 postes (2 postes/jour), et que les
   feuilles N3 portent des Ti allant jusqu'à ~70 sur toute la traversée d'un élément.
   Cohérent avec les écarts de déphasage lus au N1 : L2-L1 = 2 jours, L4-L3 = 2 jours,
   L3-L2 = 20 jours, L5-L4 = 24 jours — un déphasage petit à l'intérieur d'une paire de
   lignes (même halle) et un grand déphasage entre paires, exactement la forme du
   déphasage entre halles déjà utilisé dans l'autre outil de ce dépôt (3 segments entre
   halles ≈ 21-24 jours tempo à raison d'environ 7 jours/segment) — une cohérence externe
   qui rassure, mais qui n'a pas été confirmée verbalement par Valery ou Joanna.
2. **Une ligne relance un nouvel élément tous les 7 jours tempo.** Déduit de la feuille
   `Casting Pattern` du classeur N1 (« Casting Pattern to fit **5 castings per week** »,
   une coulée par ligne et par semaine). Réglable
   (`ParametresCalage.periode_relance_jours`), pas codé en dur — mais la valeur par défaut
   suppose cette lecture juste.

Les deux hypothèses sont posées comme des **paramètres par défaut**, pas des constantes :
tout le module `modele.py` les expose, rien n'empêche de les corriger dès qu'une réponse
arrive.

## Ce qui n'est pas encore construit, et pourquoi

- **L'ordonnancement détaillé des tâches** (qui passe avant qui, avec quelle marge, sur
  quelle fenêtre horaire précise) — un problème d'ordonnancement sous contraintes de
  ressources (RCPSP dans la littérature de recherche opérationnelle), qui suppose de
  connaître les liens de précédence entre tâches. Le classeur N3 ne les porte pas
  explicitement (pas de colonne « prédécesseur ») ; les reconstruire à partir de l'ordre
  des lignes dans chaque feuille serait une supposition, pas une lecture. Reste à
  construire une fois soit ces liens obtenus (auprès de Joanna/Valery), soit une méthode
  de reconstruction validée sur un cas connu.
- **Le système de postes de l'équipe de coulée** (3×8h ou 2×12h — toujours « No shift
  system in place » d'après la présentation Casting Team) n'est pas figé dans le moteur :
  celui-ci raisonne en **heures continues**, jamais en « postes », précisément pour ne
  pas avoir à choisir à sa place. Le jour où le système de postes est arrêté, il
  s'ajoute comme un `Calendrier` (classe déjà prévue dans `modele.py`) sans toucher au
  reste.
- **La replanification à partir d'un avancement réel** (objectif final évoqué en
  réunion : réagir après chaque poste si on lui donne la progression). Suppose d'abord
  l'ordonnancement détaillé ci-dessus — sans lui, il n'y a rien de assez précis à
  comparer à un avancement réel.
- **La logistique amont** (camions, stockage, racks, livraisons). Aucune donnée reçue à
  ce jour ne le permet (le tableau des camions « Jules Tab » et les comptages de racks de
  Valery manquent toujours — `tempo/DONNEES.md` §1). Le modèle de ressource
  (`Ressource` dans `modele.py`) est générique et accueillera un camion ou une place de
  stockage exactement comme un ouvrier ou une grue le jour où ces données arrivent — mais
  rien n'est pré-rempli pour l'instant.
- **Les pannes matérielles et les retards** (objectif de réaffectation à chaud) — supposent
  eux aussi l'ordonnancement détaillé : replanifier, c'est reprendre un ordonnancement
  existant et le rejouer avec une contrainte en moins (une ressource indisponible) ou une
  tâche en retard. Rien à replanifier tant qu'il n'y a pas de planning détaillé de base.

## Organisation des fichiers

```
tempo/moteur/
  ARCHITECTURE.md   ce document
  modele.py         les classes de données (Ressource, Tache, ParametresCalage, Calendrier)
  charge.py         construit la charge agrégée par ressource et par jour calendaire absolu
  goulots.py         compare la charge à la capacité, produit la liste des dépassements
```

`python3 -m tempo.moteur.charge <n1.xlsx> <n3.xlsx>` fait tourner l'ensemble sur les
classeurs réels et imprime les goulots trouvés, avec les tâches et les lignes en cause —
un test de bout en bout sur données réelles, pas seulement des classes qui compilent.

## Premier résultat, et un écart à éclaircir avant de s'y fier

Sur la ressource `BC` (Blue Collar), zone S (Casting Pit) seule, le moteur trouve un pic
de **228** en simultané, un jour sur deux environ (les 5 lignes s'y retrouvent ensemble,
cf. plus bas). La présentation Casting Team donne, elle, un pic standard de **105 BC**
(117 en semaine S5). L'écart n'est pas négligeable — environ un facteur 2 — et n'a **pas**
été expliqué ni corrigé silencieusement. Deux pistes, aucune confirmée :

1. Le total du moteur additionne **toute** la main-d'œuvre `BC` de la zone S (coffrage,
   préparation au skidding, etc.), alors que « 105 BC » vient d'une présentation dédiée à
   la seule **équipe de coulée** — un périmètre plus étroit.
2. Le déphasage lu au N1 (`L1-T1, L2-T3` : 2 jours d'écart seulement dans une paire de
   lignes) fait effectivement se chevaucher les 5 lignes en zone S presque toutes les
   semaines — cohérent avec le fait que le `Casting Pattern` du classeur N1 fait couler
   **les 5 lignes le même jour**, à des heures différentes. Si c'est la bonne lecture,
   228 n'est pas un artefact de calcul mais une vraie charge cumulée à ce moment-là — la
   présentation Casting Team ne dit d'ailleurs pas clairement si son « pic standard » est
   mesuré ligne par ligne ou toutes lignes confondues.

Ce point est à vérifier avec Valery/Joanna avant de prendre le chiffre du moteur pour un
dimensionnement — il est montré tel quel, pas lissé pour coller au 105 déjà connu.
