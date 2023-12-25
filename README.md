# Dictionary-aided Automatic Translation of Technical File

❌ Drawbacks of modern machine translation
* Inability to specify specific terminologies and their translations
* Difficulty in accurately understanding and translating complex terminologies

💡 Our idea
* Integrating a dictionary into the preprocessing phase of machine translation
* Allowing users to specify translations for specific terminologies

#### In the fall of 2022, I and my team have completed a translation system that enhances the accuracy of translations. Here are some key features:

* Making machine-assisted translation more practical
* No need for retraining when encountering new vocabulary
* Possibly higher generalizability to different domains of documents

## 🚀 Our Approach
#### We start by allowing users to replace specific terms in the source sentences with predefined special tokens. Then, we train a model to understand that these special tokens represent specific terms and translate them into the correct syntax.
  <img width="500" alt="image" src="https://github.com/ycccccccccccc/Dictionary-aidedTranslationSystem/assets/91601942/2da0bb34-0438-47cf-aeb3-dadc231fd0aa">

## 🚀 In this project, I learned and utilized the following skills:
### Programming Language
1. Python
2. Hugging Face Pre-train Model

## 🚀 How to reproduce the project?

### Data Preprocessing

1. Download Dataset

* Translation Dataset
    Go to the "Global Patent Search System" to apply for an API verification code (https://gpss1.tipo.gov.tw/gpsskmc/gpssapi?ID=2&SECU=1936640155&PAGE=apply_code&FITSREC=api_code:0). After approval, send an API request based on the required domain and data quantity:
    ```
    curl -o <file_name>.json "https://gpss1.tipo.gov.tw/gpsskmc/gpss_api?userCode=<your_user_code>&IC=<domain_IPC_code>&expQty=<data_quantity>&expFmt=json&expFld=PN,ID,TI,AB"
    ```
    This experiment uses four domains: HO1L, A61, C07B, F01, and trains with HO1L and A61.

* Dictionary
    Download the "Chinese-English Patent Technical Term Bilingual Vocabulary" from the "Government Open Data Platform": https://tagp.tipo.gov.tw/api/v1/datagov/pt?filename=092-105-001.zip

2. Filter Valid Data

    Valid data refers to patent cases with both English and Chinese abstracts. You can use `./data_preprocess/filter_no_english.py` for filtering. 
    The third line in the file, `raw_data_path`, is the path to the raw file downloaded from the "Global Patent Search System," and the fourth line, `filtered_data_path`, is the location to store the filtered data.

3. Organize Dictionary

    nese-English Patent Technical Term Bilingual Vocabulary," and the eighth line is the output path.

4. Build Jieba Chinese Terminology Lexicon

    Download the default Jieba lexicon: https://raw.githubusercontent.com/fxsjy/jieba/master/extra_dict/dict.txt.big

    In `./data_preprocess/build_chinese_lexicon.py`, fill in the path of the Jieba default lexicon in the fifth line, the output path of the dictionary generated in step 3 in the sixth line, the output path of the Chinese terminology lexicon in the seventh line, and execute the program to generate the Chinese terminology lexicon.

5. Mark Term Translation Pairs

    In `./data_preprocess/jieba_replacement.py`, fill in the translation data path after step 2 in the ninth line, the output path after pairing in the tenth line, the path to the Jieba default lexicon (same as the fifth line in step 4) in the eleventh line, and the path to the Chinese terminology lexicon generated in step 4 (same as the sixth line in step 4), and execute.

    Completing the above steps will yield a processed dataset. Subsequent training only requires using the file output by step 5.

### Training

  Execute `bash run_translation.sh` to start training. Before training, several important parameters in run_translation.sh need to be specified:

  --output_dir: Path to save the model
  --train_file: Path to the training dataset
  --validation_file: Path to the validation dataset
  --test_file: Path to the test dataset
  --num_train_epochs: Number of training epochs
  --replace_terms: Whether to perform term replacement (set to true for the model to have term replacement functionality)

  If inference is needed, remove `--do_train` and `--do_eval`.



