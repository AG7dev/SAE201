const { jsPDF } = window.jspdf;

// Fonction en JavaScript qui permet de télécharger le graphique en PDF
document.getElementById("chartJsDownloadButton").addEventListener("click", async () => {
    const canvas = await html2canvas(
        document.getElementById("div-graphique"), { scale: 8 }
    );
    const img = canvas.toDataURL("image/png");
    const doc = new jsPDF();
    console.log("clique détécté");
    doc.addImage(img, "PNG", 10, 10, 190, 100);
    doc.save("test.pdf");
});