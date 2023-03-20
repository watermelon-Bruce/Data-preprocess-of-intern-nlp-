# Goal of this project

### 		In this project, I wrote some modules to do some basic nlp work. As for how to use them, you can read the instruments for module in the latter part. And the main.py file will also help you understand how to use them . The text data of this project won't be upload because it is too large and I don't have the right for sharing  it

# Structure

```
├── Readme.md                   // help
├── resource                    // code
│   ├── test                    // test code
│   │   ├── main_for_test.py    
│   ├── main.py                 // 
│   ├── transfer.py             // module for transfering docx,xls to txt
│   ├── classify.py             // module for classifing files according to some rules 
│   ├── Language_divide.py      // module for dividing English and Chinese txt
│   ├── Word_cut.py             // module for word cutting
│   ├── Phrase_find.py          // module for calculating information entropy and Mutual Information
│   ├── Phrase_filter.py        // module for filting phrase according to some rules
│   ├── Score_calculate.py      // module for calculating score for phrase
│   ├── Keywords_get.py         // module for calculating tfidf value
├── docs                        // data
│   ├── txt_classification                  
│   │   ├──raw_data             // txt data
│   │   ├──Chinese              // Chinese txt data
│   │   ├──English              // English txt data
│   ├── classification_reference// reference xls for classify files
│   ├── pickle_file
│   │   ├── word_cut            // word cutting result by using jieba library(store by pckl file)
│   │   ├── keywords            // key words result(store by pckl file)
│   ├── special_stopwords       // stopwords for some specific topics
│   ├── idf_result              // tfidf value for each file
│   ├── common_stopwords        // common stopwords
│   ├── phrase_file
│   │   ├── raw_file            // all the phrase I find
│   │   ├── clean_file          // phrase after filtering by some rules
└── extra                       // extra instruments
```

# Module instruments

## transfer.py

**function:** transfer docx , xls to txt

**Class：**To_txt

**Input：**

source_road：path for docx and xls files

target_road：path for output txt files

log_road: path for log

**output：**

txt files after transfering

## classify.py

**function:** classify files according to some comparison tables

**Class：**classification

**Input：**

comparison_table_road：path of comparison tables

source_road：path of original txt files that haven't been classify

target_road：path of txt files been classified

**output：**

txt files been classified

## Language_divide.py

**function:** divide English and Chinese txt

**Class：**language_divide

**Input：**

raw_data_road：path of raw txt without beening divided by language

chinese_road：path of Chinese txt

english_road：path of English txt

**output：**

txt files after been divided by language

## Word_cut.py

**function:** cut words

**Class：**word_cut

**Input：**

mysql：database config information

stopwords_road：path of stopwords

chinese_data_road：path of Chinese road

**output：**

word cut result of txt files

## Phrase_find.py

**function:** find phrase in sentence

**Class：**phrase_find

**Input：**

max_len_word：window size

## Phrase_filter.py

**function:** filter the phrase by  information entropy and Mutual Information

**Class：**phrase_filter

**Input：**

max_len_word：window size for calculating informmation entropy and Mutual Information

content_road：path of Chinese txt files

seglist_road：path of result of word cutting

stopwords_road：path of stopwords

raw_file_newword：path of all the phrase

**output：**

all the phrase i find

## Score_calculate.py

**function:** calculate the probability for a phrase to be a real phrase

(the way i calculate the score is the TOPSIS analysis)

**Class：**score_claculate

**Input：**

single_raw_file：path of all the phrase

single_clean_file：path of the phrase of score

stopwords_road：path of stopwords

**output：**

the phrase with socre

