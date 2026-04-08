from api.database import get_connection

# -------- LISTER TOUS LES CLUBS --------
def get_all_clubs():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT club.*, sport.nom AS sport_nom
        FROM club
        JOIN sport ON club.sport_id = sport.id
    """)

    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


# -------- RÉCUPÉRER UN CLUB --------
def get_club_by_id(club_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM club WHERE id = %s
    """, (club_id,))

    club = cursor.fetchone()
    cursor.close()
    conn.close()
    return club


# -------- LISTER LES SPORTS --------
def get_all_sports():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM sport")
    sports = cursor.fetchall()

    cursor.close()
    conn.close()
    return sports


# -------- CRÉER UN CLUB --------
def create_club(nom, sport_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO club (nom, sport_id)
        VALUES (%s, %s)
    """, (nom, sport_id))

    conn.commit()
    cursor.close()
    conn.close()


# -------- MODIFIER UN CLUB --------
def update_club(club_id, nom, sport_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE club
        SET nom = %s, sport_id = %s
        WHERE id = %s
    """, (nom, sport_id, club_id))

    conn.commit()
    cursor.close()
    conn.close()


# -------- SUPPRIMER UN CLUB --------
def delete_club(club_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM club WHERE id = %s", (club_id,))
    conn.commit()

    cursor.close()
    conn.close()