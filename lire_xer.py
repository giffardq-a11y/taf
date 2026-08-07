"""Lecteur de fichier XER Primavera P6.

Le XER est une suite de tables tabulées : `%T` ouvre une table, `%F` donne ses colonnes,
`%R` porte un enregistrement. Un champ mémo peut contenir des retours à la ligne : une ligne
qui ne commence pas par un jeton `%` est donc la suite de l'enregistrement précédent, et non
un nouvel enregistrement.

Le fichier n'est jamais chargé en entier : on ne garde que les tables demandées, et d'elles
que les colonnes demandées. Sur l'export de référence — 86 Mo, 67 000 activités — cela ramène
l'empreinte mémoire à quelques dizaines de mégaoctets.

    from lire_xer import lire
    tables = lire('planning.xer', {'TASK': ['task_id', 'task_name'], 'TASKPRED': None})
"""
import io


def lire(chemin, demandes=None, encodage='cp1252'):
    """Renvoie {table: [dict, …]}. `demandes` = {table: [colonnes] ou None pour toutes}."""
    tables = {}
    table = colonnes = None
    garde = None if demandes is None else set(demandes)
    courant = None          # enregistrement en cours d'assemblage, sur plusieurs lignes

    def clore():
        if courant is None or colonnes is None:
            return
        vals = courant[1:]
        vals += [''] * (len(colonnes) - len(vals))
        voulues = demandes.get(table) if demandes else None
        tables[table].append({c: vals[i] for i, c in enumerate(colonnes)
                              if voulues is None or c in voulues})

    with io.open(chemin, encoding=encodage, errors='replace', newline='') as f:
        for ligne in f:
            ligne = ligne.rstrip('\r\n')
            if not ligne.startswith('%'):
                if courant is not None:          # suite d'un champ mémo
                    courant[-1] += '\n' + ligne
                continue
            p = ligne.split('\t')
            if p[0] == '%R':
                if courant is not None:
                    clore()
                courant = p if colonnes is not None else None
                continue
            clore()
            courant = None
            if p[0] == '%T':
                table = p[1]
                colonnes = None
                if garde is None or table in garde:
                    tables.setdefault(table, [])
            elif p[0] == '%F':
                colonnes = p[1:] if (garde is None or table in garde) else None
            elif p[0] == '%E':
                break
    clore()
    return tables


def entier(v, defaut=0):
    try:
        return int(float(v))
    except (TypeError, ValueError):
        return defaut


def reel(v, defaut=0.0):
    try:
        return float(v)
    except (TypeError, ValueError):
        return defaut


def date(v):
    """Les dates XER sont en « AAAA-MM-JJ HH:MM ». Renvoie un datetime ou None."""
    import datetime
    v = (v or '').strip()
    if not v:
        return None
    for fmt in ('%Y-%m-%d %H:%M', '%Y-%m-%d'):
        try:
            return datetime.datetime.strptime(v, fmt)
        except ValueError:
            pass
    return None
