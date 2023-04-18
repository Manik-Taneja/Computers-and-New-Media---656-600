from flask import Flask, render_template, request, redirect, url_for, session
from Backend.processing import *
app = Flask(__name__)

@app.route("/home", methods=["GET", "POST"])
def home():
    return render_template("LandingPage.html")

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("LandingPage.html")

@app.route("/Summarizer", methods=["GET", "POST"])
def Summarizer():
    return render_template("Summarizer.html")

@app.route("/TeamMembers", methods=["GET", "POST"])
def TeamMembers():
    return render_template("TeamMembers.html")


@app.route("/handle_Summarizer", methods=["GET", "POST"])
def handle_Summarizer():
    if request.method == "POST" and "Link" in request.form:
        YTLink = request.form["Link"]
        srt_data = get_link(YTLink)
        return render_template("data.html", srt_data = srt_data)


app.run(port=8000, debug=True)
