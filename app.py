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
        body { font-family: Arial; background:#f5f5f5; margin:0; }
        .container { max-width:800px; margin:auto; padding:20px; }
        input { width:100%; padding:12px; font-size:16px; }
        button { padding:10px 20px; margin-top:10px; }
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
    <div class="container">

    <form method="get">
        <input type="text" name="madde" placeholder="Madde numarası gir (örn: 73)">
        <button type="submit">Ara</button>
    </form>
    """

    if madde and madde.isdigit():
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

    if madde and karsilastir and not b:
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

    if madde and b:
        a = madde_bul(madde, maddeler)
        b_m = madde_bul(b, maddeler)

        if not b_m:
            html += """
            <div class="card">
                <p class="risk">
                ⚠️ Karşılaştırılan madde veri setinde bulunamadı.
                Bu durum uygulamada kanun boşluğu veya yorum eksikliği riskine işaret eder.
                </p>
            </div>
            """
        else:
            html += f"""
            <div class="card">
                <h4>Karşılaştırma Sonucu</h4>
                <p>
                Madde {a['madde']} ile Madde {b_m['madde']} birlikte
                yorumlandığında mali ve hukuki denge sağlanmalıdır.
                Aksi takdirde normlar arası çelişki doğabilir.
                </p>
            </div>
            """

    html += "</div></body></html>"
    return html

if __name__ == "__main__":
    app.run()
