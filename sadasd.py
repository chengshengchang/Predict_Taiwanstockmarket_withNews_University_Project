import requests
from bs4 import BeautifulSoup
import pymysql
import MySQLdb
import re
import datetime

from gensim.models import Word2Vec
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  6 00:07:41 2021

@author: admin
"""

import requests
from bs4 import BeautifulSoup
import re

#爬蟲
def getweb_page(url , head):
    html_page = requests.get(url ,headers=head)
    
    if html_page.status_code != 200:
        print('invalid page',html_page.status_code)
        return None
    else:
        return html_page.text
    
#這是讀取頭
head = {"User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.3"}

#開啟檔案
file = open('C:\\Users\\aa092\\OneDrive\\桌面\\專題\\practice.txt',"w",encoding="utf-8")



#所有文章內文
site_content=[]

#udn 聯合新聞網


#抓取網址 [[[udn]]]

site_udn = "https://udn.com/news/cate/2/6645"
html_udn = getweb_page(site_udn,head)

#soup套件處理html資料

soup_udn = BeautifulSoup(html_udn,'html.parser')
#對網頁進行析取時，並未規定解析器，此時使用的是python內部默認的解析器“html.parser”。
#解析器：BeautifulSoup做的工作就是對html標簽進行解釋和分類，不同的解析器對相同html標簽會做出不同解釋。

#yahoo

#抓取網址 [[yahoo]]
site_yahoo = 'https://tw.stock.yahoo.com/tw-market'
html_yahoo =  getweb_page(site_yahoo,head)

#soup套件處理html資料

soup_yahoo =BeautifulSoup(html_yahoo,'html.parser')


#裝article的網址                                  
site_article_yahoo = []

time_yahoo = 20
for t in range(time_yahoo):  
    href_tags_yahoo = soup_yahoo.findAll("div",{"Pos(a) T(14px) End(0) W(36px) Ta(c) NoJs_D(n) Mt(20px)"})[t].find("a").get("href")
    site_article_yahoo.append(href_tags_yahoo)
    
    html_article_yahoo = getweb_page(site_article_yahoo[t], head)
    soup_article_yahoo = BeautifulSoup(html_article_yahoo,'html.parser')
    
    #內文
    header_article_yahoo = soup_article_yahoo.findAll("div",{"class":"caas-body"})[0].text.strip()
    site_content.append(header_article_yahoo)
    
site_content = [item.replace('\n', '').replace('\r', '')for item in site_content]
#print(site_content) #爬到的文章



for i in range(len(site_content)):
    file.write(site_content[i])
    file.write('\n')
    file.write('\n')
    file.write('\n')
    
file.close()


import jieba
import re
import collections
from collections import Counter

def get_stopwords_list():
    stopwords = [line.strip() for line in open(r'C:\Users\aa092\OneDrive\桌面\專題\stop_words.txt',encoding='UTF-8').readlines()]
    return stopwords

def seg_depart(site_content):
    # 對文檔中的每一行進行中文分詞
    sentence_depart = list(jieba.cut(str(site_content)))
    return sentence_depart

def remove_digits(input_str):
    punc = u'0123456789.'
    output_str = re.sub(r'[{}]+'.format(punc), '', input_str)
    return output_str

def move_stopwords(sentence_list, stopwords_list):
    # 去停用詞
    out_list = []
    for word in sentence_list:
        if word not in stopwords_list:
            if not remove_digits(word):
                continue
            if word != '\t':
                out_list.append(word)
    return out_list


#詞向量訓練

from gensim.models import Word2Vec
import numpy as np

# 詞向量Settings
window_size = 1
vector_size = 50
min_count = 0
workers = 2


stopwords = get_stopwords_list()


for a in range(len(site_content)):
    #將文章做jieba 刪除停止詞的處理
    sentence_depart = seg_depart(str(site_content[a]))
    sentence_depart = move_stopwords(sentence_depart, stopwords)
    #利用Counter計算詞頻
    num=Counter(sentence_depart)
    word = []  #放入詞
    frequence = [] #放入詞頻
    #過濾掉詞頻為1的詞
    for k,v in num.items():
        if v !=1:
            word.append(k)
            frequence.append(v)
            num = dict(zip(word,frequence))
    print('文章中詞頻>1的詞+次數：', num)
    print('文章中詞頻>1的詞：',word) #jieba+斷詞結果
    #詞向量訓練
    model = Word2Vec([word], size=vector_size, 
                              min_count=min_count, window=window_size, 
                              workers=workers)
    #計算平均詞向量
    for i in word:
        vec=[]
        vec.append(model[i])
        avg=np.mean(vec)
    print('文章平均詞向量',avg)
    print()
    
    




