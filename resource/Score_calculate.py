import pandas as pd
import numpy as np
import chardet
import os


class score_claculate(object):
    def __init__(self,single_raw_file,single_clean_file,stopwords_road):
        self.single_raw_file=single_raw_file
        self.stopwords_road=stopwords_road
        self.single_clean_file=single_clean_file


    def get_encoding(self, file):

        with open(file, 'rb') as f:
            return chardet.detect(f.read())['encoding']

    def create_stoplist(self):
        stoplists_chinese = set()
        for dirpath, dirname, filenames in os.walk(self.stopwords_road):  # 遍历当前文件夹下所有的停用词表
            for filename in filenames:
                encode = self.get_encoding(self.stopwords_road + str(filename))
                f = open(self.stopwords_road + str(filename), "r", encoding=encode, errors='ignore')
                for word in f.readlines():
                    word = word.replace('\n', '')
                    stoplists_chinese.add(word)
        return stoplists_chinese


    def read(self,file):
        df = pd.read_csv(file)
        df.drop(df[df['word'].str.len() < 4].index, inplace=True)  # drop the phrase with length<4
        all_content = []
        all_content.append(np.array(df['freq_radio']))
        all_content.append(np.array(df['dop']))
        all_content.append(np.array(df['left_free']))
        all_content.append(np.array(df['right_free']))
        return np.array(all_content), df

    #calculate the entropy
    def entropy(self,data0):

        n, m = np.shape(data0)

        maxium = np.max(data0, axis=1)
        minium = np.min(data0, axis=1)
        for i in range(0, 4):  # standardize
            data0[i] = (data0[i] - minium[i]) / (maxium[i] - minium[i])
        sumzb = np.sum(data0, axis=1)
        for i in range(0, 4):  # calculate the probability for entropy
            data0[i] = data0[i] / sumzb[i]

        a = data0 * 1.0
        a[np.where(data0 == 0)] = 0.000000001
        # calculate the entropy
        e = (-1.0 / np.log(m)) * np.sum(data0 * np.log(a), axis=1)
        # calculate the weight
        w = (1 - e) / np.sum(1 - e)
        print("权重是：", w)
        return w


    def standerdize(self,data0):
        K = np.power(np.sum(pow(data0, 2), axis=1), 0.5)
        for i in range(0, K.size):
            for j in range(0, data0[i].size):
                data0[i, j] = data0[i, j] / K[i]
        return data0

    # the score for a phrase to be grammarly correct
    def score(self,answer, w):
        list_max = []
        #use the topsis method
        for i in answer:
            list_max.append(np.max(i[:]))
        list_max = np.array(list_max)
        list_min = []
        for i in answer:
            list_min.append(np.min(i[:]))
        list_min = np.array(list_min)
        max_list = []
        min_list = []
        answer_list = []
        for k in range(0, np.size(answer, axis=1)):
            max_sum = 0
            min_sum = 0
            for q in range(0, 4):
                max_sum += w[q] * np.power(answer[q, k] - list_max[q], 2)
                min_sum += w[q] * np.power(answer[q, k] - list_min[q], 2)
            max_list.append(pow(max_sum, 0.5))
            min_list.append(pow(min_sum, 0.5))
            answer_list.append(min_list[k] / (min_list[k] + max_list[k]))  # Si = (Di-) / ((Di+) +(Di-))
        answer = np.array(answer_list)
        return (answer / np.sum(answer))

    def to_clean_file(self):
        stoplist=self.create_stoplist()
        file = self.single_raw_file

        data0, df = self.read(file)
        data2 = self.standerdize(data0)
        w = self.entropy(data2)
        result = self.score(data2, w)
        df['score'] = result
        print(result.shape)
        print(df.shape)
        df = df.groupby('word').sum()
        df['word'] = df.index
        for word in df['word']:
            for stop_word in stoplist:
                if stop_word in word:
                    df.drop(df[df['word'] == word].index, inplace=True)
                    break
        df = df.sort_values(by='score', ascending=False)
        df.to_csv(self.single_clean_file, index=False)
























