import pykakasi
from jamdict import Jamdict
from flask import request, jsonify

from utils.classifies import classify_japanese_text

jam = Jamdict()

def get_text_aid():
    try:
        text = request.args.get("text")
        isJapanese, variantType = classify_japanese_text(text)
        
        if not isJapanese:
            return jsonify({"message": variantType})

        textAidArr = generate_text_aid(text)
        
        if not textAidArr:
            return jsonify({"success": False}), 500

        textAidAllArr = generate_text_meaning(textAidArr)
        return jsonify({"success": True, "textAid": textAidAllArr})
    except Exception as err:
        print(err)
        abort(500) 

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