# -*- coding: utf-8 -*-
import os
# 正则包
import re
# html 包
import html
# 自然语言处理包
import jieba
import jieba.analyse
# 机器学习包
import sys

from sklearn.metrics.pairwise import cosine_similarity


class CosineSimilarity(object):
    """
    余弦相似度
    """
    def __init__(self, content_x1, content_y2):
        self.s1 = content_x1
        self.s2 = content_y2

    @staticmethod
    def extract_keyword(content):  # 提取关键词
        # 正则过滤 html 标签
        re_exp = re.compile(r'(<style>.*?</style>)|(<[^>]+>)', re.S)
        content = re_exp.sub(' ', content)
        # html 转义符实体化
        content = html.unescape(content)
        # 切割
        seg = [i for i in jieba.cut(content, cut_all=True) if i != '']
        # 提取关键词
        keywords = jieba.analyse.extract_tags("|".join(seg), topK=200, withWeight=False)
        return keywords

    @staticmethod
    def one_hot(word_dict, keywords):  # oneHot编码
        # cut_code = [word_dict[word] for word in keywords]
        cut_code = [0]*len(word_dict)
        for word in keywords:
            cut_code[word_dict[word]] += 1
        return cut_code

    def main(self):
        # 去除停用词
        jieba.analyse.set_stop_words(r'C:\Users\123\AppData\Local\Programs\Python\Python37\sim_0.8\stopwords.txt')

        # 提取关键词
        keywords1 = self.extract_keyword(self.s1)
        keywords2 = self.extract_keyword(self.s2)
        # 词的并集
        union = set(keywords1).union(set(keywords2))
        # 编码
        word_dict = {}
        i = 0
        for word in union:
            word_dict[word] = i
            i += 1
        # oneHot编码
        s1_cut_code = self.one_hot(word_dict, keywords1)
        s2_cut_code = self.one_hot(word_dict, keywords2)
        # 余弦相似度计算
        sample = [s1_cut_code, s2_cut_code]
        # 除零处理
        try:
            sim = cosine_similarity(sample)
            return sim[1][0]
        except Exception as e:
            print(e)
            return 0.0
     
# 测试
if __name__ == '__main__':
    #x=r'C:\Users\123\AppData\Local\Programs\Python\Python37\sim_0.8\orig.txt'
    #y=r'C:\Users\123\AppData\Local\Programs\Python\Python37\sim_0.8\orig_0.8_add.txt'
    #输入文件路径的设置
    x=input()
    y=input()
    z=input()
    fx=open(x,'r',encoding='utf-8')
    fy=open(y,'r',encoding='utf-8')
    content_x = fx.read()
    content_y = fy.read()
    similarity = CosineSimilarity(content_x, content_y)
    similarity = similarity.main()
    #写入文件设置
    g = open(r"C:\Users\123\AppData\Local\Programs\Python\Python37\result.txt",'w+')
    file_handle=open('result.txt',mode='w')
    file_handle.write('相似度: {:.2f}' .format(similarity))
    file_handle.close()
    #print(r'C:\Users\123\AppData\Local\Programs\Python\Python37\result.txt'+':'+similarity)
    fx.close()
    fy.close()
    print('相似度: {:.2f}' .format(similarity))

