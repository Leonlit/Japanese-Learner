import subprocess

def speak_japanese(text, uuid):
    wav_file= f"{uuid}.wav"
    command = f'echo "{text}" | open_jtalk ' \
              f'-x /var/lib/mecab/dic/open-jtalk/naist-jdic ' \
              f'-m /usr/share/hts-voice/mei/mei_normal.htsvoice ' \
              f'-ow {wav_file}'

    subprocess.run(command, shell=True)

# Example usage
speak_japanese("こんにちは、元気ですか？")