import { get_text_aid_pop_up, get_and_play_text_tts } from "./helper.js";

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
        const manifest = chrome.runtime.getManifest();
        const hostDomain = manifest.host_permissions[0].replace("/*", "");
        const text = message.text;
        get_and_play_text_tts(text, hostDomain)
    }
});
