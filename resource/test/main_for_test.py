





from resource import Phrase_filter
from resource import Score_calculate
from resource import Keywords_get
from resource import WordtoVec
from resource import cluster
import os



max_len_word=6#window size(don't set to be larger than 6,which will cost a lot of time)
content_road=r'pickle/word_cut_all/content/'
seglist_road=r'pickle/word_cut_all/seglist/'
stopwords_road=r'../../docs/stopwords/'
raw_file_newword=r'file/raw_file/'
single_raw_file=r'file/raw_file/New_word_X012.csv'
single_clean_file=r'file/clean_file/New_word_X012.csv'
single_special_stopwords=r'special/X012.txt'
single_idf=r'idf/X012_idf.txt'
single_key_word=r'pickle/keywords/X012_keywords.pckl'
single_NewWords_tfidf=r'NewWords_tfidf/newword_X012.csv'
single_seglist_road=r'pickle/word_cut/seglist/seglist_X012.pckl'


if __name__=='__main__':
    # print("测试：生成初步过滤短语，结果存储在test/file/raw_file中")
    # Get_raw_file_newword =Phrase_filter.phrase_filter(max_len_word,content_road,seglist_road,stopwords_road,raw_file_newword)
    # Get_raw_file_newword.filter()
    # print("测试：计算成词得分，结果存储在test/file/clean_file中")
    # Get_clean_file_newword=Score_calculate.score_claculate(single_raw_file,single_clean_file,stopwords_road)
    # Get_clean_file_newword.to_clean_file()
    # print("测试：计算短语tfidf权重，结果存储在test/NewWords_tfidf中")
    # Get_keywords=Keywords_get.keywords_get(single_special_stopwords,single_idf,single_key_word,single_clean_file,single_NewWords_tfidf,single_seglist_road)
    # Get_keywords.to_NewWords_tfidf()
    # print("测试，计算词向量，结果存储在")
    Get_wordvec=WordtoVec.wordtovec('../../docs/pickle/word_cut/seglist/seglist_X004.pckl','../../docs/WordToVec/word2vec_X004.model',
                                    '../../docs/file/clean_file/newword_X004_4-6.csv','../../docs/file/vector_file/word_and_vector_X004.pckl')
    Get_wordvec.To_vector()
    Get_wordvec.To_phrase_vector()
    Get_cluster=cluster.Cluster(vector_file='../../docs/file/vector_file/word_and_vector_X004.pckl',single_clean_file='../../docs/file/clean_file/newword_X004_4-6.csv'
                                ,single_final_file='../../docs/file/final/final_X004.csv')
    Get_cluster.To_cluster()


































