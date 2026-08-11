# 11. Glossaire

Termes du domaine métier (chantier Fehmarnbelt), termes du modèle et acronymes
techniques, classés par ordre alphabétique. Les noms de variables ou de fonctions
du code sont donnés entre apostrophes inversées (`comme ceci`).

## Domaine métier — chantier et production

- **As-built** — état d'avancement réel constaté sur le chantier à une date
  donnée, par opposition au planning théorique. Saisi soit dans le classeur
  (colonnes dédiées de l'onglet `Inputs`), soit directement à l'écran.
- **Ballast / Ballast Jetty** — lestage d'un élément avant son immersion
  (ajout de poids pour le faire couler à la position voulue) ; *Ballast Jetty*
  désigne le quai où cette opération a lieu, dernière étape avant immersion.
- **Bassin (Lower Basin)** — plan d'eau où un élément flotte après sa mise à
  flot (*float-up*), en attente de gagner une place de parking ou le quai de
  ballastage. Le site compte 3 bassins (A, B, C) de 2 places chacun.
- **Cadence / Rythme** — durée, en semaines, nécessaire pour couler un segment
  de béton sur une ligne donnée. Plus la valeur est basse, plus la production
  est rapide. Valeurs autorisées : 1,0 / 1,5 / 2,0 / 2,5 / 3,0 / 3,5 / 4,0.
- **Clamping** — dans le planning P6, activité qui marque la fermeture
  définitive (l'étanchéité finale) d'un élément spécial (SPE).
- **CPA, CP1, CP2, CP3** — zones successives de coulée béton de la ligne SPE
  (Concrete Position A, 1, 2, 3), avant les zones d'équipement UB1-UB3.
- **Élément** — caisson préfabriqué de tunnel immergé, unité de base de la
  production. Deux familles : les éléments standards (identifiants `STE-NN` ou
  `TE-NN`) produits sur les lignes PL-1 à PL-5, et les éléments spéciaux
  (identifiants `SPE-NN`) produits sur la ligne SPE.
- **Étanchéité (jalon d')** — moment à partir duquel un élément spécial (SPE)
  est considéré étanche et peut donc être évacué du Basin C sans risque
  d'inondation prématurée. Modélisé en cascade à trois niveaux (voir ADR-010
  dans `04_journal_decisions_ADR.md`).
- **Float-up** — mise à flot d'un élément : transfert de la zone d'outfitting
  (à sec) vers un bassin (à flot).
- **Halle (Hall A / Hall B)** — bâtiment de coulée regroupant deux lignes de
  production jumelles (Hall A = PL-1/PL-2, Hall B = PL-3/PL-4). PL-5 est seule,
  hors halle jumelée.
- **Hook-up** — opération de raccordement effectuée juste avant le ballastage,
  dans le bassin ; modélisée comme les 24 dernières heures avant le départ au
  Ballast Jetty (voir ADR-019).
- **Immersion** — mise en place finale d'un élément à sa position définitive
  dans le tunnel, sous l'eau. Se fait dans un **ordre imposé**, donnée d'entrée
  du planning P6 jamais modifiée par le solveur (ADR-005).
- **Outfitting** — phase d'équipement d'un élément après sa coulée (finitions,
  installations), dans une zone dédiée à sec.
- **Parking** — zone d'attente à flot, en aval du bassin, où un élément
  patiente jusqu'à son tour de ballastage. 5 places sans limite de durée + 1
  place de réserve (ouverte seulement si un départ est proche).
- **Pente d'inertie** — variation de cadence maximale tenable par une ligne,
  par tranche de temps (par défaut : 1 semaine de variation par tranche de
  4 mois).
- **PL-1 à PL-5** — les 5 lignes de production standards.
- **Post-tension** — opération de mise en tension des câbles de précontrainte
  d'un élément, réalisée par un sous-traitant spécialisé (Dywidag dans ce
  projet), après sa coulée.
- **Segment** — portion de coulée béton d'un élément ; un élément standard se
  coule en 9 segments successifs.
- **SPE** — ligne et éléments « spéciaux » (non standards, ex. jonctions), au
  cheminement distinct des lignes PL, piloté par 7 zones nommées (CPA, CP1-CP3,
  UB1-UB3) plutôt que par des segments de coulée.
- **Staggering (déphasage)** — décalage volontaire du démarrage entre les
  halles de production, pour éviter que plusieurs bassins ne se remplissent
  le même jour.
- **Takt** — durée d'un cycle complet de production à une cadence donnée
  (`rythme × 7 × 9` jours pour un élément standard).
- **UB1, UB2, UB3** — zones successives d'équipement (*Upper Basin*) de la
  ligne SPE, après les zones de coulée CPA-CP3.

## Termes techniques du code et du modèle

- **`REGLES`** — objet JavaScript unique regroupant l'ensemble des règles et
  seuils du modèle (segments, pente d'inertie, déphasage, places de bassin et
  de parking, jours de coulage…), exposé et modifiable depuis l'interface.
- **`PARAMS`** — paramètres d'exécution d'un calcul donné, saisis à l'écran ou
  transmis par le code appelant (`lireParamsUI()` en absence d'interface).
- **`lastRhythmState`** — état courant de cadence de chaque ligne au cours de
  la simulation (rythme actif, date du dernier changement).
- **Imposition** — date de coulée ou d'immersion forcée manuellement par
  l'utilisateur (glisser-déposer), stockée à part (`IMPOSITIONS`) et réappliquée
  à chaque recalcul sans jamais modifier le classeur source.
- **Retouche** — ajustement visuel d'une barre du Gantt qui n'est *pas* une
  date pilote (donc sans effet sur le calcul), par opposition à une
  imposition.
- **SOLVEUR-CORE** — bloc de code délimité par les marqueurs
  `/* ==== SOLVEUR-CORE-DEBUT ==== */` et `/* ==== SOLVEUR-CORE-FIN ==== */`
  dans `index.html`, unique implémentation du solveur, extraite telle quelle
  par les autres composants du projet (voir ADR-003).
- **Rang d'immersion** — position d'un élément dans l'ordre d'immersion imposé
  par le planning P6.

## Acronymes

- **DCMA-14** — grille de 14 points de contrôle de la qualité d'un planning de
  projet, publiée par la *Defense Contract Management Agency* (agence du
  ministère de la Défense des États-Unis), utilisée ici comme repère de
  référence (pas comme verdict absolu) pour l'audit du planning P6. Détail des
  14 points dans `12_annexes.md`.
- **DD, DF, FD, FF** — types de liens de dépendance entre activités d'un
  planning : Début-Début, Début-Fin, Fin-Début (le plus courant), Fin-Fin.
- **KPI** — indicateur clé de performance ; dans ce projet : nombre d'éléments
  en retard, retard maximal, retard cumulé, nombre d'éléments bloqués, nombre
  d'inversions, nombre de changements de cadence.
- **P6 / Primavera P6** — logiciel de gestion de projet et de planification
  d'Oracle, utilisé pour le planning directeur du chantier Fehmarnbelt.
- **WBS** — *Work Breakdown Structure*, arborescence hiérarchique de
  décomposition d'un projet en lots de travaux, utilisée dans le planning P6
  pour organiser les activités (y compris les finitions et travaux marins
  extraits par `extraire_p6.py`).
- **XER** — format d'export tabulé (texte) de Primavera P6, contenant les
  tables d'activités, de liens, de ressources et de calendriers d'un projet.

## Identifiants et codes

- **`STE-NN` / `TE-NN`** — identifiant d'un élément standard (les deux préfixes
  coexistent dans les données du chantier).
- **`SPE-NN`** — identifiant d'un élément spécial.
- **`Beton:N`, `Outfitting`, `Zone:N`, `FloatUp`, `Basin`, `Parking[:N]`,
  `Ballast`, `Done`** — codes de statut *as-built* reconnus dans l'onglet
  `Inputs` (détail complet dans `06_documentation_technique.md`, §6.10).
