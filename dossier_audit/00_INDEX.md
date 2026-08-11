# Dossier d'audit — Lolland Master Planner

Ce dossier documente intégralement le projet **Lolland Master Planner**, un outil de
planification de la production d'éléments de tunnel immergé pour le chantier
Fehmarnbelt (liaison fixe Danemark–Allemagne, usine de préfabrication de Rødbyhavn,
Lolland, Danemark).

## À qui s'adresse ce dossier

À toute personne ou tout système — humain ou IA — devant reprendre, auditer ou faire
évoluer ce projet **sans accès à l'historique de conversation qui a produit le code**.
Chaque document se suffit à lui-même : aucune information nécessaire à sa compréhension
n'est renvoyée à une discussion externe. Les seuls renvois internes sont vers les autres
fichiers de ce même dossier, nommés explicitement.

## Comment lire ce dossier

Les fichiers sont numérotés dans l'ordre de lecture recommandé pour une prise en main
complète, mais chacun peut être lu indépendamment :

| Fichier | Contenu |
|---|---|
| `01_resume_executif.md` | Objectif, contexte, utilisateurs, problème résolu, état d'avancement |
| `02_cahier_des_charges.md` | Fonctionnalités, cas d'usage, contraintes, exigences |
| `03_architecture.md` | Composants, flux de données, choix technologiques, diagrammes Mermaid |
| `04_journal_decisions_ADR.md` | Décisions d'architecture et de règle métier, une par une, avec justification |
| `05_analyse_risques.md` | Risques techniques, métier, organisationnels, dette technique, criticité |
| `06_documentation_technique.md` | Technologies, dépendances, sécurité, déploiement, absence de backend |
| `07_structure_projet.md` | Arborescence complète, rôle de chaque fichier |
| `08_roadmap.md` | Terminé / à faire / priorités |
| `09_questions_ouvertes.md` | Décisions métier encore en attente |
| `10_hypotheses.md` | Hypothèses de conception, à vérifier ou déjà vérifiées |
| `11_glossaire.md` | Tous les termes et acronymes du domaine et du code |
| `12_annexes.md` | Tableaux de référence, valeurs par défaut, méthodologie DCMA-14 |
| `13_audit_critique.md` | Auto-évaluation honnête : forces, faiblesses, compromis, ce qui serait refait autrement |
| `14_prompts_importants.md` | Instructions et décisions métier reproduites verbatim ou fidèlement paraphrasées |

## Ce que ce dossier n'est pas

Ce n'est pas une spécification qui a précédé le code : le projet a été construit de
façon incrémentale, règle métier après règle métier, chaque règle étant vérifiée par la
mesure sur un classeur réel avant d'être considérée comme acquise. Ce dossier est une
**reconstruction a posteriori**, faite à partir du code source, de l'historique Git et
des notes de bord tenues pendant le développement (`README.md`, `SUITE.md`, à la racine
du dépôt). Il est daté et reflète l'état du dépôt à la date indiquée ci-dessous ; le
code source fait foi en cas d'écart.

**Date de rédaction du dossier :** 7 août 2026.
**Dernier commit couvert :** `688bc48` — *« Fix hook-up double-counting an element's
basin dwell against its real ballast date »*, branche
`claude/staggering-sequence-optimizer-ot6zxr`.

## Documents complémentaires déjà présents dans le dépôt

Ce dossier ne remplace pas mais synthétise et met en perspective deux documents plus
détaillés déjà présents à la racine du dépôt, qu'il cite abondamment :

- **`README.md`** (~1100 lignes) — documentation métier de référence, règle par règle,
  chacune assortie de sa justification et souvent d'une mesure chiffrée de son effet.
  C'est la source la plus fiable et la plus à jour sur *pourquoi* chaque règle existe.
- **`SUITE.md`** (~500 lignes) — note de reprise tenue en cours de développement,
  antérieure de quelques jours aux tout derniers correctifs (voir `08_roadmap.md` pour
  ce qui a changé depuis). Utile pour l'historique des mesures et des diagnostics.

Un lecteur pressé peut se limiter à ce dossier ; un auditeur technique approfondi devra
lire aussi `README.md` en complément du présent dossier, en particulier de
`06_documentation_technique.md`.
