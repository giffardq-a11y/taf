# 6. Documentation technique

## 6.1 Technologies utilisées

| Domaine | Technologie | Où |
|---|---|---|
| Langage principal (solveur, interface) | JavaScript (ES, sans transpilation, sans framework) | `index.html`, `report_template.html` |
| Balisage / mise en forme | HTML5 + CSS3 (variables CSS pour les couleurs, y compris un thème sombre) | `index.html`, `report_template.html` |
| Lecture de fichiers Excel côté navigateur | SheetJS (paquet npm `xlsx`, build « mini ») | inliné dans `rapport.html` par `build_report.py` |
| Rendu graphique | SVG généré dynamiquement (plan du site, coupe du tunnel, Gantt) — pas de bibliothèque de graphes tierce | `index.html`, `report_template.html` |
| Exécution hors navigateur | Node.js, module natif `vm` (bac à sable d'exécution du bloc solveur extrait) | `planning_runner.js` |
| Lecture de fichiers Excel côté Node.js | SheetJS (paquet npm `xlsx`) | `planning_runner.js` |
| Génération de classeurs Excel | Python, bibliothèque `openpyxl` | `post_tension.py`, `planning_cible.py`, `reduire_classeur.py`, `extraire_p6.py` |
| Lecture du format XER (Primavera P6) | Python, parseur maison (aucune bibliothèque tierce) | `lire_xer.py` |
| Tests de bout en bout (ad hoc, non versionnés) | Playwright (pilotage de Chromium) | hors dépôt, dans un répertoire de travail temporaire |

## 6.2 Frameworks et bibliothèques

Volontairement minimalistes :

- **Aucun framework JavaScript** (pas de React/Vue/Angular). Choix documenté en
  ADR-001 dans `04_journal_decisions_ADR.md`.
- **SheetJS** est la seule bibliothèque JavaScript tierce du projet.
- Côté Python, **`openpyxl`** est la seule dépendance non standard des scripts de
  génération Excel ; les scripts d'audit XER (`lire_xer.py`, `auditer_xer.py`,
  `regles_p6.py`) et `build_report.py` **n'ont aucune dépendance externe** —
  uniquement la bibliothèque standard Python (`re`, `sys`, `datetime`,
  `collections`, `pathlib`, `argparse`, `base64`, `urllib.request`).

**Aucun fichier de dépendances n'est actuellement versionné à la racine du
dépôt** (ni `package.json`, ni `requirements.txt`). Pour reconstituer un
environnement de travail :

```bash
# Pour planning_runner.js
npm install xlsx

# Pour les scripts Python
pip install openpyxl
```

Voir `05_analyse_risques.md` pour l'évaluation de ce manque et `08_roadmap.md`
pour la recommandation de le corriger.

## 6.3 API

**Aucune API** au sens réseau du terme : ni API exposée par le projet, ni API
externe consommée à l'exécution. Les seuls appels réseau du projet ont lieu au
moment du *build* de `rapport.html` (`build_report.py` télécharge SheetJS depuis
un CDN si aucune copie locale n'est trouvée) — jamais à l'exécution de l'outil
par son utilisateur final.

## 6.4 Base de données

**Aucune base de données.** L'unique support de données persistantes est le
classeur Excel fourni en entrée par l'utilisateur (et, en sortie, les fichiers
Excel générés par les scripts Python). Aucun état n'est conservé entre deux
ouvertures de `index.html` ou de `rapport.html` dans le navigateur — chaque
session repart d'un chargement de fichier.

## 6.5 Sécurité

- **Surface d'attaque réseau nulle à l'exécution** : aucune requête sortante
  n'est émise par `index.html` ou `rapport.html` une fois la page ouverte (voir
  ADR-002). Un audit de sécurité réseau se limite donc, pour ces deux fichiers, à
  vérifier l'absence de code qui contredirait cette propriété (pas de `fetch`,
  `XMLHttpRequest` ou balise pointant vers une ressource externe dans le chemin
  d'exécution normal).
- **Aucune donnée n'est transmise à un tiers.** Le classeur chargé par
  l'utilisateur reste dans la mémoire du navigateur (traité par SheetJS
  localement) et n'est jamais envoyé où que ce soit.
- **Aucune validation d'entrée formalisée au sens sécurité** (pas d'échappement
  systématique, pas de bac à sable pour le contenu du classeur) : le classeur
  d'entrée est considéré comme une donnée de confiance venant de l'utilisateur
  lui-même, pas comme une entrée potentiellement hostile. Ce choix est cohérent
  avec le contexte d'usage (outil interne, à diffusion restreinte) mais devrait
  être reconsidéré si l'outil était un jour exposé à des fichiers d'origine non
  maîtrisée.
- **Aucun secret, jeton ou identifiant** n'est stocké ou manipulé par le
  projet — cohérent avec l'absence totale de service distant.

## 6.6 Authentification

**Absente et sans objet.** L'outil n'a pas de notion de compte, de session
authentifiée ou de rôle. L'accès à l'outil se limite à l'accès au fichier lui-même
(contrôle d'accès délégué entièrement au système de fichiers ou au canal de
diffusion du fichier — messagerie, partage réseau, etc. — hors périmètre du
projet).

## 6.7 Déploiement

**Aucune infrastructure de déploiement.** Deux modes de mise à disposition :

1. **`index.html`** est distribué comme fichier autonome, ouvert directement
   dans un navigateur (double-clic, ou glissé dans un onglet).
2. **`rapport.html`**, généré par `build_report.py`, est une page HTML
   également autonome, qui peut être hébergée n'importe où (serveur de fichiers
   statique, partage interne, ou publiée comme page web) sans configuration
   serveur particulière — elle ne fait aucun appel à un backend.

Il n'existe **aucun pipeline de déploiement automatisé** (pas de CI/CD) : la
génération de `rapport.html` et sa mise à disposition sont des gestes manuels.

## 6.8 Sauvegardes

**Aucun mécanisme de sauvegarde propre au projet.** La donnée qui compte
(le classeur Excel d'entrée, et ses éventuelles évolutions au fil des cycles de
planification) est entièrement sous la responsabilité de son propriétaire, en
dehors du périmètre de l'outil. Le code source lui-même est versionné dans Git
(voir `07_structure_projet.md`), ce qui constitue la seule forme de sauvegarde
gérée par le projet.

## 6.9 Supervision

**Aucune supervision, aucune télémétrie, aucun journal centralisé.** Le seul
journal produit par l'outil (« journal de calcul », visible à l'écran) est
local à la session en cours, non persisté au-delà de la fermeture de l'onglet.
Aucune remontée d'erreur vers un système externe n'existe — cohérent avec
l'absence totale de communication réseau à l'exécution (ADR-002), mais cela
signifie aussi qu'aucune erreur rencontrée par un utilisateur sur le terrain
n'est automatiquement connue de l'équipe de développement.

## 6.10 Structure des données d'entrée (classeur Excel)

Le classeur d'entrée attendu comporte 4 onglets significatifs pour le solveur
(d'autres onglets peuvent être présents, ils sont ignorés) :

| Onglet | Rôle | Colonnes lues |
|---|---|---|
| `Inputs` | Séquences de production candidates | Colonne A = ordre ; colonnes B/D/F/H/J/L = identifiants d'élément pour PL-1 à PL-5 et SPE ; colonnes C/E/G/I/K/M = statut *as-built* de l'élément situé immédiatement à sa gauche |
| `Immersion` | Dates cibles et ordre d'immersion (donnée d'entrée intangible), plus planning détaillé | `ID Element`, `Date Immersion`, `Activity Name`, `Start`, `Finish` — ces trois dernières colonnes portent le planning P6 collé (dates de clamping, passages de zone SPE) |
| `Config_Cycles` | État actuel de cadence par ligne | Colonnes B/C (Date Seuil 1 / Cycle 1) = rythme actuel, saisi par l'utilisateur ; colonnes D à I (Seuils/Cycles 2 à 4) ignorées en entrée, calculées et réinjectées par le solveur en sortie |
| `Config_SPE` | Paramètres des 7 zones de la ligne SPE | Colonnes A à G : zone, nom, activité, durée, type, jalon d'étanchéité (semaines après entrée en UB1), rythme SPE long optionnel |

### Format des statuts *as-built* (colonnes C/E/G/I/K/M de `Inputs`)

Le statut se saisit dans la cellule immédiatement à droite de l'identifiant de
l'élément. Lecture tolérante : séparateur deux-points ou espace, accents et casse
ignorés, synonymes français acceptés.

| Code | Signification |
|---|---|
| `Beton:N` | En zone béton, au segment N (1 à 9) — lignes PL uniquement |
| `Outfitting` | En zone d'équipement — lignes PL uniquement |
| `Zone:N` | Ligne SPE uniquement : dans la zone N (1 = CPA … 7 = UB3) |
| `FloatUp` | En cours de mise à flot |
| `Basin` | En Lower Basin (hook-up en cours) |
| `Parking` ou `Parking:N` | Au parking (place N si connue, sinon première libre) |
| `Ballast` | Au quai de ballastage |
| `Done` (ou `immerge`, `termine`, `fini`) | Déjà immergé |

Suffixe de date optionnel pour préciser le début réel de la phase :
`Beton:5:2026-06-15`. Sans statut renseigné, un élément est considéré non
démarré, sauf si sa date d'immersion cible est déjà passée (il est alors déduit
comme terminé). Un code non reconnu est signalé dans le journal et l'élément est
traité comme non démarré.

## 6.11 Interfaces en ligne de commande

```bash
# Assembler la page de restitution autonome
python3 build_report.py [--xlsx chemin/vers/xlsx.full.min.js] [-o sortie.html]

# Rejouer le solveur hors navigateur, produire un JSON du plan calculé
node planning_runner.js <classeur.xlsx> [date-de-référence] [options...]
# Options : --variante=N  --sans-optimiseur  --flux-tendu  --en-cours-de-cycle
#           --sans-staggering  --budget=ms  --sans-vacances  --sans-porte-unique
#           --sans-jour-coulage  --sans-bassin-libre

# Générer le planning de post-tension (Gantt classique, format Dywidag)
python3 post_tension.py plan.json Post_tension.xlsx \
    [--threading N] [--stressing N] [--grouting N] [--retard N]

# Générer le planning d'occupation du site (format Target schedule)
python3 planning_cible.py plan.json Target_schedule_solveur.xlsx [donnees_p6.txt]

# Extraire les travaux marins et finitions du planning P6
python3 extraire_p6.py TUXERev2LinkedActivities.xlsx donnees_p6.txt

# Réduire un classeur d'entrée à ce que le solveur lit réellement
python3 reduire_classeur.py source.xlsm reduit.xlsx

# Lire et auditer un export XER de Primavera P6
python3 auditer_xer.py planning.xer -o audit.txt
```

## 6.12 Compatibilité navigateur

Aucune matrice de compatibilité formelle n'a été établie. Le projet utilise des
API JavaScript standards (ES2017+, SVG, `FileReader`, `<dialog>`) sans
polyfill : il cible implicitement les navigateurs modernes à jour (Chromium,
Firefox, Safari récents). Les tests de bout en bout réalisés en cours de projet
l'ont été exclusivement sur Chromium (via Playwright).
