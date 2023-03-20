import jieba
import chardet
import os
import pymysql




class word_cut(object):
    def __init__(self,mysql,stopwords_road,chinese_data_road):
        self.mysql=mysql
        self.stopwords_road=stopwords_road
        self.chinese_data_road=chinese_data_road


    def get_encoding(self,file):
        with open(file, 'rb') as f:
            return chardet.detect(f.read())['encoding']

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

    def to_cut(self):
        # connect to database to store the result of word cut
        db = self.mysql.cursor()
        dir_names = os.listdir(self.chinese_data_road)
        for dir_name in dir_names:
            number = 0
            for dirpath, dirname, filenames in os.walk(self.chinese_data_road + dir_name):
                for filename in filenames:
                    encode = self.get_encoding(self.chinese_data_road + dir_name + "/" + filename)
                    f = open(self.chinese_data_road + dir_name + "/" + filename, "r", encoding=encode,
                             errors='ignore')
                    content = f.read()

                    seg_list = jieba.cut(content, cut_all=True)
                    try:

                        str_len = len(content)
                        seg_len = len(jieba.lcut(content))
                        if str_len / seg_len < 1.2:  # whether we can not read the files because of the method of encoding

                            print(filename + "是乱码文件")
                            f.close()
                            os.remove(self.chinese_data_road + dir_name + "/" + filename)
                            print(filename + "已删除")
                            continue
                    except:
                        pass

                    words_after_stop = []
                    for w in seg_list:
                        if w not in self.chinese_data_road():
                            words_after_stop.append(w)

                    if len(words_after_stop) != 0:
                        sentence = ""
                        for i in words_after_stop:
                            sentence += i
                            sentence += " "
                        sql = "insert into matrix_cut_all(filename,category,content,word_cut_all)" \
                              "values(" + "'" + filename + "'" + ',' + "'" + dir_name + "'" + ',' + "'" + \
                              content + "'" + ',' + "'" + sentence + "'" + ')'  # 这个数据表需要之前设置好
                        try:
                            # excute the sql
                            db.execute(sql)
                            self.mysql.commit()
                        except Exception as e:
                            print(filename + '操作失败', e)
                            self.mysql.rollback()
                        number += 1
                        if number % 20 == 0:
                            print(dir_name + "类型文档已经处理了" + str(number) + "篇")
            print(dir_name)






























