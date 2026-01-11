from flask import Flask

app = Flask(__name__)

@app.route("/")
def ana_sayfa():
    return "MaliOdak sitesine hos geldin! Site calisiyor."

if __name__ == "__main__":
    app.run()
