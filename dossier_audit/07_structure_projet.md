# 7. Structure du projet

## 7.1 Arborescence complète (fichiers versionnés dans Git)

```
taf/                                 (racine du dépôt)
├── .gitignore
├── README.md                        Documentation métier de référence, règle par règle
├── SUITE.md                         Note de reprise / journal de mesures en cours de projet
├── index.html                       Outil complet + unique implémentation du solveur
├── report_template.html             Gabarit de la page de restitution publiée
├── build_report.py                  Assemble rapport.html à partir des deux fichiers ci-dessus
├── planning_runner.js               Exécution du solveur en ligne de commande (Node.js)
├── post_tension.py                  Génère le planning de post-tension (Gantt, format Dywidag)
├── planning_cible.py                Génère le planning d'occupation (format Target schedule)
├── extraire_p6.py                   Extrait travaux marins et finitions d'un export P6
├── reduire_classeur.py              Réduit un classeur d'entrée à ce que le solveur lit
├── lire_xer.py                      Lecteur générique du format XER (Primavera P6)
├── auditer_xer.py                   Audit qualité d'un planning P6 (méthode DCMA-14 étendue)
├── regles_p6.py                     Extraction des règles/motifs répétés d'un planning P6
├── vendor_plan.png                  Image de fond du plan d'installation générale (inlinée dans rapport.html)
├── donnees_p6.txt                   Sortie mise en cache de extraire_p6.py (voir remarque ci-dessous)
├── Post_tension.xlsx                Dernier planning de post-tension généré (voir remarque ci-dessous)
├── __pycache__/                     Bytecode Python compilé (voir remarque ci-dessous)
└── dossier_audit/                   Le présent dossier d'audit
    ├── 00_INDEX.md
    ├── 01_resume_executif.md
    ├── 02_cahier_des_charges.md
    ├── 03_architecture.md
    ├── 04_journal_decisions_ADR.md
    ├── 05_analyse_risques.md
    ├── 06_documentation_technique.md
    ├── 07_structure_projet.md        (ce fichier)
    ├── 08_roadmap.md
    ├── 09_questions_ouvertes.md
    ├── 10_hypotheses.md
    ├── 11_glossaire.md
    ├── 12_annexes.md
    ├── 13_audit_critique.md
    └── 14_prompts_importants.md
```

**Fichier non versionné, généré à la demande :** `rapport.html`, produit par
`python3 build_report.py`, explicitement exclu par `.gitignore` avec ce
commentaire dans le dépôt : *« Page de restitution générée par
build_report.py […]. Reconstruite à la demande, jamais éditée à la main : elle
n'a pas sa place dans l'historique. »*

## 7.2 Rôle de chaque fichier

### Cœur du produit

- **`index.html`** — voir `03_architecture.md`, section 3.2, pour le détail de
  ses deux rôles (outil interactif complet + unique source du solveur).
- **`report_template.html`** — gabarit de la page publiée : reprend la
  structure d'`index.html` en y ajoutant les fonctionnalités propres à la
  restitution (Gantt déplaçable, rapport de conséquences, comparatif de
  séquences, planning imprimable, contraintes exhaustives). Contient les jetons
  de substitution `/*__SOLVEUR__*/`, `/*__XLSX__*/`, `/*__PLAN__*/ null`
  consommés par `build_report.py`.
- **`build_report.py`** — assemble les deux fichiers précédents plus SheetJS et
  l'image de fond en une seule page autonome `rapport.html`.
- **`planning_runner.js`** — exécute le même solveur hors navigateur, produit un
  JSON exploitable par les scripts Python en aval.

### Générateurs de plannings dérivés

- **`post_tension.py`** — planning de post-tension Dywidag (Gantt classique).
- **`planning_cible.py`** — planning d'occupation du site au format
  *Target schedule*, avec intégration optionnelle des travaux marins et des
  finitions.
- **`extraire_p6.py`** — extrait du planning P6 les seules données
  d'habillage nécessaires à `planning_cible.py` (jamais consommées par le
  solveur lui-même).
- **`reduire_classeur.py`** — produit une version allégée du classeur d'entrée,
  utile pour vérifier rapidement ce que le solveur lit réellement.

### Boîte à outils d'audit du planning P6 (indépendante du solveur)

- **`lire_xer.py`** — lecteur générique et économe en mémoire du format XER.
- **`auditer_xer.py`** — audit de qualité (méthode DCMA-14 étendue).
- **`regles_p6.py`** — extraction de motifs et de règles répétées.

### Documentation

- **`README.md`** — documentation métier de référence : chaque règle du modèle,
  sa justification, et le plus souvent une mesure chiffrée de son effet.
  Table des matières interne (près de 40 sections) couvrant l'ensemble des
  règles, du format du classeur d'entrée jusqu'aux limites connues.
- **`SUITE.md`** — note de reprise tenue en cours de développement,
  antérieure de quelques jours aux tout derniers correctifs du dépôt (voir
  `08_roadmap.md` pour ce qui a changé depuis sa dernière mise à jour).
  Contient l'historique détaillé des diagnostics de retard et leur résolution
  progressive.
- **`dossier_audit/`** — le présent dossier, reconstruction a posteriori d'une
  documentation projet complète et autonome (résumé exécutif, cahier des
  charges, architecture, décisions, risques, etc.).

### Fichiers de données / artefacts (statut à clarifier — voir remarque ci-dessous)

- **`vendor_plan.png`** — image de fond du plan d'installation générale du
  site, utilisée pour caler la position des éléments sur le plan animé.
  Légitimement versionnée : c'est une donnée source, pas un artefact généré.
- **`donnees_p6.txt`** — sortie de `extraire_p6.py`, mise en cache pour éviter
  de retraiter l'export P6 à chaque génération de planning d'occupation.
- **`Post_tension.xlsx`** — dernier planning de post-tension généré par
  `post_tension.py` au moment de sa livraison à l'utilisateur.
- **`__pycache__/`** — répertoire de bytecode Python compilé, généré
  automatiquement par l'interpréteur Python à l'exécution des scripts.

> **Remarque d'audit.** `donnees_p6.txt`, `Post_tension.xlsx` et `__pycache__/`
> sont, à la date de ce dossier, suivis par Git — alors que `rapport.html`, un
> artefact de build de même nature (résultat d'une exécution de script, pas une
> donnée source), est explicitement exclu. Cette incohérence de convention est
> documentée comme dette technique dans `05_analyse_risques.md` et priorisée
> dans `08_roadmap.md`. `__pycache__/` en particulier ne devrait, dans
> l'absolu, jamais être versionné (il est spécifique à l'environnement
> d'exécution local).

## 7.3 Fichiers explicitement absents

Pour éviter toute ambiguïté à un auditeur qui chercherait ces éléments
usuels et ne les trouverait pas :

- Pas de `package.json`, pas de `requirements.txt`, pas de fichier de verrou de
  dépendances (`package-lock.json`, etc.) à la racine.
- Pas de répertoire `tests/` ou `test/` versionné.
- Pas de configuration d'intégration continue (`.github/workflows/`, etc.).
- Pas de fichier de licence.
- Pas de `CHANGELOG.md` séparé — l'historique Git et `SUITE.md` en tiennent
  lieu de façon informelle.
