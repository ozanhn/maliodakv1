from flask import Flask, request
import json, os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data.json")

def madde_bul(no, maddeler):
    return next((m for m in maddeler if str(m.get("madde")) == str(no)), None)

def uyum_hesapla(a, b):
    if not b:
        return 20, "Veri eksikliği nedeniyle ciddi kanun boşluğu riski bulunmaktadır."
    if a["baslik"] == b["baslik"]:
        return 95, "Maddeler arasında çok yüksek anayasal uyum vardır."
    if "vergi" in a["baslik"].lower() or "mali" in a["baslik"].lower():
        return 70, "Mali ilkeler bakımından kısmi uyum bulunmaktadır."
    return 40, "Normlar arası yorum farklılığı ve çelişki riski mevcuttur."

def renk(y):
    if y >= 80: return "green"
    if y >= 50: return "orange"
    return "red"

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
        body { font-family: Arial; background:#f5f5f5; margin:0; }
        .center { display:flex; flex-direction:column; justify-content:center; align-items:center; height:100vh; }
        h1 { font-size:48px; }
        input { padding:14px; width:300px; font-size:16px; }
        button { padding:10px 20px; margin-top:10px; }
        .container { max-width:800px; margin:auto; padding:20px; }
        .card { background:white; padding:20px; border-radius:10px; margin-top:20px; }
        .plus { float:right; background:orange; color:white; padding:6px 12px; border-radius:50%; text-decoration:none; }
        .bar { height:20px; border-radius:10px; }
        details summary { font-weight:bold; cursor:pointer; margin-top:10px; }
    </style>
    </head><body>
    """

    if not madde:
        html += """
        <div class="center">
            <h1>MaliOdak</h1>
            <form>
                <input name="madde" placeholder="Madde numarası (örn: 73)">
                <br><button>Ara</button>
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

                <details>
                    <summary>Neden Bu Madde Var?</summary>
                    <p>{a['neden'] or 'Henüz eklenmedi.'}</p>
                </details>

                <details>
                    <summary>Olmasaydı Ne Olurdu?</summary>
                    <p>{a['olmasaydi'] or 'Henüz eklenmedi.'}</p>
                </details>

                <details>
                    <summary>Olası Hukuki Risk</summary>
                    <p>{a['risk'] or 'Belirtilmemiştir.'}</p>
                </details>
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
                </form>
            </div>
            """

        if b:
            b_m = madde_bul(b, maddeler)
            yuzde, yorum = uyum_hesapla(a, b_m)
            renkli = renk(yuzde)

            html += f"""
            <div class="card">
                <h4>Karşılaştırma Sonucu</h4>
                <p><b>Uyum Oranı:</b> %{yuzde}</p>
                <div class="bar" style="width:{yuzde}%; background:{renkli};"></div>
                <p>{yorum}</p>
            </div>
            """

        html += "</div>"

    html += "</body></html>"
    return html

if __name__ == "__main__":
    app.run()
