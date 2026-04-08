from api.database import get_connection
from collections import defaultdict



def get_all_eleves():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, nom, age, email, promotion_id FROM eleve")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


def get_eleve_by_id(eleve_id):
    eleves = get_all_eleves()
    for eleve in eleves:
        if eleve["id"] == eleve_id:
            return eleve
    return {"erreur": "Élève non trouvé"}



def get_eleves_avertis():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT eleve.id, eleve.nom,
               dossier.avertissement_travail,
               dossier.avertissement_comportement
        FROM eleve
        JOIN dossier ON eleve.id = dossier.eleve_id
    """)
    data = cursor.fetchall()
    cursor.close()
    conn.close()

    result = []
    for row in data:
        if row["avertissement_travail"] == 1 or row["avertissement_comportement"] == 1:
            result.append({
                "id": row["id"],
                "nom": row["nom"],
                "avertissement_travail": row["avertissement_travail"],
                "avertissement_comportement": row["avertissement_comportement"]
            })
    return result



def get_bonne_notes():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT eleve.id, eleve.nom, note.note
        FROM eleve
        JOIN note ON eleve.id = note.eleve_id
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    eleves_notes = {}

    for row in data:
        eleves_notes.setdefault(row["nom"], []).append(float(row["note"]))

    result = []

    for nom, notes in eleves_notes.items():
        moyenne = sum(notes) / len(notes)
        if moyenne > 12:
            result.append({
                "nom": nom,
                "moyenne": round(moyenne, 2)
            })

    # tri PYTHON (important)
    result.sort(key=lambda x: x["moyenne"], reverse=True)

    return result



def get_absence_eleve(eleve_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT eleve_id, duree_minutes
        FROM absence
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    total = 0

    for row in data:
        if row["eleve_id"] == eleve_id:
            total += row["duree_minutes"]

    return {
        "eleve_id": eleve_id,
        "absence_heures": round(total / 60, 2)
    }



def create_eleve(nom, email, age, promotion_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO eleve (nom, email, age, promotion_id) VALUES (%s, %s, %s, %s)",
        (nom, email, age, promotion_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Élève ajouté"}



def update_eleve(eleve_id, nom, email, age, promotion_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE eleve SET nom=%s, email=%s, age=%s, promotion_id=%s WHERE id=%s",
        (nom, email, age, promotion_id, eleve_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Élève modifié"}



def delete_eleve(eleve_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM eleve WHERE id=%s", (eleve_id,))
    if cursor.fetchone() is None:
        return {"error": "Élève introuvable"}
    
    # Suppression
    cursor.execute("DELETE FROM note WHERE eleve_id=%s", (eleve_id,))
    cursor.execute("DELETE FROM absence WHERE eleve_id=%s", (eleve_id,))
    cursor.execute("DELETE FROM dossier WHERE eleve_id=%s", (eleve_id,))
    cursor.execute("DELETE FROM eleve WHERE id=%s", (eleve_id,))

    conn.commit()

    cursor.close()
    conn.close()

    return {"message": "OK"}



def get_notes_eleve(eleve_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT eleve.id, eleve.nom, note.note, cours.nom AS cours
        FROM eleve
        JOIN note ON eleve.id = note.eleve_id
        JOIN cours ON cours.id = note.cours_id
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    result = []

    for row in data:
        if row["id"] == eleve_id:
            result.append({
                "nom": row["nom"],
                "cours": row["cours"],
                "note": float(row["note"])
            })

    return result



def get_dossier_eleve(eleve_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT eleve_id, avertissement_travail, avertissement_comportement
        FROM dossier
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    for row in data:
        if row["eleve_id"] == eleve_id:
            return row

    return {}