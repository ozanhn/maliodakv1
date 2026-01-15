from flask import Flask, request
import json, os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data.json")

ANAHTAR_KELIMELER = ["vergi", "mali", "kamu", "harcama", "bütçe", "gelir"]

def madde_bul(no, maddeler):
    return next((m for m in maddeler if str(m.get("madde")) == str(no)), None)

def uyum_hesapla(a, b):
    puan = 20
    if a["baslik"] == b["baslik"]:
        puan += 40

    ortak = sum(1 for k in ANAHTAR_KELIMELER if k in a["metin"].lower() and k in b["metin"].lower())
    puan += min(ortak * 6, 30)

    fark = abs(len(a["metin"]) - len(b["metin"]))
    puan += 20 if fark < 100 else -20
    puan = max(10, min(puan, 95))

    if puan >= 80:
        yorum = "Maddeler arasında yüksek düzeyde normatif uyum bulunmaktadır."
    elif puan >= 50:
        yorum = "Maddeler arasında kısmi uyum mevcuttur."
    else:
        yorum = "Normlar arası çelişki tespit edilmiştir."

    return puan, yorum

def renk(p):
    return "#2e7d32" if p >= 80 else "#f9a825" if p >= 50 else "#c62828"

@app.route("/", methods=["GET"])
def ana():
    with open(DATA_PATH, encoding="utf-8-sig") as f:
        maddeler = json.load(f)

    madde = request.args.get("madde")
    karsilastir = request.args.get("karsilastir")
    b = request.args.get("b")

    html = """
    <html><head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family:Segoe UI;
            background:
              linear-gradient(135deg, rgba(26,35,126,0.04) 25%, transparent 25%) -50px 0,
              linear-gradient(225deg, rgba(26,35,126,0.04) 25%, transparent 25%) -50px 0,
              linear-gradient(315deg, rgba(26,35,126,0.04) 25%, transparent 25%),
              linear-gradient(45deg, rgba(26,35,126,0.04) 25%, transparent 25%);
            background-size:100px 100px;
            background-color:#eef1f4;
            margin:0;
        }
        .center {height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;}
        .logo {font-size:46px;color:#1a237e;margin-bottom:25px;}
        input {padding:12px;width:280px;}
        button {padding:10px 20px;background:#1a237e;color:white;border:none;}
        .container {max-width:900px;margin:auto;padding:30px;}
        .card {background:white;padding:25px;margin-top:25px;border-left:5px solid #1a237e;}
        .plus {float:right;background:#1565c0;color:white;padding:6px 12px;border-radius:50%;text-decoration:none;}
        .bar {height:16px;}
        .uyari {background:#ffebee;border-left:5px solid #c62828;padding:15px;margin-top:20px;color:#b71c1c;}
        .about-btn {position:fixed;right:20px;bottom:20px;color:#1a237e;cursor:pointer;}
        .about-box {display:none;position:fixed;right:20px;bottom:60px;width:300px;background:white;padding:15px;border:1px solid #ccc;}
    </style>
    <script>
        function toggleAbout(){
            var b=document.getElementById("about");
            b.style.display=b.style.display==="block"?"none":"block";
        }
    </script>
    </head><body>
    """

    if not madde:
        html += """
        <div class="center">
            <div class="logo">MaliOdak</div>
            <form><input name="madde" placeholder="Anayasa Madde Numarası"><br><button>Analiz Et</button></form>
        </div>
        """
    else:
        a = madde_bul(madde, maddeler)
        html += f"""
        <div class="container">
        <div class="card">
        <h3>Madde {a['madde']} – {a['baslik']}
        <a class="plus" href="/?madde={madde}&karsilastir=1">+</a></h3>
        <p>{a['metin']}</p>
        </div>
        """

        if karsilastir and not b:
            html += f"""
            <div class="card">
            <form>
                <input type="hidden" name="madde" value="{madde}">
                <input type="hidden" name="karsilastir" value="1">
                <input name="b" placeholder="Karşılaştırılacak madde">
                <button>Karşılaştır</button>
            </form></div>
            """

        if b:
            b_m = madde_bul(b, maddeler)
            puan, yorum = uyum_hesapla(a, b_m)
            html += f"""
            <div class="card">
            <p><b>Uyum Oranı:</b> %{puan}</p>
            <div style="background:#ddd;"><div class="bar" style="width:{puan}%;background:{renk(puan)};"></div></div>
            <p>{yorum}</p>
            """
            if puan < 50:
                html += "<div class='uyari'>⚠️ Normlar arası ciddi çelişki bulunmaktadır.</div>"
            html += "</div>"

        html += "</div>"

    html += """
    <div class="about-btn" onclick="toggleAbout()">MaliOdak nedir?</div>
    <div class="about-box" id="about">
        <b>MaliOdak</b>, Türkiye Cumhuriyeti Anayasası’ndaki mali ve vergisel hükümleri
        karşılaştırmalı ve yüzdelik analiz yöntemiyle inceleyen akademik bir platformdur.
        <br><br>
        <b>Fikrî mülkiyet Doç. Dr. Doğan BOZDOĞAN’a aittir.</b>
    </div>
    </body></html>
    """
    return html

if __name__ == "__main__":
    app.run()
