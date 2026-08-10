"""Lit un fichier MS Project (.mpp) et en tire les affectations de ressources, jour par
jour — de quoi tracer comment un effectif varie dans le temps, à partir d'un vrai
planning daté plutôt que du gabarit générique N3 (qui ne porte aucune date calendaire
propre, cf. `tempo/DONNEES.md`).

    python3 tempo/lire_mpp.py Tempo_full_schedule_linked_V4_70_jour.mpp

Le format .mpp est binaire et propriétaire (Microsoft Project) ; il n'existe pas de
lecteur Python natif fiable. Ce module s'appuie sur **MPXJ** (bibliothèque Java,
paquet PyPI `mpxj`, exécutée via `jpype` — nécessite un JDK). Si l'un des deux manque,
l'erreur le dit explicitement plutôt que de laisser un `ImportError` nu remonter d'un
module tiers.

Attention aux noms de paquets Java : les versions récentes de MPXJ ont renommé leurs
classes de `net.sf.mpxj.*` vers `org.mpxj.*`. Ce module cible `org.mpxj` ; un fichier
lu avec un MPXJ plus ancien pourra nécessiter d'ajuster ce préfixe.
"""
import argparse
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta


def _demarrer_mpxj():
    try:
        import mpxj
        import jpype
    except ImportError as e:
        raise SystemExit(
            "Lecture d'un .mpp : nécessite les paquets Python `mpxj` et `jpype1` "
            "(pip install mpxj jpype1), et un JDK installé sur la machine. "
            f"Import manquant : {e}"
        )
    if not jpype.isJVMStarted():
        jpype.startJVM(classpath=mpxj.getClassPath())
    return jpype


def lire_affectations(chemin_mpp):
    """Renvoie une liste de {tache, ressource, type_ressource, unites_pct, debut, fin}
    — une entrée par affectation ressource × tâche, telle que MS Project la porte.
    `unites_pct` est le pourcentage d'affectation MS Project (100 = une personne à
    temps plein sur la période ; 200 = deux personnes, etc. — c'est la convention
    MS Project, pas une nôtre)."""
    jpype = _demarrer_mpxj()
    UniversalProjectReader = jpype.JClass('org.mpxj.reader.UniversalProjectReader')
    projet = UniversalProjectReader().read(str(chemin_mpp))

    out = []
    for a in projet.getResourceAssignments():
        r, t = a.getResource(), a.getTask()
        debut, fin = a.getStart(), a.getFinish()
        if r is None or t is None or debut is None or fin is None:
            continue
        out.append({
            'tache': str(t.getName()) if t.getName() else '',
            'ressource': str(r.getName()) if r.getName() else '',
            'type_ressource': str(r.getType()),
            'unites_pct': float(a.getUnits()) if a.getUnits() is not None else 0.0,
            'debut': _vers_datetime(debut),
            'fin': _vers_datetime(fin),
        })
    return out


def _vers_datetime(v):
    """MPXJ (via jpype) renvoie un `java.time.LocalDateTime` : converti en `datetime`
    Python plutôt que laissé en objet Java, pour que le reste du module n'ait pas à
    savoir que MPXJ existe."""
    return datetime(v.getYear(), v.getMonthValue(), v.getDayOfMonth(),
                     v.getHour(), v.getMinute())


def courbe_effectifs(affectations, ressources=None):
    """{ressource: {jour: effectif}} — l'effectif d'un jour est la somme des
    `unites_pct / 100` de toutes les affectations actives ce jour-là (une affectation
    couvrant plusieurs jours compte sur chacun d'eux, pas seulement son premier jour).
    Ne garde que les ressources de type WORK (main-d'œuvre) — le type MATERIAL
    (consommables) n'a pas de sens en « personnes ». `ressources`, si fourni, restreint
    aux noms donnés."""
    par_ressource = defaultdict(lambda: defaultdict(float))
    for a in affectations:
        if a['type_ressource'] != 'WORK':
            continue
        if ressources and a['ressource'] not in ressources:
            continue
        j = a['debut'].date()
        fin = a['fin'].date()
        while j <= fin:
            par_ressource[a['ressource']][j] += a['unites_pct'] / 100
            j += timedelta(days=1)
    return {r: dict(sorted(jours.items())) for r, jours in par_ressource.items()}


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('mpp')
    ap.add_argument('--ressource', action='append', help='ne garder que cette ressource (répétable)')
    args = ap.parse_args()

    affectations = lire_affectations(args.mpp)
    print(f"{len(affectations)} affectation(s) lues.")
    par_ressource_brut = defaultdict(int)
    for a in affectations:
        par_ressource_brut[a['ressource']] += 1
    print("\nAffectations par ressource :")
    for r, n in sorted(par_ressource_brut.items(), key=lambda kv: -kv[1]):
        print(f"  {r:28s} {n:>4}")

    courbes = courbe_effectifs(affectations, args.ressource)
    print(f"\nCourbes d'effectif (main-d'œuvre uniquement) — {len(courbes)} ressource(s) :")
    for r, jours in sorted(courbes.items(), key=lambda kv: -max(kv[1].values())):
        pic_jour = max(jours, key=jours.get)
        print(f"  {r:28s} pic {jours[pic_jour]:.1f} le {pic_jour}, "
              f"actif du {min(jours)} au {max(jours)} ({len(jours)} jours)")


if __name__ == '__main__':
    main()
