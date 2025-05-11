import os
import re
from flask import Flask, request
from download_reel import download_instagram_reel  

app = Flask(__name__)

@app.route("/download", methods=["POST"])
def download():
    data = request.json
    if not data or "reel_url" not in data:
        return "Invalid request", 400
    
    reel_url = data["reel_url"]

    # Convert "/reels/" to "/reel/"
    reel_url = reel_url.replace("/reels/", "/reel/")
    
    # Extract shortcode from URL using regex
    match = re.search(r"/reel/([^/?]+)/", reel_url)
    if not match:
        return "Invalid Instagram Reel URL", 400
    global shortcode
    shortcode = match.group(1)

    # Create a folder for this shortcode inside "downloads/"
    save_path = os.path.join("downloads", shortcode)
    os.makedirs(save_path, exist_ok=True)  # Ensure folder creation

    print(f"Processed URL: {reel_url}, Saving to: {save_path}")  

    # Run the function with new folder structure
   
    download_instagram_reel(reel_url, save_path)

    print("About to upload to youtube")
    upload_to_youtube()
   
    return f"Download started! Files will be saved in {save_path}"


def upload_to_youtube():
    # Ensure the shortcode is available
    print(f"Uploading to YouTube with shortcode: {shortcode}")
    if 'shortcode' not in globals():
        return "No shortcode available for upload", 400
    os.system(f"python upload_youtube.py {shortcode}")



if __name__ == "__main__":
    app.run(port=5000)



# Upload the reels to YouTube
