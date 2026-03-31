import requests

BASE_URL = "http://127.0.0.1:8000"

def menu():
    while True:
        print("\n=== Menu Admin ===")
        print("1. Voir tous les élèves")
        print("2. Ajouter un élève")
        print("3. Supprimer un élève")
        print("4. Voir élèves avec bonnes notes")
        print("5. Quitter")

        choix = input("> ")

        if choix == "1":
            r = requests.get(f"{BASE_URL}/eleve/")
            if r.status_code == 200:
                for eleve in r.json():
                    print(f"ID: {eleve['id']} | Nom: {eleve['nom']} | Age: {eleve['age']}")
            else:
                print("Erreur lors de la récupération des élèves.")

        elif choix == "2":
            nom = input("Nom: ")
            email = input("Email: ")
            age = int(input("Age: "))
            promo = int(input("Promotion ID: "))
            r = requests.post(f"{BASE_URL}/eleve/", json={
                "nom": nom, "email": email, "age": age, "promotion_id": promo
            })
            print(r.json()["message"])

        elif choix == "3":
            id_eleve = int(input("ID de l'élève à supprimer: "))
            r = requests.delete(f"{BASE_URL}/eleve/{id_eleve}")
            print(r.json()["message"])

        elif choix == "4":
            r = requests.get(f"{BASE_URL}/eleve/bonne_notes")
            if r.status_code == 200:
                print("=== Élèves avec moyenne > 12 ===")
                for eleve in r.json():
                    print(f"{eleve['nom']} | Moyenne: {eleve['moyenne']}")
            else:
                print("Erreur lors de la récupération des bonnes notes.")

        elif choix == "5":
            print("Au revoir !")
            break

        else:
            print("Choix invalide. Réessayez.")

if __name__ == "__main__":
    menu()