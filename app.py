from flask import Flask, request
import json
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data.json")

VERGI_KELIMELERI = {
    "vergi": 40,
    "mali": 20,
    "kamu": 20,
    "gider": 10,
    "harç": 10
}

def vergi_puani(metin):
    metin = metin.lower()
    puan = 0
    for k, v in VERGI_KELIMELERI.items():
        if k in metin:
            puan += v
    return min(puan, 100)

def renk(p):
    if p >= 70:
        return "green"
    elif p >= 30:
        return "orange"
    return "red"

def load_json_safely(path):
    with open(path, "rb") as f:
        raw = f.read()
    text = raw.decode("utf-8-sig")
    return json.loads(text)

def madde_bul(no, maddeler):
    return next((m for m in maddeler if str(m["madde"]) == str(no)), None)

@app.route("/", methods=["GET"])
def ana():
    madde = request.args.get("madde")
    karsilastir = request.args.get("karsilastir")
    b = request.args.get("b")

    maddeler = load_json_safely(DATA_PATH)

    html = """
    <html>
    <head>
    <style>
        body { font-family: Arial; background:#f9f9f9; }
        .container { width: 600px; margin: 100px auto; text-align:center; }
        input { width: 70%; padding:12px; font-size:16px; }
        button { padding:12px 20px; font-size:16px; }
        .card {
            background:white;
            padding:20px;
            margin-top:20px;
            border-radius:10px;
            box-shadow:0 0 10px rgba(0,0,0,0.1);
            text-align:left;
        }
        .plus {
            float:right;
            background:orange;
            color:white;
            padding:5px 10px;
            border-radius:50%;
            text-decoration:none;
        }
    </style>
    </head>
    <body>
    <div class="container">
        <h1>MaliOdak</h1>
        <form method="get">
            <input type="text" name="madde" placeholder="Madde numarası gir (örn: 73)">
            <button type="submit">Ara</button>
        </form>
    """

    if madde and madde.isdigit() and not karsilastir:
        m = madde_bul(madde, maddeler)
        if m:
            p = vergi_puani(m["metin"])
            html += f"""
            <div class="card">
                <h3>
                    Madde {m['madde']} – {m['baslik']}
                    <a class="plus" href="/?madde={m['madde']}&karsilastir=1">+</a>
                </h3>
                <p>{m['metin']}</p>
                <p><b>Vergiyle İlgililik:</b>
                <span style="color:{renk(p)}">%{p}</span></p>
            </div>
            """

    if madde and karsilastir and not b:
        html += f"""
        <div class="card">
            <h3>Madde {madde} ile karşılaştır</h3>
            <form method="get">
                <input type="hidden" name="madde" value="{madde}">
                <input type="hidden" name="karsilastir" value="1">
                <input type="text" name="b" placeholder="Karşılaştırılacak madde (örn: 10)">
                <button type="submit">Karşılaştır</button>
            </form>
        </div>
        """

    if madde and b and madde.isdigit() and b.isdigit():
        a_m = madde_bul(madde, maddeler)
        b_m = madde_bul(b, maddeler)

        if a_m and b_m:
            ap = vergi_puani(a_m["metin"])
            bp = vergi_puani(b_m["metin"])

            html += f"""
            <div class="card">
                <h3>Madde {madde}</h3>
                <p>{a_m['metin']}</p>
                <p><b>Vergiyle İlgililik:</b>
                <span style="color:{renk(ap)}">%{ap}</span></p>

                <h3>Madde {b}</h3>
                <p>{b_m['metin']}</p>
                <p><b>Vergiyle İlgililik:</b>
                <span style="color:{renk(bp)}">%{bp}</span></p>
            </div>
            """

    html += "</div></body></html>"
    return html

if __name__ == "__main__":
    app.run(debug=True)
