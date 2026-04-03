import requests
import os
import sys

BASE_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

# ─────────────────────────────────────────
# COULEURS TERMINAL
# ─────────────────────────────────────────

RESET   = "\033[0m"
BOLD    = "\033[1m"
CYAN    = "\033[96m"
GREEN   = "\033[92m"
YELLOW  = "\033[93m"
RED     = "\033[91m"
MAGENTA = "\033[95m"
BLUE    = "\033[94m"
WHITE   = "\033[97m"
DIM     = "\033[2m"


def clr(text, color):
    return f"{color}{text}{RESET}"

def titre(text):
    largeur = 60
    ligne = "─" * largeur
    print(f"\n{clr(ligne, CYAN)}")
    print(f"{clr('  ' + text.upper(), BOLD + CYAN)}")
    print(f"{clr(ligne, CYAN)}")

def sous_titre(text):
    print(f"\n{clr('  ▶  ' + text, BOLD + YELLOW)}")

def succes(msg):
    print(f"\n  {clr('✓', GREEN + BOLD)}  {clr(msg, GREEN)}")

def erreur(msg):
    print(f"\n  {clr('✗', RED + BOLD)}  {clr(msg, RED)}")

def info(label, valeur):
    print(f"  {clr(label + ':', CYAN)} {valeur}")

def separateur():
    print(f"  {clr('·' * 50, DIM)}")

def saisie(prompt):
    return input(f"  {clr('›', MAGENTA)} {prompt}: ").strip()

def saisie_optionnelle(prompt):
    v = input(f"  {clr('›', DIM)} {prompt} {clr('(laisser vide pour ignorer)', DIM)}: ").strip()
    return v if v else None

def afficher_menu(options: list[tuple[str, str]]):
    print()
    for key, label in options:
        print(f"    {clr(f'[{key}]', BOLD + YELLOW)}  {label}")
    print()

def confirmer(msg="Confirmer ?") -> bool:
    rep = input(f"  {clr('?', YELLOW + BOLD)}  {msg} {clr('(o/N)', DIM)}: ").strip().lower()
    return rep in ("o", "oui", "y", "yes")

def pause():
    input(f"\n  {clr('Appuyez sur Entrée pour continuer…', DIM)}")


# ─────────────────────────────────────────
# CLIENT API
# ─────────────────────────────────────────

def api_get(endpoint):
    try:
        r = requests.get(f"{BASE_URL}{endpoint}")
        r.raise_for_status()
        return r.json()
    except requests.exceptions.ConnectionError:
        erreur("Impossible de joindre l'API. Vérifiez qu'elle est lancée.")
        return None
    except Exception as e:
        erreur(f"Erreur API : {e}")
        return None

def api_post(endpoint, data):
    try:
        r = requests.post(f"{BASE_URL}{endpoint}", json=data)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.ConnectionError:
        erreur("Impossible de joindre l'API.")
        return None
    except Exception as e:
        try:
            detail = r.json().get("detail", str(e))
        except Exception:
            detail = str(e)
        erreur(f"Erreur : {detail}")
        return None

def api_put(endpoint, data):
    try:
        r = requests.put(f"{BASE_URL}{endpoint}", json=data)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.ConnectionError:
        erreur("Impossible de joindre l'API.")
        return None
    except Exception as e:
        try:
            detail = r.json().get("detail", str(e))
        except Exception:
            detail = str(e)
        erreur(f"Erreur : {detail}")
        return None

def api_delete(endpoint):
    try:
        r = requests.delete(f"{BASE_URL}{endpoint}")
        r.raise_for_status()
        return r.json()
    except requests.exceptions.ConnectionError:
        erreur("Impossible de joindre l'API.")
        return None
    except Exception as e:
        erreur(f"Erreur : {e}")
        return None


# ─────────────────────────────────────────
# AFFICHAGE TABLEAUX
# ─────────────────────────────────────────

def afficher_tableau(headers: list[str], rows: list[list], widths: list[int] = None):
    if not widths:
        widths = [max(len(str(headers[i])), max((len(str(r[i])) for r in rows), default=0)) + 2
                  for i in range(len(headers))]
    ligne = "  ┌" + "┬".join("─" * w for w in widths) + "┐"
    milieu = "  ├" + "┼".join("─" * w for w in widths) + "┤"
    bas = "  └" + "┴".join("─" * w for w in widths) + "┘"
    fmt_header = "  │" + "│".join(f"{clr(str(h).center(w), BOLD + CYAN)}" for h, w in zip(headers, widths)) + "│"
    print(clr(ligne, DIM))
    print(fmt_header)
    print(clr(milieu, DIM))
    for row in rows:
        fmt_row = "  │" + "│".join(str(v).center(w) for v, w in zip(row, widths)) + "│"
        print(fmt_row)
    print(clr(bas, DIM))


# ─────────────────────────────────────────
# SECTION : ÉLÈVES
# ─────────────────────────────────────────

def menu_eleves():
    while True:
        titre("Gestion des Élèves")
        afficher_menu([
            ("1", "Lister tous les élèves"),
            ("2", "Voir un élève"),
            ("3", "Ajouter un élève"),
            ("4", "Modifier un élève"),
            ("5", "Supprimer un élève"),
            ("6", "Élèves avec avertissement"),
            ("7", "Élèves avec bonne moyenne (> 12)"),
            ("8", "Absences d'un élève"),
            ("0", "Retour"),
        ])
        choix = saisie("Choix")

        if choix == "1":
            titre("Liste des Élèves")
            data = api_get("/eleve/")
            if data:
                rows = [[e["id"], e["nom"], e["age"]] for e in data]
                afficher_tableau(["ID", "Nom", "Âge"], rows)
            pause()

        elif choix == "2":
            titre("Détail Élève")
            eid = saisie("ID de l'élève")
            data = api_get(f"/eleve/{eid}")
            if data:
                separateur()
                info("ID", data["id"])
                info("Nom", data["nom"])
                info("Email", data["email"])
                info("Âge", data["age"])
                info("Promotion ID", data.get("promotion_id", "—"))
                # Notes de l'élève
                notes = api_get(f"/notes/{eid}")
                if notes:
                    sous_titre("Notes")
                    rows = [[n["matiere"], n["note"]] for n in notes]
                    afficher_tableau(["Matière", "Note"], rows)
                separateur()
            pause()

        elif choix == "3":
            titre("Ajouter un Élève")
            nom = saisie("Nom complet")
            email = saisie("Email")
            age = saisie("Âge")
            prom_id = saisie_optionnelle("ID Promotion")

            payload = {"nom": nom, "email": email, "age": int(age)}
            if prom_id:
                payload["promotion_id"] = int(prom_id)

            res = api_post("/eleve/", payload)
            if res:
                succes(f"Élève créé avec l'ID {res['id']}")
            pause()

        elif choix == "4":
            titre("Modifier un Élève")
            eid = saisie("ID de l'élève à modifier")
            existing = api_get(f"/eleve/{eid}")
            if not existing:
                pause()
                continue
            info("Actuel", f"{existing['nom']} | {existing['email']} | âge: {existing['age']}")
            print(f"  {clr('Laissez vide pour ne pas modifier', DIM)}")
            nom = saisie_optionnelle(f"Nouveau nom ({existing['nom']})")
            email = saisie_optionnelle(f"Nouvel email ({existing['email']})")
            age = saisie_optionnelle(f"Nouvel âge ({existing['age']})")
            prom_id = saisie_optionnelle(f"Nouvelle promotion_id ({existing.get('promotion_id','—')})")

            payload = {}
            if nom: payload["nom"] = nom
            if email: payload["email"] = email
            if age: payload["age"] = int(age)
            if prom_id: payload["promotion_id"] = int(prom_id)

            res = api_put(f"/eleve/{eid}", payload)
            if res:
                succes("Élève mis à jour !")
            pause()

        elif choix == "5":
            titre("Supprimer un Élève")
            eid = saisie("ID de l'élève à supprimer")
            existing = api_get(f"/eleve/{eid}")
            if not existing:
                pause()
                continue
            erreur(f"Vous allez supprimer : {existing['nom']}")
            if confirmer("Confirmer la suppression ?"):
                res = api_delete(f"/eleve/{eid}")
                if res:
                    succes("Élève supprimé.")
            pause()

        elif choix == "6":
            titre("Élèves avec Avertissement")
            data = api_get("/eleve/avertis")
            if data:
                rows = []
                for e in data:
                    av_t = clr("OUI", RED) if e["avertissement_travail"] else "non"
                    av_c = clr("OUI", RED) if e["avertissement_comportement"] else "non"
                    rows.append([e["id"], e["nom"], av_t, av_c])
                afficher_tableau(["ID", "Nom", "Av. Travail", "Av. Comportement"], rows)
            pause()

        elif choix == "7":
            titre("Élèves avec Bonne Moyenne")
            data = api_get("/eleve/bonne_notes")
            if data:
                rows = [[i+1, e["nom"], f"{e['moyenne']:.2f}/20"] for i, e in enumerate(data)]
                afficher_tableau(["Classement", "Nom", "Moyenne"], rows)
            pause()

        elif choix == "8":
            titre("Absences d'un Élève")
            eid = saisie("ID de l'élève")
            data = api_get(f"/eleve/{eid}/absence")
            if data:
                separateur()
                info("Élève", data["eleve"])
                info("Total", f"{data['affichage']} ({data['total_minutes']} minutes)")
                separateur()
            pause()

        elif choix == "0":
            break


# ─────────────────────────────────────────
# SECTION : PROFS
# ─────────────────────────────────────────

def menu_profs():
    while True:
        titre("Gestion des Professeurs")
        afficher_menu([
            ("1", "Lister tous les profs"),
            ("2", "Voir un prof"),
            ("3", "Ajouter un prof"),
            ("4", "Modifier un prof"),
            ("5", "Supprimer un prof"),
            ("6", "Profs sévères (moyenne donnée < 8)"),
            ("0", "Retour"),
        ])
        choix = saisie("Choix")

        if choix == "1":
            titre("Liste des Professeurs")
            data = api_get("/prof/")
            if data:
                rows = [[p["id"], p["nom"], p["email"], p["age"]] for p in data]
                afficher_tableau(["ID", "Nom", "Email", "Âge"], rows)
            pause()

        elif choix == "2":
            titre("Détail Professeur")
            pid = saisie("ID du prof")
            data = api_get(f"/prof/{pid}")
            if data:
                separateur()
                info("ID", data["id"])
                info("Nom", data["nom"])
                info("Email", data["email"])
                info("Âge", data["age"])
                separateur()
            pause()

        elif choix == "3":
            titre("Ajouter un Professeur")
            nom = saisie("Nom complet")
            email = saisie("Email")
            age = saisie("Âge")
            res = api_post("/prof/", {"nom": nom, "email": email, "age": int(age)})
            if res:
                succes(f"Professeur créé avec l'ID {res['id']}")
            pause()

        elif choix == "4":
            titre("Modifier un Professeur")
            pid = saisie("ID du prof à modifier")
            existing = api_get(f"/prof/{pid}")
            if not existing:
                pause()
                continue
            info("Actuel", f"{existing['nom']} | {existing['email']} | âge: {existing['age']}")
            nom = saisie_optionnelle(f"Nouveau nom")
            email = saisie_optionnelle(f"Nouvel email")
            age = saisie_optionnelle(f"Nouvel âge")
            payload = {}
            if nom: payload["nom"] = nom
            if email: payload["email"] = email
            if age: payload["age"] = int(age)
            res = api_put(f"/prof/{pid}", payload)
            if res:
                succes("Professeur mis à jour !")
            pause()

        elif choix == "5":
            titre("Supprimer un Professeur")
            pid = saisie("ID du prof à supprimer")
            existing = api_get(f"/prof/{pid}")
            if not existing:
                pause()
                continue
            erreur(f"Vous allez supprimer : {existing['nom']}")
            if confirmer():
                res = api_delete(f"/prof/{pid}")
                if res:
                    succes("Professeur supprimé.")
            pause()

        elif choix == "6":
            titre("Professeurs Sévères")
            data = api_get("/prof/severe")
            if data:
                if not data:
                    info("Info", "Aucun prof sévère détecté.")
                else:
                    rows = [[p["id"], p["nom"], f"{p['moyenne_notes_donnees']:.2f}/20"] for p in data]
                    afficher_tableau(["ID", "Nom", "Moy. notes données"], rows)
            pause()

        elif choix == "0":
            break


# ─────────────────────────────────────────
# SECTION : NOTES
# ─────────────────────────────────────────

def menu_notes():
    while True:
        titre("Gestion des Notes")
        afficher_menu([
            ("1", "Lister toutes les notes"),
            ("2", "Notes par type (élève/prof/cours/promotion)"),
            ("3", "Ajouter une note"),
            ("4", "Modifier une note (uniquement à la hausse)"),
            ("0", "Retour"),
        ])
        choix = saisie("Choix")

        if choix == "1":
            titre("Toutes les Notes")
            data = api_get("/notes/")
            if data:
                rows = [[n["id"], n["eleve_id"], n["cours_id"], n["prof_id"], f"{n['note']:.2f}"] for n in data]
                afficher_tableau(["ID", "Élève ID", "Cours ID", "Prof ID", "Note"], rows)
            pause()

        elif choix == "2":
            titre("Notes par Type")
            print(f"  Types disponibles : {clr('eleve', CYAN)}, {clr('prof', CYAN)}, {clr('cours', CYAN)}, {clr('promotion', CYAN)}")
            par = saisie("Type")
            data = api_get(f"/note?par={par}")
            if data:
                for cle, notes in data.items():
                    sous_titre(str(cle))
                    for n in notes:
                        print(f"    {clr('•', MAGENTA)} {n['nomEleve']} | {n['cours']} | prof: {n['nomProf']} | {clr(str(n['note']), BOLD)}/20")
            pause()

        elif choix == "3":
            titre("Ajouter une Note")
            # Afficher élèves et cours disponibles
            eleves = api_get("/eleve/") or []
            cours = api_get("/cours/") or []
            profs = api_get("/prof/") or []

            sous_titre("Élèves disponibles")
            for e in eleves:
                print(f"    {clr(str(e['id']), YELLOW)} - {e['nom']}")

            sous_titre("Cours disponibles")
            for c in cours:
                print(f"    {clr(str(c['id']), YELLOW)} - {c['nom']}")

            sous_titre("Profs disponibles")
            for p in profs:
                print(f"    {clr(str(p['id']), YELLOW)} - {p['nom']}")

            eleve_id = saisie("ID Élève")
            cours_id = saisie("ID Cours")
            prof_id = saisie("ID Prof")
            note = saisie("Note (0-20)")

            res = api_post("/note/", {
                "eleve_id": int(eleve_id),
                "cours_id": int(cours_id),
                "prof_id": int(prof_id),
                "note": float(note)
            })
            if res:
                succes(f"Note {note}/20 ajoutée !")
            pause()

        elif choix == "4":
            titre("Modifier une Note")
            nid = saisie("ID de la note à modifier")
            existing = api_get(f"/note/{nid}")
            if not existing:
                pause()
                continue
            info("Note actuelle", f"{existing['note']}/20")
            nouvelle = saisie("Nouvelle note (doit être >= note actuelle)")
            res = api_put(f"/note/{nid}", {"note": float(nouvelle)})
            if res:
                succes("Note mise à jour !")
            pause()

        elif choix == "0":
            break


# ─────────────────────────────────────────
# SECTION : DOSSIERS
# ─────────────────────────────────────────

def menu_dossiers():
    while True:
        titre("Gestion des Dossiers")
        afficher_menu([
            ("1", "Voir le dossier d'un élève"),
            ("2", "Modifier un dossier"),
            ("0", "Retour"),
        ])
        choix = saisie("Choix")

        if choix == "1":
            titre("Dossier Élève")
            eid = saisie("ID de l'élève")
            data = api_get(f"/dossier/{eid}")
            if data:
                separateur()
                info("Élève", data["nom_eleve"])
                info("Infos", data.get("infos") or "—")
                av_t = clr("OUI ⚠", RED) if data["avertissement_travail"] else clr("non", GREEN)
                av_c = clr("OUI ⚠", RED) if data["avertissement_comportement"] else clr("non", GREEN)
                info("Avertissement travail", av_t)
                info("Avertissement comportement", av_c)
                separateur()
            pause()

        elif choix == "2":
            titre("Modifier un Dossier")
            eid = saisie("ID de l'élève")
            existing = api_get(f"/dossier/{eid}")
            if not existing:
                pause()
                continue
            info("Actuel", existing.get("infos") or "—")
            infos = saisie_optionnelle("Nouvelles infos")
            avt = saisie_optionnelle("Avertissement travail (0 ou 1)")
            avc = saisie_optionnelle("Avertissement comportement (0 ou 1)")
            payload = {}
            if infos: payload["infos"] = infos
            if avt is not None: payload["avertissement_travail"] = int(avt)
            if avc is not None: payload["avertissement_comportement"] = int(avc)
            res = api_put(f"/dossier/{eid}", payload)
            if res:
                succes("Dossier mis à jour !")
            pause()

        elif choix == "0":
            break


# ─────────────────────────────────────────
# SECTION : INSTANCES DE COURS
# ─────────────────────────────────────────

def menu_instances_cours():
    while True:
        titre("Gestion des Instances de Cours")
        afficher_menu([
            ("1", "Lister toutes les instances"),
            ("2", "Voir une instance"),
            ("3", "Ajouter une instance"),
            ("4", "Modifier une instance"),
            ("5", "Supprimer une instance"),
            ("0", "Retour"),
        ])
        choix = saisie("Choix")

        if choix == "1":
            titre("Instances de Cours")
            data = api_get("/instance_cours/")
            if data:
                rows = [[ic["id"], ic["cours"], ic["prof"], str(ic["date"])[:16]] for ic in data]
                afficher_tableau(["ID", "Cours", "Prof", "Date"], rows)
            pause()

        elif choix == "2":
            titre("Détail Instance")
            iid = saisie("ID de l'instance")
            data = api_get(f"/instance_cours/{iid}")
            if data:
                separateur()
                info("ID", data["id"])
                info("Cours ID", data["cours_id"])
                info("Prof ID", data["prof_id"])
                info("Date", data["date"])
                separateur()
            pause()

        elif choix == "3":
            titre("Ajouter une Instance de Cours")
            cours = api_get("/cours/") or []
            profs = api_get("/prof/") or []
            sous_titre("Cours disponibles")
            for c in cours:
                print(f"    {clr(str(c['id']), YELLOW)} - {c['nom']}")
            sous_titre("Profs disponibles")
            for p in profs:
                print(f"    {clr(str(p['id']), YELLOW)} - {p['nom']}")
            cours_id = saisie("ID Cours")
            prof_id = saisie("ID Prof")
            date = saisie("Date (YYYY-MM-DD HH:MM:SS)")
            res = api_post("/instance_cours/", {
                "cours_id": int(cours_id),
                "prof_id": int(prof_id),
                "date": date
            })
            if res:
                succes(f"Instance créée avec l'ID {res['id']}")
            pause()

        elif choix == "4":
            titre("Modifier une Instance de Cours")
            iid = saisie("ID de l'instance")
            existing = api_get(f"/instance_cours/{iid}")
            if not existing:
                pause()
                continue
            cours_id = saisie_optionnelle(f"Nouveau cours_id ({existing['cours_id']})")
            prof_id = saisie_optionnelle(f"Nouveau prof_id ({existing['prof_id']})")
            date = saisie_optionnelle(f"Nouvelle date ({existing['date']})")
            payload = {}
            if cours_id: payload["cours_id"] = int(cours_id)
            if prof_id: payload["prof_id"] = int(prof_id)
            if date: payload["date"] = date
            res = api_put(f"/instance_cours/{iid}", payload)
            if res:
                succes("Instance mise à jour !")
            pause()

        elif choix == "5":
            titre("Supprimer une Instance de Cours")
            iid = saisie("ID de l'instance à supprimer")
            if confirmer("Confirmer la suppression ?"):
                res = api_delete(f"/instance_cours/{iid}")
                if res:
                    succes("Instance supprimée.")
            pause()

        elif choix == "0":
            break


# ─────────────────────────────────────────
# SECTION : CLUBS (fonctionnalité supplémentaire)
# ─────────────────────────────────────────

def menu_clubs():
    while True:
        titre("Gestion des Clubs Sportifs")
        afficher_menu([
            ("1", "Lister tous les clubs"),
            ("2", "Membres d'un club"),
            ("3", "Stats d'un club"),
            ("4", "Créer un club"),
            ("5", "Modifier un club"),
            ("6", "Supprimer un club"),
            ("7", "Ajouter un membre"),
            ("8", "Retirer un membre"),
            ("0", "Retour"),
        ])
        choix = saisie("Choix")

        if choix == "1":
            titre("Liste des Clubs")
            data = api_get("/clubs/")
            if data:
                rows = [[c["id"], c["nom"], c["sport"], c.get("responsable") or "—", c.get("nb_membres_max") or "—"] for c in data]
                afficher_tableau(["ID", "Nom", "Sport", "Responsable", "Max membres"], rows)
            pause()

        elif choix == "2":
            titre("Membres d'un Club")
            cid = saisie("ID du club")
            data = api_get(f"/clubs/{cid}/membres")
            if data:
                sous_titre(data["club"])
                rows = [[m["id"], m["nom"], m["role"], str(m["date_adhesion"])] for m in data["membres"]]
                afficher_tableau(["ID", "Nom", "Rôle", "Adhésion"], rows)
            pause()

        elif choix == "3":
            titre("Statistiques Club")
            cid = saisie("ID du club")
            data = api_get(f"/clubs/{cid}/stats")
            if data:
                separateur()
                info("Club", data["club"])
                info("Membres", data["nb_membres"])
                info("Événements", data["nb_evenements"])
                info("Total participations", data["total_participations"])
                separateur()
            pause()

        elif choix == "4":
            titre("Créer un Club")
            sports = api_get("/sports/") or []
            profs = api_get("/prof/") or []
            sous_titre("Sports disponibles")
            for s in sports:
                print(f"    {clr(str(s['id']), YELLOW)} - {s['nom']}")
            sous_titre("Responsables disponibles (profs)")
            for p in profs:
                print(f"    {clr(str(p['id']), YELLOW)} - {p['nom']}")
            nom = saisie("Nom du club")
            sport_id = saisie("ID Sport")
            resp_id = saisie_optionnelle("ID Responsable (prof)")
            date = saisie_optionnelle("Date de création (YYYY-MM-DD)")
            max_m = saisie_optionnelle("Nombre max de membres")
            payload = {"nom": nom, "sport_id": int(sport_id)}
            if resp_id: payload["responsable_id"] = int(resp_id)
            if date: payload["date_creation"] = date
            if max_m: payload["nb_membres_max"] = int(max_m)
            res = api_post("/clubs/", payload)
            if res:
                succes(f"Club '{nom}' créé avec l'ID {res['id']}")
            pause()

        elif choix == "5":
            titre("Modifier un Club")
            cid = saisie("ID du club")
            nom = saisie_optionnelle("Nouveau nom")
            sport_id = saisie_optionnelle("Nouveau sport_id")
            resp_id = saisie_optionnelle("Nouveau responsable_id")
            max_m = saisie_optionnelle("Nouveau nb_membres_max")
            payload = {}
            if nom: payload["nom"] = nom
            if sport_id: payload["sport_id"] = int(sport_id)
            if resp_id: payload["responsable_id"] = int(resp_id)
            if max_m: payload["nb_membres_max"] = int(max_m)
            res = api_put(f"/clubs/{cid}", payload)
            if res:
                succes("Club mis à jour !")
            pause()

        elif choix == "6":
            titre("Supprimer un Club")
            cid = saisie("ID du club")
            if confirmer("Confirmer la suppression ?"):
                res = api_delete(f"/clubs/{cid}")
                if res:
                    succes("Club supprimé.")
            pause()

        elif choix == "7":
            titre("Ajouter un Membre à un Club")
            cid = saisie("ID du club")
            eid = saisie("ID de l'élève")
            print(f"  Rôles : {clr('membre', CYAN)}, {clr('capitaine', CYAN)}, {clr('coach', CYAN)}")
            role = saisie("Rôle (défaut: membre)") or "membre"
            res = api_post(f"/clubs/{cid}/membres", {"eleve_id": int(eid), "role": role})
            if res:
                succes("Membre ajouté au club !")
            pause()

        elif choix == "8":
            titre("Retirer un Membre d'un Club")
            cid = saisie("ID du club")
            eid = saisie("ID de l'élève à retirer")
            if confirmer():
                res = api_delete(f"/clubs/{cid}/membres/{eid}")
                if res:
                    succes("Membre retiré.")
            pause()

        elif choix == "0":
            break


# ─────────────────────────────────────────
# MENU PRINCIPAL
# ─────────────────────────────────────────

def afficher_banniere():
    print(clr("""
  ╔═══════════════════════════════════════════════════════╗
  ║                                                       ║
  ║         🎓  ADMINISTRATION ÉCOLE  🎓                  ║
  ║                                                       ║
  ║         Interface de gestion – API FastAPI            ║
  ║                                                       ║
  ╚═══════════════════════════════════════════════════════╝
""", CYAN + BOLD))

def menu_principal():
    afficher_banniere()
    while True:
        titre("Menu Principal")
        afficher_menu([
            ("1", "👤  Élèves"),
            ("2", "📚  Professeurs"),
            ("3", "📝  Notes"),
            ("4", "📂  Dossiers"),
            ("5", "🗓  Instances de Cours"),
            ("6", "⚽  Clubs Sportifs"),
            ("0", "❌  Quitter"),
        ])
        choix = saisie("Votre choix")

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
            print(clr("\n  Au revoir ! 👋\n", CYAN + BOLD))
            sys.exit(0)
        else:
            erreur("Choix invalide, réessayez.")


if __name__ == "__main__":
    menu_principal()
