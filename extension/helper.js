async function get_text_aid_pop_up(text, hostDomain) {
    const trimmedText = text.trim()
    const url = `${hostDomain}/getTextAid?text=` + encodeURIComponent(trimmedText);
    
    return await fetch(url)
        .then(res => res.json())
        .then(data => {
            console.log(data);
            return data
        })
        .catch(err => {
            console.error("API fetch failed", err);
        });
}


async function get_and_play_text_tts(text, hostDomain) {
    const trimmedText = text.trim()
    const url = `${hostDomain}/getTextTTS?text=` + encodeURIComponent(trimmedText);
    fetch(url)
        .then(res => res.blob())
        .then(blob => {
            const audioUrl = URL.createObjectURL(blob);
            const audio = new Audio(audioUrl);
            audio.play();
        })
        .catch(err => {
            console.error("API fetch failed", err);
        });
}

export {
    get_text_aid_pop_up,
    get_and_play_text_tts,
}