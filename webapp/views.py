from webapp import app
from datetime import date

@app.route("/")
def root():
    return "Hello user!"


@app.route("/healthcheck")
def health():
    return {
        "status": "success",
        "date": str(date.today())
    }
