chrome.runtime.onInstalled.addListener(() => {
    chrome.contextMenus.create({
        id: "howToReadThis",
        title: "How to read this Japanese",
        contexts: ["selection"]
    });
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
    if (info.menuItemId === "howToReadThis") {
        chrome.scripting.executeScript({
            target: { tabId: tab.id },
            files: ["content.js"]
        });
    }
});

// handle message from content.js
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "howToReadThis") {
        const text = message.text;
        const url = "http://localhost:5000/getTextAid?text=" + encodeURIComponent(text);

        fetch(url)
            .then(res => res.json())
            .then(data => {
                console.log("Response from API:", data);
                // Optional: send a message back to content script or popup
            })
            .catch(err => {
                console.error("API fetch failed", err);
            });
    }
});
