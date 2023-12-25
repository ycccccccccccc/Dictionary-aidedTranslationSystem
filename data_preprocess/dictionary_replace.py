import pandas as pd
import tqdm
import json
import xml.etree.ElementTree as ET
import re

DICT_PATH = "../../../../data/dictionary/092-105-001/opendata.xml"
OUTPUT_DICT_PATH = "../dict/dictionary.json"
# DICT_PATH = "./dict/test.xml"
tree = ET.parse(DICT_PATH)
root = tree.getroot()

res = {}
for term in tqdm.tqdm(root):
    remove_list = ["&amp;", "quot;", "apos;"]
    eng_words = term.find('TERM_EN_NAME').text.lower()

    for rm in remove_list:
        eng_words.replace(rm, "")
    abbrs = re.findall(r'\{\=(.*?)\}', eng_words)
    eng_words = re.sub(r'{=(.*?)}', "", eng_words )
    eng_words = eng_words.split(";")

    eng_words = [en.lstrip().rstrip() for en in eng_words]
    eng_words = [en[en.startswith("the ") and len("the ") : ] for en in eng_words]
    eng_words = [en[en.startswith("a ") and len("a ") : ] for en in eng_words]
    # eng_words = [en.lstrip().rstrip().lstrip("the ").lstrip("a ").rstrip(".") for en in eng_words]
    eng_words = list(dict.fromkeys(eng_words))

    filtered_eng_words = list(filter(lambda eng_word: (not eng_word.startswith("and ")), eng_words))
    eng_words = filtered_eng_words

    tw_words = term.find('TERM_TW_NAME').text
    tw_words = tw_words.replace(" ","").split('；')
    for tw_word in tw_words: 
        if tw_word in res:
            if isinstance(res[tw_word], list):
                res[tw_word] += eng_words
        else:
            res[tw_word] = eng_words
        if abbrs: res[tw_word] += abbrs

        if len(res[tw_word]) == 0:
            res.pop(tw_word, None)

for key in tqdm.tqdm(res):
    res[key] = list(dict.fromkeys(res[key]))


with open(OUTPUT_DICT_PATH, "w", encoding='utf8') as f:
    json.dump(res, f, indent=4, ensure_ascii=False)

