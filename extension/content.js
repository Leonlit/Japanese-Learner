(function () {
    const selectedText = window.getSelection().toString();
    console.log("Selected text:", selectedText)
    chrome.runtime.sendMessage({
        action: "howToReadThis",
        text: selectedText
    }, (response) => {
        console.log(response);
        
        if (response && response.success) {
            show_pop_up(response.textAid);
        }
    });
})();


function show_pop_up(data) {
    console.log("in show pop up");
    
    const selection = window.getSelection();
    console.log(selection);
    
    if (selection.rangeCount === 0) return;

    const range = selection.getRangeAt(0);
    const rect = range.getBoundingClientRect();

    const popup = document.createElement("div");
    popup.innerText = data;
    popup.style.position = "fixed";
    popup.style.left = `${rect.left + window.scrollX}px`;
    popup.style.top = `${rect.bottom + window.scrollY}px`;
    popup.style.backgroundColor = "white";
    popup.style.border = "1px solid black";
    popup.style.padding = "5px";
    popup.style.zIndex = 9999;
    popup.style.maxWidth = "300px";
    popup.style.boxShadow = "0 2px 6px rgba(0,0,0,0.3)";
    popup.style.fontSize = "14px";

    document.body.appendChild(popup);
}