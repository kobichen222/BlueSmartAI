<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
  <meta charset="UTF-8">
  <title>ShotMark AI</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body {
      font-family: Arial, sans-serif;
      background: #f4f7fc;
      margin: 0;
      padding: 20px;
      text-align: center;
    }

    h1 {
      color: #003366;
      margin-bottom: 10px;
    }

    input, button {
      padding: 10px;
      margin: 10px;
      font-size: 16px;
      border-radius: 6px;
    }

    #result {
      margin-top: 20px;
      padding: 20px;
      background: #fff;
      border-radius: 10px;
      box-shadow: 0 2px 10px rgba(0,0,0,0.1);
      direction: rtl;
    }

    img {
      max-width: 100%;
      margin-top: 15px;
      border: 2px solid #007bff;
      border-radius: 8px;
    }

    .score {
      font-size: 22px;
      color: green;
    }

    canvas {
      margin-top: 30px;
    }
  </style>
</head>
<body>

  <h1>ShotMark AI</h1>
  <input type="file" id="imageInput" accept="image/*">
  <button onclick="analyzeImage()">שלח לניתוח</button>

  <div id="result" style="display:none;">
    <p id="aiScore" class="score"></p>
    <p id="hitCount"></p>
    <p id="summary"></p>
    <p id="details"></p>
    <img id="resultImage" src="" hidden>
    <canvas id="hitChart" width="300" height="150"></canvas>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <script>
    async function analyzeImage() {
      const input = document.getElementById('imageInput');
      const file = input.files[0];
      if (!file) return alert("יש לבחור תמונה קודם");

      const formData = new FormData();
      formData.append("image", file);

      const res = await fetch("/api/analyze", {
        method: "POST",
        body: formData
      });

      const data = await res.json();
      if (data.status !== "success") {
        alert(data.message || "שגיאה לא צפויה");
        return;
      }

      document.getElementById("result").style.display = "block";
      document.getElementById("aiScore").textContent = `AI SCORE: ${data.score || 0}/100`;
      document.getElementById("hitCount").textContent = `פגיעות חוקיות: ${data.hits}`;
      document.getElementById("summary").textContent = data.message;
      document.getElementById("details").textContent =
        `יורה: ${data.shooter || "לא ידוע"} | נשק: ${data.weapon || "לא צויין"} | מרחק: ${data.distance || "לא ידוע"} | תאריך: ${data.timestamp || ""}`;

      const img = document.getElementById("resultImage");
      img.src = data.image_url;
      img.hidden = false;

      const ctx = document.getElementById("hitChart").getContext("2d");
      new Chart(ctx, {
        type: 'bar',
        data: {
          labels: ['פגיעות'],
          datasets: [{
            label: 'מספר הפגיעות',
            data: [data.hits],
            backgroundColor: '#007bff'
          }]
        },
        options: {
          scales: { y: { beginAtZero: true } }
        }
      });
    }
  </script>
</body>
</html>