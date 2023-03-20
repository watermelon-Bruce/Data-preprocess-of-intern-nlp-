from gensim.models import Word2Vec
import pickle
import jieba
import chardet
import os
import pandas as pd
import gensim
import numpy as np


class wordtovec(object):
    def __init__(self,seglist_road,model_road,single_clean_file,vector_file):
        self.seglist_road=seglist_road
        self.model_road=model_road
        self.single_clean_file=single_clean_file
        self.vector_file=vector_file


    def To_vector(self):
        f1 = open(self.seglist_road, 'rb')
        seglist = pickle.load(f1)
        f1.close()
        text=[]
        for sentence in seglist:
            sentence=sentence.split()
            text.append(sentence)

        model = Word2Vec(sentences=text,window=10,sg=1,epochs=100)
        model.save(self.model_road)

    def To_phrase_vector(self):
        df=pd.read_csv(self.single_clean_file)
        model = gensim.models.Word2Vec.load(self.model_road)
        keys = model.wv.index_to_key
        wordvector = model.wv.vectors

        df['word_vector_sum']=np.nan
        df['word_vector_number']=np.nan
        df['word_vector_average']=np.nan
        word=list(df['word'])
        word_vector_sum=[]
        word_vector_number=[]
        word_vector_average=[]
        word_and_vector = {}
        i=0
        for phrase in df['word']:
            word_vector_sum.append(np.zeros(100))
            word_vector_number.append(0)
            word_vector_average.append(0)
            phrase_cut=list(jieba.cut(phrase))

            for j in range(len(keys)):
                if keys[j] in phrase_cut:
                    word_vector_sum[-1]+=wordvector[j]
                    word_vector_number[-1]+=1
                    word_vector_average[-1]=word_vector_sum[-1]/word_vector_number[-1]
                    word_and_vector[phrase]=word_vector_average[-1]
            i+=1
            if i%1000==0:
                print('已计算',i,'行短语的vector')


        print(word_and_vector)
        file = open(self.vector_file, 'wb')
        pickle.dump(word_and_vector, file)
        file.close()











