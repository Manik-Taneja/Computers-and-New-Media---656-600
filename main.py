from flask import Flask, render_template, request, redirect, url_for, session
from Backend.processing import *
import librosa
import matplotlib.pyplot as plt
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
    
@app.route("/ProposedSolution", methods=["GET", "POST"])
def ProposedSolution():
    return render_template("ProposedSolution.html")

@app.route("/videoSummarized", methods=["GET", "POST"])
def videoSummarized():
    return render_template("videoSummarized.html")


# @app.route("/graph", methods=["GET", "POST"])
# def graph():
#     plt.rcParams["figure.figsize"] = [7.50, 3.50]
#     plt.rcParams["figure.autolayout"] = True
#     input_data = read('static/Audio/output_1.wav')
#     audio = input_data[1]
#     plt.plot(audio[0:1024])
#     plt.ylabel("Amplitude")
#     plt.xlabel("Time")
#     plt.show()
#     return "GOT IT"

app.run(port=8000, debug=True)
