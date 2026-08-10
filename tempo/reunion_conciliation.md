# Réunion de conciliation TEMPO — support de convocation

Document généré à partir de `tempo/dossier_zones.py` (`REGISTRE_VALIDATION`), pour
préparer la ou les réunions nécessaires à trancher les points ouverts identifiés en
lisant les documents TEMPO (Rebar/Casting/Logistique). Organisé par personne
responsable pressentie, dans l'ordre où les convoquer probablement (les points
« critique » d'abord). Chaque point renvoie à la zone correspondante du schéma
interactif : <https://claude.ai/code/artifact/43d995d8-8533-45a6-af98-d7afd7fc9706>
(cliquer sur la zone citée pour voir la donnée complète, ses sources, et les
contradictions relevées).

Rien ci-dessous n'a été tranché par avance : c'est la liste des questions, pas des
réponses proposées.

---

## ⚠ Point critique ajouté le 10/08/2026 — Valery Claise / Joanna

**Sujet : le code zone (lettres A-I / M-L, utilisé partout dans ce dossier et le schéma)
n'est pas fiable.** Contrôle croisé : sur les 3243 tâches du classeur N3, **aucune**
n'est étiquetée `UNIT=« Panel Factory »`, alors que la feuille `Data` du classeur
déclare que la lettre M désigne « Panel Factory » — la plupart des tâches des feuilles
`*__M` sont en réalité étiquetées `UNIT=« Casting Pit »`. Le même écart existe pour les
18 autres lettres. La zone S (Casting Pit) est le cas le plus proche d'une lecture
correcte (51% de ses tâches sont bien `UNIT=Casting Pit`), mais 49% ne le sont pas.

**Conséquence :** tout chiffre « par zone lettre » calculé avant aujourd'hui dans ce
dossier (le pic BC en « zone S », par exemple) est à prendre avec cette réserve. Les
courbes de main-d'œuvre ajoutées le 10/08/2026 regroupent désormais par la colonne
`UNIT` (l'attribut fiable), pas par la lettre.

**Question à trancher :** que représentent réellement ces lettres si ce n'est pas
l'aire physique de la feuille `Data` — un repère de gabarit/position dans le cycle de
70 jours tempo, une autre convention ?

*Zones concernées : toutes. Impact : critique — remet en question l'attribution
physique de toute donnée « par zone » calculée avant le 10/08/2026.*

---

## Olivier Bonnot — arbitrage transverse

**Sujet : durée d'un poste de travail.** Quatre valeurs différentes trouvées selon
le document, sur un sujet qui conditionne toute la grille horaire du simulateur :

| Source | Durée trouvée |
|---|---|
| Présentation Rebar (TEMPO_N2_Presentation_Rebar_04062026.pptx) | 9h |
| Truck_for_All_Set__V2.xlsx (feuille Hypothèses) | 10h |
| Présentation Casting Team (TEMPO_N2_Presentation_Casting_Team_10062026.pptx) | 8h ou 12h, non tranché dans le document lui-même |
| Grille horaire du classeur N3 (fenêtres CP/PeP/PoP) | ~4h45 à 5h par fenêtre |
| Cranes_conclusions.xlsx (ratio durée/heures grue) | 9h (cohérent avec la présentation Rebar) |

**Question à trancher :** quelle est la durée de poste retenue pour le
dimensionnement — et est-ce la même partout (coulée, ferraillage, logistique) ou
varie-t-elle par zone ?

*Zone concernée : Logistique (vue d'ensemble). Impact : critique.*

---

## Équipe Casting Team

**Sujet 1 : système de postes.** « No shift system in place » — le document
lui-même indique que le choix entre 3×8h et 2×12h n'est pas fait. Conditionne
directement la grille horaire du moteur de simulation, au même titre que la
question adressée à Olivier Bonnot ci-dessus — les deux sont peut-être la même
décision vue sous deux angles.

*Zone concernée : S (Casting Pit). Impact : critique.*

**Sujet 2 : pic d'effectif BC (Blue Collar) en Casting Pit.** Le moteur de
simulation (`tempo/moteur/charge.py`), en additionnant la charge BC de la zone S sur
les 5 lignes décalées, trouve un pic de **228 personnes simultanées** — environ le
double des **105 à 117** cités dans la présentation Casting Team. Deux explications
possibles, aucune vérifiée à ce stade :
- le moteur additionne toute la main-d'œuvre BC de la zone (coffrage compris), pas
  la seule équipe de coulée ;
- le chevauchement réel des 5 lignes le même jour (visible dans le Casting Pattern)
  est plus large que ce que « 105-117 » mesurait.

**Question à trancher :** quel périmètre couvre le chiffre « 105-117 » — permet de
savoir si l'écart est réel ou un artefact du moteur.

*Zone concernée : S (Casting Pit). Impact : élevé.*

---

## Valery Claise / Joanna — points de contact données

**Sujet 1 : segments N3 manquants, désaccord avec le suivi officiel.** Notre lecture
du classeur N3 (`tempo/comparer_n1_n3.py`) et le suivi officiel
(`Comparison_N1_shifts_to_target.xlsx`, onglet « N3 Overview (Missing) ») ne sont
presque pas d'accord :

| | Notre lecture | Suivi officiel |
|---|---|---|
| Walls (zone N) | S4, S5 manquants | S1/S3/S5/S7/S9 manquants (segments impairs) |
| Base Slab (zone O) | S5-S8 manquants | complet partout |
| LASCA (zone P) | S6-S8 manquants | non couvert par ce suivi (qui ne traite que BS/W/TS) |

**Question à trancher :** le classeur N3 a-t-il évolué depuis la version V0.1 que
nous avons lue, ou le critère de « manquant » diffère-t-il entre les deux lectures ?
Détermine où concentrer le chiffrage restant.

*Zones concernées : N, O, P. Impact : élevé.*

**Sujet 2 : ordre d'installation des murs.** Cité en réunion du 10/08 comme
B-C-A-D-E-F, mais la transcription automatique était très bruyante à cet endroit.

*Zone concernée : N. Impact : moyen.*

**Sujet 3 : correspondance planning MPP ↔ codes de zone N1/N3.** Le planning MS
Project de l'outfitting (`Tempo_full_schedule_linked_V4_70_jour.mpp`, 631 tâches
pour un seul élément) organise son détail par segment (S1 à S9) d'un élément, pas
par les codes OF1-OF5/SG (Outfitting Area) ou UB-S9/S8/S7 (Upper Basin) utilisés en
N1/N3. Les deux décrivent vraisemblablement les mêmes travaux vus sous deux
découpages différents, mais rien ne le confirme.

**Question à trancher :** existe-t-il une table de correspondance segment ↔ zone,
ou faut-il la construire ?

*Zones concernées : A, B, C, D, E, F, G, H, I. Impact : moyen.*

---

## Équipe TEMPO — arbitrage global

**Sujet : travail du week-end.** L'hypothèse de calage actuelle est « aucun travail
le week-end », mais quatre indices indépendants suggèrent un besoin réel :
- 4 samedis par cycle nécessaires pour les murs, d'après le calcul de la présentation
  Rebar ;
- « Still Sunday skidding in N1 staggering » (présentation Skidding) ;
- « S2 skidding in L4 are Sat. and casting is Monday. Works Sunday TO PREPARE? »
  (présentation Casting Team, question ouverte dans le document source lui-même) ;
- deux échantillons de planning ESS réel et daté (semaines du 27/04/2026 et du
  20/07/2026) montrent des livraisons effectivement programmées le samedi.

**Question à trancher :** le week-end est-il travaillé, et si oui selon quelles
règles (quelles équipes, quelle fréquence) ? C'est une hypothèse structurante pour
tout calage calendaire du simulateur.

*Zones concernées : N, S, Logistique. Impact : élevé.*

---

## Valery Claise

**Sujet 1 : nom et nombre de types de rack.** Trois désignations trouvées pour ce qui
pourrait être le même objet, ou pas : « mesh » / « ESS » (réunion du 10/08),
« White Rack » (MASTERVIEW.xlsm), « Yellow Rack » (LAYOUT_RF.pptx).

**Question à trancher :** combien de types de rack existent réellement, et quel nom
retenir pour chacun ?

*Zone concernée : Logistique. Impact : moyen.*

**Sujet 2 : les noms Lyon/Brest sont-ils des destinations réelles ?** Un fichier de
dimensionnement du stockage (`TOPICS_RISK_ANALYSIS_SUB_ELEMENT_SIZIING.xlsx`, feuille
MAX STORAGE) utilise « Lyon », « Toulouse », « Varsovie », « Cracovie », « Monaco »,
« Drogo » comme noms de zones de stockage sur site, aux côtés de « Sogod » — ce qui
suggère que ce sont des noms de code internes (sans rapport géographique réel), et
non les destinations effectives des camions comme nous l'avions d'abord supposé.

**Question à trancher :** confirmer si Lyon/Brest désignent des points de chargement
géographiquement réels, des zones de stockage nommées par convention, ou les deux
selon le contexte.

*Zone concernée : Logistique. Impact : moyen — structure toute la lecture des flux.*

---

## Équipe logistique

**Sujet 1 : nombre de camions à Lyon 2 et Brest 2.** Deux documents donnent des
totaux différents :

| Point de chargement | Detailed_Truck_Loading_Time.xlsx | Quantity_Designation_Surface.xlsx |
|---|---|---|
| Lyon 2 | 12 camions | 13 camions |
| Brest 2 | 14,5 camions | 12,5 camions |

Lyon 1, Lyon 3 et Brest 1 concordent entre les deux fichiers.

**Question à trancher :** quelle est la version à jour ?

*Zone concernée : Logistique. Impact : moyen.*

**Sujet 2 : risque n°1 du registre RF officiel.** Le registre de risques logistiques
(`TOPICS_RISK_ANALYSIS_SUB_ELEMENT_SIZIING.xlsx`, feuille RISK ANALYSIS) classe en
tête (score 50/25) le risque « plateformes insuffisantes pour l'approvisionnement
production », avec pour action préventive proposée un tampon de 3 à 5 remorques
supplémentaires — non encore chiffré ni validé.

**Question à trancher :** ce tampon est-il retenu, et sur quelle base le
dimensionner ? Sert directement à construire le module de replanification sur aléa
du simulateur.

*Zone concernée : Logistique. Impact : élevé.*

**Sujet 3 : nombre de places de parking remorques.** 13 dans
`TRAILER_CAPACITY.pptx` (une zone précise) contre 59 dans `LAYOUT_RF.pptx`
(« TOTAL ») — périmètres probablement différents, à confirmer.

*Zone concernée : Logistique. Impact : faible.*

---

## Lotte (pour WL) / équipe TEMPO (pour le reste)

**Sujet : codes de ressource non décodés.** GTA (27 affectations confirmées dans le
planning MS Project, nom complet inconnu), MSE (peut-être « MSI », orthographe à
confirmer), WL (le référentiel N3 lui-même note « ask Lotte »).

**Question à trancher :** décoder ces trois codes — n'affecte pas les calculs, gêne
seulement la lecture des tableaux.

*Zones concernées : toutes. Impact : faible.*

---

## Comment utiliser ce document

Chaque point est autoportant (contexte + sources + question), donc les sujets
peuvent être traités en réunions séparées par responsable, ou en une seule réunion
si tout le monde est disponible en même temps — les sujets « critique » (Olivier
Bonnot, Casting Team sur le système de postes) devraient passer en premier, les
autres en découlent partiellement.

À la clôture de chaque point, la réponse doit être reportée dans
`tempo/dossier_zones.py` (champ `statut` passé à `confirme`, contradiction retirée
ou requalifiée) pour que le schéma interactif reflète l'état réel — ce document n'est
qu'un instantané au 10/08/2026.
