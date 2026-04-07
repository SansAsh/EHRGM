from api.database import get_connection
from collections import defaultdict

# ---------------- PROF SEVERE ----------------
def get_prof_severe():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT prof.id, prof.nom, note.note
        FROM prof
        JOIN note ON prof.id = note.prof_id
    """)
    data = cursor.fetchall()
    cursor.close()
    conn.close()

    notes_par_prof = defaultdict(list)
    for row in data:
        notes_par_prof[(row["id"], row["nom"])].append(float(row["note"]))

    result = []
    for (prof_id, prof_nom), notes in notes_par_prof.items():
        moyenne = sum(notes) / len(notes)
        if moyenne < 11:
            result.append({
                "id": prof_id,
                "prof": prof_nom,
                "moyenne": round(moyenne, 2)
            })

    result.sort(key=lambda x: x["moyenne"])
    return result

# ---------------- TOUS LES PROFS ----------------
def get_all_profs():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, nom, email , age FROM prof")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

# ---------------- GET PROF BY ID ----------------
def get_prof_by_id(prof_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM prof WHERE id = %s", (prof_id,))
    prof = cursor.fetchone()
    cursor.close()
    conn.close()
    return prof

# ---------------- CREATE ----------------
def create_prof(nom, email, age):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO prof (nom, email, age) VALUES (%s, %s, %s)", (nom, email, age))
    conn.commit()
    cursor.close()
    conn.close()

# ---------------- UPDATE ----------------
def update_prof(prof_id, nom, email, age):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE prof SET nom = %s, email = %s, age = %s WHERE id = %s", (nom, email, age, prof_id))
    conn.commit()
    cursor.close()
    conn.close()

# ---------------- DELETE ----------------
def delete_prof(prof_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # supprimer les notes liées
        cursor.execute("DELETE FROM note WHERE prof_id=%s", (prof_id,))

        # supprimer le prof
        cursor.execute("DELETE FROM prof WHERE id=%s", (prof_id,))

        conn.commit()

    except Exception as e:
        conn.rollback()
        print("ERREUR DELETE PROF:", e)
        raise e

    finally:
        cursor.close()
        conn.close()