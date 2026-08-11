"""Classes de données du moteur. Rien ici n'exécute de calcul — c'est le vocabulaire
commun sur lequel `charge.py` et `goulots.py` s'appuient, construit pour rester valable
quelle que soit la réponse aux points encore ouverts (`tempo/DONNEES.md` §4) : le temps
se compte en heures continues, jamais en « postes », et une ressource peut aussi bien
être un ouvrier qu'un camion — le type ne change rien à la mécanique.
"""
from dataclasses import dataclass, field


@dataclass
class Tache:
    """Une tâche telle que lue dans une feuille N3 (`lire_tempo.lire_taches_n3`), avec
    sa charge en ressource. Le temps reste relatif au jour tempo de la ligne qui la
    porte — c'est `charge.py` qui le convertit en jour calendaire absolu."""
    feuille: str
    ligne_excel: int
    zone: str
    segment: str | None
    etape: str | None
    equipe: str | None
    nom: str | None
    ressource: str | None       # type de ressource (BC, GTA, Dywidag...) — Type of Ressources
    sous_equipe: str | None
    jour_tempo_relatif: int     # Ti tel que lu dans la feuille (relatif au parcours de CET élément)
    fenetre: tuple[float, float]  # (début, fin) en heure du jour, cf. lire_tempo._plage_fenetre
    tampon: bool                # fenêtre marquée OT (hors tempo) : à n'utiliser qu'en dernier recours
    effectif: float | None      # None si la case est un jalon ('x'), pas une charge chiffrée
    jalon: bool


@dataclass
class Ressource:
    """Une réserve partagée — main-d'œuvre ou matériel — consommée par les tâches qui la
    citent en `Tache.ressource`. `capacite` est le nombre d'unités simultanément
    disponibles ; None tant qu'elle n'est pas connue (le moteur peut alors mesurer la
    demande sans juger si elle dépasse quoi que ce soit — utile avant d'avoir un chiffre
    de dimensionnement à comparer)."""
    code: str
    nom: str = ''
    capacite: float | None = None


@dataclass
class ParametresCalage:
    """Les deux hypothèses de reconstitution du calendrier absolu, posées en
    `tempo/moteur/ARCHITECTURE.md` — des paramètres, pas des constantes : à corriger dès
    qu'une réponse arrive de Valery/Joanna, sans toucher au reste du moteur.

    `demarrage_tempo` : jour tempo absolu (Ti) où chaque ligne démarre son cycle, lu
    directement dans le classeur N1 (`lire_n1(...)['demarrage']`, ex. « L4 - T25 » -> 25).
    `periode_relance_jours` : nombre de jours tempo entre deux éléments consécutifs sur
    une même ligne — 7 par défaut (« 5 castings per week », une coulée par ligne et par
    semaine, `Casting Pattern` du classeur N1).
    """
    demarrage_tempo: dict[str, int]
    periode_relance_jours: int = 7


@dataclass
class PointDeCharge:
    """La demande cumulée d'une ressource, sur une fenêtre horaire d'un jour calendaire
    absolu donné, avec le détail de ce qui la compose — jamais un total nu : un goulot
    sans ses causes ne se corrige pas."""
    ressource: str
    jour_absolu: int
    fenetre: tuple[float, float] | None
    demande: float
    detail: list[tuple[str, str, float]] = field(default_factory=list)  # (ligne, tache, quantité)
