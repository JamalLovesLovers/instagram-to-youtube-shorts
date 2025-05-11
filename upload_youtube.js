const { google } = require("googleapis");
const fs = require("fs");
const path = require("path");

// Load credentials (Ensure your OAuth2 client is set up!)
const OAuth2 = google.auth.OAuth2;
const CLIENT_ID = "";
const CLIENT_SECRET = "";
const REDIRECT_URI = "";
const REFRESH_TOKEN = "";

// Authenticate YouTube API
const oauth2Client = new OAuth2(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI);
oauth2Client.setCredentials({ refresh_token: REFRESH_TOKEN });

const youtube = google.youtube({ version: "v3", auth: oauth2Client });

async function uploadVideo(shortcode) {
    const folderPath = path.join("downloads", shortcode);
    const files = fs.readdirSync(folderPath);

    // Find video & caption files dynamically
    const videoPath = files.find(file => file.endsWith(".mp4")) ? path.join(folderPath, files.find(file => file.endsWith(".mp4"))) : null;
    const captionPath = files.find(file => file.endsWith(".txt")) ? path.join(folderPath, files.find(file => file.endsWith(".txt"))) : null;

    if (!videoPath || !captionPath) {
        console.error("⚠️ Missing required files (video/caption) in:", folderPath);
        process.exit(1);
    }

    // Read caption for title & description
    const titleDescription = fs.readFileSync(captionPath, "utf8").trim();

    console.log(`Uploading ${videoPath} to YouTube...`);

    try {
        const response = await youtube.videos.insert({
            part: "snippet,status",
            requestBody: {
                snippet: {
                    title: titleDescription, // Title = Caption
                    description: titleDescription, // Description = Caption
                    tags: ["Instagram", "Reels"],
                    categoryId: "22" // Entertainment category
                },
                status: { privacyStatus: "public" }
            },
            media: {
                body: fs.createReadStream(videoPath)
            }
        });

        console.log(`✅ Video uploaded! Watch it here: https://www.youtube.com/watch?v=${response.data.id}`);
    } catch (error) {
        console.error("❌ Upload failed:", error);
    }
}

// Get shortcode from command line input
const shortcode = process.argv[2];
if (!shortcode) {
    console.error("⚠️ Please provide a shortcode!");
    process.exit(1);
}

uploadVideo(shortcode);
