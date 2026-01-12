from flask import Flask
import json
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data.json")

@app.route("/")
def ana_sayfa():
    with open(DATA_PATH, encoding="utf-8") as f:
        maddeler = json.load(f)

    sonuc = ""
    for m in maddeler:
        sonuc += f"<h3>Madde {m['madde']} - {m['baslik']}</h3>"
        sonuc += f"<p>{m['metin']}</p><hr>"

    return sonuc
