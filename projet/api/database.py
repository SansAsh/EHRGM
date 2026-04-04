import mysql.connector
import os

# Connexion à la base de données
DB_CONFIG = {
    # Adresse du serveur de la base de données
    "host": os.getenv("DB_HOST", "127.0.0.1"),

    # Nom d'utilisateur pour la connexion à la base
    "user": os.getenv("DB_USER", "root"),

    # Mot de passe associé à l'utilisateur (vide par défaut)
    "password": os.getenv("DB_PASSWORD", ""),

    # Nom de la base de données à utiliser
    "database": os.getenv("DB_NAME", "marco_enzo_lajeune_hugo_laquaye_remi_clement_maxime_donati_gabri"),

    # Port de connexion (3306)
    "port": int(os.getenv("DB_PORT", 3306)),
}


# Etablir une connexion à la bdd
def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

# Fonction pour exécuter une requête SELECT
def fetch_all(query: str, params=None):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params or ())
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

# Fonction pour exécuter une requête SELECT
def fetch_one(query: str, params=None):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params or ())
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row

# Fonction pour exécuter des requêtes modifiant la base (INSERT, UPDATE, DELETE)
def execute(query: str, params=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params or ())
    conn.commit()
    last_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return last_id
