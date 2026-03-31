from database import get_connection
from collections import defaultdict

# GET /notes/{eleve_id}
def get_notes_by_eleve(eleve_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT note.note, cours.nom as cours, eleve.nom as eleve
        FROM note
        JOIN eleve ON note.eleve_id = eleve.id
        JOIN cours ON note.cours_id = cours.id
        WHERE eleve.id = %s
    """, (eleve_id,))

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data


# GET /note?type=...
def get_notes_par(type):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT eleve.nom as eleve, cours.nom as cours, prof.nom as prof, note.note
        FROM note
        JOIN eleve ON note.eleve_id = eleve.id
        JOIN cours ON note.cours_id = cours.id
        JOIN prof ON note.prof_id = prof.id
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    result = defaultdict(list)

    for row in data:
        key = row[type]
        result[key].append({
            "note": float(row["note"]),
            "eleve": row["eleve"],
            "cours": row["cours"],
            "prof": row["prof"]
        })

    return dict(result)