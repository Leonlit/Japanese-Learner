from flask import Flask, request, jsonify
from flask_cors import CORS
from classifies import classify_japanese_text

app = Flask(__name__)
CORS(app)

# GET endpoint
@app.route("/howToReadText", methods=["GET"])
def how_to_read_Text():
    text = request.args.get("text")
    isJapanese, variantType = classify_japanese_text(text)
    response = f"Japanese: {isJapanese}, type: {variantType}"
    return jsonify({"message": response })


if __name__ == "__main__":
    app.run(debug=True, port=5000)