import pykakasi
from jamdict import Jamdict

jam = Jamdict()

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
            print(word)
            ori = word[0]
            result = jam.lookup(ori)
            if result.entries:
                entry = result.entries[0]
            else:
                entry = "Not found"
            meaning.append([ori, word[1], entry])
        return meaning
    except Exception as err:
        print(err)
        return False
