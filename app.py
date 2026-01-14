from flask import Flask, request
import json
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data.json")

@app.route("/")
def ana():
    with open(DATA_PATH, encoding="utf-8-sig") as f:
        maddeler = json.load(f)

    madde = request.args.get("madde")
    html = "<h2>MaliOdak calisiyor</h2>"

    if madde:
        for m in maddeler:
            if str(m.get("madde")) == madde:
                html += f"""
                <h3>Madde {m.get('madde')} - {m.get('baslik')}</h3>
                <p>{m.get('metin')}</p>
                <b>Neden:</b> {m.get('neden','')}<br>
                <b>Olmasaydi:</b> {m.get('olmasaydi','')}<br>
                <b>Risk:</b> {m.get('risk','')}
                """
                break

    return html

if __name__ == "__main__":
    app.run()
