import requests

BASE_URL = "http://127.0.0.1:8000"
TOKEN = None  # rempli après login

def get_headers():
    return {"Authorization": f"Bearer {TOKEN}"}

def api_get(url):
    return requests.get(url, headers=get_headers())

def api_post(url, json):
    return requests.post(url, json=json, headers=get_headers())

def api_put(url, json):
    return requests.put(url, json=json, headers=get_headers())

def api_delete(url):
    return requests.delete(url, headers=get_headers())

# -------------- Login -----------------

def login():
    global TOKEN
    print("\n=== Connexion à l'API École ===")
    username = input("Nom d'utilisateur : ")
    password = input("Mot de passe : ")
    r = requests.post(f"{BASE_URL}/login?username={username}&password={password}")
    if r.status_code == 200:
        TOKEN = r.json()["token"]
        print("Connexion réussie.")
        return True
    else:
        print("Identifiants invalides.")
        return False

# -------------- Eleves -----------------

def menu_eleves():
    while True:
        print("\n=== Menu Élèves ===")
        print("1. Voir tous les élèves")
        print("2. Voir un élève par ID")
        print("3. Ajouter un élève")
        print("4. Modifier un élève")
        print("5. Supprimer un élève")
        print("6. Élèves avec avertissement")
        print("7. Élèves avec bonne moyenne (> 12)")
        print("8. Heures d'absence d'un élève")
        print("0. Retour")
        choix = input("> ")

        if choix == "1":
            r = api_get(f"{BASE_URL}/eleve/")
            if r.status_code == 200:
                print("\n=== Liste des élèves ===")
                for e in r.json():
                    print(f"ID: {e['id']} | Nom: {e['nom']} | Age: {e['age']}")
            else:
                print("Erreur lors de la récupération des élèves.")

        elif choix == "2":
            eid = input("ID de l'élève : ")
            r = api_get(f"{BASE_URL}/eleve/{eid}")
            if r.status_code == 200:
                e = r.json()
                print(f"\nID: {e['id']} | Nom: {e['nom']} | Email: {e['email']} | Age: {e['age']} | Promotion ID: {e['promotion_id']}")
                rn = api_get(f"{BASE_URL}/notes/{eid}")
                if rn.status_code == 200 and rn.json():
                    print("Notes :")
                    for n in rn.json():
                        print(f"  - {n['matiere']} : {n['note']}/20")
            else:
                print("Élève introuvable.")

        elif choix == "3":
            nom = input("Nom : ")
            email = input("Email : ")
            age = int(input("Age : "))
            promo = input("Promotion ID (laisser vide si aucune) : ")
            payload = {"nom": nom, "email": email, "age": age}
            if promo:
                payload["promotion_id"] = int(promo)
            r = api_post(f"{BASE_URL}/eleve/", payload)
            if r.status_code == 201:
                print(f"Élève créé avec l'ID {r.json()['id']}.")
            else:
                print(f"Erreur : {r.json().get('detail', 'Inconnue')}")

        elif choix == "4":
            eid = input("ID de l'élève à modifier : ")
            r = api_get(f"{BASE_URL}/eleve/{eid}")
            if r.status_code != 200:
                print("Élève introuvable.")
                continue
            e = r.json()
            print(f"Actuel : {e['nom']} | {e['email']} | Age: {e['age']}")
            print("Laissez vide pour ne pas modifier.")
            nom = input(f"Nouveau nom ({e['nom']}) : ")
            email = input(f"Nouvel email ({e['email']}) : ")
            age = input(f"Nouvel age ({e['age']}) : ")
            promo = input(f"Nouvelle promotion_id ({e['promotion_id']}) : ")
            payload = {}
            if nom: payload["nom"] = nom
            if email: payload["email"] = email
            if age: payload["age"] = int(age)
            if promo: payload["promotion_id"] = int(promo)
            r = api_put(f"{BASE_URL}/eleve/{eid}", payload)
            if r.status_code == 200:
                print("Élève mis à jour.")
            else:
                print(f"Erreur : {r.json().get('detail', 'Inconnue')}")

        elif choix == "5":
            eid = input("ID de l'élève à supprimer : ")
            r = api_get(f"{BASE_URL}/eleve/{eid}")
            if r.status_code != 200:
                print("Élève introuvable.")
                continue
            print(f"Vous allez supprimer : {r.json()['nom']}")
            confirm = input("Confirmer ? (o/N) : ")
            if confirm.lower() == "o":
                r = api_delete(f"{BASE_URL}/eleve/{eid}")
                if r.status_code == 200:
                    print("Élève supprimé.")
                else:
                    print(f"Erreur : {r.json().get('detail', 'Inconnue')}")

        elif choix == "6":
            r = api_get(f"{BASE_URL}/eleve/avertis")
            if r.status_code == 200:
                data = r.json()
                if not data:
                    print("Aucun élève avec avertissement.")
                else:
                    print("\n=== Élèves avec avertissement ===")
                    for e in data:
                        av_t = "OUI" if e["avertissement_travail"] else "non"
                        av_c = "OUI" if e["avertissement_comportement"] else "non"
                        print(f"ID: {e['id']} | Nom: {e['nom']} | Av. travail: {av_t} | Av. comportement: {av_c}")
            else:
                print("Erreur lors de la récupération.")

        elif choix == "7":
            r = api_get(f"{BASE_URL}/eleve/bonne_notes")
            if r.status_code == 200:
                data = r.json()
                if not data:
                    print("Aucun élève avec une moyenne > 12.")
                else:
                    print("\n=== Élèves avec moyenne > 12 ===")
                    for i, e in enumerate(data, 1):
                        print(f"{i}. {e['nom']} | Moyenne: {e['moyenne']}/20")
            else:
                print("Erreur lors de la récupération des bonnes notes.")

        elif choix == "8":
            eid = input("ID de l'élève : ")
            r = api_get(f"{BASE_URL}/eleve/{eid}/absence")
            if r.status_code == 200:
                d = r.json()
                print(f"\n{d['eleve']} : {d['affichage']} d'absence ({d['total_minutes']} minutes)")
            else:
                print(f"Erreur : {r.json().get('detail', 'Inconnue')}")

        elif choix == "0":
            break
        else:
            print("Choix invalide. Réessayez.")

# -------------- Professeurs -----------------

def menu_profs():
    while True:
        print("\n=== Menu Professeurs ===")
        print("1. Voir tous les profs")
        print("2. Voir un prof par ID")
        print("3. Ajouter un prof")
        print("4. Modifier un prof")
        print("5. Supprimer un prof")
        print("6. Profs sévères (moyenne notes données < 8)")
        print("0. Retour")
        choix = input("> ")

        if choix == "1":
            r = api_get(f"{BASE_URL}/prof/")
            if r.status_code == 200:
                print("\n=== Liste des professeurs ===")
                for p in r.json():
                    print(f"ID: {p['id']} | Nom: {p['nom']} | Email: {p['email']} | Age: {p['age']}")
            else:
                print("Erreur lors de la récupération des profs.")

        elif choix == "2":
            pid = input("ID du prof : ")
            r = api_get(f"{BASE_URL}/prof/{pid}")
            if r.status_code == 200:
                p = r.json()
                print(f"\nID: {p['id']} | Nom: {p['nom']} | Email: {p['email']} | Age: {p['age']}")
            else:
                print("Professeur introuvable.")

        elif choix == "3":
            nom = input("Nom : ")
            email = input("Email : ")
            age = int(input("Age : "))
            r = api_post(f"{BASE_URL}/prof/", {"nom": nom, "email": email, "age": age})
            if r.status_code == 201:
                print(f"Professeur créé avec l'ID {r.json()['id']}.")
            else:
                print(f"Erreur : {r.json().get('detail', 'Inconnue')}")

        elif choix == "4":
            pid = input("ID du prof à modifier : ")
            r = api_get(f"{BASE_URL}/prof/{pid}")
            if r.status_code != 200:
                print("Professeur introuvable.")
                continue
            p = r.json()
            print(f"Actuel : {p['nom']} | {p['email']} | Age: {p['age']}")
            print("Laissez vide pour ne pas modifier.")
            nom = input(f"Nouveau nom ({p['nom']}) : ")
            email = input(f"Nouvel email ({p['email']}) : ")
            age = input(f"Nouvel age ({p['age']}) : ")
            payload = {}
            if nom: payload["nom"] = nom
            if email: payload["email"] = email
            if age: payload["age"] = int(age)
            r = api_put(f"{BASE_URL}/prof/{pid}", payload)
            if r.status_code == 200:
                print("Professeur mis à jour.")
            else:
                print(f"Erreur : {r.json().get('detail', 'Inconnue')}")

        elif choix == "5":
            pid = input("ID du prof à supprimer : ")
            r = api_get(f"{BASE_URL}/prof/{pid}")
            if r.status_code != 200:
                print("Professeur introuvable.")
                continue
            print(f"Vous allez supprimer : {r.json()['nom']}")
            confirm = input("Confirmer ? (o/N) : ")
            if confirm.lower() == "o":
                r = api_delete(f"{BASE_URL}/prof/{pid}")
                if r.status_code == 200:
                    print("Professeur supprimé.")
                else:
                    print(f"Erreur : {r.json().get('detail', 'Inconnue')}")

        elif choix == "6":
            r = api_get(f"{BASE_URL}/prof/severe")
            if r.status_code == 200:
                data = r.json()
                if not data:
                    print("Aucun prof sévère détecté.")
                else:
                    print("\n=== Profs sévères (du plus au moins sévère) ===")
                    for p in data:
                        print(f"ID: {p['id']} | Nom: {p['nom']} | Moyenne notes données: {p['moyenne_notes_donnees']}/20")
            else:
                print("Erreur lors de la récupération.")

        elif choix == "0":
            break
        else:
            print("Choix invalide. Réessayez.")

# -------------- Notes -----------------

def menu_notes():
    while True:
        print("\n=== Menu Notes ===")
        print("1. Voir toutes les notes")
        print("2. Notes par type (eleve / prof / cours / promotion)")
        print("3. Ajouter une note")
        print("4. Modifier une note (uniquement à la hausse)")
        print("0. Retour")
        choix = input("> ")

        if choix == "1":
            r = api_get(f"{BASE_URL}/notes/")
            if r.status_code == 200:
                print("\n=== Toutes les notes ===")
                for n in r.json():
                    print(f"ID: {n['id']} | Élève ID: {n['eleve_id']} | Cours ID: {n['cours_id']} | Prof ID: {n['prof_id']} | Note: {n['note']}/20")
            else:
                print("Erreur lors de la récupération des notes.")

        elif choix == "2":
            print("Types disponibles : eleve, prof, cours, promotion")
            par = input("Type : ")
            r = api_get(f"{BASE_URL}/note?par={par}")
            if r.status_code == 200:
                print(f"\n=== Notes par {par} ===")
                for cle, notes in r.json().items():
                    print(f"\n{cle} :")
                    for n in notes:
                        print(f"  - {n['nomEleve']} | {n['cours']} | prof: {n['nomProf']} | {n['note']}/20")
            else:
                print(f"Erreur : {r.json().get('detail', 'Inconnue')}")

        elif choix == "3":
            re = api_get(f"{BASE_URL}/eleve/")
            rc = api_get(f"{BASE_URL}/cours/")
            rp = api_get(f"{BASE_URL}/prof/")
            if re.status_code == 200:
                print("\nÉlèves disponibles :")
                for e in re.json():
                    print(f"  ID {e['id']} - {e['nom']}")
            if rc.status_code == 200:
                print("\nCours disponibles :")
                for c in rc.json():
                    print(f"  ID {c['id']} - {c['nom']}")
            if rp.status_code == 200:
                print("\nProfs disponibles :")
                for p in rp.json():
                    print(f"  ID {p['id']} - {p['nom']}")
            eleve_id = int(input("\nID Élève : "))
            cours_id = int(input("ID Cours : "))
            prof_id = int(input("ID Prof : "))
            note = float(input("Note (0-20) : "))
            r = api_post(f"{BASE_URL}/note/", {
                "eleve_id": eleve_id, "cours_id": cours_id, "prof_id": prof_id, "note": note
            })
            if r.status_code == 201:
                print(f"Note {note}/20 ajoutée.")
            else:
                print(f"Erreur : {r.json().get('detail', 'Inconnue')}")

        elif choix == "4":
            nid = input("ID de la note à modifier : ")
            r = api_get(f"{BASE_URL}/note/{nid}")
            if r.status_code != 200:
                print("Note introuvable.")
                continue
            print(f"Note actuelle : {r.json()['note']}/20")
            nouvelle = float(input("Nouvelle note (doit être >= note actuelle) : "))
            r = api_put(f"{BASE_URL}/note/{nid}", {"note": nouvelle})
            if r.status_code == 200:
                print("Note mise à jour.")
            else:
                print(f"Erreur : {r.json().get('detail', 'Inconnue')}")

        elif choix == "0":
            break
        else:
            print("Choix invalide. Réessayez.")

# -------------- Dossiers -----------------

def menu_dossiers():
    while True:
        print("\n=== Menu Dossiers ===")
        print("1. Voir le dossier d'un élève")
        print("2. Modifier un dossier")
        print("0. Retour")
        choix = input("> ")

        if choix == "1":
            eid = input("ID de l'élève : ")
            r = api_get(f"{BASE_URL}/dossier/{eid}")
            if r.status_code == 200:
                d = r.json()
                av_t = "OUI" if d["avertissement_travail"] else "non"
                av_c = "OUI" if d["avertissement_comportement"] else "non"
                print(f"\nÉlève : {d['nom_eleve']}")
                print(f"Infos : {d.get('infos') or '-'}")
                print(f"Avertissement travail : {av_t}")
                print(f"Avertissement comportement : {av_c}")
            else:
                print(f"Erreur : {r.json().get('detail', 'Inconnue')}")

        elif choix == "2":
            eid = input("ID de l'élève : ")
            r = api_get(f"{BASE_URL}/dossier/{eid}")
            if r.status_code != 200:
                print("Dossier introuvable.")
                continue
            d = r.json()
            print(f"Infos actuelles : {d.get('infos') or '-'}")
            print("Laissez vide pour ne pas modifier.")
            infos = input("Nouvelles infos : ")
            avt = input("Avertissement travail (0 ou 1) : ")
            avc = input("Avertissement comportement (0 ou 1) : ")
            payload = {}
            if infos: payload["infos"] = infos
            if avt: payload["avertissement_travail"] = int(avt)
            if avc: payload["avertissement_comportement"] = int(avc)
            r = api_put(f"{BASE_URL}/dossier/{eid}", payload)
            if r.status_code == 200:
                print("Dossier mis à jour.")
            else:
                print(f"Erreur : {r.json().get('detail', 'Inconnue')}")

        elif choix == "0":
            break
        else:
            print("Choix invalide. Réessayez.")

# -------------- Cours -----------------

def menu_instances_cours():
    while True:
        print("\n=== Menu Instances de Cours ===")
        print("1. Voir toutes les instances")
        print("2. Voir une instance par ID")
        print("3. Ajouter une instance")
        print("4. Modifier une instance")
        print("5. Supprimer une instance")
        print("0. Retour")
        choix = input("> ")

        if choix == "1":
            r = api_get(f"{BASE_URL}/instance_cours/")
            if r.status_code == 200:
                print("\n=== Instances de cours ===")
                for ic in r.json():
                    print(f"ID: {ic['id']} | Cours: {ic['cours']} | Prof: {ic['prof']} | Date: {str(ic['date'])[:16]}")
            else:
                print("Erreur lors de la récupération.")

        elif choix == "2":
            iid = input("ID de l'instance : ")
            r = api_get(f"{BASE_URL}/instance_cours/{iid}")
            if r.status_code == 200:
                ic = r.json()
                print(f"\nID: {ic['id']} | Cours ID: {ic['cours_id']} | Prof ID: {ic['prof_id']} | Date: {ic['date']}")
            else:
                print("Instance introuvable.")

        elif choix == "3":
            rc = api_get(f"{BASE_URL}/cours/")
            rp = api_get(f"{BASE_URL}/prof/")
            if rc.status_code == 200:
                print("\nCours disponibles :")
                for c in rc.json():
                    print(f"  ID {c['id']} - {c['nom']}")
            if rp.status_code == 200:
                print("\nProfs disponibles :")
                for p in rp.json():
                    print(f"  ID {p['id']} - {p['nom']}")
            cours_id = int(input("\nID Cours : "))
            prof_id = int(input("ID Prof : "))
            date = input("Date (YYYY-MM-DD HH:MM:SS) : ")
            r = api_post(f"{BASE_URL}/instance_cours/", {
                "cours_id": cours_id, "prof_id": prof_id, "date": date
            })
            if r.status_code == 201:
                print(f"Instance créée avec l'ID {r.json()['id']}.")
            else:
                print(f"Erreur : {r.json().get('detail', 'Inconnue')}")

        elif choix == "4":
            iid = input("ID de l'instance à modifier : ")
            r = api_get(f"{BASE_URL}/instance_cours/{iid}")
            if r.status_code != 200:
                print("Instance introuvable.")
                continue
            ic = r.json()
            print(f"Actuel : cours_id={ic['cours_id']} | prof_id={ic['prof_id']} | date={ic['date']}")
            print("Laissez vide pour ne pas modifier.")
            cours_id = input(f"Nouveau cours_id ({ic['cours_id']}) : ")
            prof_id = input(f"Nouveau prof_id ({ic['prof_id']}) : ")
            date = input(f"Nouvelle date ({ic['date']}) : ")
            payload = {}
            if cours_id: payload["cours_id"] = int(cours_id)
            if prof_id: payload["prof_id"] = int(prof_id)
            if date: payload["date"] = date
            r = api_put(f"{BASE_URL}/instance_cours/{iid}", payload)
            if r.status_code == 200:
                print("Instance mise à jour.")
            else:
                print(f"Erreur : {r.json().get('detail', 'Inconnue')}")

        elif choix == "5":
            iid = input("ID de l'instance à supprimer : ")
            confirm = input("Confirmer la suppression ? (o/N) : ")
            if confirm.lower() == "o":
                r = api_delete(f"{BASE_URL}/instance_cours/{iid}")
                if r.status_code == 200:
                    print("Instance supprimée.")
                else:
                    print(f"Erreur : {r.json().get('detail', 'Inconnue')}")

        elif choix == "0":
            break
        else:
            print("Choix invalide. Réessayez.")

# -------------- Club -----------------

def menu_clubs():
    while True:
        print("\n=== Menu Clubs Sportifs ===")
        print("1. Voir tous les clubs")
        print("2. Voir les membres d'un club")
        print("3. Voir les stats d'un club")
        print("4. Ajouter un club")
        print("5. Modifier un club")
        print("6. Supprimer un club")
        print("7. Ajouter un membre à un club")
        print("8. Retirer un membre d'un club")
        print("0. Retour")
        choix = input("> ")

        if choix == "1":
            r = api_get(f"{BASE_URL}/clubs/")
            if r.status_code == 200:
                print("\n=== Liste des clubs ===")
                for c in r.json():
                    resp = c.get("responsable") or "-"
                    print(f"ID: {c['id']} | Nom: {c['nom']} | Sport: {c['sport']} | Responsable: {resp} | Max membres: {c.get('nb_membres_max') or '-'}")
            else:
                print("Erreur lors de la récupération des clubs.")

        elif choix == "2":
            cid = input("ID du club : ")
            r = api_get(f"{BASE_URL}/clubs/{cid}/membres")
            if r.status_code == 200:
                d = r.json()
                print(f"\n=== Membres de {d['club']} ===")
                for m in d["membres"]:
                    print(f"ID: {m['id']} | Nom: {m['nom']} | Rôle: {m['role']} | Adhésion: {m['date_adhesion']}")
            else:
                print(f"Erreur : {r.json().get('detail', 'Inconnue')}")

        elif choix == "3":
            cid = input("ID du club : ")
            r = api_get(f"{BASE_URL}/clubs/{cid}/stats")
            if r.status_code == 200:
                d = r.json()
                print(f"\n=== Stats de {d['club']} ===")
                print(f"Membres : {d['nb_membres']}")
                print(f"Événements : {d['nb_evenements']}")
                print(f"Total participations : {d['total_participations']}")
            else:
                print(f"Erreur : {r.json().get('detail', 'Inconnue')}")

        elif choix == "4":
            rs = api_get(f"{BASE_URL}/sports/")
            rp = api_get(f"{BASE_URL}/prof/")
            if rs.status_code == 200:
                print("\nSports disponibles :")
                for s in rs.json():
                    print(f"  ID {s['id']} - {s['nom']}")
            if rp.status_code == 200:
                print("\nResponsables disponibles (profs) :")
                for p in rp.json():
                    print(f"  ID {p['id']} - {p['nom']}")
            nom = input("\nNom du club : ")
            sport_id = int(input("ID Sport : "))
            resp_id = input("ID Responsable (laisser vide si aucun) : ")
            date = input("Date de création (YYYY-MM-DD, laisser vide si aucune) : ")
            max_m = input("Nombre max de membres (laisser vide si aucun) : ")
            payload = {"nom": nom, "sport_id": sport_id}
            if resp_id: payload["responsable_id"] = int(resp_id)
            if date: payload["date_creation"] = date
            if max_m: payload["nb_membres_max"] = int(max_m)
            r = api_post(f"{BASE_URL}/clubs/", payload)
            if r.status_code == 201:
                print(f"Club '{nom}' créé avec l'ID {r.json()['id']}.")
            else:
                print(f"Erreur : {r.json().get('detail', 'Inconnue')}")

        elif choix == "5":
            cid = input("ID du club à modifier : ")
            print("Laissez vide pour ne pas modifier.")
            nom = input("Nouveau nom : ")
            sport_id = input("Nouveau sport_id : ")
            resp_id = input("Nouveau responsable_id : ")
            max_m = input("Nouveau nb_membres_max : ")
            payload = {}
            if nom: payload["nom"] = nom
            if sport_id: payload["sport_id"] = int(sport_id)
            if resp_id: payload["responsable_id"] = int(resp_id)
            if max_m: payload["nb_membres_max"] = int(max_m)
            r = api_put(f"{BASE_URL}/clubs/{cid}", payload)
            if r.status_code == 200:
                print("Club mis à jour.")
            else:
                print(f"Erreur : {r.json().get('detail', 'Inconnue')}")

        elif choix == "6":
            cid = input("ID du club à supprimer : ")
            confirm = input("Confirmer la suppression ? (o/N) : ")
            if confirm.lower() == "o":
                r = api_delete(f"{BASE_URL}/clubs/{cid}")
                if r.status_code == 200:
                    print("Club supprimé.")
                else:
                    print(f"Erreur : {r.json().get('detail', 'Inconnue')}")

        elif choix == "7":
            cid = input("ID du club : ")
            eid = input("ID de l'élève : ")
            print("Rôles disponibles : membre, capitaine, coach")
            role = input("Rôle (défaut: membre) : ") or "membre"
            r = api_post(f"{BASE_URL}/clubs/{cid}/membres", {"eleve_id": int(eid), "role": role})
            if r.status_code == 201:
                print("Membre ajouté au club.")
            else:
                print(f"Erreur : {r.json().get('detail', 'Inconnue')}")

        elif choix == "8":
            cid = input("ID du club : ")
            eid = input("ID de l'élève à retirer : ")
            confirm = input("Confirmer ? (o/N) : ")
            if confirm.lower() == "o":
                r = api_delete(f"{BASE_URL}/clubs/{cid}/membres/{eid}")
                if r.status_code == 200:
                    print("Membre retiré du club.")
                else:
                    print(f"Erreur : {r.json().get('detail', 'Inconnue')}")

        elif choix == "0":
            break
        else:
            print("Choix invalide. Réessayez.")

# -------------- Menue principal -----------------

def menu():
    while True:
        print("\n=== Menu Admin ===")
        print("1. Élèves")
        print("2. Professeurs")
        print("3. Notes")
        print("4. Dossiers")
        print("5. Instances de cours")
        print("6. Clubs sportifs")
        print("0. Quitter")
        choix = input("> ")

        if choix == "1":
            menu_eleves()
        elif choix == "2":
            menu_profs()
        elif choix == "3":
            menu_notes()
        elif choix == "4":
            menu_dossiers()
        elif choix == "5":
            menu_instances_cours()
        elif choix == "6":
            menu_clubs()
        elif choix == "0":
            print("Au revoir !")
            break
        else:
            print("Choix invalide. Réessayez.")


if __name__ == "__main__":
    if login():
        menu()
