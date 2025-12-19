const canvas = document.getElementById('diskUsageCanvas');
const diskUsagePercentage = 100 - parseFloat(canvas.dataset.percentageFree);

// const originalWidth = 800; 
// const originalHeight = 400;

function resizeCanvas() {
    const container = canvas.parentElement;
    const containerWidth = container.clientWidth;

    canvas.width = containerWidth;
    canvas.height = containerWidth / 2;

    console.log('Resized canvas to', canvas.width, 'x', canvas.height);
    
    drawDiskUsageChart('diskUsageCanvas', diskUsagePercentage);
}

function drawDiskUsageChart(canvasId, usagePercentage) {
    const canvas = document.getElementById(canvasId);
    const ctx = canvas.getContext('2d');
    
    const width = canvas.width;
    const height = canvas.height;
    const radius = Math.min(width, height) / 2;

    ctx.clearRect(0, 0, width, height);
    
    // Centre du cercle
    const centerX = width / 2;
    const centerY = height / 2;
    
    // Couleurs
    const usedColor = '#789779';
    const freeColor = '#F1E8DC';
    
    // Angles pour chaque partie du graphique
    const endAngleUsed = (usagePercentage / 100) * 2 * Math.PI;
    const startAngleFree = endAngleUsed;
    const endAngleFree = 2 * Math.PI;

    // Dessin de la partie "utilisée"
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, 0, endAngleUsed);
    ctx.lineTo(centerX, centerY); // Dessine vers le centre
    ctx.fillStyle = usedColor;
    ctx.fill();
    
    // Dessin de la partie "libre"
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, startAngleFree, endAngleFree);
    ctx.lineTo(centerX, centerY); // Dessine vers le centre
    ctx.fillStyle = freeColor;
    ctx.fill();
    
    // Cercle interne pour créer un effet "anneau"
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius * 0.6, 0, 2 * Math.PI);
    ctx.fillStyle = 'rgb(224,213,194)';
    ctx.fill();

    // Ajout du text pourcentage comme etiquette sur la partie utilisée
    const fontSize = Math.max(14, radius * 0.15); // Minimum 14px
    ctx.fillStyle = "#000000";
    ctx.font = `bold ${fontSize}px Arial`;
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText(`${usagePercentage.toFixed(2)}%`, centerX, centerY);

    // Légende au centre à droite du graphique 
    const legendX = Math.min(centerX - radius, 20); // Ajustement auto
    const legendY = Math.max(centerY, radius * 0.5);

    // Taille des rectangles qui s'adapte à la taille du disk
    const legendWidth = Math.max(12, radius * 0.1); 
    const legendHeight = Math.max(8, radius * 0.05);

    const legendFontSize = Math.max(10, radius * 0.08);
    ctx.font = `bold ${legendFontSize}px Arial`;
    const textSpacing = Math.max(5, radius * 0.3);

    // Dessiner la légende pour "Utilisé"
    ctx.fillStyle = usedColor;
    ctx.fillRect(legendX, legendY, legendWidth, legendHeight);
    ctx.fillStyle = "#000000";
    ctx.fillText("Utilisé", legendX + legendWidth + textSpacing, legendY + legendHeight / 2);

    // Dessiner la légende pour "Libre"
    ctx.fillStyle = freeColor;
    ctx.fillRect(legendX, legendY + legendHeight * 2, legendWidth, legendHeight);
    ctx.fillStyle = "#000000";
    ctx.fillText("Libre", legendX + legendWidth + textSpacing, legendY + legendHeight * 2 + legendHeight / 2);
    
}

resizeCanvas();
window.addEventListener("resize", resizeCanvas);