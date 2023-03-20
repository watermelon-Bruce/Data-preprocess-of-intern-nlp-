import re
import chardet
import warnings
import os





class language_divide(object):

    def __init__(self,raw_data_road,chinese_road,english_road):
        self.chinese_road=chinese_road
        self.english_road=english_road
        self.raw_data_road=raw_data_road
        warnings.filterwarnings("ignore")
        '''This function is used to get the encoding of the current file, 
        and then pass the encoding to the open function to solve the problem 
        of opening different files with different encodings.'''

    def get_encoding(self,file):

        with open(file, 'rb') as f:
            return chardet.detect(f.read())['encoding']

    # divide the files by languages
    def Divide(self,content):
        chinese = re.findall('[\u4e00-\u9fa5]+', content)# recognize the encoding
        english = re.findall('[a-zA-Z]+', content)
        chinese_content = ''
        english_content = ''
        for i in chinese:
            chinese_content += str(i)
        for i in english:
            english_content += (str(i) + " ")
        return chinese_content, english_content

    def to_divide(self):
        catogerys = os.listdir(self.raw_data_road)
        for catogery in catogerys:
            os.mkdir(self.chinese_road + str(catogery))
            os.mkdir(self.english_road + str(catogery))
            for dirpath, dirname, filenames in os.walk(self.raw_data_road + str(catogery)):
                for filename in filenames:
                    try:
                        encode = get_encoding(
                            self.raw_data_road + str(catogery) + "/" + filename)
                        f = open(self.raw_data_road + str(catogery) + "/" + filename, "r", encoding=encode,
                                 errors='ignore')
                        content = f.read()
                        chinese_content, english_content = Divide(content)
                        if len(chinese_content) != 0:
                            chinese_file = open(self.chinese_road + str(catogery) + "/" + filename,
                                                'w')
                            chinese_file.write(chinese_content)
                            chinese_file.close()
                        if len(english_content) != 0:
                            english_file = open(self.english_road + str(catogery) + "/" + filename,
                                                'w')
                            english_file.write(english_content)
                            english_file.close()
                    except:
                        raise
                        print(filename)
            print(catogery)















