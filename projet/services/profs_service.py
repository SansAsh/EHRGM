from api.database import get_connection
from collections import defaultdict

def get_prof_severe():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT prof.nom, note.note
        FROM prof
        JOIN note ON prof.id = note.prof_id
    """)
    data = cursor.fetchall()
    cursor.close()
    conn.close()

    notes_par_prof = defaultdict(list)
    for row in data:
        notes_par_prof[row["nom"]].append(float(row["note"]))

    result = []
    for prof, notes in notes_par_prof.items():
        moyenne = sum(notes) / len(notes)
        if moyenne < 8:
            result.append({
                "prof": prof,
                "moyenne": round(moyenne, 2)
            })

    # Trier du plus sévère au moins sévère
    result.sort(key=lambda x: x["moyenne"])
    return result