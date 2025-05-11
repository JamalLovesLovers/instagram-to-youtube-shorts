import os
import re
from pathlib import Path
from instaloader import Instaloader, Post

def download_instagram_reel(url, download_dir="./downloads"):
    # Extract shortcode from URL
    match = re.search(r"/reel/([^/?]+)/", url)
    if not match:
        raise ValueError("Invalid Instagram Reel URL.")
    shortcode = match.group(1)

    # Prepare folder
    download_dir = Path(download_dir)
    download_dir.mkdir(parents=True, exist_ok=True)

    # Download
    loader = Instaloader()
    post = Post.from_shortcode(loader.context, shortcode)
    loader.download_post(post, target=download_dir)

    # Clean up
    for f in download_dir.glob("*.json.xz"):
        f.unlink()

    print(f"✅ Download complete in: {download_dir.resolve()}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 1:
        print("Usage: python download_reel.py <reel_url> [optional_save_directory]")
    else:
        reel_url = input("Enter the Instagram Reel URL: ") if len(sys.argv) < 2 else sys.argv[1]
        save_dir = sys.argv[2] if len(sys.argv) > 2 else "downloads"
        download_instagram_reel(reel_url, save_dir)


# Trial url: https://www.instagram.com/reel/DIkSHcGIBib/ ; https://www.instagram.com/reels/DJRCbZ0C-JX/