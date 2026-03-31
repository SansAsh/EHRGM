const BASE_URL = "http://127.0.0.1:8000";

// Ajouter un élève
document.getElementById("btn-ajouter").addEventListener("click", async () => {
    const nom = document.getElementById("nom").value;
    const email = document.getElementById("email").value;
    const age = parseInt(document.getElementById("age").value);
    const promo = parseInt(document.getElementById("promo").value);
    const message = document.getElementById("message");

    if (!nom || !email || !age || !promo) {
        message.textContent = "Merci de remplir tous les champs !";
        message.style.color = "red";
        return;
    }

    const res = await fetch(`${BASE_URL}/eleve/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nom, email, age, promotion_id: promo })
    });
    const data = await res.json();
    message.textContent = data.message;
    message.style.color = "green";

    document.getElementById("nom").value = "";
    document.getElementById("email").value = "";
    document.getElementById("age").value = "";
    document.getElementById("promo").value = "";
});

// Afficher tous les élèves
document.getElementById("btn-liste").addEventListener("click", async () => {
    const res = await fetch(`${BASE_URL}/eleve/`);
    const data = await res.json();
    const liste = document.getElementById("liste-eleves");
    liste.innerHTML = "";

    data.forEach(eleve => {
        const div = document.createElement("div");
        div.className = "list-item";
        div.textContent = `ID: ${eleve.id} | Nom: ${eleve.nom} | Age: ${eleve.age}`;
        liste.appendChild(div);
    });
});

// Afficher les bonnes notes
document.getElementById("btn-bonne-notes").addEventListener("click", async () => {
    const res = await fetch(`${BASE_URL}/eleve/bonne_notes`);
    const data = await res.json();
    const liste = document.getElementById("liste-bonnes-notes");
    liste.innerHTML = "";

    data.forEach(eleve => {
        const div = document.createElement("div");
        div.className = "list-item";
        div.textContent = `${eleve.nom} | Moyenne: ${eleve.moyenne}`;
        liste.appendChild(div);
    });
});