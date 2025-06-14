from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from flask import Blueprint

from controllers.text_aid_controller import get_text_aid
from controllers.text_to_speech_controller import get_text_tts

app = Flask(__name__)
CORS(app)

text_bp = Blueprint("text", __name__)

text_bp.route("/getTextAid", methods=["GET"])(get_text_aid)
text_bp.route("/getTextTTS", methods=["GET"])(get_text_tts)

app.register_blueprint(text_bp) 

if __name__ == "__main__":
    try:
        app.run(debug=True, port=5000)
    except Exception as ex:
        print(ex)