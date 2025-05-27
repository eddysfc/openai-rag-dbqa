from flask import Flask, render_template
from dotenv import load_dotenv
import os
import requests

app = Flask(__name__)

load_dotenv()
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)