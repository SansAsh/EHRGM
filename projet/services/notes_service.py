from api.database import get_connection

# -------- CRÉER UNE NOTE --------
def create_note(eleve_id, prof_id, note_valeur):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO note (eleve_id, prof_id, note) VALUES (%s, %s, %s)",
        (eleve_id, prof_id, note_valeur)
    )
    conn.commit()
    cursor.close()
    conn.close()

# -------- MODIFIER UNE NOTE --------
def update_note(note_id, eleve_id, prof_id, note_valeur):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE note SET eleve_id=%s, prof_id=%s, note=%s WHERE id=%s",
        (eleve_id, prof_id, note_valeur, note_id)
    )
    conn.commit()
    cursor.close()
    conn.close()

# -------- LISTER LES NOTES --------
def get_all_notes():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT note.id, note.note, eleve.nom AS eleve_nom, prof.nom AS prof_nom
        FROM note
        JOIN eleve ON note.eleve_id = eleve.id
        JOIN prof ON note.prof_id = prof.id
    """)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

# -------- LISTER LES ÉLÈVES AVEC MOYENNE > 12 --------
from collections import defaultdict

def get_eleves_moyenne_sup12():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT eleve.id, eleve.nom, note.note
        FROM eleve
        JOIN note ON note.eleve_id = eleve.id
    """)
    data = cursor.fetchall()
    cursor.close()
    conn.close()

    notes_par_eleve = defaultdict(list)
    for row in data:
        notes_par_eleve[(row["id"], row["nom"])].append(float(row["note"]))

    result = []
    for (eleve_id, eleve_nom), notes in notes_par_eleve.items():
        moyenne = sum(notes) / len(notes)
        if moyenne > 12:
            result.append({
                "id": eleve_id,
                "nom": eleve_nom,
                "moyenne": round(moyenne, 2)
            })

    # Tri du + haut au + bas
    result.sort(key=lambda x: x["moyenne"], reverse=True)
    return result