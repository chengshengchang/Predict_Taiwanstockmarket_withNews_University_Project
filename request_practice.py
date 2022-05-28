import requests
from bs4 import BeautifulSoup
import pymysql
import MySQLdb
import re
import datetime
#資料庫
'''
conn = MySQLdb.connect(host='127.0.0.1',port=3306,user='root',passwd='',db='student_project',charset='utf8')
cur= conn.cursor()
'''

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




#所有文章內文
site_content=[]

#範圍時間
#開盤時間ㄋ
d_time = datetime.datetime.strptime(str(datetime.datetime.now().date())+'9:30:00', '%Y-%m-%d%H:%M:%S')  


#收盤時間
d_time1 =  datetime.datetime.strptime(str(datetime.datetime.now().date())+'13:30:00', '%Y-%m-%d%H:%M:%S')
    


#會影響今日股價文章
site_content_today=[]

#會影響到明日股價文章
site_content_tomorrow = []

#今日日期(爬取時間閜五5點)
today_time =  str(datetime.date.today())
string_today = str(today_time+'影響今日股價文本.txt')


#今日日期(爬取時間閜五5點)
string_tomorrow = str(today_time+'影響明日股價文本.txt')


#udn


#抓取網址 [[[udn]]]

site_udn = "https://udn.com/news/cate/2/6645"
html_udn = getweb_page(site_udn,head)

#soup套件處理html資料

soup_udn = BeautifulSoup(html_udn,'html.parser')

#udn標題網站網址
site_article_udn= []
udn = 'http://udn.com'
# udn request
time_udn = 4
for t in range(time_udn):
    href_tags_udn = soup_udn.findAll("section",{"class":"thumb-news more-news thumb-news--big context-box"})[1].findAll("div",{"class":"story-list__news"})[t].findAll("h2")[0].find(["p","a"]).get('href')
    
    search_time_udn = soup_udn.findAll("section",{"class":"thumb-news more-news thumb-news--big context-box"})[1].findAll("div",{"class":"story-list__news"})[t].findAll("time")[0].text
    str_search_time_udn = str(search_time_udn+":00")
    datetime_udn= datetime.datetime.strptime(str_search_time_udn , '%Y-%m-%d %H:%M:%S')
    
    
    
    
    if datetime_udn > d_time and datetime_udn < d_time1:
        print("會影響到今日股價")
        all_href_tags =udn+href_tags_udn
        site_article_udn.append(all_href_tags)
          
     
        html_article_udn = getweb_page(site_article_udn[t], head)
        soup_article_udn = BeautifulSoup(html_article_udn,'html.parser')
    
    
        try:
        #內文
            header_article_udn = soup_article_udn.findAll("div",{"class":"article-content__paragraph"})[0].text.strip()
            site_content_today.append(header_article_udn)
        
    
        except:
            continue
        
        #影響今日的文本
        file_today = open(string_today,"w")
        for i in range(len(site_content_today)):
            file_today.write(site_content_today[i])
            
        file_today.close()
        
        
        
        
    else:
        print("會影響到明日股價")  
                             
    
        all_href_tags =udn+href_tags_udn
        site_article_udn.append(all_href_tags)
          
     
        html_article_udn = getweb_page(site_article_udn[t], head)
        soup_article_udn = BeautifulSoup(html_article_udn,'html.parser')
    
    
        try:
            #內文
            header_article_udn = soup_article_udn.findAll("div",{"class":"article-content__paragraph"})[0].text.strip()
            site_content_tomorrow.append(header_article_udn)
        
    
        except:
            continue
        #影響明日的文本
        file_tomorrow =open('文本紀錄/'+string_tomorrow,"w")
        for i in range(len(site_content_tomorrow)):
            file_tomorrow.write(site_content_tomorrow[i])
        
        file_tomorrow.close()
    
    
    

#ettoday


#抓取網址 [[ettoday]]

site_ettoday ='https://finance.ettoday.net/focus/175'
html_ettoday = getweb_page(site_ettoday,head)

#soup套件處理html資料

soup_ettoday =BeautifulSoup(html_ettoday,'html.parser')

#裝article的網址
site_article_ettoday = []

#爬取href tag 數
time_ettoday = 10
for t in range(time_ettoday):
    href_tags_ettoday = soup_ettoday.findAll("div",{"class":"part_pictxt_3"})[0].findAll("a")[t].get('href')
    site_article_ettoday.append(href_tags_ettoday)
    
    
    html_article_ettoday = getweb_page(site_article_ettoday[t], head)
    soup_article_ettoday = BeautifulSoup(html_article_ettoday,'html.parser')
    
    #抓內文
    header_article_ettoday = soup_article_ettoday.findAll("div",{"class":"story"})[0].text.strip()
    site_content.append(header_article_ettoday)
    
    


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
    




#爬取所有文章的次數 之後雙重迴圈用
all_the_time = time_ettoday + time_udn + time_yahoo


#-------------------------------------------------------------
#以下為關鍵字挑選文本


#台積電
#篩選過的文章儲存於這(但可能有重複的文章) tsmc
selected_content_redundancy_tsmc = []

#凱起關鍵字檔案 以台積電為例
f1_tsmc = open("tsmc.txt","r",encoding="utf-8")
#讀黨的一些步驟
txt1_tsmc = f1_tsmc.read()
f1_tsmc.close()

#關鍵字 把自分開
line1_tsmc = txt1_tsmc.split()

#有幾個分開的字
length_tsmc = len(line1_tsmc)

#看有幾關鍵字當它的長度，與另外一個site_content(文章內容)比較
for i in range(length_tsmc):
    #time_udn是我爬取udn文章的數目
    for j in range(all_the_time):
        try:
            if line1_tsmc[i] in site_content[j]:
               selected_content_redundancy_tsmc.append(site_content[j])  
        except:
            continue

#處理重複資料  對列表重複資料進行刪除
unique_set_tsmc=set(selected_content_redundancy_tsmc)

#得到新的文本無重複資料
selected_content_tsmc = list(unique_set_tsmc)







#---------------------------------------------------------



#台泥
#篩選過的文章儲存於這(但可能有重複的文章) tinei
selected_content_redundancy_tinei = []


#開起關鍵字檔案 以台尼為例
f2_tinei = open("tinei.txt","r",encoding="utf-8")
#讀黨的一些步驟
txt2_tinei = f2_tinei.read()
f2_tinei.close()

#關鍵字 把自分開
line2_tinei = txt2_tinei.split()

#有幾個分開的字
length_tinei = len(line2_tinei)

#看有幾關鍵字當它的長度，與另外一個site_content(文章內容)比較
for i in range(length_tinei):
    #time_udn是我爬取udn文章的數目
    for j in range(all_the_time):
        try:
            if line2_tinei[i] in site_content[j]:
               selected_content_redundancy_tinei.append(site_content[j])  
        except:
            continue

#處理重複資料  對列表重複資料進行刪除
unique_set_tinei=set(selected_content_redundancy_tinei)

#得到新的文本無重複資料
selected_content_tinei = list(unique_set_tinei)
    
    




#--------------------------------------------------------


#鴻海
#篩選過的文章儲存於這(但可能有重複的文章) redsea
selected_content_redundancy_redsea = []


#開起關鍵字檔案 以台尼為例
f3_redsea = open("redsea.txt","r",encoding="utf-8")
#讀黨的一些步驟
txt3_redsea = f3_redsea.read()
f3_redsea.close()

#關鍵字 把自分開
line3_redsea = txt3_redsea.split()

#有幾個分開的字
length_redsea = len(line3_redsea)

#看有幾關鍵字當它的長度，與另外一個site_content(文章內容)比較
for i in range(length_redsea):
    #time_udn是我爬取udn文章的數目
    for j in range(all_the_time):
        try:
            if line3_redsea[i] in site_content[j]:
               selected_content_redundancy_redsea.append(site_content[j])  
        except:
            continue

#處理重複資料  對列表重複資料進行刪除
unique_set_redsea=set(selected_content_redundancy_redsea)

#得到新的文本無重複資料
selected_content_redsea = list(unique_set_redsea)

for i in range(len(selected_content_redsea)):
    print(selected_content_redsea[i])
        
        
        


    
        
        
        
    
   



