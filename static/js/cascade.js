/* 
  ==================================================
    SAÉ 2.01 - Développement d'une application WEB
  ==================================================
*/

/* Fichier JavaScript principal pour l'application web de la SAE 2.01 */

document.getElementById("region").addEventListener("change", async (e) => {
    const regionId = e.target.value;
    const selectDept = document.getElementById("departement");

    // Réinitialisation de la liste des départements
    selectDept.innerHTML = '<option value="">-- Choisir --</option>';
    if (!regionId) return;

    // Requête AJAX vers l'API pour récupérer les départements de la région sélectionnée
    const response = await fetch(`/api/departements/${regionId}`);
    const depts = await response.json();

    // Injection des départements dans la liste déroulante
    for (const dept of depts) {
        const opt = document.createElement("option");
        opt.value = dept.id;
        opt.textContent = `${dept.code} – ${dept.libelle}`;
        selectDept.appendChild(opt);
    }
});