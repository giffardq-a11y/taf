# 9. Questions ouvertes

Décisions métier ou techniques qui restent à trancher, classées par ordre
d'importance décroissante. Pour chacune : la question, pourquoi elle est ouverte,
et ce qui bloque sa résolution.

## 9.1 Calendriers des activités marines (8 h vs 10 h par jour)

**Question.** L'audit du planning P6 a détecté des paires de calendriers portant
le même préfixe de nom et la même capacité annuelle déclarée (2000 h/an), mais
deux durées journalières différentes (8 h et 10 h) — par exemple
`TUX-MAR-DPP+DOP` et `TUX-MAR-TRW-TSHD`. Est-ce une saisie incohérente à
corriger dans le planning P6, ou une distinction légitime entre deux types
d'opérations en mer (l'une gérée en dragage/granulats, gérée par fenêtres
météo, l'autre en opérations portuaires continues) ?

**Pourquoi c'est ouvert.** L'utilisateur a explicitement demandé de **mettre
cette question en attente** le temps qu'il en discute avec le planificateur
responsable de ce périmètre sur le chantier. Aucune action n'a été engagée sur ce
point depuis cette instruction.

**Ce qui bloque.** Une réponse humaine, côté chantier, sur l'interprétation
correcte de ces calendriers. Rien côté code ne peut trancher cette question :
elle est de nature métier, pas technique.

**À ne pas faire tant que non tranché.** Ne pas modifier `auditer_xer.py` pour
supprimer ou minimiser la détection de cette anomalie ; ne pas modifier le
modèle du solveur sur la base d'une hypothèse non confirmée à ce sujet.

## 9.2 Durées réelles des opérations de post-tension (Dywidag)

**Question.** Quelles sont les vraies durées, en postes (demi-journées), des
trois opérations de post-tension — enfilage (*threading*), mise en tension
(*stressing*), injection (*grouting*) ?

**Pourquoi c'est ouvert.** Le script `post_tension.py` utilise actuellement des
valeurs par défaut (6, 4 et 2 postes respectivement) explicitement documentées
comme des repères à remplacer, faute d'avoir reçu les vraies valeurs du
sous-traitant Dywidag.

**Ce qui bloque.** Une transmission de données de la part de Dywidag.

## 9.3 Interprétation de la règle de délai de post-tension

**Question.** La cellule E31 du modèle Dywidag fourni indique : *« post
tensioning start two days after casting of SE next element »*. Le modèle
interprète cela comme deux jours après le **démarrage** de la coulée de
l'élément suivant sur la même ligne (pas sa fin). Cette interprétation est-elle
correcte ? Que signifie précisément « SE » dans ce contexte ?

**Pourquoi c'est ouvert.** Interprétation raisonnable mais non confirmée par le
sous-traitant ou par le planificateur.

**Ce qui bloque.** Une confirmation explicite, côté chantier ou côté Dywidag.

## 9.4 Nombre d'équipes de post-tension disponibles

**Question.** Combien d'équipes Dywidag peuvent travailler en parallèle sur les
6 lignes de production ?

**Pourquoi c'est ouvert.** Le planning de post-tension généré suppose
actuellement un parallélisme illimité (aucune contrainte de ressource humaine).
Si le nombre réel d'équipes est limité, le planning généré serait irréaliste par
endroits (plusieurs opérations apparaissant simultanées alors qu'une seule
équipe existe).

**Ce qui bloque.** Une donnée organisationnelle côté sous-traitant ou côté
chantier. Si la réponse révèle une contrainte réelle, cela impliquerait de faire
évoluer `post_tension.py` vers un ordonnancement sous contrainte de ressources
(actuellement absent).

## 9.5 Positions géométriques extrapolées

**Question.** Quelles sont les coordonnées réelles, sur le plan d'installation
générale, de la zone de stockage tampon dédiée à la ligne SPE, et du quai de
ballastage (Ballast Jetty) ?

**Pourquoi c'est ouvert.** Ces deux positions ont été extrapolées faute de plan
officiel les indiquant précisément au moment de leur ajout au modèle
(respectivement à l'ouest du Basin C, et dans l'axe du parking). Leur capacité
fonctionnelle (une place de stockage SPE, position du quai) est, elle, confirmée
par le chantier — seule la position visuelle sur le plan est approximative.

**Ce qui bloque.** L'obtention d'un plan officiel plus précis. Sans effet sur le
calcul de cadence, seulement sur la fidélité du rendu visuel.

## 9.6 Plan de coupe réel du tunnel

**Question.** Quelles sont les abscisses réelles de pose de chaque élément dans
le tunnel immergé ?

**Pourquoi c'est ouvert.** La coupe longitudinale actuellement affichée utilise
l'**ordre** de pose (juste) mais pas les **distances** réelles entre éléments
(approximées par un espacement régulier).

**Ce qui bloque.** L'obtention du plan de coupe officiel du tunnel, pas encore
disponible au moment de la construction de cette vue.

## 9.7 Interaction déphasage / jour de coulage sur PL-5, cas limite

**Question.** Un test synthétique isolé, construit pour valider le correctif de
désactivation du jour de coulage aux cadences intermédiaires (voir ADR-015 dans
`04_journal_decisions_ADR.md`), a révélé une dégradation mesurable des
indicateurs de retard dans une configuration spécifique — déphasage entre
halles actif, cadences mixtes entières et intermédiaires, séquence non
optimisée par le chemin réel de l'interface. Ce cas se produit-il réellement en
usage normal, ou est-ce un artefact du protocole de test synthétique employé ?

**Pourquoi c'est ouvert.** Vérifié **non reproduit** en bout en bout sur le
chemin réel de l'interface (zéro retard avant et après le correctif, sur le
classeur de référence, avec la séquence réellement optimisée par le bouton
« Optimiser »). Mais l'espace complet des configurations possibles n'a pas été
exploré de façon exhaustive — seule la configuration effectivement utilisée par
défaut a été validée.

**Ce qui bloque.** Un travail d'investigation supplémentaire, non entamé, pour
déterminer si ce cas limite est atteignable via l'interface réelle (par exemple
en combinant certaines options manuellement) ou seulement via un appel direct
au moteur de simulation hors de son usage normal.

## 9.8 Résolu — traçabilité pour mémoire

Cette section conserve la trace de questions qui étaient ouvertes puis ont été
tranchées, pour qu'un lecteur ne les rouvre pas par erreur :

- **Post-tension de la ligne SPE** — tranché : **aucune** post-tension n'est
  générée pour la ligne SPE, confirmé explicitement par l'utilisateur. Le
  script `post_tension.py` l'exclut délibérément et le signale à l'exécution
  (le solveur ne date jamais la fin de coulée d'un élément spécial, seulement
  ses passages de zone — lui inventer une date de post-tension serait une
  donnée fabriquée).
- **Cadence de départ du modèle** — tranché : 3 semaines/segment, confirmé par
  l'utilisateur comme correspondant à `Config_Cycles` du classeur réel.
- **Nombre de places de la zone de stockage SPE** — tranché : une seule place,
  confirmée suffisante par la mesure (une deuxième place n'apporte aucun gain).
- **Correspondance des zones de la ligne SPE** (`FI1`/`FI2`/`FI3` du planning
  P6 vs `UB1`/`UB2`/`UB3` de `Config_SPE`) — tranché : correspondance directe
  confirmée, la zone tampon est bien dans le Basin C.
- **Règle de sortie du bassin vers le parking** — tranché et corrigé (voir
  ADR-016) : un élément part dès qu'une place est libre, sauf séjour court et
  non bloquant, confirmé par observation directe du chantier.
- **Désactivation du jour de coulage aux cadences intermédiaires** — tranché et
  implémenté (voir ADR-015) : instruction explicite de l'utilisateur, appliquée
  telle quelle.
