
import json
import tqdm

DEFAULT_LEXICON = "../dict/default_lexicon.txt"
DICTIONARY = "../dict/dictionary.json"
TERM_LEXICON = "../dict/term_lexicon.txt"

with open(DEFAULT_LEXICON,"r") as f:
    default_words = f.readlines()

default_words_set = set()
for word in default_words:
    word = word.split(' ')[0]
    default_words_set.add(word)
    

with open(DICTIONARY,"r") as f:
    dictionary = json.load(f)

with open(TERM_LEXICON,"w", encoding="utf8") as f:
    for key in tqdm.tqdm(dictionary):
        if key not in default_words_set:
            f.write(key + "\n")


