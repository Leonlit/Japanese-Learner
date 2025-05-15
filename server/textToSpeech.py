import subprocess

WAV_FOLDER="wavs"

def tts_text(text, uuid):
    wav_file = f"{WAV_FOLDER}/{uuid}.wav"
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