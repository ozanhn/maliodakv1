from flask import Flask, request
import json
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data.json")

def madde_bul(no, maddeler):
    return next((m for m in maddeler if str(m.get("madde")) == str(no)), None)

@app.route("/", methods=["GET"])
def ana():
    madde = request.args.get("madde")

    with open(DATA_PATH, encoding="utf-8") as f:
        maddeler = json.load(f)

    html = """
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial; background:#f5f5f5; }
        .container { max-width:800px; margin:auto; padding:20px; }
        input { width:100%; padding:12px; }
        button { padding:10px 20px; margin-top:10px; }
        .card { background:white; padding:20px; margin-top:20px; border-radius:10px; }
        .risk { color:red; font-weight:bold; }
    </style>
    </head>
    <body>
    <div class="container">
    <h2>MaliOdak – Anayasal Vergi Analizi</h2>

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
                <h3>Madde {m['madde']} – {m['baslik']}</h3>
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

    html += "</div></body></html>"
    return html

if __name__ == "__main__":
    app.run()
