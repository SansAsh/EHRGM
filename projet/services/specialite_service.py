from api.database import get_connection
from collections import defaultdict

def get_cours_by_specialite(specialite_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT specialite.id, cours.nom
        FROM specialite
        JOIN cours ON cours.specialite_id = specialite.id
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    result = []

    for row in data:
        if row["id"] == specialite_id:
            result.append(row["nom"])

    return result

def get_promotions_by_specialite(specialite_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT specialite.id, promotion.id AS promotion, promotion.annee
        FROM specialite
        JOIN promotion ON promotion.specialite_id = specialite.id
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    result = []

    for row in data:
        if row["id"] == specialite_id:
            result.append({
                "id": row["promotion"],
                "annee": row["annee"]
            })

    return result