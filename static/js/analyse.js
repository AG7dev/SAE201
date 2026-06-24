function afficherAnalyse(id, bouton) {

    document.querySelectorAll(".bloc-analyse").forEach(section => {
        section.classList.add("cache");
    });

    document.getElementById(id).classList.remove("cache");

    document.querySelectorAll(".menu-analyse button").forEach(btn => {
        btn.classList.remove("onglet-actif");
    });

    bouton.classList.add("onglet-actif");
}