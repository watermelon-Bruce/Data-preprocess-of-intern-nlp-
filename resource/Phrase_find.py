import math
import re
import pandas as pd


class phrase_find(object):
    def __init__(self, max_len_word):
        self.max_len_word = max_len_word  # windows size for n-gram
        self.words = {}

    def find_words(self, doc):
        '''
        找出所有可能出现的词， doc为传进去的文本
        :param doc:
        :param max_len_word:
        :return:
        '''
        len_doc = len(doc)  # length of doc
        for i in range(len_doc):
            for j in range(i + 1, i + self.max_len_word + 1):
                if doc[i:j] in self.words:
                    self.words[doc[i:j]]['freq'] += 1
                else:
                    self.words[doc[i:j]] = {}
                    self.words[doc[i:j]]['freq'] = 1

    def dop(self):
        '''
        compute the dop
        :param words:
        :return:
        '''
        len_words = len(self.words)

        for k, v in self.words.items():
            self.words[k]['freq_radio'] = self.words[k]['freq'] / (5 * len_words)  # 计算每个词的概率
        for k, v in self.words.items():
            dop = []
            l = len(k)
            if l == 1:  # for every single characters, the dop is set to be 0
                self.words[k]['dop'] = 0
            else:
                for i in range(1, l):

                    word = self.words[k[0:i]]['freq_radio'] * self.words[k[i:l]]['freq_radio']
                    dop.append(word)
                dop = sum(dop)
                self.words[k]['dop'] = self.words[k]['freq_radio'] / dop

    def left_free(self, doc):
        '''
        left degree of freedom
        :param words:
        :return:
        '''
        for k, v in self.words.items():
            left_list = [m.start() for m in re.finditer(k, doc) if m.start() != 1]
            len_left_list = len(left_list)
            left_item = {}
            for li in left_list:
                if li - 1 >= 0:
                    if doc[li - 1] in left_item:
                        left_item[doc[li - 1]] += 1
                    else:
                        left_item[doc[li - 1]] = 1
            left = 0
            for _k, _v in left_item.items():
                left += abs((left_item[_k] / len_left_list) * math.log(1 / len(left_item)))
            self.words[k]['left_free'] = left

    def right_free(self, doc):
        '''
        right degree of freedom
        :param words:
        :return:
        '''
        for k, v in self.words.items():
            right_list = [m.start() for m in re.finditer(k, doc) if m.start() < len(doc) - 5]
            len_right_list = len(right_list)
            right_item = {}
            for li in right_list:
                if li + len(k) < len(doc):
                    if doc[li + len(k)] in right_item:
                        right_item[doc[li + len(k)]] += 1
                    else:
                        right_item[doc[li + len(k)]] = 1
            right = 0
            for _k, _v in right_item.items():
                right += abs((right_item[_k] / len_right_list) * math.log(1 / len(right_item)))
            self.words[k]['right_free'] = right

    def get_df(self):
        df = pd.DataFrame(self.words)
        df = df.T
        df['score'] = df['dop'] + df['left_free'] + df['right_free']
        df = df.sort_values(by='score', ascending=False)
        return df

    def run(self, doc):
        self.find_words(doc)
        self.dop()
        self.left_free(doc)
        self.right_free(doc)
        df = self.get_df()
        return df