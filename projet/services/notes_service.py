from api.database import get_connection
from collections import defaultdict

def get_notes_by_eleve(eleve_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT eleve.id,
               eleve.nom AS eleve,
               cours.nom AS cours,
               note.note
        FROM note
        JOIN eleve ON note.eleve_id = eleve.id
        JOIN cours ON note.cours_id = cours.id
    """)
    data = cursor.fetchall()
    cursor.close()
    conn.close()

    result = []
    for row in data:
        if row["id"] == eleve_id:
            result.append({
                "eleve": row["eleve"],
                "cours": row["cours"],
                "note": float(row["note"])
            })
    return result

def get_notes_par(par):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT eleve.nom AS eleve,
               cours.nom AS cours,
               prof.nom AS prof,
               promotion.nom AS promotion,
               note.note
        FROM note
        JOIN eleve ON note.eleve_id = eleve.id
        JOIN cours ON note.cours_id = cours.id
        JOIN prof ON note.prof_id = prof.id
        JOIN promotion ON eleve.promotion_id = promotion.id
    """)
    data = cursor.fetchall()
    cursor.close()
    conn.close()

    if par not in ["eleve", "prof", "cours", "promotion"]:
        return {"erreur": "paramètre invalide"}

    result = defaultdict(list)
    for row in data:
        cle = row[par]
        result[cle].append({
            "note": float(row["note"]),
            "eleve": row["eleve"],
            "cours": row["cours"],
            "prof": row["prof"],
            "promotion": row["promotion"]
        })

    return dict(result)