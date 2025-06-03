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
chrome.runtime.onMessage.addListener(async (message, sender, sendResponse) => {
    const manifest = chrome.runtime.getManifest();
    const hostDomain = manifest.host_permissions[0].replace("/*", "");
    const text = message.text;
    if (message.action === "howToReadThis") {
        const responseData = await get_text_aid_pop_up(text, hostDomain)
        return responseData
    }else if (message.action === "howToReadThisTTS") {
        const responseData = await get_and_play_text_tts(text, hostDomain)
        return responseData
    }
});
