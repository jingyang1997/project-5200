# -*- coding:utf-8 -*-
import urllib
import re
from html.parser import HTMLParser
import nltk
import html


class dataProcesser(object):
    def __init__(self, min_len):
        self.MIN_LEN = min_len
        self.SEN = ['<', '>', ',', ':', '\'', '/', ';', '"', '{', '}', '(', ')']
        self.tokens_pattern = r'''(?x)
             "[^"]+"
            |http://\S+
            |</\w+>
            |<\w+>
            |<\w+
            |\w+=
            |>
            |\w+\([^<]+\) #函数 比如alert(String.fromCharCode(88,83,83))
            |\w+
            '''
        self.index_wordbag=1
        self.wordbag={}

    def ischeck(self, str):
        if re.match(r'^(http)', str):
            return False
        for i, c in enumerate(str):
            if ord(c) > 127 or ord(c) < 31:
                return False
            if c in self.SEN:
                return True
            # 排除中文干扰 只处理127以内的字符

        return False

    def do_str(self, line):
        words = nltk.regexp_tokenize(line, self.tokens_pattern)
        # print  words
        return words

    def load_wordbag(self, filename, max=100):
        X = [[0]]
        X_lens = [1]
        tokens_list = []

        with open(filename) as f:
            for line in f:
                line = line.strip('\n')
                # url解码
                line = urllib.parse.unquote(line)

                # 处理html转义字符
                line = html.unescape(line)
                if len(line) >= self.MIN_LEN:
                    # print "Learning xss query param:(%s)" % line
                    # 数字常量替换成8
                    line, number = re.subn(r'\d+', "8", line)
                    # ulr日换成http://u
                    line, number = re.subn(r'(http|https)://[a-zA-Z0-9\.@&/#!#\?:=]+', "http://u", line)
                    # 干掉注释
                    line, number = re.subn(r'\/\*.?\*\/', "", line)
                    # print "Learning xss query etl param:(%s) " % line
                    tokens_list += self.do_str(line)

                # X=np.concatenate( [X,vers])
                # X_lens.append(len(vers))

        fredist = nltk.FreqDist(tokens_list)  # 单文件词频
        keys = list(fredist.keys())
        keys = keys[:max]
        for localkey in keys:  # 获取统计后的不重复词集
            if localkey in self.wordbag.keys():  # 判断该词是否已在词袋中
                continue
            else:
                self.wordbag[localkey] = self.index_wordbag
                self.index_wordbag += 1

        print("GET wordbag size(%d)" % self.index_wordbag)
        print(self.wordbag.keys())

testDataProcessor = dataProcesser(5)
testDataProcessor.load_wordbag("xss-train.txt", 2000)
