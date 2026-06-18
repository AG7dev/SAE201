/* ==================================================
    SAÉ 2.01 - Développement d'une application WEB
  ==================================================
*/

/* Fichier JavaScript principal pour l'application web de la SAE 2.01 */

// Fonction générique pour lier un sélecteur de région à un sélecteur de département
function configurerCascade(idRegion, idDepartement) {
    const selectRegion = document.getElementById(idRegion);
    const selectDept = document.getElementById(idDepartement);

    // On vérifie que les deux éléments existent bien sur la page avant de continuer
    if (!selectRegion || !selectDept) return;

    selectRegion.addEventListener("change", async (e) => {
        const regionId = e.target.value;

        // Réinitialisation de la liste des départements
        selectDept.innerHTML = '<option value="">-- Choisir --</option>';
        if (!regionId) return;

        try {
            // Requête AJAX vers l'API pour récupérer les départements de la région sélectionnée
            const response = await fetch(`/api/departements/${regionId}`);
            if (!response.ok) throw new Error("Erreur lors de la récupération des données");
            
            const depts = await response.json();

            // Injection des départements dans la liste déroulante
            for (const dept of depts) {
                const opt = document.createElement("option");
                opt.value = dept.id;
                opt.textContent = `${dept.code} – ${dept.libelle}`;
                selectDept.appendChild(opt);
            }
        } catch (error) {
            console.error("Erreur Cascade JS :", error);
            selectDept.innerHTML = '<option value="">Erreur de chargement</option>';
        }
    });
}

// On attend que la page soit bien chargée, puis on applique la logique aux deux formulaires
document.addEventListener("DOMContentLoaded", () => {
    // Application pour le premier formulaire (Effectifs) -> ID region0 et departement0
    configurerCascade("region0", "departement0");

    // Application pour le second formulaire (Prescriptions) -> ID region1 et departement1
    configurerCascade("region1", "departement1");
});