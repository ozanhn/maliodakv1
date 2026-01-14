from flask import Flask, request
import json, os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data.json")

def madde_bul(no, maddeler):
    return next((m for m in maddeler if str(m.get("madde")) == str(no)), None)

def uyum_hesapla(a, b):
    if not b:
        return 0, "Karşılaştırma yapılamadı."
    if a["baslik"] == b["baslik"]:
        return 90, "Maddeler arasında yüksek düzeyde anayasal uyum mevcuttur."
    if "vergi" in a["baslik"].lower() or "mali" in a["baslik"].lower():
        return 65, "Mali ilkeler bakımından kısmi uyum söz konusudur."
    return 40, "Normlar arası yorum farklılığı ve çelişki riski bulunmaktadır."

@app.route("/", methods=["GET"])
def ana():
    with open(DATA_PATH, encoding="utf-8-sig") as f:
        maddeler = json.load(f)

    madde = request.args.get("madde")
    karsilastir = request.args.get("karsilastir")
    b = request.args.get("b")

    html = "<h1>MaliOdak</h1>"

    if not madde:
        html += """
        <form>
            <input name="madde" placeholder="Madde numarası">
            <button>Ara</button>
        </form>
        """
        return html

    a = madde_bul(madde, maddeler)
    if not a:
        return "Madde bulunamadı."

    html += f"""
    <h3>Madde {a['madde']} – {a['baslik']}
    <a href="/?madde={madde}&karsilastir=1">[+]</a></h3>
    <p>{a['metin']}</p>
    """

    # 🔴 EKSİK OLAN KISIM BURASIYDI
    if karsilastir and not b:
        html += f"""
        <hr>
        <form>
            <input type="hidden" name="madde" value="{madde}">
            <input type="hidden" name="karsilastir" value="1">
            <input name="b" placeholder="Karşılaştırılacak madde">
            <button>Karşılaştır</button>
        </form>
        """
        return html

    if b:
        b_m = madde_bul(b, maddeler)
        yuzde, yorum = uyum_hesapla(a, b_m)
        html += f"""
        <hr>
        <h4>Uyum Oranı: %{yuzde}</h4>
        <p>{yorum}</p>
        """

    return html

if __name__ == "__main__":
    app.run()
