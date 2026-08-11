# 5. Analyse des risques

Classement de criticité utilisé dans ce document : **Critique** (peut invalider un
résultat de calcul sans avertissement visible, ou bloquer l'usage de l'outil) —
**Élevé** (dégrade significativement la fiabilité, la maintenabilité ou la
confidentialité, sans bloquer l'usage immédiat) — **Modéré** (gêne ou ralentit,
sans conséquence sur la justesse du résultat) — **Faible** (cosmétique ou
théorique).

## 5.1 Risques techniques

| Risque | Criticité | Description | Mitigation actuelle |
|---|---|---|---|
| Absence de suite de tests automatisée **versionnée** | Élevé | Les seuls tests existants (santé de la page, comparaison avant/après un changement, tests de bout en bout avec un navigateur piloté) ont été écrits et exécutés dans un répertoire de travail temporaire, hors du dépôt Git. Aucun test ne s'exécute automatiquement à chaque modification. | Discipline manuelle : chaque changement de règle métier documenté dans ce projet a été mesuré avant/après sur le classeur de référence. Cette discipline n'est pas *appliquée* par un outil, elle dépend de la rigueur de la personne qui modifie le code. |
| Absence de fichier de dépendances versionné (`package.json`, `requirements.txt`) | Élevé | `planning_runner.js` dépend du paquet npm `xlsx` ; les scripts Python dépendent d'`openpyxl`. Aucun de ces deux dépendances n'est déclaré dans un fichier versionné à la racine du dépôt. Un clone frais du dépôt ne permet pas de faire tourner `planning_runner.js` sans deviner qu'il faut `npm install xlsx`. | Aucune. Voir `08_roadmap.md` pour la recommandation de corriger ce point rapidement. |
| Extraction de code par marqueurs de commentaire, sans garde-fou automatique | Élevé | Si les marqueurs `SOLVEUR-CORE-DEBUT`/`FIN` sont supprimés, dupliqués ou mal renommés par une future modification, `build_report.py` et `planning_runner.js` échoueraient (le premier avec un message d'erreur explicite ; il faudrait vérifier le second) ou, pire, extrairaient une portion de code incorrecte sans le signaler. | `build_report.py` vérifie la présence des marqueurs et s'arrête sinon (`sys.exit`) — protection partielle, seulement sur ce point d'entrée. |
| Duplication de valeurs par défaut entre `report_template.html` et `planning_runner.js` | Élevé | Un défaut de synchronisation a déjà eu lieu une fois en cours de projet (voir ADR-018 dans `04_journal_decisions_ADR.md`) et a rendu les exports de planning dérivés temporairement incohérents avec ce que l'interface affichait, sans qu'aucune erreur ne soit levée. | Correction ponctuelle faite ; aucun test automatique n'empêche une nouvelle divergence si un paramètre est ajouté dans un seul des deux fichiers. |
| Fichiers générés versionnés dans Git de façon incohérente | Modéré | `rapport.html` est explicitement exclu du suivi Git (`.gitignore`), au motif documenté qu'un artefact de build ne doit pas être versionné. Mais `Post_tension.xlsx`, `donnees_p6.txt` et un répertoire `__pycache__/` (bytecode Python compilé) sont, eux, actuellement suivis par Git — incohérent avec la règle appliquée à `rapport.html`. | Aucune ; à corriger, voir `08_roadmap.md`. |
| Fichier `index.html` volumineux et multi-rôles (~4000 lignes) | Modéré | Le même fichier porte le solveur, l'interface de développement et la logique d'habillage (chargement de fichiers, génération de classeur modèle). Un tiers qui doit modifier une règle métier doit d'abord identifier si son code est dans le périmètre partagé (entre les marqueurs) ou local à `index.html`. | Commentaires de section numérotés, marqueurs de périmètre explicites. Pas de séparation physique en plusieurs fichiers. |
| Simulation gloutonne non garantie optimale | Modéré | Documenté comme limite assumée : le solveur décide ligne par ligne, sans arbitrage global entre lignes concurrentes pour les ressources partagées. Sur des jeux de données très différents de celui testé, le résultat pourrait s'éloigner davantage d'un optimum théorique sans qu'aucun signal ne le mesure. | Le solveur ne modélise pas non plus, au moment du choix de cadence, les portes du Basin C ni le déphasage entre halles (il les applique correctement dans la simulation aval, mais pas dans son estimation prospective de faisabilité) — cause documentée d'oscillations de cadence supplémentaires possibles sur PL-5. |
| Interaction non totalement validée entre le déphasage entre halles et la désactivation du jour de coulage à cadence intermédiaire (ADR-015) | Modéré | Un test synthétique isolé, non représentatif du chemin réellement emprunté par l'interface, a révélé une dégradation mesurable (nombre de retards et retard cumulé) dans une configuration spécifique (déphasage actif, cadences mixtes entières/intermédiaires, une variante de séquence non optimisée par le chemin réel de l'optimiseur). | Vérifié non reproduit en bout en bout sur le chemin réel de l'interface (zéro retard avant/après, sur le classeur de référence, séquence optimisée par le bouton réel). Non blanchi sur l'espace complet des configurations possibles. |
| Positions géométriques extrapolées, non mesurées | Modéré | La zone de stockage tampon SPE et le quai de ballastage (Ballast Jetty) ont des coordonnées extrapolées sur le plan (pas de plan officiel disponible au moment de leur ajout). N'affecte que le rendu visuel, pas le calcul de cadence. | Documenté explicitement dans `README.md` (section « Limites connues ») comme à recalibrer. |
| `Config_Cycles` limité à 3 emplacements de changement de cadence par ligne | Faible | Si le solveur calcule plus de 3 changements de cadence pour une ligne, les changements au-delà du 3e ne sont pas réinjectés dans cet onglet Excel à l'export (un avertissement le signale). La liste complète reste disponible ailleurs (rapport, CSV). | Avertissement explicite au moment de l'export. |

## 5.2 Risques métier

| Risque | Criticité | Description | Mitigation actuelle |
|---|---|---|---|
| Calendriers des activités marines (8 h vs 10 h par jour) | Élevé | Une anomalie a été détectée par l'outil d'audit XER (deux versions du même calendrier, même capacité annuelle déclarée, mais deux durées journalières différentes) mais son traitement est **explicitement mis en attente** à la demande de l'utilisateur, le temps qu'il tranche avec le planificateur responsable de ce périmètre. Tant que la question n'est pas tranchée, aucune correction n'est apportée au modèle sur ce point. | Aucune action en cours, sur instruction explicite — voir `09_questions_ouvertes.md`. |
| Durée réelle par élément non disponible pour le float-up | Élevé | Contrairement à la durée de ballast (lue par élément dans le planning P6), aucune source de donnée réelle par élément n'existe à ce jour pour la durée de float-up ; le paramètre d'interface correspondant reste donc une valeur forfaitaire, avec le même risque de sur- ou sous-estimation qui a été corrigé pour le hook-up et le ballast (voir ADR-019). | Aucune, faute de donnée source identifiée dans le planning P6 actuellement exploité. |
| Durées de post-tension (Dywidag) non confirmées | Élevé | Le générateur de planning de post-tension (`post_tension.py`) utilise des durées d'opération par défaut (enfilage, mise en tension, injection) explicitement présentées comme des repères à remplacer par les vraies valeurs du sous-traitant, pas encore reçues. | Message d'avertissement explicite affiché à chaque exécution du script. |
| Nombre d'équipes de post-tension non contraint | Élevé | Le planning de post-tension généré suppose un parallélisme illimité entre les 6 lignes de production ; si le sous-traitant dispose d'un nombre limité d'équipes, le planning généré serait irréaliste (toutes les opérations pourraient apparaître simultanées). | Aucune, question posée à l'utilisateur, sans réponse à ce jour — voir `09_questions_ouvertes.md`. |
| Règle d'interprétation du délai de post-tension à confirmer | Élevé | Le modèle interprète « post tensioning starts two days after casting of next element » comme deux jours après le **démarrage** de la coulée de l'élément suivant (pas sa fin). Cette interprétation n'a pas été confirmée par le sous-traitant. | Documenté explicitement en tête du script `post_tension.py`. |
| Qualité du planning directeur P6 lui-même | Modéré | Le solveur fait une confiance totale aux dates du planning P6 collées dans le classeur d'entrée (immersion, passages de zone SPE, durées de ballast). Une erreur de saisie ou une incohérence dans le planning P6 se propage telle quelle dans le résultat du solveur, sans détection automatique — sauf à faire tourner, séparément, la boîte à outils d'audit XER. | La boîte à outils d'audit existe (`auditer_xer.py`) mais n'est **pas** exécutée automatiquement à chaque calcul de cadence ; c'est un geste manuel, distinct. |
| Position réelle des lieux extrapolés (voir aussi risques techniques) | Faible | N'a pas d'effet sur les décisions de cadence, seulement sur la lecture visuelle du plan animé — un planificateur pourrait mésinterpréter une distance ou une position sur le plan comme fiable alors qu'elle est approximative. | Documenté dans `README.md`. |

## 5.3 Risques organisationnels

| Risque | Criticité | Description | Mitigation actuelle |
|---|---|---|---|
| Connaissance du projet concentrée dans les messages de commit et deux fichiers de notes (`README.md`, `SUITE.md`) | Élevé | Aucune spécification n'a précédé le code ; les règles métier et leurs justifications ont été construites et documentées au fil de l'eau, principalement en français dans `README.md`, et en anglais dans l'historique Git. Une personne qui ne lirait ni l'un ni l'autre manquerait le *pourquoi* de nombreuses règles, alors même que le code applique correctement le *quoi*. | Ce dossier d'audit (`dossier_audit/`) est une tentative de consolidation de cette connaissance dans un format indépendant de l'historique de conversation ; il reste néanmoins postérieur au code, pas antérieur. |
| Absence de relecture par un second développeur | Élevé | Le projet a été développé par un seul interlocuteur métier en dialogue direct avec un assistant IA, sans processus de revue de code par un pair humain avant intégration. | Aucune. Recommandation dans `13_audit_critique.md`. |
| Absence d'intégration continue | Modéré | Rien n'empêche techniquement un commit de casser silencieusement le rendu de la page, l'extraction du solveur, ou un des scripts Python — seule une exécution manuelle des tests ad hoc (non versionnés) le révélerait. | Voir recommandation dans `08_roadmap.md`. |
| Dépendance à un unique classeur de référence pour toutes les mesures | Modéré | La quasi-totalité des chiffrages avancés dans `README.md`, `SUITE.md` et ce dossier proviennent d'un seul classeur réel (« classeur de référence », 89 éléments). Aucune validation croisée sur un second jeu de données n'a été documentée à ce jour. | Aucune. À surveiller si un second chantier ou une seconde phase du même chantier devait utiliser l'outil. |

## 5.4 Dépendances

| Dépendance | Nature | Criticité si indisponible/modifiée |
|---|---|---|
| **SheetJS** (bibliothèque `xlsx`, npm) | Lecture des classeurs Excel côté navigateur et côté Node.js | Élevé — sans elle, aucune lecture de classeur n'est possible dans aucun des trois contextes d'exécution. Une copie « mini » est inlinée dans `rapport.html` au moment du build (pas de dépendance réseau à l'exécution), mais `build_report.py` la télécharge depuis un CDN public si aucune copie locale n'est trouvée — point de fragilité au moment du *build*, pas de l'usage. |
| **openpyxl** (Python) | Lecture/écriture des classeurs Excel dans tous les scripts Python (générateurs de plannings dérivés, réducteur de classeur) | Élevé pour ces scripts uniquement — sans effet sur le solveur JavaScript. |
| **Playwright** (utilisé de façon ad hoc, hors dépôt) | Tests de bout en bout par pilotage de navigateur | Faible pour le fonctionnement de l'outil ; élevé pour la capacité à vérifier une non-régression avant livraison, puisque c'est le seul mécanisme de test de bout en bout qui existe, et il n'est pas versionné. |
| **Format XER de Primavera P6** | Format d'entrée de la boîte à outils d'audit | Modéré — un changement de version majeure du format par Oracle (éditeur de Primavera) pourrait nécessiter une adaptation de `lire_xer.py`. |

## 5.5 Points bloquants actuels

- **Aucun point bloquant technique** n'empêche l'usage courant de l'outil à la
  date de ce dossier : le calcul de cadence fonctionne, produit un résultat sans
  retard ni blocage sur le classeur de référence, et l'ensemble des
  fonctionnalités décrites dans `02_cahier_des_charges.md` est opérationnel.
- **Un point bloquant métier** est en attente : la question des calendriers des
  activités marines (voir ci-dessus et `09_questions_ouvertes.md`), qui reste
  sans effet sur le résultat courant tant qu'elle n'est pas activement exploitée
  par une nouvelle règle, mais qui doit être tranchée avant toute évolution du
  modèle sur ce périmètre.

## 5.6 Dette technique — synthèse

Par ordre de priorité de résorption recommandée (détail dans `08_roadmap.md`) :

1. Ajouter `package.json` et `requirements.txt` (ou équivalents) à la racine du
   dépôt.
2. Committer une suite de tests minimale (santé de page, non-régression de
   KPI sur le classeur de référence, extraction correcte du bloc
   `SOLVEUR-CORE`) directement dans le dépôt, hors d'un répertoire de travail
   temporaire.
3. Nettoyer le suivi Git des fichiers générés incohérents
   (`__pycache__/`, `Post_tension.xlsx`, `donnees_p6.txt` — décider au cas par
   cas s'ils doivent être régénérés à la demande comme `rapport.html`, ou
   déplacés vers un répertoire d'exemples explicitement versionné).
4. Mettre en place une intégration continue minimale qui exécute cette suite de
   tests à chaque modification.
5. Documenter, sous forme de test, la garantie de synchronisation entre les
   valeurs par défaut de `report_template.html` et de `planning_runner.js`
   (ADR-018), pour empêcher une nouvelle divergence silencieuse.
