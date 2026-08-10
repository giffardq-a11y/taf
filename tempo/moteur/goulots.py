"""Diagnostic de goulots d'étranglement : prend la charge agrégée construite par
`charge.construire_charge` et la caractérise ressource par ressource — pic, récurrence
du pic, lignes en cause — et, si une capacité est fournie, le dépassement. Répond
directement à deux des objectifs posés au départ du simulateur : détecter les goulots
d'étranglement, vérifier que la cadence retenue est tenable avec les ressources réelles.

    python3 -m tempo.moteur.goulots <n1.xlsx> <n3.xlsx> [--capacite BC=85] [--horizon 140]

Sans `--capacite`, le diagnostic reste descriptif (pic, récurrence) sans juger d'un
dépassement : aucun chiffre de dimensionnement n'est encore validé pour la plupart des
ressources (voir `tempo/dossier_zones.py`, `REGISTRE_VALIDATION`) — inventer une
capacité pour pouvoir conclure serait justement le genre de raccourci que ce dépôt
évite. `--capacite` reste disponible pour tester une hypothèse une fois qu'elle est
posée en réunion (ex. les 70 ou 85 BC cités pour l'équipe de coulée, contradictoires
entre eux, voir le registre de validation).
"""
import argparse
import math
import pathlib
import sys
from collections import defaultdict

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
from tempo.moteur.modele import Ressource


def statistiques_ressource(points, seuil_recurrence=0.8):
    """Caractérise une ressource à partir de ses points de charge : pic (valeur, jour,
    fenêtre, lignes en cause), moyenne, et récurrence — le nombre de points à au moins
    `seuil_recurrence` × le pic, pour distinguer un pic isolé d'une charge structurellement
    élevée (un pic qui revient toutes les semaines n'appelle pas la même réponse qu'un
    pic une fois sur 140 jours)."""
    points = sorted(points, key=lambda p: -p.demande)
    pic = points[0]
    lignes_au_pic = sorted({d[0] for d in pic.detail})
    seuil = seuil_recurrence * pic.demande
    recurrents = [p for p in points if p.demande >= seuil]
    moyenne = sum(p.demande for p in points) / len(points)
    return {
        'pic': pic.demande,
        'jour_pic': pic.jour_absolu,
        'fenetre_pic': pic.fenetre,
        'lignes_au_pic': lignes_au_pic,
        'moyenne': moyenne,
        'nb_points': len(points),
        'nb_points_recurrents': len(recurrents),
        'jours_recurrents': sorted({p.jour_absolu for p in recurrents}),
    }


def diagnostiquer(points, capacites=None, seuil_recurrence=0.8):
    """`points` : dict {(ressource, jour, fenetre): PointDeCharge}, comme renvoyé par
    `charge.construire_charge`. `capacites` : dict optionnel {code_ressource: Ressource}.
    Renvoie {ressource: {**statistiques_ressource(...), 'capacite':, 'depassement':,
    'nb_jours_depassement':}} — `capacite`/`depassement` restent `None` si aucune
    capacité n'est fournie pour cette ressource : un `None` n'est jamais un zéro déguisé."""
    par_ressource = defaultdict(list)
    for p in points.values():
        par_ressource[p.ressource].append(p)

    diagnostic = {}
    for ressource, pts in par_ressource.items():
        stats = statistiques_ressource(pts, seuil_recurrence)
        capacite = capacites.get(ressource) if capacites else None
        if capacite is not None and capacite.capacite is not None:
            stats['capacite'] = capacite.capacite
            stats['depassement'] = stats['pic'] - capacite.capacite
            stats['nb_jours_depassement'] = sum(1 for p in pts if p.demande > capacite.capacite)
        else:
            stats['capacite'] = None
            stats['depassement'] = None
            stats['nb_jours_depassement'] = None
        diagnostic[ressource] = stats
    return diagnostic


def equipes_tournantes(duree_poste_h, amplitude_h=24.0):
    """Nombre minimal d'équipes qui se relaient pour couvrir `amplitude_h` d'affilée
    avec des postes de `duree_poste_h` chacun — un simple plafond (arrondi supérieur),
    pas une règle sociale (repos, jours fériés...) : juste la contrainte arithmétique
    la plus basique. Sert à chiffrer, pour chaque hypothèse de durée de poste encore en
    débat (voir `tempo/dossier_zones.py`), combien d'équipes distinctes ça impose —
    un argument concret pour la réunion de conciliation, pas une réponse à sa place."""
    return math.ceil(amplitude_h / duree_poste_h)


def tableau_scenarios_poste(amplitude_h=24.0, durees=(8, 9, 10, 12)):
    """Le classeur N3 tuile ses fenêtres horaires (CP/PeP : 5 fenêtres ~5h ; PoP :
    4 fenêtres de 6h) sur la totalité des 24h de la journée — la production tourne en
    continu, quelle que soit la durée de poste retenue. Ce que la durée de poste change,
    c'est le nombre d'équipes distinctes nécessaires pour couvrir ces 24h."""
    return {d: equipes_tournantes(d, amplitude_h) for d in durees}


def _parse_capacites(valeurs):
    capacites = {}
    for v in valeurs or []:
        code, _, valeur = v.partition('=')
        if not valeur:
            raise ValueError(f"--capacite attend CODE=VALEUR, reçu {v!r}")
        capacites[code] = Ressource(code=code, capacite=float(valeur))
    return capacites


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('n1')
    ap.add_argument('n3')
    ap.add_argument('--horizon', type=int, default=140, help='jours simulés (défaut 140)')
    ap.add_argument('--capacite', action='append',
                     help="CODE=VALEUR, répétable (ex. --capacite BC=85 --capacite BC=70 "
                          "pour comparer les deux chiffres contradictoires du registre de "
                          "validation — un seul par code, le dernier écrase le précédent)")
    ap.add_argument('--seuil-recurrence', type=float, default=0.8,
                     help='fraction du pic au-delà de laquelle un jour compte comme récurrent (défaut 0.8)')
    args = ap.parse_args()

    import warnings
    warnings.filterwarnings('ignore', module='openpyxl')
    from openpyxl import load_workbook
    from tempo.lire_tempo import lire_n1, lire_taches_n3
    from tempo.moteur.charge import construire_charge, params_depuis_n1

    wb1 = load_workbook(args.n1, data_only=True)
    feuille_n1 = sorted([n for n in wb1.sheetnames if '5 Lines' in n])[-1]
    n1 = lire_n1(args.n1, feuille_n1)
    params = params_depuis_n1(n1)
    taches, charges = lire_taches_n3(args.n3)
    points = construire_charge(taches, charges, params, args.horizon)

    capacites = _parse_capacites(args.capacite)
    diagnostic = diagnostiquer(points, capacites, args.seuil_recurrence)

    def criticite(item):
        _, stats = item
        if stats['depassement'] is not None:
            return (1, stats['depassement'])
        return (0, stats['pic'])

    print(f"Diagnostic sur {len(diagnostic)} ressource(s), horizon {args.horizon} jours "
          f"({params.demarrage_tempo}).\n")
    for ressource, stats in sorted(diagnostic.items(), key=criticite, reverse=True):
        entete = f"=== {ressource} — pic {stats['pic']:.1f} au jour {stats['jour_pic']}"
        if stats['capacite'] is not None:
            marque = "DÉPASSEMENT" if stats['depassement'] > 0 else "dans la capacité"
            entete += f", capacité {stats['capacite']:.0f} ({marque}, écart {stats['depassement']:+.1f})"
        entete += " ==="
        print(entete)
        print(f"  fenêtre du pic : {stats['fenetre_pic']}  |  lignes au pic : "
              f"{', '.join(stats['lignes_au_pic'])}")
        print(f"  moyenne sur {stats['nb_points']} points de charge : {stats['moyenne']:.1f}  |  "
              f"{stats['nb_points_recurrents']} points ≥ {args.seuil_recurrence*100:.0f}% du pic "
              f"({len(stats['jours_recurrents'])} jours distincts)")
        if stats['nb_jours_depassement'] is not None:
            print(f"  jours en dépassement de capacité : {stats['nb_jours_depassement']}")
        print()

    print("--- Impact de la durée de poste non tranchée (registre de validation) ---")
    print("Les fenêtres N3 tuilent les 24h de la journée (production continue) : ce que")
    print("change la durée de poste, c'est le nombre d'équipes distinctes nécessaires.\n")
    for duree, nb in sorted(tableau_scenarios_poste().items()):
        print(f"  poste de {duree:>2}h  ->  {nb} équipe(s) tournante(s) pour couvrir 24h")


if __name__ == '__main__':
    main()
