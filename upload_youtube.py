import os
import json
import google.oauth2.credentials
import googleapiclient.discovery

# Set up credentials
CLIENT_ID = ""
CLIENT_SECRET = ""
REDIRECT_URI = ""
REFRESH_TOKEN = ""

# Authenticate YouTube API
def get_authenticated_service():
    credentials = google.oauth2.credentials.Credentials.from_authorized_user_info({
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN,
        "token_uri": "https://oauth2.googleapis.com/token"
    })
    return googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

def upload_video(shortcode):
    folder_path = f"downloads/{shortcode}"
    
    # Find video & caption files dynamically
    video_path = next((os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".mp4")), None)
    caption_path = next((os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".txt")), None)

    if not video_path or not caption_path:
        print("⚠️ Missing required files (video/caption) in:", folder_path)
        return

    # Read caption for title & description
    with open(caption_path, "r", encoding="utf-8") as file:
        title_description = file.read().strip()

    title = title_description[:100]  # Limit to 100 characters for title
    print(f"Uploading {video_path} to YouTube...")

    youtube = get_authenticated_service()

    request_body = {
        "snippet": {
            "title": title,  # Title = Caption
            "description": title_description,  # Description = Caption
            "tags": ["Instagram", "Reels"],
            "categoryId": "22"  # Entertainment category
        },
        "status": {"privacyStatus": "public"}
    }

    media_body = googleapiclient.http.MediaFileUpload(video_path, mimetype="video/mp4", resumable=True)

    try:
        request = youtube.videos().insert(
            part="snippet,status",
            body=request_body,
            media_body=media_body
        )
        response = request.execute()
        print(f"✅ Video uploaded! Watch it here: https://www.youtube.com/watch?v={response['id']}")
    except Exception as e:
        print(f"❌ Upload failed: {e}")


    if (input("Do you want to delete the local video file? (y/n): ").strip().lower() == 'y'):
        try:
            os.remove(video_path)
            print(f"✅ Deleted local video file: {video_path}")
        except Exception as e:
            print(f"❌ Failed to delete local video file: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("⚠️ Please provide a shortcode!")
        sys.exit(1)

    shortcode = sys.argv[1]
    upload_video(shortcode)

