const BASE_URL = "http://127.0.0.1:8000/eleve";

// Ajouter un élève
document.getElementById("btn-add").addEventListener("click", async () => {
    const nom = document.getElementById("nom").value;
    const email = document.getElementById("email").value;
    const age = parseInt(document.getElementById("age").value);
    const promo = parseInt(document.getElementById("promo").value);

    await fetch(BASE_URL + "/", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({nom, email, age, promotion_id: promo})
    });

    location.reload(); // simple reload pour rafraîchir la liste
});

// Supprimer un élève
async function deleteEleve(id) {
    await fetch(`${BASE_URL}/${id}`, { method: "DELETE" });
    location.reload();
}

document.querySelectorAll(".btn-delete").forEach(btn => {
    btn.addEventListener("click", async () => {
        const eleveId = btn.dataset.id;
        await fetch(`/eleve/${eleveId}`, { method: "DELETE" });
        location.reload(); // pour rafraîchir la liste
    });
});