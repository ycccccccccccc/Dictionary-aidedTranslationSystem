import jieba 
import jieba.analyse
import json
import tqdm
import re
import nltk
import ssl

TRAIN_DATA_PATH = "../filtered/C07B-10000-1230.json"
TRAIN_DATA_OUTPUT_PATH = "../replaced/C07B.json"
DEFAULT_LEXICON = '../dict/default_lexicon.txt'
TERM_LEXICON = "../dict/term_lexicon.txt"

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')


jieba.load_userdict(DEFAULT_LEXICON) 
jieba.load_userdict(TERM_LEXICON)

print("\n\n[jieba] User dict loaded\n\n")

# Read training data

with open(TRAIN_DATA_PATH, "r", encoding="utf8") as f:
    training_data = json.load(f)

print("\n\n[train] Training data loaded\n\n")

# Load term dictionary
TERM_DICT = "../dict/dictionary.json"
with open(TERM_DICT, "r", encoding="utf8") as f:
    term_dictionary = json.load(f)

print("\n\n[dict] Term dict loaded\n\n")

new_dataset = []

for idx in tqdm.tqdm(range(len(training_data))):
    en_abs = training_data[idx]["abstract"]["en"].replace("(", "").replace(")", "")
    zh_abs = training_data[idx]["abstract"]["zh"]

    possible_terms = jieba.analyse.extract_tags(zh_abs, topK=20, withWeight=False, allowPOS=("n", "x", "nr", "ns", "nt", "nz"))

    test = possible_terms.copy()
    possible_terms.sort(key=len, reverse=True)

    # tokene into words
    en_tokens = nltk.word_tokenize(en_abs)

    # parts of speech tagging
    en_pos_tags = nltk.pos_tag(en_tokens)
    en_abs = ""
    en_pos_dict = dict()
    for i in range(len(en_pos_tags)):

        temp = en_pos_tags[i][0]
        temp_pos = en_pos_tags[i][1]
        
        if temp_pos == 'NNS' and temp.endswith('s'):
            temp = temp[:-1]
            temp_pos = "NN"

        if temp in en_pos_dict:
            if en_pos_dict[temp] == "NN":
                en_pos_dict[temp] = temp_pos
        else:
            en_pos_dict[temp] = temp_pos      
          
        en_abs += (temp + ' ')
        en_abs_ref = en_abs
        zh_abs_ref = zh_abs

    glossary = {}
    for zh_term in possible_terms:
        if zh_term not in term_dictionary: continue

        # count how many times zh_term occur
        zh_term_occurrence = zh_abs.count(zh_term)

        term_en_trans = sorted(term_dictionary[zh_term], key=len, reverse=True)

        matched_en_term = ""
        matched_en_is_valid = False
        matched_count = 0
        for en_term in term_en_trans:
            if len(en_term.split(" ")) == 1:
                if en_term not in en_pos_dict:
                    continue
                if en_pos_dict[en_term] != "NN": 
                    continue
            
            en_term_occurrence = len(re.findall(rf"\b{re.escape(en_term)}\b", en_abs, re.IGNORECASE))
            
            if en_term_occurrence == zh_term_occurrence:
                if  en_term in  en_pos_dict:
                    pos =  en_pos_dict[en_term]
                else:
                    pos = "null"
                # print(zh_term, ": ", en_term , " | ", zh_term_occurrence, " | ", pos)
                
                if matched_en_term:
                    if en_term in matched_en_term:
                        continue
                    else:
                        matched_en_is_valid = False
                        break
                else:
                    matched_en_is_valid = True
                    matched_en_term = en_term
                    matched_count = en_term_occurrence
        if matched_en_is_valid:
            glossary[zh_term] = {
                "en" : matched_en_term,
                "count" : matched_count
            }
            en_abs = re.sub(rf"\b{re.escape(en_term)}\b", "", en_abs, re.IGNORECASE)
            zh_abs = zh_abs.replace(zh_term, "")
    
    training_data[idx]["abstract"]["en"] = en_abs_ref
    training_data[idx]["abstract"]["zh"] = zh_abs_ref
    training_data[idx]["glossary"] = []

    for key in glossary:
        training_data[idx]["glossary"].append({
            "en": glossary[key]["en"],
            "zh": key,
            "count" : glossary[key]["count"]
        })

with open(TRAIN_DATA_OUTPUT_PATH, "w", encoding='utf8') as f:
    json.dump(training_data, f, indent=4, ensure_ascii=False)

