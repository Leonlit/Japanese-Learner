import re

def classify_japanese_text(text):
    try:
        text = text.strip()
        if not text:
            return "Empty or invalid input"

        has_hiragana = bool(re.search(r'[\u3040-\u309F]', text))
        has_katakana = bool(re.search(r'[\u30A0-\u30FF]', text))
        has_kanji    = bool(re.search(r'[\u4E00-\u9FFF]', text))
        has_romaji   = bool(re.search(r'[a-zA-Z]', text))

        total_types = sum([has_hiragana, has_katakana, has_kanji, has_romaji])

        if total_types > 1:
            return True, "Mixed"
        elif has_hiragana:
            return True, "Hiragana"
        elif has_katakana:
            return True, "Katakana"
        elif has_kanji:
            return True, "Kanji"
        elif has_romaji:
            return True, "Romaji"
        else:
            return False, "Not a Japanese text"
    except Exception as ex:
        print("[-] Error in classifying text.")
        print(ex)
        return False, "Error Occured"