from flask import Flask, request, render_template
from download_reel import download_instagram_reel  

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")  # Load HTML file


@app.route("/download", methods=["POST"])
def download():
    reel_url = request.form.get("reel_url")  # Get input from HTML
    print(f"Received URL: {reel_url}")  
    #download_instagram_reel(reel_url, "downloads")  # Call function
    return "Download started!"

if __name__ == "__main__":
    app.run(port=5000)
