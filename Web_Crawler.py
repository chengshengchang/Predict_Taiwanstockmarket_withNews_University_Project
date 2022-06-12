import requests
from bs4 import BeautifulSoup
import pymysql
import MySQLdb
import re
import datetime
import time
import sys


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


#範圍時間
#開盤時間ㄋ
d_time = datetime.datetime.strptime(str(datetime.datetime.now().date())+'9:30:00', '%Y-%m-%d%H:%M:%S')  



#收盤時間
d_time1 =  datetime.datetime.strptime(str(datetime.datetime.now().date())+'13:30:00', '%Y-%m-%d%H:%M:%S')
    




#會影響今日股價文章(udn)
site_content_udn_today=[]

#會影響到明日股價文章(udn)
site_content_udn_tomorrow = []

#今日日期(爬取時間閜五5點)
today_time =  str(datetime.date.today())
string_today = str(today_time+'影響今日股價文本.txt')


#今日日期(爬取時間閜五5點)
string_tomorrow = str(today_time+'影響明日股價文本.txt')






#開啟紀錄文本檔案
file_today = open('文本紀錄/'+string_today,"w",encoding="utf-8")
file_tomorrow = open('文本紀錄/'+string_tomorrow,"w",encoding="utf-8")


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
        
        all_href_tags =udn+href_tags_udn
        site_article_udn.append(all_href_tags)
          
     
        html_article_udn = getweb_page(site_article_udn[t], head)
        soup_article_udn = BeautifulSoup(html_article_udn,'html.parser')
    
    
        try:
        #內文
            header_article_udn = soup_article_udn.findAll("div",{"class":"article-content__paragraph"})[0].text.strip()
            site_content_udn_today.append(header_article_udn)
        
    
        except:
            continue
        
        #影響今日的文本
        
       
        for i in range(len(site_content_udn_today)):
            file_today.write(site_content_udn_today[i])
            
        
        
        
        
        
    else:
         
                             
    
        all_href_tags =udn+href_tags_udn
        site_article_udn.append(all_href_tags)
          
     
        html_article_udn = getweb_page(site_article_udn[t], head)
        soup_article_udn = BeautifulSoup(html_article_udn,'html.parser')
    
    
        try:
            #內文
            header_article_udn = soup_article_udn.findAll("div",{"class":"article-content__paragraph"})[0].text.strip()
            site_content_udn_tomorrow.append(header_article_udn)
        
    
        except:
            continue
        #影響明日的文本
        
        
        for i in range(len(site_content_udn_tomorrow)):
            file_tomorrow.write(site_content_udn_tomorrow[i])
        
        







#ettoday


#會影響今日股價文章(ettoday)
site_content_ettoday_today= []

#會影響到明日股價文章(ettoday)
site_content_ettoday_tomorrow = []





#ettoday


#抓取網址 [[ettoday]]

site_ettoday ='https://finance.ettoday.net/focus/175'
html_ettoday = getweb_page(site_ettoday,head)

#soup套件處理html資料

soup_ettoday =BeautifulSoup(html_ettoday,'html.parser')

#裝article的網址
site_article_ettoday = []


#爬取href tag 數
time_ettoday = 20







for t in range(time_ettoday):
    href_tags_ettoday = soup_ettoday.findAll("div",{"class":"part_pictxt_3"})[0].findAll("a")[t].get('href')
    site_article_ettoday.append(href_tags_ettoday)
    
    
    html_article_ettoday = getweb_page(site_article_ettoday[t], head)
    soup_article_ettoday = BeautifulSoup(html_article_ettoday,'html.parser')
    
    #抓內文
    header_article_ettoday = soup_article_ettoday.findAll("div",{"class":"story"})[0].text.strip()
    
    try:
        search_time_ettoday = soup_article_ettoday.findAll("div",{"class":"breadcrumb_box clearfix"})[0].findAll("time")[0].text.strip()
        str_search_time_ettoday = str(search_time_ettoday+":00")
        datetime_ettoday = datetime.datetime.strptime(search_time_ettoday ,'%Y-%m-%d %H:%M')
        
        if datetime_ettoday > d_time and datetime_ettoday < d_time1:
            site_content_ettoday_today.append(header_article_ettoday)
            
        else:
                site_content_ettoday_tomorrow.append(header_article_ettoday)
    
        
        
        
   
        
        
        
    except:
        search_time_ettoday = soup_article_ettoday.findAll("div",{"class":"part_breadcrumb_1 clearfix"})[0].findAll("time")[0].text.strip()
        
        str_search_time_ettoday = str(search_time_ettoday+":00")
        datetime_ettoday = datetime.datetime.strptime(str_search_time_ettoday , '%Y年%m月%d日 %H:%M:%S')
        
        
        array = time.strptime(str_search_time_ettoday, u"%Y年%m月%d日 %H:%M:%S")
        try:
            search_time_ettoday = time.strftime("%Y-%m-%d %H:%M:%S", array)
        except Exception as e:  
            print(e)
        if datetime_ettoday > d_time and datetime_ettoday < d_time1:
            site_content_ettoday_today.append(header_article_ettoday)
            
        else:
            site_content_ettoday_tomorrow.append(header_article_ettoday)
            
       
         
    #影響今日的文本





for i in range(len(site_content_ettoday_today)):
    file_today.write(site_content_ettoday_today[i])
      

for i in range(len(site_content_ettoday_tomorrow)):
    file_tomorrow.write(site_content_ettoday_tomorrow[i])
'''
#關閉檔案    
file_today.close()
file_tomorrow.close()    
'''
   
    

#yahoo

#會影響今日股價文章(ettoday)
site_content_yahoo_today= []

#會影響到明日股價文章(ettoday)
site_content_yahoo_tomorrow = []


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
    
    
    old2_search_time_yahoo = soup_article_yahoo.findAll("div",{"class":"caas-attr-time-style"})[0].find("time").get('datetime')
    '''
    str_search_time_ettoday = str(search_time_ettoday+":00")
    datetime_ettoday = datetime.datetime.strptime(search_time_ettoday ,'%Y-%m-%d %H:%M')
    site_content.append(header_article_yahoo)
    '''
    nonsence = old2_search_time_yahoo[-8:]
    old_search_time_yahoo = old2_search_time_yahoo.replace(nonsence,'').replace('T0',' 8')
       
    ymd = old_search_time_yahoo[:10]
    ms = old_search_time_yahoo[-3:]    
    a = str(int(old_search_time_yahoo[-5])+int(old_search_time_yahoo[-4]))   
    search_time_yahoo = ymd+' '+a+ms
    
    str_search_time_yahoo = str(search_time_yahoo+":00")
    datetime_yahoo = datetime.datetime.strptime(search_time_yahoo ,'%Y-%m-%d %H:%M')
    
    
    
        
    if datetime_yahoo > d_time and datetime_yahoo < d_time1:
        site_content_yahoo_today.append(header_article_yahoo)
            
    else:
        site_content_yahoo_tomorrow.append(header_article_yahoo)





for i in range(len(site_content_yahoo_today)):
    file_today.write(site_content_yahoo_today[i])
       

for i in range(len(site_content_yahoo_tomorrow)):
    file_tomorrow.write(site_content_yahoo_tomorrow[i])
   
    
file_today.close()
file_tomorrow.close()     
   


#爬取所有文章的次數 之後雙重迴圈用
all_the_time = time_ettoday + time_udn + time_yahoo



    
    
    
#所有文本(今日)
all_site_content_today = site_content_ettoday_today + site_content_udn_today + site_content_yahoo_today

#所以文本(明日)
all_site_content_tomorrow = site_content_ettoday_tomorrow + site_content_udn_tomorrow + site_content_yahoo_tomorrow
    


#-------------------------------------------------------------
#以下為關鍵字挑選文本

#台積電

#今日日期(爬取時間閜五5點)
string_tsmc_today = str(today_time+'影響台積電今日股價文本.txt')


#今日日期(爬取時間閜五5點)
string_tsmc_tomorrow = str(today_time+'影響台積電明日股價文本.txt')




#開啟紀錄文本檔案
file_tsmc_today = open('關鍵字文本/'+string_tsmc_today,"w",encoding="utf-8")
file_tsmc_tomorrow = open('關鍵字文本/'+string_tsmc_tomorrow,"w",encoding="utf-8")


#篩選過的文章儲存於這(但可能有重複的文章) tsmc (今日)
selected_content_redundancy_tsmc_today = []
#篩選過的文章儲存於這(但可能有重複的文章) tsmc (明日)
selected_content_redundancy_tsmc_tomorrow = []
#凱起關鍵字檔案 以台積電為例
f1_tsmc = open("個股關鍵字/tsmc.txt","r",encoding="utf-8")
#讀黨的一些步驟
txt1_tsmc = f1_tsmc.read()
f1_tsmc.close()

#關鍵字 把自分開
line1_tsmc = txt1_tsmc.split()

#有幾個分開的字
length_tsmc = len(line1_tsmc)

#看有幾關鍵字當它的長度，與另外一個site_content(文章內容)比較
#(today)
for i in range(length_tsmc):
    #time_udn是我爬取udn文章的數目
    for j in range(len(all_site_content_today)):
        try:
            if line1_tsmc[i] in all_site_content_today[j]:
               selected_content_redundancy_tsmc_today.append(all_site_content_today[j])  
        except:
            continue
#(tomorrow)
for i in range(length_tsmc):
    #time_udn是我爬取udn文章的數目
    for j in range(len(all_site_content_tomorrow)):
        try:
            if line1_tsmc[i] in all_site_content_tomorrow[j]:
               selected_content_redundancy_tsmc_tomorrow.append(all_site_content_tomorrow[j])  
        except:
            continue

#處理重複資料  對列表重複資料進行刪除(今日)
unique_set_tsmc_today=set(selected_content_redundancy_tsmc_today)

#得到新的文本無重複資料(今日)
selected_content_tsmc_today = list(unique_set_tsmc_today)


#處理重複資料  對列表重複資料進行刪除 (明日)
unique_set_tsmc_tomorrow=set(selected_content_redundancy_tsmc_tomorrow)

#得到新的文本無重複資料 (明日)
selected_content_tsmc_tomorrow = list(unique_set_tsmc_tomorrow)


for i in range(len(selected_content_tsmc_today)):
    file_tsmc_today.write(selected_content_tsmc_today[i])
    
for i in range(len(selected_content_tsmc_tomorrow)):
    file_tsmc_tomorrow.write(selected_content_tsmc_tomorrow[i])
       

file_tsmc_today.close()
file_tsmc_tomorrow.close()



#---------------------------------------------------------

#台泥

#今日日期(爬取時間閜五5點)
string_tinei_today = str(today_time+'影響台泥今日股價文本.txt')


#今日日期(爬取時間閜五5點)
string_tinei_tomorrow = str(today_time+'影響台泥明日股價文本.txt')




#開啟紀錄文本檔案
file_tinei_today = open('關鍵字文本/'+string_tinei_today,"w",encoding="utf-8")
file_tinei_tomorrow = open('關鍵字文本/'+string_tinei_tomorrow,"w",encoding="utf-8")


#篩選過的文章儲存於這(但可能有重複的文章) tsmc (今日)
selected_content_redundancy_tinei_today = []
#篩選過的文章儲存於這(但可能有重複的文章) tsmc (明日)
selected_content_redundancy_tinei_tomorrow = []
#凱起關鍵字檔案 以台積電為例
f1_tinei = open("個股關鍵字/tinei.txt","r",encoding="utf-8")
#讀黨的一些步驟
txt1_tinei = f1_tinei.read()
f1_tinei.close()

#關鍵字 把自分開
line1_tinei = txt1_tinei.split()

#有幾個分開的字
length_tinei = len(line1_tinei)

#看有幾關鍵字當它的長度，與另外一個site_content(文章內容)比較
#(today)
for i in range(length_tinei):
    #time_udn是我爬取udn文章的數目
    for j in range(len(all_site_content_today)):
        try:
            if line1_tinei[i] in all_site_content_today[j]:
               selected_content_redundancy_tinei_today.append(all_site_content_today[j])  
        except:
            continue
#(tomorrow)
for i in range(length_tinei):
    #time_udn是我爬取udn文章的數目
    for j in range(len(all_site_content_tomorrow)):
        try:
            if line1_tsmc[i] in all_site_content_tomorrow[j]:
               selected_content_redundancy_tinei_tomorrow.append(all_site_content_tomorrow[j])  
        except:
            continue

#處理重複資料  對列表重複資料進行刪除(今日)
unique_set_tinei_today=set(selected_content_redundancy_tinei_today)

#得到新的文本無重複資料(今日)
selected_content_tinei_today = list(unique_set_tinei_today)


#處理重複資料  對列表重複資料進行刪除 (明日)
unique_set_tinei_tomorrow=set(selected_content_redundancy_tinei_tomorrow)

#得到新的文本無重複資料 (明日)
selected_content_tinei_tomorrow = list(unique_set_tinei_tomorrow)


for i in range(len(selected_content_tinei_today)):
    file_tinei_today.write(selected_content_tinei_today[i])
    
for i in range(len(selected_content_tinei_tomorrow)):
    file_tinei_tomorrow.write(selected_content_tinei_tomorrow[i])
       

file_tinei_today.close()
file_tinei_tomorrow.close()



#--------------------------------------------------------- 
    


#鴻海

#今日日期(爬取時間閜五5點)
string_redsea_today = str(today_time+'影響鴻海今日股價文本.txt')


#今日日期(爬取時間閜五5點)
string_redsea_tomorrow = str(today_time+'影響鴻海明日股價文本.txt')





#開啟紀錄文本檔案
file_redsea_today = open('關鍵字文本/'+string_redsea_today,"w",encoding="utf-8")
file_redsea_tomorrow = open('關鍵字文本/'+string_redsea_tomorrow,"w",encoding="utf-8")


#篩選過的文章儲存於這(但可能有重複的文章) tsmc (今日)
selected_content_redundancy_redsea_today = []
#篩選過的文章儲存於這(但可能有重複的文章) tsmc (明日)
selected_content_redundancy_redsea_tomorrow = []
#凱起關鍵字檔案 以台積電為例
f1_redsea = open("個股關鍵字/redsea.txt","r",encoding="utf-8")
#讀黨的一些步驟
txt1_redsea = f1_redsea.read()
f1_redsea.close()

#關鍵字 把自分開
line1_redsea = txt1_redsea.split()

#有幾個分開的字
length_redsea = len(line1_redsea)

#看有幾關鍵字當它的長度，與另外一個site_content(文章內容)比較
#(today)
for i in range(length_redsea):
    #time_udn是我爬取udn文章的數目
    for j in range(len(all_site_content_today)):
        try:
            if line1_redsea[i] in all_site_content_today[j]:
               selected_content_redundancy_redsea_today.append(all_site_content_today[j])  
        except:
            continue
#(tomorrow)
for i in range(length_redsea):
    #time_udn是我爬取udn文章的數目
    for j in range(len(all_site_content_tomorrow)):
        try:
            if line1_redsea[i] in all_site_content_tomorrow[j]:
               selected_content_redundancy_redsea_tomorrow.append(all_site_content_tomorrow[j])  
        except:
            continue

#處理重複資料  對列表重複資料進行刪除(今日)
unique_set_redsea_today=set(selected_content_redundancy_redsea_today)

#得到新的文本無重複資料(今日)
selected_content_redsea_today = list(unique_set_redsea_today)


#處理重複資料  對列表重複資料進行刪除 (明日)
unique_set_redsea_tomorrow=set(selected_content_redundancy_redsea_tomorrow)

#得到新的文本無重複資料 (明日)
selected_content_redsea_tomorrow = list(unique_set_redsea_tomorrow)


for i in range(len(selected_content_redsea_today)):
    file_redsea_today.write(selected_content_redsea_today[i])
    
for i in range(len(selected_content_redsea_tomorrow)):
    file_redsea_tomorrow.write(selected_content_redsea_tomorrow[i])
       

file_redsea_today.close()
file_redsea_tomorrow.close()



#--------------------------------------------------------- 
    
    
    
    
    
    
    
    
    
