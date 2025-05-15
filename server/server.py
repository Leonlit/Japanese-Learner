from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from classifies import classify_japanese_text
from textToSpeech import tts_text
from utils import generate_uuid_for_user_tts
from textAid import generate_text_aid, generate_text_meaning

app = Flask(__name__)
CORS(app)

@app.route("/getTextAid", methods=["GET"])
def get_text_aid():
    text = request.args.get("text")
    isJapanese, variantType = classify_japanese_text(text)
    
    if not isJapanese:
        return jsonify({"message": variantType})

    textAidArr = generate_text_aid(text)
    
    if not textAidArr:
        return jsonify({"success": False}), 500

    textAidAllArr = generate_text_meaning(textAidArr)
    print(textAidAllArr)
    return jsonify({"success": True, "textAidArr": textAidAllArr})

# GET endpoint
@app.route("/getTextTTS", methods=["GET"])
def get_text_tts():
    text = request.args.get("text")
    isJapanese, variantType = classify_japanese_text(text)
    
    if not isJapanese:
        return jsonify({"message": "Not a Japanese text"})

    uuid = generate_uuid_for_user_tts()
    wavFilePath = tts_text(text, uuid)
    return send_file(wavFilePath, mimetype="audio/wav")

if __name__ == "__main__":
    app.run(debug=True, port=5000)