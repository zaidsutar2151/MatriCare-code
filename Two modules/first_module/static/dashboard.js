// ===== Live Patient Monitoring Dashboard =====

// Parameter names
const featureNames = ["SysBP", "DiaBP", "HR", "Temp", "SpO2", "RR", "FHR", "Toco"];
const charts = {};
let running = false;

// Initialize all parameter charts
featureNames.forEach(name => {
    const ctx = document.getElementById(name).getContext("2d");
    charts[name] = new Chart(ctx, {
        type: "line",
        data: {
            labels: [],
            datasets: [{
                label: name,
                data: [],
                borderColor: "#007bff",
                borderWidth: 2,
                fill: false,
                tension: 0.3,
                pointRadius: 2
            }]
        },
        options: {
            responsive: true,
            animation: false,
            scales: {
                x: {
                    ticks: { display: false }
                },
                y: {
                    beginAtZero: false,
                    grid: { color: "rgba(0,0,0,0.05)" }
                }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });
});

// Function to fetch prediction and update dashboard
async function updateData() {
    if (!running) return;

    try {
        const response = await fetch("/predict");
        const data = await response.json();

        // Update prediction status display
        const predictionElem = document.getElementById("prediction");
        const box = document.getElementById("predictionBox");

        predictionElem.textContent = data.prediction;
        predictionElem.style.color = data.color;
        box.style.background = data.color + "33"; // translucent tint

        // Update each parameter chart
        featureNames.forEach(name => {
            const chart = charts[name];
            const newValue = data.features[name];
            const now = new Date().toLocaleTimeString().split(" ")[0];

            chart.data.labels.push(now);
            chart.data.datasets[0].data.push(newValue);

            // Keep max 15 points on chart
            if (chart.data.labels.length > 15) {
                chart.data.labels.shift();
                chart.data.datasets[0].data.shift();
            }

            // Change line color to match prediction state
            chart.data.datasets[0].borderColor = data.color;

            chart.update();
        });

    } catch (err) {
        console.error("Error updating data:", err);
    }

    // Repeat after 1.5 seconds
    setTimeout(updateData, 1500);
}

// Handle start/stop button
document.getElementById("startBtn").addEventListener("click", () => {
    running = !running;
    const btn = document.getElementById("startBtn");

    if (running) {
        btn.textContent = "⏸️ Stop Monitoring";
        btn.style.background = "#dc3545";
        updateData();
    } else {
        btn.textContent = "▶️ Start Monitoring";
        btn.style.background = "#007bff";
    }
});
