import matplotlib.pyplot as plt
from gensim.models import word2vec
from sklearn.cluster import KMeans
import gensim
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import pairwise_distances
import chardet
import pickle
import jieba
import os



class Cluster(object):
    def __init__(self,vector_file,single_clean_file,single_final_file):
        self.vector_file=vector_file
        self.single_clean_file=single_clean_file
        self.single_final_file=single_final_file

    def cosine_similarity(self,x,y):#calculate the cosin similarity
        num = x.dot(y.T)
        denom = np.linalg.norm(x) * np.linalg.norm(y)
        return num / denom



    def To_cluster(self):
        print("正在开始聚类")
        f1 = open(self.vector_file, 'rb')
        word_and_vector = pickle.load(f1)
        f1.close()
        wordvector=[]
        word=[]
        for key,value in word_and_vector.items():
            word.append(key)
            wordvector.append(value)
        distortions=[]
        topword_all=[]
        for i in range(1,10):
            km=KMeans(n_clusters=i,init='k-means++',max_iter=300,tol=1e-4,random_state=0)
            km.fit(wordvector)
            labels=km.labels_#k labels
            center_vector_list=km.cluster_centers_#the centre of every cluster
            for center_vector in center_vector_list:
                classdict = {}  # store the index of the points which are most close to their centre
                for j in range(len(word)):
                    classdict[word[j]]=self.cosine_similarity(np.array(center_vector),np.array(wordvector[j]))
                a1 = sorted(classdict.items(), key=lambda x: x[1], reverse=True)
                number=0
                topword=[]
                for sets in a1:
                    if sets[1]>=0.6:
                        topword.append(sets[0])
                    number+=1

                print(topword)
                topword_all.append(topword)
                print('')


            distortions.append(km.inertia_)
            print(km.inertia_)
        plt.plot(range(1,10),distortions)
        plt.show()
        return topword_all

    def To_final(self):
        topword_all=self.To_cluster()
        df=pd.read_csv(self.single_clean_file)
        df['is_center_phrase']=''
        is_center_phrase=[]
        df['bad_phrase']=''
        bad_phrase=[]
        number=0#计数器
        for word in df['word']:
            is_center_phrase.append(False)
            for i in topword_all:
                if word in i:
                    is_center_phrase[-1]=True
            number+=1
            if number%100==0:
                print(number)
            phrase_cut=list(jieba.cut(word))
            if len(phrase_cut[0])==1 or len(phrase_cut[-1])==1:
                bad_phrase.append(True)
            else:
                bad_phrase.append(False)
        df['is_center_phrase']=is_center_phrase
        df['bad_phrase']=bad_phrase
        df.drop(df[(df['is_center_phrase'] == False)|(df['bad_phrase']==True)].index, inplace=True)
        df.to_csv(self.single_final_file)


















