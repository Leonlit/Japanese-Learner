import pykakasi
from jamdict import Jamdict
from flask import request, jsonify, abort
import requests

from utils.classifies import classify_japanese_text

jam = Jamdict()

def get_text_aid():
    try:
        text = request.args.get("text")
        isJapanese, variantType = classify_japanese_text(text)
        
        if not isJapanese:
            return jsonify({"message": variantType})

        textTranslation = translate_text(text)
        textAidArr = generate_text_aid(text)
        
        if not textAidArr:
            return jsonify({"success": False}), 500

        textAidAllArr = generate_text_meaning(textAidArr)
        return jsonify({"success": True, "textAid": textAidAllArr, "translatedText": textTranslation})
    except Exception as err:
        print(err)
        abort(500)


def translate_text(text, source_lang='ja', target_lang='en'):
    url = 'http://localhost:5050/translate'

    payload = {
        'q': text,
        'source': source_lang,
        'target': target_lang,
        'format': 'text'
    }

    response = requests.post(url, data=payload)
    if response.status_code == 200:
        return response.json()['translatedText']
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")

def generate_text_aid(text):
    try:
        kakasi = pykakasi.kakasi()
        results = kakasi.convert(text)
        resultArr = [[item['orig'], item['hepburn']] for item in results]
        return resultArr
    except Exception as err:
        print(err)
        return False

def generate_text_meaning(textAidArr):
    try:
        meaning = []
        for word in textAidArr:
            ori = word[0]
            result = jam.lookup(ori)
            if result.entries:
                entry_data = [jmdentry_to_senses_dict(e) for e in result.entries]
            else:
                entry_data = "None"

            meaning.append([ori, word[1], entry_data])
        return meaning
    except Exception as err:
        print(err)
        return False

def jmdentry_to_senses_dict(entry):
    return {
        "senses": [
            {
                "gloss": [g.text for g in sense.gloss]
            }
            for sense in entry.senses
        ]
    }