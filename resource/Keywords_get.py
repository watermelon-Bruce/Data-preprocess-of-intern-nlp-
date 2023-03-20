from jieba.analyse import *
from pymysql import cursors
import jieba
import math
import chardet
import pickle
import pandas as pd
import os

class keywords_get(object):
    def __init__(self,single_special_stopwords,single_idf,single_key_word,single_clean_file,single_NewWords_tfidf,single_seglist_road):
        self.single_special_stopwords=single_special_stopwords
        self.single_seglist_road=single_seglist_road
        self.single_idf=single_idf
        self.single_key_word=single_key_word
        self.single_clean_file=single_clean_file
        self.single_NewWords_tfidf=single_NewWords_tfidf


    def get_encoding(self,file):
        # detect the languages by the methods of encoding
        with open(file, 'rb') as f:
            return chardet.detect(f.read())['encoding']

    def get_stopwords(self):
        stoplists_chinese = set()
        encode = self.get_encoding(self.single_special_stopwords)
        f = open(self.single_special_stopwords, "r", encoding=encode, errors='ignore')
        for word in f.readlines():
            word = word.replace('\n', '')
            stoplists_chinese.add(word)
        return stoplists_chinese

    def claculate_keyword(self):
        f2 = open(self.single_seglist_road, 'rb')
        word_cut_list = pickle.load(f2)
        f2.close()
        special_stop_word=self.get_stopwords()
        corpous = []
        contents = ''
        for word_cut in word_cut_list:
            result_clean=word_cut
            for stop_word in special_stop_word:
                result_clean = result_clean.replace(' ' + stop_word, '')
            corpous.append(result_clean)
            contents += result_clean
        #claculate the tfidf
        idf_dic = {}
        doc_count = len(corpous)  # number of docs
        print("开始计算逆文档数")
        for i in range(len(corpous)):
            new_content = corpous[i].split(' ')
            for word in set(new_content):
                if len(word) > 1:
                    idf_dic[word] = idf_dic.get(word, 0.0) + 1.0

        print("开始计算idf")
        for k, v in idf_dic.items():
            w = k
            p = '%.10f' % (math.log(doc_count / (1.0 + v)))  # 结合上面的tf-idf算法公式
            idf_dic[w] = p
        print("开始写入idf文件")
        with open(self.single_idf, 'w', encoding='utf-8') as f:
            for k in idf_dic:
                if k != '\n':
                    f.write(str(k) + ' ' + str(idf_dic[k]) + '\n')  # 写入txt文件，注意utf-8，否则jieba不认

        print('读取idf文件')
        jieba.analyse.set_idf_path(self.single_idf)  # 载入自定义idf库
        print('开始提取关键词')
        keywords = tfidf(contents, topK=3000, withWeight=True, allowPOS=('n', 'nr', 'ns'))
        # for keyword in keywords:
        #     print(keyword[0])
        file = open(self.single_key_word, 'wb')  # store the top 3000 keywords
        pickle.dump(keywords, file)
        file.close()

    def to_NewWords_tfidf(self):
        self.claculate_keyword()
        # calculate the tfidf for every phrase
        f1 = open(self.single_key_word, 'rb')
        keywords = pickle.load(f1)
        f1.close()
        df = pd.read_csv(self.single_clean_file)
        # print(df.columns)
        df['tfidf'] = ''
        for i in range(len(df['word'])):  # for every phrase
            df.iloc[i, 8] = 0
            for j in range(len(keywords)):
                if keywords[j][0] in df.iloc[i, 7]:
                    df.iloc[i, 8] += keywords[j][1]
            # if i % 10 == 0:
            #     print(i)
        df.to_csv(self.single_NewWords_tfidf)  # store the tfidf result of phrases





























