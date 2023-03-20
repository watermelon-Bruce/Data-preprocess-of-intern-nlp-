from chen import Phrase_find
import os
import pickle
import pandas as pd
import chardet
import re


class phrase_filter(object):
    def __init__(self,max_len_word,content_road,seglist_road,stopwords_road,raw_file_newword):
        self.max_len_word=max_len_word
        self.content_road=content_road
        self.seglist_road=seglist_road
        self.stopwords_road=stopwords_road
        self.raw_file_newword=raw_file_newword


    def get_encoding(self, file):
        with open(file, 'rb') as f:
            return chardet.detect(f.read())['encoding']

    #create the stopwords list by union the several stopwords list
    def create_stoplist(self):
        stoplists_chinese = set()
        for dirpath, dirname, filenames in os.walk(self.stopwords_road):
            for filename in filenames:
                encode = self.get_encoding(self.stopwords_road + str(filename))
                f = open(self.stopwords_road + str(filename), "r", encoding=encode, errors='ignore')
                for word in f.readlines():
                    word = word.replace('\n', '')
                    stoplists_chinese.add(word)

        return stoplists_chinese

    def filter(self):
        content_list = os.listdir(self.content_road)  # original txt
        seglist_list = os.listdir(self.seglist_road)  # word cut result
        for j in range(len(content_list)):
            f1 = open(self.content_road + content_list[j], 'rb')
            sentence = pickle.load(f1)
            f1.close()
            f2 = open(self.seglist_road + seglist_list[j], 'rb')
            word_cut_all = pickle.load(f2)
            f2.close()
            df_all = pd.DataFrame(
                columns=['word', 'freq', 'freq_radio', 'dop', 'left_free', 'right_free', 'score', 'NewWord'])
            try:
                for i in range(len(sentence)):
                    try:
                        nw = Phrase_find.phrase_find(max_len_word=self.max_len_word)  # 6-gram模型
                        df = nw.run(sentence[i])
                        df = df.reset_index()
                        df.columns = ['word', 'freq', 'freq_radio', 'dop', 'left_free', 'right_free', 'score']

                        stopwords=self.create_stoplist()
                        df['NewWord'] = df.apply(
                            lambda x: x['word'] not in word_cut_all[i] and x['word'] not in stopwords, axis=1)

                        df.drop(df[(df['NewWord'] == False) | (df['left_free'] == 0) | (df['right_free'] == 0) | (
                                    df['freq'] == 1) | (
                                           df['dop'] == 0)].index, inplace=True)
                        df_all = pd.concat([df_all, df], ignore_index=True)  # 将发现的短语与之前的dataframe拼接
                        # print(i)
                        if i % 20 == 0:  # for every 20 files,we store the result
                            df_all.to_csv(
                                self.raw_file_newword + 'New_word'+str(re.findall("_.*\d", content_list[j])[0]) + '.csv',
                                index=False)
                    except:

                        pass
            except:
                pass
            df_all.to_csv(self.raw_file_newword + 'New_word'+str(re.findall("_.*\d", content_list[j])[0]) + '.csv', index=False)


















