import os
import re
import subprocess as sp
import xlrd


#transfer the docx,xlx to txt
class To_txt(object):
    def __init__(self,source_road,target_road,log_road):
        self.source_road=source_road
        self.target_road=target_road
        self.log_road=log_road

    def get_file_road(self,source_road):
        source_dir_list = os.listdir(source_road)
        source_dir_path = []
        for i in source_dir_list:
            source_dir_path.append(source_road + i)
        return source_dir_path,source_dir_list

    # use the extra instruments to transfer the docx to xlx
    def doc2txt(self,source_road, target_road, log_path):
        parse_path = r'../extra/parse_doc_docx.exe'  # path of the extra instruments
        p = sp.Popen(parse_path, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
        p.stdin.write(bytes(source_road + '\n', 'gbk'))
        p.stdin.flush()
        p.stdin.write(bytes(target_road + '\n', 'gbk'))
        p.stdin.flush()
        p.stdin.write(bytes(log_path + '\n', 'gbk'))
        p.stdin.flush()
        stdout, stderr = p.communicate()
        print('stdout is:', stdout.decode('gbk'))
        print('stderr is:', stderr.decode('gbk'))
        return stderr

    # transfer the whole row of a xlx file to txt
    def strs(self,row):
        try:
            values = "";
            for i in range(len(row)):
                if i == len(row) - 1:
                    values = values + str(row[i])
                else:

                    values = values + str(row[i]) + ","
            return values
        except:
            raise

    # transfer xlx to txt
    def xls_txt(self,xls_name, txt_name):
        """

        :param xls_name excel 文件名称
        :param txt_name txt   文件名称
        """
        try:
            data = xlrd.open_workbook(xls_name)
            num = data.nsheets  # get the number of the sheets
            sqlfile = open(txt_name, "a", encoding='utf-8')
            for i in range(num):
                sheet = data.sheets()[i]
                nrows = sheet.nrows  # the number of rows
                for ronum in range(nrows):
                    row = sheet.row_values(ronum)
                    values = self.strs(row)
                    sqlfile.writelines(values)
            sqlfile.close()
        except:
            print(xls_name)
            pass

    def to_txt(self):
        i = 0
        source_dir_path,source_dir_list=self.get_file_road(self.source_road)
        for path in source_dir_path:
            if source_dir_list[i] not in os.listdir(self.target_road):
                os.mkdir(self.target_road + source_dir_list[i])
            try:
                self.doc2txt(path, self.target_road + source_dir_list[i],
                        self.log_road)
            except:
                print(path + "word文档未能成功转换")
            for dirpath, dirnames, filenames in os.walk(path):
                for filename in filenames:
                    str1 = re.compile('(.*?).(xls|xlsx)$')  # find the xlx file
                    match_obj1 = re.findall(str1, filename)
                    if match_obj1:
                        try:
                            self.xls_txt(path + "/" + filename,
                                    self.target_road + source_dir_list[i] + "/" + filename + '.txt')
                        except:
                            raise
            i += 1
            print(i)

























