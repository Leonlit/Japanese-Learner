(function () {
    const selectedText = window.getSelection().toString();
    console.log("Selected text:", selectedText)
    chrome.runtime.sendMessage({
        action: "howToReadThis",
        text: selectedText
    });
})();