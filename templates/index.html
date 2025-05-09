<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
  <meta charset="UTF-8">
  <title>ShotMark AI - ניתוח ירי</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    body {
      font-family: Arial, sans-serif;
      background: #eef3f9;
      color: #222;
      text-align: center;
      padding: 20px;
    }
    h1 { color: #0057b7; }
    input, button {
      font-size: 16px;
      padding: 10px;
      margin: 8px auto;
      width: 90%;
      max-width: 400px;
      border-radius: 6px;
      border: 1px solid #ccc;
      display: block;
      box-sizing: border-box;
    }
    button {
      background-color: #0057b7;
      color: white;
      border: none;
      cursor: pointer;
    }
    button:hover {
      background-color: #003e8a;
    }
    #result { margin-top: 20px; font-size: 18px; }
    img {
      margin-top: 15px;
      max-width: 100%;
      border: 2px solid #0057b7;
      border-radius: 10px;
    }
    .summary-table {
      margin: 20px auto;
      border-collapse: collapse;
      width: 95%;
      max-width: 500px;
      background: #fff;
    }
    .summary-table td, .summary-table th {
      border: 1px solid #ddd;
      padding: 8px;
    }
    .summary-table th {
      background-color: #f2f2f2;
      font-weight: bold;
    }
    .actions {
      margin-top: 20px;
    }
    .actions button { margin: 5px; width: 48%; }
  </style>
</head>
<body>

  <h1>🔵 ShotMark AI</h1>
  <p>מדריך ירי חכם – ניתוח פגיעות בזמן אמת</p>

  <input type="text" id="shooter" placeholder="שם יורה (למשל: עזרא)">
  <input type="text" id="weapon" placeholder="סוג נשק (למשל: Glock 19)">
  <input type="text" id="distance" placeholder="מרחק מהמטרה (מטרים)">
  <input type="file" id="imageInput" accept="image/*">
  <button onclick="analyzeImage()">שלח לניתוח</button>

  <div id="result"></div>
  <img id="resultImage" hidden>

  <div class="actions" id="actions" style="display:none;">
    <button onclick="window.print()">הדפס</button>
    <button onclick="downloadImage()">שמור כתמונה</button>
  </div>

  <script>
    async function analyzeImage() {
      const file = document.getElementById("imageInput").files[0];
      const shooter = document.getElementById("shooter").value;
      const weapon = document.getElementById("weapon").value;
      const distance = document.getElementById("distance").value;

      if (!file) {
        alert("נא לבחור תמונה לניתוח.");
        return;
      }

      const formData = new FormData();
      formData.append("image", file);
      formData.append("shooter", shooter);
      formData.append("weapon", weapon);
      formData.append("distance", distance);

      const resultDiv = document.getElementById("result");
      resultDiv.innerHTML = "⏳ ניתוח...";
      document.getElementById("resultImage").hidden = true;

      try {
        const response = await fetch("/api/analyze", {
          method: "POST",
          body: formData
        });
        const data = await response.json();

        if (data.status === "success") {
          const summaryTable = `
            <table class="summary-table">
              <tr><th>שם יורה</th><td>${data.shooter}</td></tr>
              <tr><th>נשק</th><td>${data.weapon}</td></tr>
              <tr><th>מרחק</th><td>${data.distance} מטר</td></tr>
              <tr><th>פגיעות</th><td>${data.hits}</td></tr>
              <tr><th>תאריך</th><td>${data.timestamp}</td></tr>
              <tr><th>הערכת AI</th><td>${generateAnalysis(data.hits)}</td></tr>
            </table>
          `;
          resultDiv.innerHTML = summaryTable;
          const img = document.getElementById("resultImage");
          img.src = data.image_url;
          img.hidden = false;
          document.getElementById("actions").style.display = "block";
        } else {
          resultDiv.innerHTML = "שגיאה: " + data.message;
        }
      } catch (error) {
        resultDiv.innerHTML = "שגיאה: " + error.message;
      }
    }

    function generateAnalysis(hits) {
      if (hits >= 15) return "ירי מדויק מאוד. שליטה מעולה.";
      if (hits >= 10) return "פגיעות טובות. לשפר ריכוז.";
      if (hits >= 5) return "ירי בינוני. יש לעבוד על יציבות.";
      return "נדרשת עבודה בסיסית על אחיזה ותנוחה.";
    }

    function downloadImage() {
      const img = document.getElementById("resultImage");
      const link = document.createElement("a");
      link.href = img.src;
      link.download = "shotmark_result.jpg";
      link.click();
    }
  </script>

</body>
</html>