/* ==================================================
   SAÉ 2.01 - Développement d'une application WEB
================================================== */

function configurerCascade(idRegion, idDepartement) {

    const selectRegion = document.getElementById(idRegion);
    const selectDepartement = document.getElementById(idDepartement);

    if (!selectRegion || !selectDepartement) return;

    selectRegion.addEventListener("change", async function () {

        const regionId = this.value;

        selectDepartement.innerHTML =
            '<option value="">-- Choisir un département --</option>';

        if (!regionId) return;

        try {

            const response =
                await fetch(`/api/departements/${regionId}`);

            const departements =
                await response.json();

            departements.forEach(dept => {

                const option =
                    document.createElement("option");

                option.value = dept.id;
                option.textContent =
                    `${dept.code} - ${dept.libelle}`;

                selectDepartement.appendChild(option);
            });

        } catch (erreur) {

            console.error(
                "Erreur chargement départements :",
                erreur
            );

        }

    });

}

document.addEventListener("DOMContentLoaded", () => {

    /* Analyse Effectifs */
    configurerCascade(
        "region_effectif",
        "departement_effectif"
    );

    /* Analyse Honoraires */
    configurerCascade(
        "region_honoraires",
        "departement_honoraires"
    );

    /* Analyse Prescriptions */
    configurerCascade(
        "region_prescription",
        "departement_prescription"
    );

    /* Page Comparaison */
    configurerCascade(
        "region1_id",
        "departement1_id"
    );

    configurerCascade(
        "region2_id",
        "departement2_id"
    );

});