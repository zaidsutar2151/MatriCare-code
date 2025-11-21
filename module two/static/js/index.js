document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("healthForm");
  const resultBox = document.getElementById("resultBox");
  const predictBtn = document.getElementById("predictBtn");

  const samples = {
    1: [105.07, 63.11, 114.17, 36.75, 1.65, 0.92, 143.25, 1.12, 10.16, 98.76, 2.1, 3.97, 33.63, 2831.39, 3.29, 0.5, 1.78, 2.69, 1.25],
    2: [102.4, 64.01, 108.5, 36.02, 13.04, 2.87, 141.33, 1.6, 15.82, 99.7, 1.11, 2.98, 48.94, 2544.68, 0.19, 1.17, 2.09, 2.97, 1.06],
    3: [137.64, 108.53, 117.56, 45.23, 20.98, 14.88, 179.78, 8.3, 24.81, 114.55, 21.15, 17.37, 78.07, 3011.78, 17.43, 10.96, 23.64, 20.49, 11.59],
  };

  // Load sample data
  document.querySelectorAll(".sample").forEach(btn => {
    btn.addEventListener("click", () => {
      const sample = samples[btn.dataset.sample];
      const inputs = form.querySelectorAll("input[type='number']");
      inputs.forEach((inp, i) => (inp.value = sample[i]));
    });
  });

  // Function to clean LLM output
  const cleanText = (text) => {
    return text
      .replace(/\*\*/g, "")
      .replace(/##/g, "")
      .replace(/\*/g, "")
      .replace(/[\#\_]/g, "")
      .trim();
  };

  // Handle submit
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const formData = new FormData(form);

    // Show loading animation
    predictBtn.disabled = true;
    predictBtn.innerHTML = `<span class="spinner"></span> Analyzing...`;

    try {
      const res = await fetch("/predict", { method: "POST", body: formData });
      const data = await res.json();

      // Show results
      resultBox.classList.remove("hidden");

      const predEl = document.getElementById("predLabel");
      predEl.textContent = data.prediction;
      predEl.className = ""; // reset
      predEl.classList.add("pred", data.prediction.toLowerCase());

      document.getElementById("summary").textContent = cleanText(data.summary);
      document.getElementById("future").textContent = cleanText(data.future);
      document.getElementById("basic").textContent = cleanText(data.basic);
      document.getElementById("advanced").textContent = cleanText(data.advanced);
    } catch (err) {
      alert("⚠️ Something went wrong while analyzing.");
      console.error(err);
    } finally {
      predictBtn.disabled = false;
      predictBtn.textContent = "Predict & Analyze";
    }
  });
});
