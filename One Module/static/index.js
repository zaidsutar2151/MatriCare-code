document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("healthForm");
  const resultBox = document.getElementById("resultBox");
  const predictBtn = document.getElementById("predictBtn");

  const samples = {
    1: [105, 63, 114, 36, 1, 1, 143, 1, 10, 98, 2, 3, 33, 2800, 3, 1, 1, 2, 1],
    2: [102, 64, 108, 36, 13, 2, 141, 1, 15, 99, 1, 2, 48, 2500, 0, 1, 2, 2, 1],
    3: [137, 108, 117, 45, 20, 14, 179, 8, 24, 114, 21, 17, 78, 3000, 9, 10, 10, 8, 9],
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
      const res = await fetch("/maternal/predict", { method: "POST", body: formData });
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
