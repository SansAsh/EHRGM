from api.database import get_connection

# -------- LISTER TOUS LES DOSSIERS --------
def get_all_dossiers():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT eleve_id, avertissement_travail, avertissement_comportement FROM dossier")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

# -------- RÉCUPÉRER LE DOSSIER D'UN ÉLÈVE --------
def get_dossier_by_eleve(eleve_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM dossier WHERE eleve_id=%s", (eleve_id,))
    dossier = cursor.fetchone()
    cursor.close()
    conn.close()
    return dossier or {"eleve_id": eleve_id, "avertissement_travail": 0, "avertissement_comportement": 0}

# -------- MODIFIER LE DOSSIER D'UN ÉLÈVE --------
def update_dossier(eleve_id, avertissement_travail: int, avertissement_comportement: int):
    conn = get_connection()
    cursor = conn.cursor()
    # Si dossier existe → update, sinon → insert
    cursor.execute("SELECT eleve_id FROM dossier WHERE eleve_id=%s", (eleve_id,))
    if cursor.fetchone():
        cursor.execute(
            "UPDATE dossier SET avertissement_travail=%s, avertissement_comportement=%s WHERE eleve_id=%s",
            (avertissement_travail, avertissement_comportement, eleve_id)
        )
    else:
        cursor.execute(
            "INSERT INTO dossier (eleve_id, avertissement_travail, avertissement_comportement) VALUES (%s, %s, %s)",
            (eleve_id, avertissement_travail, avertissement_comportement)
        )
    conn.commit()
    cursor.close()
    conn.close()