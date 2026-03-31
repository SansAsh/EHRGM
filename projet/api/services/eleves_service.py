from database import get_connection
from collections import defaultdict

# GET /eleve/
def get_all_eleves():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id, nom, age FROM eleve")
    data = cursor.fetchall()

    cursor.close()
    conn.close()
    return data


# GET /eleve/{id}
def get_eleve_by_id(eleve_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id, nom, age FROM eleve WHERE id = %s", (eleve_id,))
    data = cursor.fetchone()

    cursor.close()
    conn.close()
    return data


# GET /eleve/avertis
def get_eleves_avertis():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT eleve.nom, dossier.avertissement_travail, dossier.avertissement_comportement
        FROM eleve
        JOIN dossier ON eleve.id = dossier.eleve_id
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return [
        e for e in data
        if e["avertissement_travail"] == 1
        or e["avertissement_comportement"] == 1
    ]


# GET /eleve/bonne_notes
def get_bonne_notes():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT eleve.nom, note.note
        FROM eleve
        JOIN note ON eleve.id = note.eleve_id
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    notes_par_eleve = defaultdict(list)

    for row in data:
        notes_par_eleve[row["nom"]].append(float(row["note"]))

    result = []

    for eleve, notes in notes_par_eleve.items():
        moyenne = sum(notes) / len(notes)
        if moyenne > 12:
            result.append({"nom": eleve, "moyenne": moyenne})

    result.sort(key=lambda x: x["moyenne"], reverse=True)

    return result


# GET /eleve/{id}/absence
def get_absence_eleve(eleve_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT duree_minutes
        FROM absence
        WHERE eleve_id = %s
    """, (eleve_id,))

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    total = sum([row["duree_minutes"] for row in data])

    return {"eleve_id": eleve_id, "total_absence_minutes": total}


# CRUD
def create_eleve(nom, email, age, promotion_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO eleve (nom, email, age, promotion_id)
        VALUES (%s, %s, %s, %s)
    """, (nom, email, age, promotion_id))

    conn.commit()
    cursor.close()
    conn.close()

    return {"message": "Élève ajouté"}


def delete_eleve(eleve_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM eleve WHERE id = %s", (eleve_id,))
    conn.commit()

    cursor.close()
    conn.close()

    return {"message": "Élève supprimé"}