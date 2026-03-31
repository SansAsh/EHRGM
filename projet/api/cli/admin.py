import requests

BASE_URL = "http://127.0.0.1:8000"

def menu():
    while True:
        print("\n1. Voir élèves")
        print("2. Ajouter élève")
        print("3. Supprimer élève")
        print("4. Bonnes notes")
        print("5. Quitter")

        choix = input("> ")

        if choix == "1":
            print(requests.get(f"{BASE_URL}/eleve/").json())

        elif choix == "2":
            nom = input("Nom: ")
            email = input("Email: ")
            age = int(input("Age: "))
            promo = int(input("Promotion: "))

            requests.post(f"{BASE_URL}/eleve/", json={
                "nom": nom,
                "email": email,
                "age": age,
                "promotion_id": promo
            })

        elif choix == "3":
            id = int(input("ID: "))
            requests.delete(f"{BASE_URL}/eleve/{id}")

        elif choix == "4":
            print(requests.get(f"{BASE_URL}/eleve/bonne_notes").json())

        elif choix == "5":
            break

menu()