from flask import Flask, request
import json, os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data.json")

def madde_bul(no, maddeler):
    return next((m for m in maddeler if str(m.get("madde")) == str(no)), None)

def uyum_hesapla(a, b):
    if not b:
        return 25, "Veri eksikliği nedeniyle norm boşluğu riski bulunmaktadır."
    if a["baslik"] == b["baslik"]:
        return 90, "Maddeler arasında yüksek düzeyde anayasal uyum mevcuttur."
    if "vergi" in a["baslik"].lower() or "mali" in a["baslik"].lower():
        return 65, "Mali ilkeler bakımından kısmi uyum söz konusudur."
    return 40, "Normlar arası yorum farklılığı ve çelişki riski bulunmaktadır."

def seviye(y):
    if y >= 80: return "Yüksek Uyum"
    if y >= 50: return "Orta Uyum"
    return "Riskli"

def renk(y):
    if y >= 80: return "#2e7d32"
    if y >= 50: return "#f9a825"
    return "#c62828"

@app.route("/", methods=["GET"])
def ana():
    with open(DATA_PATH, encoding="utf-8-sig") as f:
        maddeler = json.load(f)

    madde = request.args.get("madde")
    karsilastir = request.args.get("karsilastir")
    b = request.args.get("b")

    html = """
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: "Segoe UI", Arial;
            background:#eef1f4;
            margin:0;
        }
        .center {
            height:100vh;
            display:flex;
            justify-content:center;
            align-items:center;
            flex-direction:column;
        }
        .logo {
            font-size:48px;
            font-weight:600;
            color:#1a237e;
            margin-bottom:30px;
        }
        input {
            width:320px;
            padding:14px;
            font-size:16px;
        }
        button {
            margin-top:10px;
            padding:10px 24px;
            font-size:15px;
            background:#1a237e;
            color:white;
            border:none;
            cursor:pointer;
        }
        .container {
            max-width:900px;
            margin:auto;
            padding:30px;
        }
        .card {
            background:white;
            padding:25px;
            margin-top:25px;
            border-radius:6px;
            border-left:5px solid #1a237e;
        }
        .plus {
            float:right;
            background:#1565c0;
            color:white;
            padding:6px 12px;
            border-radius:50%;
            text-decoration:none;
        }
        details summary {
            margin-top:15px;
            font-weight:600;
            cursor:pointer;
        }
        .bar-container {
            background:#ddd;
            border-radius:5px;
            height:18px;
            overflow:hidden;
        }
        .bar {
            height:18px;
            transition: width 1s ease;
        }
        .etiket {
            margin-top:8px;
            font-weight:600;
        }
        .about-btn {
            position:fixed;
            right:20px;
            bottom:20px;
            font-size:14px;
            color:#1a237e;
            cursor:pointer;
        }
        .about-box {
            display:none;
            position:fixed;
            right:20px;
            bottom:60px;
            width:300px;
            background:white;
            border:1px solid #ccc;
            padding:15px;
            font-size:14px;
            box-shadow:0 0 10px rgba(0,0,0,0.2);
        }
    </style>
    <script>
        function toggleAbout() {
            var box = document.getElementById("about");
            box.style.display = box.style.display === "block" ? "none" : "block";
        }
    </script>
    </head>
    <body>
    """

    if not madde:
        html += """
        <div class="center">
            <div class="logo">MaliOdak</div>
            <form>
                <input name="madde" placeholder="Anayasa Madde Numarası">
                <br>
                <button>Analiz Et</button>
            </form>
        </div>
        """

    if madde:
        html += '<div class="container">'
        a = madde_bul(madde, maddeler)
        if a:
            html += f"""
            <div class="card">
                <h3>
                    Madde {a['madde']} – {a['baslik']}
                    <a class="plus" href="/?madde={madde}&karsilastir=1">+</a>
                </h3>
                <p>{a['metin']}</p>

                <details><summary>Neden Bu Madde Var?</summary><p>{a['neden']}</p></details>
                <details><summary>Olmasaydı Ne Olurdu?</summary><p>{a['olmasaydi']}</p></details>
                <details><summary>Olası Hukuki Risk</summary><p>{a['risk']}</p></details>
            </div>
            """

        if karsilastir and b:
            b_m = madde_bul(b, maddeler)
            yuzde, yorum = uyum_hesapla(a, b_m)
            renkli = renk(yuzde)
            etiket = seviye(yuzde)

            html += f"""
            <div class="card">
                <h4>Norm Uyum Analizi</h4>
                <p><b>Uyum Oranı:</b> %{yuzde}</p>
                <div class="bar-container">
                    <div class="bar" style="width:{yuzde}%; background:{renkli};"></div>
                </div>
                <div class="etiket" style="color:{renkli};">{etiket}</div>
                <p>{yorum}</p>
            </div>
            """

        html += "</div>"

    html += """
    <div class="about-btn" onclick="toggleAbout()">MaliOdak nedir?</div>
    <div class="about-box" id="about">
        <b>MaliOdak</b>, Türkiye Cumhuriyeti Anayasası’nda yer alan mali ve vergisel
        hükümleri analiz etmeyi amaçlayan akademik bir değerlendirme platformudur.<br><br>
        Sistem, anayasa maddeleri arasındaki norm uyumunu ve olası çelişkileri
        karşılaştırmalı ve yüzdelik analiz yöntemiyle incelemektedir.<br><br>
        <b>Fikrî mülkiyet Doç. Dr. Doğan BOZDOĞAN’a aittir.</b>
    </div>
    </body></html>
    """
    return html

if __name__ == "__main__":
    app.run()
