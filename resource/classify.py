import os
import re
import shutil
import pandas as pd





class classification(object):
    def __init__(self,comparison_table_road,source_road,target_road):
        self.comparison_table_road=comparison_table_road
        self.source_road=source_road
        self.target_road=target_road
    def to_classify(self):
        # get the path of reference table
        tabels_list = os.listdir(self.comparison_table_road)  #list contains all the names of the reference tables
        tabels_paths = []
        for name in tabels_list:
            tabels_paths.append(self.comparison_table_road + name)

        print(os.listdir(self.source_road))
        i = 0
        try:
            for tabel in tabels_list:
                str1 = re.compile('(.*?).(xls|xlsx)$')
                match_obj1 = re.findall(str1, tabel)
                filelist = os.listdir(self.source_road + match_obj1[0][0])  # get all the files contained in reference table
                df = pd.read_excel(tabels_paths[i], usecols=[0, 1, 4, 5], dtype='object')
                df.columns = ['项目号', '一级行业', '类别', '备注']
                df.dropna(axis=0, inplace=True, subset=['项目号', '一级行业', '类别'], how='any')
                new_level1 = []
                for j in df['一级行业']:  # Uniform the format
                    new_level1.append(str(j).rjust(3, '0'))
                df['一级行业'] = new_level1
                project_name_clean = []
                for j in df['项目号']:
                    project_name_clean.append(re.match(r'(\w)*', j).group())
                df['项目号'] = project_name_clean
                df_group = df.groupby(['一级行业', '类别'])
                for name, group in df_group:  # for every specific category,create a fold
                    try:
                        current_dir = re.findall('([A-Za-z]+[0-9]+)', name[1])
                        first_dir = re.findall('[0-9]{1,3}', name[0])  # whether the current file belong to multiple categories
                        for first in first_dir:
                            for catogoty in current_dir:
                                catogoty = str(catogoty)
                                if 'O' in catogoty:
                                    catogoty = catogoty.replace('O', '0')
                                fullname = str(first) + "," + catogoty
                                if fullname not in os.listdir(self.target_road):
                                    os.mkdir(self.target_road + fullname)
                                current_project_numbers = list(df_group.get_group(name)['项目号'])  # find all the file id of current category
                                current_extra = list(df_group.get_group(name)['备注'])
                                current_prefix = []
                                for extra in current_extra:  # find all the file with prefix (Q1,Q2,Q3,Q4)
                                    prefixs = re.findall('(Q1|Q2|Q3|Q4)', str(extra))
                                    if len(prefixs) != 0:
                                        content = ''
                                        for prefix in prefixs:
                                            content += "@"
                                            content += str(prefix)
                                        current_prefix.append(content)
                                    else:
                                        current_prefix.append('')
                                for j in range(len(current_project_numbers)):
                                    for file in filelist:
                                        if re.match(current_project_numbers[j] + '.*', file) != None:
                                            shutil.copyfile(
                                                self.source_road + match_obj1[0][0] + "/" + file,
                                                self.target_road + fullname + "/" +
                                                current_prefix[j] + file)
                    except:
                        print(str(name) + "出错")
                        pass
                i += 1
        except:
            print("遍历对照表时出错")
            raise
            pass


































