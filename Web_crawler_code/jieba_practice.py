import requests
from bs4 import BeautifulSoup
import json
import jieba
from jieba import analyse


def getweb_page(url , head):
    html_page = requests.get(url ,headers=head)
    
    if html_page.status_code != 200:
        print('invalid page',html_page.status_code)
        return None
    else:
        return html_page.text
    
head = {"User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.3"}
#抓取網站    
site = "https://tw.stock.yahoo.com/tw-market"
html = getweb_page(site,head)
soup = BeautifulSoup(html,'html.parser')

header = soup.findAll("ul",{"class":"My(0) Ov(h) P(0) Wow(bw)"})[0].find("div").text
print(header)
'''
gen = jieba.cut(header)
word = ' '.join(gen)
    
print(word)

#jieba分析
result =analyse.extract_tags(word,topK=500,withWeight=True)
print(result)
'''