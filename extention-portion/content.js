const button = document.createElement("button");
button.innerText = "Download Reel";
button.style.position = "fixed";
button.style.bottom = "10px";
button.style.right = "10px";
button.style.opacity = "0.7";
button.style.background = "black";
button.style.color = "white";
button.style.padding = "8px";
button.style.zIndex = "9999";
document.body.appendChild(button);

button.addEventListener("click", () => {
    console.log("Button clicked");
    const currentUrl = window.location.href;
    chrome.runtime.sendMessage({ reelUrl: currentUrl });
});
