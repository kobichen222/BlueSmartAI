<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ShotMark AI</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background: #f4f7fc;
      text-align: center;
      padding: 40px 20px;
      margin: 0;
    }
    h1 {
      color: #0057b7;
      font-size: 28px;
      margin-bottom: 10px;
    }
    p {
      font-size: 16px;
      margin-bottom: 20px;
    }
    input, button {
      padding: 12px;
      font-size: 16px;
      border-radius: 8px;
      margin: 10px auto;
      width: 90%;
      max-width: 400px;
      box-sizing: border-box;
    }
    button {
      background-color: #0057b7;
      color: white;
      border: none;
    }
    button:hover {
      background-color: #004aa3;
    }
    img {
      margin-top: 20px;
      width: 90%;
      max-width: 400px;
      border: 2px solid #0057b7;
      border-radius: 10px;
    }
  </style>
</head>
<body>

  <h1>🔵 ShotMark AI</h1>
  <p>בחר תמונה מהמכשיר לניתוח פגיעות</p>

  <input type="file" id="imageInput" accept="image/*">
  <button onclick="analyzeImage()">שלח לניתוח</button>

  <p id="result"></p>
  <img id="resultImage" src="" alt="" hidden>

  <script>
    async function analyzeImage() {
      const file = document.getElementById('imageInput').files[0];
      if (!file) {
        alert("יש לבחור תמונה לניתוח");
        return;
      }

      const formData = new FormData();
      formData.append("image", file);

      document.getElementById("result").innerText = "⏳ מנתח...";
      document.getElementById("resultImage").hidden = true;

      try {
        const response = await fetch("/api/analyze", {
          method: "POST",
          body: formData
        });

        const data = await response.json();
        if (data.status === "success") {
          document.getElementById("result").innerText = data.message;
          const img = document.getElementById("resultImage");
          img.src = data.image_url;
          img.hidden = false;
        } else {
          document.getElementById("result").innerText = "שגיאה: " + data.message;
        }
      } catch (error) {
        document.getElementById("result").innerText = "שגיאה בהעלאה: " + error.message;
      }
    }
  </script>

</body>
</html>