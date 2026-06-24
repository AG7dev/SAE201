/* 
  ==================================================
    SAÉ 2.01 - Développement d'une application WEB
  ==================================================
*/

/* Fichier JavaScript pour le téléchargement d'un graphique HTML en PDF via html2canvas + jsPDF */

const { jsPDF } = window.jspdf;

// Téléchargement d'un graphique HTML en PDF via html2canvas + jsPDF
document.getElementById("chartJsDownloadButton").addEventListener("click", async () => {
    const canvas = await html2canvas(
        document.getElementById("div-graphique"),
        { scale: 8 } // augmentation de la résolution de l'image générée
    );

    // Conversion du canvas en image exploitable par jsPDF
    const img = canvas.toDataURL("image/png");

    const doc = new jsPDF();

    // Insertion de l'image dans le PDF (position + dimensions)
    doc.addImage(img, "PNG", 10, 10, 190, 100);

    // Téléchargement du fichier PDF généré
    doc.save("graphique.pdf");
});