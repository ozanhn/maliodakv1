from flask import Flask, request
import json, os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data.json")

def madde_bul(no, maddeler):
    return next((m for m in maddeler if str(m.get("madde")) == str(no)), None)

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
            font-family: Arial;
            background:#f5f5f5;
            margin:0;
            height:100vh;
        }
        .center-box {
            display:flex;
            flex-direction:column;
            justify-content:center;
            align-items:center;
            height:100vh;
            text-align:center;
        }
        h1 {
            font-size:48px;
            margin-bottom:20px;
        }
        form {
            width:100%;
            max-width:400px;
        }
        input {
            width:100%;
            padding:14px;
            font-size:18px;
        }
        button {
            margin-top:10px;
            padding:10px 20px;
            font-size:16px;
        }
        .container {
            max-width:800px;
            margin:auto;
            padding:20px;
        }
        .card {
            background:white;
            padding:20px;
            margin-top:20px;
            border-radius:10px;
            box-shadow:0 0 10px rgba(0,0,0,0.1);
        }
        .risk { color:red; font-weight:bold; }
        .plus {
            float:right;
            background:orange;
            color:white;
            padding:6px 12px;
            border-radius:50%;
            text-decoration:none;
        }
    </style>
    </head>
    <body>
    """

    # MERKEZDE ARAMA (madde yoksa)
    if not madde:
        html += """
        <div class="center-box">
            <h1>MaliOdak</h1>
            <form method="get">
                <input type="text" name="madde" placeholder="Madde numarası gir (örn: 73)">
                <button type="submit">Ara</button>
            </form>
        </div>
        """

    # SONUÇLAR
    if madde:
        html += '<div class="container">'
        m = madde_bul(madde, maddeler)
        if m:
            html += f"""
            <div class="card">
                <h3>
                    Madde {m['madde']} – {m['baslik']}
                    <a class="plus" href="/?madde={m['madde']}&karsilastir=1">+</a>
                </h3>
                <p>{m['metin']}</p>

                <h4>Neden Bu Madde Var?</h4>
                <p>{m['neden'] or 'Henüz analiz eklenmedi.'}</p>

                <h4>Olmasaydı Ne Olurdu?</h4>
                <p>{m['olmasaydi'] or 'Henüz analiz eklenmedi.'}</p>

                <h4>Olası Hukuki Risk</h4>
                <p class="risk">{m['risk'] or 'Belirtilmemiştir.'}</p>
            </div>
            """
        else:
            html += "<p>Madde bulunamadı.</p>"

        # Karşılaştırma formu
        if karsilastir and not b:
            html += f"""
            <div class="card">
                <h4>Karşılaştırılacak Madde</h4>
                <form method="get">
                    <input type="hidden" name="madde" value="{madde}">
                    <input type="hidden" name="karsilastir" value="1">
                    <input type="text" name="b" placeholder="İkinci madde numarası">
                    <button type="submit">Karşılaştır</button>
                </form>
            </div>
            """

        if b:
            b_m = madde_bul(b, maddeler)
            if not b_m:
                html += """
                <div class="card">
                    <p class="risk">
                    ⚠️ Karşılaştırılan madde veri setinde bulunamadı.
                    Bu durum kanun boşluğu riskine işaret eder.
                    </p>
                </div>
                """
            else:
                html += f"""
                <div class="card">
                    <h4>Karşılaştırma Sonucu</h4>
                    <p>
                    Madde {madde} ile Madde {b} birlikte yorumlanırken
                    normlar arası denge gözetilmelidir.
                    </p>
                </div>
                """

        html += "</div>"

    html += "</body></html>"
    return html

if __name__ == "__main__":
    app.run()
