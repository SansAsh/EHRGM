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
        SELECT eleve.nom AS eleve, note.note
        FROM eleve
        JOIN note ON eleve.id = note.eleve_id
    """)
    data = cursor.fetchall()
    cursor.close()
    conn.close()

    notes_par_eleve = defaultdict(list)
    for row in data:
        notes_par_eleve[row["eleve"]].append(float(row["note"]))

    result = []
    for eleve, notes in notes_par_eleve.items():
        moyenne = sum(notes) / len(notes)
        if moyenne > 12:
            result.append({"nom": eleve, "moyenne": round(moyenne, 2)})

    # Tri de la moyenne la plus haute à la plus basse
    result.sort(key=lambda x: x["moyenne"], reverse=True)
    return result

def get_absence_eleve(eleve_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT duree_minutes, eleve_id FROM absence
    """)
    data = cursor.fetchall()
    cursor.close()
    conn.close()

    total = sum(row["duree_minutes"] for row in data if row["eleve_id"] == eleve_id)

    return {
        "eleve_id": eleve_id,
        "absence_minutes": total,
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
    cursor.execute("DELETE FROM eleve WHERE id=%s", (eleve_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Élève supprimé"}