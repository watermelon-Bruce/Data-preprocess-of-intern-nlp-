from transfer import To_txt
from classify import classification
from Language_divide import language_divide
from Word_cut import word_cut
from Phrase_filter import phrase_filter
from Score_calculate import score_claculate
from resource.Keywords_get import keywords_get
import pymysql

source_road=''#path of docx,xls file
target_road=''#path of raw txt file
log_road=''#path for log
comparison_table_road = '../docs/classification_reference'#path of comparison tables
raw_data_road = '../docs/txt_classification/raw_data'#path of raw txt without beening divided by language
chinese_data_road = '../docs/txt_classification/Chinese'#path of Chinese txt
english_data_road = '../docs/txt_classification/English'#path of English txt
stopwords_road='../docs/stopwords'#path of stopwords
content_road='../docs/pickle/content'#path of Chinese txt files
seglist_road='../docs/pickle/seglist'#path of result of word cutting
raw_file_newword='../docs/file/raw_file'
clean_file_newword='../docs/file/clean_file'
single_raw_file='../docs/file/raw_file/New_word_002.csv'
single_clean_file='../docs/file/clean_file/newword_002_4-6.csv'
single_special_stopwords='../docs/special/002.txt'
single_idf='../docs/idf/002_idf.txt'
single_key_word='../docs/pickle/keywords/002_keywords.pickle'
single_NewWords_tfidf='../docs/NewWords_tfidf/newword_002_4-6.csv'

mysql = pymysql.connect(
    host='localhost',
    user='root',
    password='ch111111',
    port=3306,
    charset='utf8',
    database='transon02'
)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':


    Get_txt=To_txt(source_road,target_road,log_road)
    '''
    To_txt class
    :param source_road:path for docx and xls files
    :param target_road:path for output txt files
    :param log_road:path for log
    '''
    Get_txt.to_txt()#transfer docx , xls to txt

    Get_classification=classification(comparison_table_road,target_road,raw_data_road)
    '''
    :param comparison_table_road: path of comparison tables
    :param target_road:path of original txt files that haven't been classify
    :param raw_data_road:txt path of txt files been classified
    '''
    Get_classification.to_classify()#classify files according to some comparison tables


    Get_divide=language_divide(raw_data_road,chinese_data_road,english_data_road)
    '''
    :param raw_data_road txt:path of raw txt without beening divided by language
    :param chinese_data_road:path of Chinese txt
    :param english_data_road:path of English txt
    '''
    Get_divide.to_divide()#divide English and Chinese txt

    Get_word_cut=word_cut(mysql,stopwords_road,chinese_data_road)
    '''
    :param mysql:database config information
    :param stopwords_road:path of stopwords
    :param chinese_data_road:path of Chinese road
    '''
    Get_word_cut.to_cut()# cut words

    Get_raw_file_newword=phrase_filter(max_len_word=6,content_road=content_road,seglist_road=seglist_road,stopwords_road=stopwords_road,raw_file_newword=raw_file_newword)
    '''
    :param max_len_word:window size for calculating informmation entropy and Mutual Information
    :param content_road pickle:path of Chinese txt files
    :param seglist_road pickle:path of result of word cutting
    :param raw_file_newword :path of all the phrase
    '''
    Get_raw_file_newword.filter()#filter the phrase by  information entropy and Mutual Information

    Get_clean_file_newword=score_claculate(single_raw_file=single_raw_file,single_clean_file=single_clean_file,stopwords_road=stopwords_road)
    '''
    :param single_raw_file raw_file:path of all the phrase
    :param single_clean_file clean_file:path of the phrase of score
    '''
    Get_clean_file_newword.to_clean_file()

    Get_keywords=keywords_get(single_special_stopwords,single_idf,single_key_word,single_clean_file,single_NewWords_tfidf,mysql)
    '''
    single_idf每一个类下的idf值路径
    '''
    Get_keywords.to_NewWords_tfidf()























