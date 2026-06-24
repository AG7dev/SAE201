function afficherAnalyse(id) {

    document.querySelectorAll(".bloc-analyse").forEach(section => {
        section.classList.add("cache");
    });

    document.getElementById(id).classList.remove("cache");

}