"""Charge logistique (camions/plateformes), construite depuis `MASTERVIEW.xlsm`, sur le
même modèle (`PointDeCharge`) que la charge de main-d'œuvre — répond à l'objectif
« prévoir la logistique : déplacements des camions, stockage, livraisons » posé au
départ du simulateur.

Différence importante avec `charge.py` : ici la donnée est calée sur de VRAIES dates
calendaires dès le départ (`DeliveryPlan.date_retenue`), pas sur un jour tempo relatif
à calibrer via `ParametresCalage` — c'est la ressource la mieux ancrée du moteur
aujourd'hui, alors même que le calage calendaire de la main-d'œuvre reste un point
ouvert (`tempo/dossier_zones.py`, contradiction sur l'ordre des lignes en date de
livraison). Les deux parties du moteur ne partagent donc pas encore le même axe
temporel — à unifier le jour où l'une des deux hypothèses de `ParametresCalage` est
confirmée.

    python3 -m tempo.moteur.logistique MASTERVIEW.xlsm [--par lieu_livraison|lignes]
"""
import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
from tempo.moteur.modele import PointDeCharge
from tempo.moteur.goulots import statistiques_ressource

# Cycle logistique moyen mesuré par GPS (SENSOLUS), déjà noté dans
# tempo/dossier_zones.py (LOGISTIQUE) : ~3h40 aller-retour pour le flux Stock->Halls,
# et un cycle détaillé (chargement + transport + attente + déchargement + retour)
# d'environ 4h40 pour le flux RF (TOPICS_RISK_ANALYSIS, feuille NUMBER PLATFORM,
# 40+10+180+40+10 = 280 min). Deux chiffres différents pour deux flux différents —
# aucun n'est utilisé comme constante de calcul ici, seulement rappelé en commentaire
# pour situer les livraisons/jour trouvées ci-dessous.
LIVRAISONS_PAR_PLATEFORME_JOUR = 3.5  # milieu de la fourchette « 3 à 4 » citée dans
                                       # TOPICS_RISK_ANALYSIS_SUB_ELEMENT_SIZIING.xlsx


def charge_livraisons(livraisons, groupe_par='lieu_livraison'):
    """Une `PointDeCharge` par (groupe, jour civil réel) — la demande est le nombre de
    livraisons ce jour-là. `date_retenue` sert de date, tronquée au jour (l'heure n'est
    pas assez fiable pour distinguer un vrai pic d'un simple étalement dans la journée,
    cf. tempo/DONNEES.md). `jour_absolu` porte ici un vrai `datetime.date`, pas un
    entier relatif — voir la note de module ci-dessus."""
    points = {}
    for liv in livraisons:
        date = liv.get('date_retenue')
        if not hasattr(date, 'date'):
            continue
        jour = date.date()
        groupe = liv.get(groupe_par) or 'NC'
        ressource = f"livraisons/{groupe}"
        cle = (ressource, jour)
        if cle not in points:
            points[cle] = PointDeCharge(ressource=ressource, jour_absolu=jour, fenetre=None, demande=0)
        p = points[cle]
        p.demande += 1
        p.detail.append((str(liv.get('lignes') or '?'),
                          f"{liv.get('segment')}/{liv.get('designation')}/{liv.get('evenement')}", 1))
    return points


def charge_livraisons_toutes(livraisons):
    """Même chose, tous groupes confondus — pour lire directement le nombre de
    livraisons sitewide par jour, à comparer au dimensionnement de flotte retenu
    (24 plateformes, cf. tempo/dossier_zones.py, LOGISTIQUE)."""
    points = {}
    for liv in livraisons:
        date = liv.get('date_retenue')
        if not hasattr(date, 'date'):
            continue
        jour = date.date()
        cle = ('livraisons/TOUTES', jour)
        if cle not in points:
            points[cle] = PointDeCharge(ressource='livraisons/TOUTES', jour_absolu=jour, fenetre=None, demande=0)
        points[cle].demande += 1
    return points


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('masterview')
    ap.add_argument('--par', default='lieu_livraison', choices=['lieu_livraison', 'lignes'],
                     help="regroupement (défaut lieu_livraison)")
    ap.add_argument('--top', type=int, default=10)
    args = ap.parse_args()

    from tempo.lire_masterview import lire_livraisons
    livraisons = lire_livraisons(args.masterview)
    print(f"{len(livraisons)} livraisons lues (DeliveryPlan).")

    points_groupe = charge_livraisons(livraisons, args.par)
    from collections import defaultdict
    par_ressource = defaultdict(list)
    for p in points_groupe.values():
        par_ressource[p.ressource].append(p)

    print(f"\n--- Pics de livraisons/jour, par {args.par} ---")
    for ressource, pts in sorted(par_ressource.items(), key=lambda kv: -max(p.demande for p in kv[1])):
        stats = statistiques_ressource(pts)
        print(f"  {ressource:<24}  pic {stats['pic']:.0f}/j le {stats['jour_pic']}  |  "
              f"moyenne {stats['moyenne']:.1f}/j sur {stats['nb_points']} jours avec livraison")

    points_total = charge_livraisons_toutes(livraisons)
    pts = list(points_total.values())
    stats = statistiques_ressource(pts)
    plateformes_estimees = stats['pic'] / LIVRAISONS_PAR_PLATEFORME_JOUR
    print(f"\n--- Sitewide, tous groupes confondus ---")
    print(f"pic {stats['pic']:.0f} livraisons le {stats['jour_pic']}, moyenne "
          f"{stats['moyenne']:.1f}/j sur {stats['nb_points']} jours avec au moins une livraison.")
    print(f"À raison de {LIVRAISONS_PAR_PLATEFORME_JOUR} livraisons/plateforme/jour (milieu de la "
          f"fourchette citée dans TOPICS_RISK_ANALYSIS_SUB_ELEMENT_SIZIING.xlsx), le pic observé "
          f"correspondrait à environ {plateformes_estimees:.0f} plateformes simultanées — à comparer "
          f"aux 24 plateformes recommandées dans TRAILER_QUANTITY_PER_FLOW.xlsx (flux Stock->Halls "
          f"seulement, périmètre plus étroit que ce calcul sitewide — pas directement comparable, "
          f"affiché à titre indicatif).")


if __name__ == '__main__':
    main()
