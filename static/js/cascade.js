/* 
  ==================================================
    SAÉ 2.01 - Développement d'une application WEB
  ==================================================
*/

/**
 * Gestion de la cascade région → département.
 * Ce script supporte plusieurs paires région / département
 * sur une même page.
 */

function chargerDepartements(regionSelectId, deptSelectId) {
    const regionSelect = document.getElementById(regionSelectId);
    const selectDept = document.getElementById(deptSelectId);

    if (!regionSelect || !selectDept) return;

    regionSelect.addEventListener("change", async (e) => {
        const regionId = e.target.value;
        selectDept.innerHTML = '<option value="">-- Choisir --</option>';

        if (!regionId) return;

        const response = await fetch(`/api/departements/${regionId}`);
        const depts = await response.json();

        for (const dept of depts) {
            const opt = document.createElement("option");
            opt.value = dept.id;
            opt.textContent =
                `${dept.code} – ${dept.libelle}`;

            selectDept.appendChild(opt);
        }
    });
}


// Chargement d'une cascade
chargerDepartements("region", "departement");

// Chargement de deux cascade (Page de comparaison)
chargerDepartements("region1_id", "departement1_id");
chargerDepartements("region2_id", "departement2_id");