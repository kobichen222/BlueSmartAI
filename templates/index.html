<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>ShotMark AI</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background: #f0f4f9;
      margin: 0;
      padding: 20px;
      text-align: center;
    }

    .container {
      background: #fff;
      border-radius: 16px;
      padding: 20px;
      max-width: 500px;
      margin: auto;
      box-shadow: 0 0 20px rgba(0,0,0,0.1);
    }

    h1 {
      color: #003366;
    }

    input, button {
      padding: 12px;
      font-size: 16px;
      margin: 10px 5px;
    }

    .result {
      margin-top: 20px;
      font-size: 18px;
    }

    .ai-score {
      font-size: 24px;
      font-weight: bold;
      color: green;
    }

    img {
      max-width: 100%;
      border-radius: 8px;
      margin-top: 15px;
    }

    canvas {
      margin-top: 20px;
    }
  </style>
</head>
<body>

<div class="container">
  <h1>ShotMark AI</h1>
  <p>בחר תמונה או צלם מטרה</p>
  <input type="file" accept="image/*" id="imageInput" capture="environment">
  <br>
  <button onclick="analyze()">שלח לניתוח</button>

  <div class="result" id="resultBox" style="display:none;">
    <p class="ai-score" id="scoreText"></p>
    <p id="messageText"></p>
    <img id="resultImage" src="">
    <canvas id="hitsChart" width="300" height="200"></canvas>
  </div>
</div>

<script>
async function analyze() {
  const input = document.getElementById('imageInput');
  const file = input.files[0];
  if (!file) {
    alert("בחר תמונה קודם");
    return;
  }

  const formData = new FormData();
  formData.append("image", file);

  const res = await fetch("/api/analyze", {
    method: "POST",
    body: formData
  });

  const data = await res.json();
  if (data.status === "success") {
    document.getElementById('resultBox').style.display = 'block';
    document.getElementById('scoreText').innerText = `AI SCORE: ${Math.min(data.hits * 10, 100)}/100`;
    document.getElementById('messageText').innerText = data.message;
    document.getElementById('resultImage').src = data.image_url;

    // גרף פגיעות - אופציונלי בהמשך
    const ctx = document.getElementById("hitsChart").getContext("2d");
    if (window.hitsChartInstance) window.hitsChartInstance.destroy();
    window.hitsChartInstance = new Chart(ctx, {
      type: "bar",
      data: {
        labels: ["פגיעות"],
        datasets: [{
          label: "כמות",
          data: [data.hits],
          backgroundColor: "green"
        }]
      },
      options: {
        responsive: true,
        plugins: { legend: { display: false } }
      }
    });
  } else {
    alert(data.message);
  }
}
</script>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</body>
</html>