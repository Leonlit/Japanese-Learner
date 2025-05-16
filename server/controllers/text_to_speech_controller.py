import subprocess
import os
from flask import request, jsonify, send_file, abort, after_this_request

from utils.classifies import classify_japanese_text
from utils.utilities import generate_uuid_for_user_tts, make_sure_directory_exists

WAV_FOLDER="wavs"

def get_text_tts():
    try:
        text = request.args.get("text")
        isJapanese, variantType = classify_japanese_text(text)
        
        if not isJapanese:
            return jsonify({"message": "Not a Japanese text"})

        uuid = generate_uuid_for_user_tts()
        wavFilePath = get_tts_japanese_text(text, uuid)

        @after_this_request
        def remove_file(response):
            try:
                os.remove(wavFilePath)
            except Exception as e:
                print(f"Could not delete file {wavFilePath}: {e}")
            return response

        return send_file(wavFilePath, mimetype="audio/wav")
    except Exception as err:
        print(err)
        abort(500) 

def get_tts_japanese_text(text, uuid):
    wav_file = f"{WAV_FOLDER}/{uuid}.wav"
    make_sure_directory_exists(WAV_FOLDER)
    process = subprocess.run(
        ['open_jtalk',
         '-x', '/var/lib/mecab/dic/open-jtalk/naist-jdic',
         '-m', '/usr/share/hts-voice/mei/mei_normal.htsvoice',
         '-ow', wav_file],
        input=text.encode('utf-8'),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    if process.returncode != 0:
        print("Error:", process.stderr.decode())
    else:
        print(f"Finished generating: {wav_file}")
    return wav_file