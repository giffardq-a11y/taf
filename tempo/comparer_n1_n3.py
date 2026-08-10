"""Rapproche le calage haut niveau (N1, postes par segment et par catégorie) du détail
tâche par tâche (N3), pour vérifier — ou mettre en doute — le lien décrit dans
`tempo/DONNEES.md` §2.

    python3 tempo/comparer_n1_n3.py General_Tempo_Staggering.xlsx STE__TEMPO__N3_Takt_Plan__V0_1.xlsx

Ce que ce script NE prétend PAS faire : un rapprochement chiffré exact. Les tâches N3
d'une zone ne sont pas organisées par segment — chaque zone couvre une plage de jours
tempo (Ti) continue, pendant laquelle des tâches de plusieurs segments s'enchaînent ou se
chevauchent (LASCA, par exemple, est active de T5 à T35, largement plus large qu'un seul
segment). Convertir un nombre de jours tempo occupés en « postes » suppose de savoir
combien de postes tient un jour tempo — 2, generalement, mais ce n'est pas garanti partout
(cf. la grille à 5 fenêtres de la zone CP contre les 4 fenêtres de la zone PoP).

Ce que ce script fait, plus modestement : pour chaque catégorie N1 (Walls, BS, LASCA,
Buffer, CP), reportée sur sa zone N3 correspondante (référentiel `Data`, colonne UNIT),
il compare la **forme** du profil par segment — où N1 dit qu'un segment demande plus de
postes qu'un autre, N3 doit montrer, sur ce même segment, plus de tâches et plus
d'heures-homme. Une divergence de forme est un signal à vérifier ; une concordance de
forme est un repère de cohérence, pas une preuve d'exactitude.
"""
import argparse
import sys
from collections import defaultdict

from lire_tempo import lire_n1, lire_taches_n3

# Catégorie N1 -> code de zone N3 (référentiel `Data`, colonne UNIT — cf. DONNEES.md §2).
ZONE_PAR_CATEGORIE = {'walls': 'N', 'bs': 'O', 'lasca': 'P', 'buffer': 'Q', 'cp': 'S'}


def _duree_fenetre_h(fenetre):
    if not fenetre:
        return 0
    debut, fin = fenetre
    return (fin - debut) if fin >= debut else (24 - debut + fin)


def profil_n3_par_segment(taches, charges, zone):
    """{segment: {'taches': n, 'heures_homme': h, 'jours_tempo': {Ti,...}}} pour une zone."""
    par_ligne_excel = {(t['feuille'], t['ligne_excel']): t for t in taches}
    profil = defaultdict(lambda: {'taches': set(), 'heures_homme': 0.0, 'jours_tempo': set()})
    for c in charges:
        if c['zone'] != zone or c['jalon']:
            continue
        t = par_ligne_excel.get((c['feuille'], c['ligne_excel']))
        seg = t['segment'] if t else None
        if not seg or not seg.startswith('S') or not seg[1:].isdigit():
            continue
        p = profil[seg]
        p['taches'].add((c['feuille'], c['ligne_excel']))
        p['heures_homme'] += (c['effectif'] or 0) * _duree_fenetre_h(c['fenetre'])
        if c['tempo'] is not None:
            p['jours_tempo'].add(c['tempo'])
    return {seg: {'taches': len(v['taches']), 'heures_homme': round(v['heures_homme'], 1),
                  'jours_tempo': len(v['jours_tempo'])}
            for seg, v in profil.items()}


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('n1')
    ap.add_argument('n3')
    ap.add_argument('--feuille-n1', default=None)
    args = ap.parse_args()

    taches, charges = lire_taches_n3(args.n3)

    from openpyxl import load_workbook
    import warnings
    warnings.filterwarnings('ignore', module='openpyxl')
    wb1 = load_workbook(args.n1, data_only=True)
    feuille_n1 = args.feuille_n1 or sorted([n for n in wb1.sheetnames if '5 Lines' in n])[-1]
    n1 = lire_n1(args.n1, feuille_n1)

    profils_zone = {cat: profil_n3_par_segment(taches, charges, zone)
                     for cat, zone in ZONE_PAR_CATEGORIE.items()}

    # Le classeur N3 décrit un élément générique (colonne Élément = En/En-1/En+1) : sa
    # décomposition en tâches ne varie pas d'une ligne à l'autre. Seul le calage N1
    # (postes par segment) diffère ligne par ligne — inutile de réafficher 5 fois le même
    # profil N3 ; on le montre une fois, puis on compare chaque ligne dessus.
    print("Profil N3 par catégorie et segment (identique pour les 5 lignes, l'élément N3 "
          "n'est pas rattaché à une ligne) :")
    trous = []
    for cle, zone in ZONE_PAR_CATEGORIE.items():
        profil = profils_zone[cle]
        total_taches = sum(p['taches'] for p in profil.values())
        total_h = round(sum(p['heures_homme'] for p in profil.values()))
        print(f"\n  {cle.upper():8s} (zone {zone}) — {total_taches} tâches, {total_h} h-homme au total")
        for i in range(1, 10):
            seg = f'S{i}'
            p = profil.get(seg, {'taches': 0, 'heures_homme': 0, 'jours_tempo': 0})
            marque = '  <-- aucune tâche N3 détaillée pour ce segment' if p['taches'] == 0 else ''
            if p['taches'] == 0:
                trous.append((cle.upper(), seg))
            print(f"    {seg}: {p['taches']:>4} tâches, {p['heures_homme']:>7.0f} h-homme, "
                  f"{p['jours_tempo']:>2} jours tempo touchés{marque}")

    print(f"\n\nComparaison avec les postes N1 (par ligne), pour repère — les deux ne sont "
          f"PAS dans la même unité (postes vs heures-homme), cf. l'en-tête du script :")
    for e in sorted(n1, key=lambda e: (e['ligne'], e['categorie'])):
        cle = e['categorie'].strip().lower()
        if cle not in ZONE_PAR_CATEGORIE:
            continue
        print(f"  {e['ligne']:22s} {e['categorie']:8s} postes/segment={e['segments']}")

    if trous:
        print(f"\n\n{len(trous)} combinaison(s) catégorie×segment sans aucune tâche détaillée "
              f"dans le classeur N3 (cohérent avec son statut « V0.1, encore en cours » — "
              f"cf. la présentation Rebar : « Takt N3 still ongoing ») :")
        for cat, seg in trous:
            print(f"    {cat} {seg}")


if __name__ == '__main__':
    main()
