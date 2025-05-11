console.log("Background script running");

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    fetch("http://127.0.0.1:5000/download", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ reel_url: message.reelUrl })
    })
    .then(response => response.text())
    .then(data => console.log("Response from Python:", data));
});
