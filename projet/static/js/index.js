const btnEleves = document.getElementById("btn-eleves");
const btnAccueil = document.getElementById("btn-accueil");
const contentArea = document.getElementById("content-area");

btnAccueil.addEventListener("click", () => {
    contentArea.innerHTML = `<p>Cliquez sur "Élèves" pour gérer la liste des élèves.</p>`;
});

btnEleves.addEventListener("click", async () => {
    // Charge le template partiel de la liste élèves
    const eleveTemplate = await fetch('/eleve/template').then(res => res.text());
    contentArea.innerHTML = eleveTemplate;

    // Charge la liste des élèves via API
    loadEleves();

    // Configure bouton Ajouter
    document.getElementById("btn-ajouter").addEventListener("click", () => {
        alert("Ici tu pourras afficher le formulaire d'ajout !");
    });
});

async function loadEleves() {
    const res = await fetch("/eleve/");
    const eleves = await res.json();

    const ul = document.getElementById("eleves-list");
    ul.innerHTML = "";

    eleves.forEach(eleve => {
        const li = document.createElement("li");
        li.textContent = `ID: ${eleve.id} | Nom: ${eleve.nom} | Age: ${eleve.age}`;
        ul.appendChild(li);
    });
}