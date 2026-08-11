"""Courbes de main-d'œuvre dans le temps, par zone et globale — pour le schéma
interactif (`tempo_zones.html`). S'appuie sur `charge.construire_charge`, donc sur le
même jour tempo relatif (pas encore calé sur une date calendaire réelle, cf.
`tempo/moteur/ARCHITECTURE.md`) : l'axe des courbes reste « jour tempo », pas une date.

Méthode retenue pour passer d'une charge par (ressource, jour, fenêtre) à une seule
valeur par jour (une « courbe ») : pour chaque jour, on additionne d'abord toutes les
ressources actives sur une même fenêtre horaire (ce sont des types de main-d'œuvre
différents, présents en même temps), puis on garde la fenêtre la plus chargée du jour
— l'effectif au plus fort de la journée, pas une moyenne qui lisserait les pics.
Approximation assumée pour la courbe « globale » (toutes zones) : la somme, jour par
jour, du pic de chaque zone — correcte si les zones sont vraiment des lieux physiques
distincts (donc leurs effectifs s'additionnent), mais surestime légèrement si le pic
d'une zone donnée ne tombe pas exactement à la même heure que celui d'une autre zone
le même jour (le calcul ne regarde plus l'heure une fois par zone).

    python3 -m tempo.moteur.courbes <n1.xlsx> <n3.xlsx> [--horizon 140]
"""
import argparse
import pathlib
import sys
from collections import defaultdict

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))


def courbe_zone(taches, charges, params, zone, horizon_jours=140):
    """Renvoie {jour_absolu: effectif_pic_du_jour} pour une seule zone — toutes
    ressources et toutes lignes confondues, fenêtre la plus chargée du jour."""
    from tempo.moteur.charge import construire_charge

    charges_zone = [c for c in charges if c['zone'] == zone]
    if not charges_zone:
        return {}
    points = construire_charge(taches, charges_zone, params, horizon_jours)

    par_jour_fenetre = defaultdict(lambda: defaultdict(float))
    for p in points.values():
        par_jour_fenetre[p.jour_absolu][p.fenetre] += p.demande

    return {jour: max(par_fenetre.values()) for jour, par_fenetre in par_jour_fenetre.items()}


def courbes_toutes_zones(taches, charges, params, zones, horizon_jours=140):
    """{zone: {jour: effectif}} pour chaque zone de `zones`, plus une entrée 'GLOBAL'
    qui est la somme jour par jour des courbes par zone (voir la réserve dans la
    docstring du module).

    ATTENTION — `zone` ici est le code lettre lu en colonne A de chaque feuille N3
    (« TEMPO » dans l'en-tête du classeur), PAS la colonne UNIT. Un contrôle croisé
    (voir `tempo/dossier_zones.py`, REGISTRE_VALIDATION, point critique ajouté le
    10/08/2026) a montré que ce code lettre ne correspond PAS de façon fiable à
    l'aire physique déclarée dans la feuille `Data` du classeur (ex. la lettre M est
    censée désigner « Panel Factory », mais aucune tâche du classeur n'est jamais
    étiquetée UNIT=« Panel Factory » ; la plupart des tâches des feuilles *__M sont en
    réalité étiquetées UNIT=« Casting Pit »). Préférer `courbes_par_unite` ci-dessous
    pour une courbe fiable par aire physique — cette fonction reste disponible pour
    reproduire les calculs déjà publiés (goulots BC en "zone S", etc.), pas pour de
    nouvelles courbes présentées comme fiables par aire."""
    par_zone = {}
    for zone in zones:
        c = courbe_zone(taches, charges, params, zone, horizon_jours)
        if c:
            par_zone[zone] = c

    global_ = defaultdict(float)
    for c in par_zone.values():
        for jour, effectif in c.items():
            global_[jour] += effectif
    par_zone['GLOBAL'] = dict(global_)
    return par_zone


def _points_par_unite(taches, charges, params, horizon_jours=140):
    from tempo.moteur.modele import PointDeCharge

    par_cle = {(t['feuille'], t['ligne_excel']): t for t in taches}
    points = {}
    for ligne, demarrage in params.demarrage_tempo.items():
        nb_elements = max(1, horizon_jours // params.periode_relance_jours)
        for indice in range(nb_elements):
            offset = demarrage + indice * params.periode_relance_jours - 1
            for c in charges:
                if c['jalon'] or not c['effectif'] or c['tempo'] is None:
                    continue
                t = par_cle.get((c['feuille'], c['ligne_excel']))
                unite = (t and t.get('unite')) or 'NC (unité non renseignée)'
                jour_absolu = offset + c['tempo']
                cle = (unite, jour_absolu, c['fenetre'])
                if cle not in points:
                    points[cle] = PointDeCharge(ressource=unite, jour_absolu=jour_absolu,
                                                 fenetre=c['fenetre'], demande=0)
                points[cle].demande += c['effectif']
    return points


def courbes_par_unite(taches, charges, params, horizon_jours=140):
    """Même principe que `courbes_toutes_zones`, mais regroupé par la colonne UNIT de
    chaque tâche (l'aire/le process physiquement déclaré ligne par ligne) plutôt que
    par le code lettre de la feuille — l'axe fiable, voir la mise en garde ci-dessus.
    Renvoie {unite: {jour: effectif}} plus 'GLOBAL'."""
    points = _points_par_unite(taches, charges, params, horizon_jours)
    par_jour_fenetre = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
    for p in points.values():
        par_jour_fenetre[p.ressource][p.jour_absolu][p.fenetre] += p.demande

    par_unite = {}
    for unite, par_jour in par_jour_fenetre.items():
        par_unite[unite] = {jour: max(par_fenetre.values()) for jour, par_fenetre in par_jour.items()}

    global_ = defaultdict(float)
    for c in par_unite.values():
        for jour, effectif in c.items():
            global_[jour] += effectif
    par_unite['GLOBAL'] = dict(global_)
    return par_unite


def _recouvrement(debut, fin, borne_debut, borne_fin):
    """Heures de recouvrement entre [debut, fin) et [borne_debut, borne_fin), sans
    wraparound — utilisé par `_repartir_par_shift` après découpage des fenêtres qui
    traversent minuit."""
    return max(0.0, min(fin, borne_fin) - max(debut, borne_debut))


def _shift_dominant(fenetre, duree_shift_h=12):
    """Renvoie l'indice de shift (0, 1, ... `24/duree_shift_h - 1`) où une fenêtre
    horaire (debut, fin) passe le plus de temps — les fenêtres qui traversent minuit
    (ex. (21.0, 1.75)) sont découpées en deux segments avant comparaison. Une fenêtre
    à cheval entre deux shifts est donc rattachée à celui où elle passe la majorité de
    son temps, pas la moyenne des deux."""
    debut, fin = fenetre
    segments = [(debut, 24.0), (0.0, fin)] if fin <= debut else [(debut, fin)]
    nb_shifts = max(1, round(24 / duree_shift_h))
    bornes = [(i * duree_shift_h, (i + 1) * duree_shift_h) for i in range(nb_shifts)]
    recouvrements = [sum(_recouvrement(d, f, b0, b1) for d, f in segments) for b0, b1 in bornes]
    return max(range(nb_shifts), key=lambda i: recouvrements[i])


def courbes_par_unite_par_shift(taches, charges, params, horizon_jours=140, duree_shift_h=12):
    """Comme `courbes_par_unite`, mais la valeur par jour est éclatée en shifts de
    `duree_shift_h` heures (2 shifts de 12h par défaut, hypothèse « pour le moment »)
    au lieu d'un seul point par jour — chaque fenêtre horaire N3 est rattachée au
    shift où elle passe le plus de temps (voir `_shift_dominant`). Clé renvoyée :
    (jour_absolu, indice_shift), triable directement (tuple). Les phases A-I et M-L
    partagent le même axe temporel par ligne (le même `offset` dans
    `construire_charge`) — pas de recalage supplémentaire nécessaire pour les rendre
    concurrentes, elles le sont déjà dans le moteur."""
    points = _points_par_unite(taches, charges, params, horizon_jours)
    par_unite_shift = defaultdict(lambda: defaultdict(float))
    for p in points.values():
        shift = _shift_dominant(p.fenetre, duree_shift_h) if p.fenetre else 0
        par_unite_shift[p.ressource][(p.jour_absolu, shift)] += p.demande

    par_unite = {u: dict(d) for u, d in par_unite_shift.items()}
    global_ = defaultdict(float)
    for c in par_unite.values():
        for cle, effectif in c.items():
            global_[cle] += effectif
    par_unite['GLOBAL'] = dict(global_)
    return par_unite


def courbes_par_aire_par_shift(courbes_unite_shift, aire_par_zone):
    """Regroupe des courbes par-zone-par-shift (ex. la sortie de
    `courbes_par_unite_par_shift`) en courbes par AIRE (Panel Factory, Rebar Hall,
    Production Hall, Curing Hall, Outfitting Area, Upper Basin), en sommant les zones
    qui appartiennent à la même aire — `aire_par_zone` : {nom_zone: nom_aire}, tel que
    fourni par `tempo.dossier_zones.ZONES_REELLES[...]['aire']`."""
    par_aire = defaultdict(lambda: defaultdict(float))
    for zone, courbe in courbes_unite_shift.items():
        if zone == 'GLOBAL':
            continue
        aire = aire_par_zone.get(zone)
        if not aire:
            continue
        for cle, effectif in courbe.items():
            par_aire[aire][cle] += effectif
    return {aire: dict(c) for aire, c in par_aire.items()}


def _heures_grue_numerique(tache):
    v = tache.get('heures_grue')
    return v if isinstance(v, (int, float)) else None


def courbes_grue_par_unite_par_shift(taches, charges, params, horizon_jours=140, duree_shift_h=12):
    """Charge grue par zone et par shift, en heures — même principe temporel que
    `courbes_par_unite_par_shift`, mais sur `Tache.heures_grue` plutôt que sur
    l'effectif. Donnée nettement plus incomplète que la main-d'œuvre : seules 185 des
    3243 tâches du classeur portent un `heures_grue` numérique (le champ contient
    parfois du texte), et seulement pour les phases M à L (aucune pour A à I) — les
    zones sans grue documentée n'apparaissent tout simplement pas ici, ce n'est pas
    forcément qu'aucune grue n'y est utilisée.

    `heures_grue` est une donnée par TÂCHE (pas par fenêtre horaire) ; en l'absence
    d'une répartition explicite par fenêtre, elle est divisée à parts égales entre les
    fenêtres non vides de la tâche — une hypothèse de calcul, pas une lecture directe,
    à traiter comme telle."""
    from tempo.moteur.modele import PointDeCharge

    par_cle = {(t['feuille'], t['ligne_excel']): t for t in taches}
    nb_fenetres_par_tache = defaultdict(int)
    for c in charges:
        if not c['jalon'] and c['effectif'] and c['tempo'] is not None:
            nb_fenetres_par_tache[(c['feuille'], c['ligne_excel'])] += 1

    points = {}
    for ligne, demarrage in params.demarrage_tempo.items():
        nb_elements = max(1, horizon_jours // params.periode_relance_jours)
        for indice in range(nb_elements):
            offset = demarrage + indice * params.periode_relance_jours - 1
            for c in charges:
                if c['jalon'] or not c['effectif'] or c['tempo'] is None:
                    continue
                cle_tache = (c['feuille'], c['ligne_excel'])
                t = par_cle.get(cle_tache)
                if not t:
                    continue
                hg = _heures_grue_numerique(t)
                if hg is None:
                    continue
                nb_fenetres = nb_fenetres_par_tache.get(cle_tache, 1) or 1
                unite = t.get('unite') or 'NC (unité non renseignée)'
                jour_absolu = offset + c['tempo']
                shift = _shift_dominant(c['fenetre'], duree_shift_h) if c['fenetre'] else 0
                cle = (unite, jour_absolu, shift)
                if cle not in points:
                    points[cle] = 0.0
                points[cle] += hg / nb_fenetres

    par_unite = defaultdict(dict)
    for (unite, jour, shift), heures in points.items():
        par_unite[unite][(jour, shift)] = heures
    return dict(par_unite)


def utilisation_grue_pct(courbe_heures_grue, nb_grues=1, duree_shift_h=12):
    """Convertit une courbe d'heures-grue par (jour, shift) en pourcentage
    d'utilisation, sur la base de `nb_grues` grues disponibles pendant tout le shift —
    capacité = nb_grues x duree_shift_h. `nb_grues` par défaut à 1 : à corriger zone
    par zone dès qu'un chiffre de dimensionnement grue existe (cf.
    tempo/dossier_zones.py — 1,5 pour Base Slab, 2 pour Top Slab, 1 pour un mur...)."""
    capacite = max(0.001, nb_grues * duree_shift_h)
    return {cle: min(999.0, heures / capacite * 100) for cle, heures in courbe_heures_grue.items()}


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('n1')
    ap.add_argument('n3')
    ap.add_argument('--horizon', type=int, default=140)
    args = ap.parse_args()

    import warnings
    warnings.filterwarnings('ignore', module='openpyxl')
    from openpyxl import load_workbook
    from tempo.lire_tempo import lire_n1, lire_taches_n3
    from tempo.moteur.charge import params_depuis_n1

    wb1 = load_workbook(args.n1, data_only=True)
    feuille_n1 = sorted([n for n in wb1.sheetnames if '5 Lines' in n])[-1]
    n1 = lire_n1(args.n1, feuille_n1)
    params = params_depuis_n1(n1)
    taches, charges = lire_taches_n3(args.n3)

    zones = sorted({c['zone'] for c in charges if c['zone']})
    courbes = courbes_toutes_zones(taches, charges, params, zones, args.horizon)

    for zone, c in sorted(courbes.items(), key=lambda kv: -max(kv[1].values()) if kv[1] else 0):
        if not c:
            continue
        pic_jour = max(c, key=c.get)
        print(f"{zone:<8} pic {c[pic_jour]:.1f} au jour {pic_jour}  |  {len(c)} jours avec charge  |  "
              f"moyenne {sum(c.values())/len(c):.1f}")


if __name__ == '__main__':
    main()
