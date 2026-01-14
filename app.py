from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>MaliOdak çalışıyor</h1><p>Render Flask ayakta.</p>"

if __name__ == "__main__":
    app.run()
