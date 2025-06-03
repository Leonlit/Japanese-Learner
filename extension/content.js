(function () {
    const selectedText = window.getSelection().toString();
    
    chrome.runtime.sendMessage({
        action: "howToReadThis",
        text: selectedText
    }, (response) => {
        if (response && response.success) {
            show_pop_up(selectedText, response);
        }
    });
})();


function show_pop_up(selectedText, data) {
    const textAidArr = data.textAid
    const translatedText = data.translatedText

    const selection = window.getSelection();
    if (selection.rangeCount === 0) return;

    const range = selection.getRangeAt(0);
    const rect = range.getBoundingClientRect();

    // Create host element
    const host = document.createElement("div");
    host.style.position = "fixed";
    host.style.left = `${rect.left + window.scrollX}px`;
    host.style.top = `${rect.bottom + window.scrollY}px`;
    host.style.zIndex = "9999";

    // Attach Shadow DOM
    const shadow = host.attachShadow({ mode: "open" });

    // Create <style> for scoped CSS
    const style = document.createElement("style");
    style.textContent = `
        .popup {
            background-color: white;
            border: 1px solid black;
            padding: 20px;
            max-width: 500px;
            max-height: 300px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.3);
            font-size: 16px;
            overflow-y: auto;
            font-family: sans-serif;
        }

        .flex-column {
            display: flex;
            flex-direction: column;
            text-align: left;
            line-height: 1.5;
        }

        .italic {
            font-style: italic;
        }

        .block-ele {
            display: block;
        }

        .custom-ul {
            list-style-type: circle;
        }

        .custom-ol {
            list-style-type: decimal;
        }

        .custom-hr {
            width: 100%;
        }
    `;

    // Create popup content wrapper
    const popup = document.createElement("div");
    popup.className = "popup";
    popup.appendChild(construct_interface(selectedText, textAidArr, translatedText));

    // Append style and popup to shadow DOM
    shadow.appendChild(style);
    shadow.appendChild(popup);

    // Append to body
    document.body.appendChild(host);
}

function construct_interface(selectedText, textAid, translatedText) {
    const miniPage = document.createElement("div")

    const readAloudContainer = document.createElement("div")
    readAloudContainer.classList.add("flex-column")

    const translatedTextContainer = document.createElement("div")
    translatedTextContainer.classList.add("flex-column")

    translatedTextContainer.innerText = translatedText
    
    const readAloudLink = document.createElement("a")
    readAloudLink.innerHTML = "🎵"
    readAloudLink.addEventListener("click", (evt) => {
        handleReadAloud(selectedText)
    })

    readAloudContainer.appendChild(readAloudLink)
    
    miniPage.appendChild(readAloudContainer)
    miniPage.appendChild(translatedTextContainer)

    //[0] = original word
    //[1] = romanji
    //[2] = gloss/meaning
    textAid.forEach((item, idx) => {
        const container = document.createElement("div")
        const originalWord = document.createElement("h2")
        const romanjiWord = document.createElement("span")
        const meaningContaienr = document.createElement("ol")

        container.classList.add("flex-column")
        
        romanjiWord.classList.add("italic")

        meaningContaienr.classList.add("flex-column")
        meaningContaienr.classList.add("custom-ol")

        originalWord.innerText = item[0]
        romanjiWord.innerText = item[1]

        const senses = item[2];
        if (senses != "None") {
            senses.forEach(senseItem => {
                const senseContainer = document.createElement("li")
                const currSenseArr = senseItem.senses

                currSenseArr.forEach(currSense => {
                    const senseEle = document.createElement("ul")
                    senseEle.classList.add("custom-ul")
                    const glossArr = currSense.gloss

                    glossArr.forEach(glossText => {
                        const glossEle = document.createElement("li")
                        glossEle.innerText = "\t" + glossText
                        senseEle.appendChild(glossEle)
                    });
                    senseContainer.appendChild(senseEle)
                });

                meaningContaienr.appendChild(senseContainer)
            });
        }else {
            const senseEle = document.createElement("div")
            const glossEle = document.createElement("span")

            glossEle.innerText = "None"
            senseEle.appendChild(glossEle)

            meaningContaienr.appendChild(senseEle)
        }

        container.appendChild(originalWord)
        container.appendChild(romanjiWord)
        container.appendChild(meaningContaienr)

        if (idx < textAid.length - 1) {
            const divider = document.createElement('hr');
            divider.classList.add("custom-hr")
            container.appendChild(divider);
        }

        miniPage.appendChild(container)
    });
    return miniPage
}

async function handleReadAloud(selectedText) {
    try {
        const response = await read_aloud_text(selectedText);

        console.log(response);
        
        //TODO: play the audio
    } catch (err) {
        console.error("Error getting TTS:", err);
    }
}

function read_aloud_text(selectedText) {
    return new Promise((resolve, reject) => {
        chrome.runtime.sendMessage({
            action: "howToReadThisTTS",
            text: selectedText
        }, (response) => {
            if (chrome.runtime.lastError) {
                return reject(chrome.runtime.lastError);
            }

            if (response && response.success) {
                resolve(response);
            } else {
                reject(new Error("Failed to get TTS data"));
            }
        });
    });
}