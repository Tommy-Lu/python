# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 14:32:40 2018

@author: tommy
#简单网络爬虫学习
爬取sina新闻
重点注意问题：
0, 爬去新浪新闻国内版块中的最新新闻下， 没一页中的新闻内容。   http://news.sina.com.cn/china/
1, 最新新闻版块的url地址，需要使用chrome的检查(inspect)工具来查找。
   新闻地址：http://news.sina.com.cn/c/gat/2018-08-29/doc-ihikcahf3559217.shtml
   版块下的页面地址：https://feed.sina.com.cn/api/roll/get?pageid=121&lid=1356&num=20&versionNumber=1.2.4&\
             page={}&encode=utf-8&callback=feedCardJsonpCallback&_=1535523489635
   所以需要将页面地址中和页相关的page={}，用{}.format来格式化，获取到不同的页面地址。
2, 评论的网页地址和新闻的网页地址不一样，也是需要通过chrome检查（inspect）工具来查找评论网页地址。
   评论的问页地址："http://comment5.news.sina.com.cn/page/info?version=1&format=json&\
channel=gn&newsid=comos-{}&group=undefined&compress=0&ie=utf-8&oe=utf-8&page=1&page_size=3"
   其中newsid=comos-{}处和新闻地址中的最后一部分的ID号匹配，以找到相应的新闻评论。所以需要将新闻地址的后部分中的ID号解析出来用与查找评论。
"""
import requests
from bs4 import BeautifulSoup
import json

"""
#newsurl = 'http://news.sina.com.cn/china/'
newsurl = 'http://news.sina.com.cn/c/2018-08-28/doc-ihikcahe7514629.shtml'
#res = requests.get(newsurl) 得到乱码，
res = requests.get(newsurl)
res.encoding = 'utf-8'   #制定编码方式为utf-8
#print(res.text)  #获取到网页资料，但是镶嵌在非结构数据中。

#print(type(res))

soup = BeautifulSoup(res.text) #将request到的网页内容装进BeautifulSoup中。
title = soup.select('.main-title')[0].text  # 通过网页工具，观察到标题处在class中：
#datesource = soup.select('.date-source')[0]                       #<h1 class="main-title">美称中国可能转变不首先使用核武器方针 中方回应</h1>
timesource = soup.select('.date-source')[0].contents[1].text  #获取到时间和出处模块
namesoure =  soup.select('.date-source')[0].contents[-2].text
article = soup.select('.article')[0].text.strip() #获取到新闻正文
#print([p.text.strip for p in soup.select('.article')[0]])
#print(title)
#print(timesource +'\t\t'+ namesoure)
#print(article)
author = soup.select('.show_author')[0].text.lstrip('责任编辑：')  #获取编辑作者

#comment = soup.select('.hd clearfix')
#comment_url = "http://comment5.news.sina.com.cn/page/info?version=1&format=json&\
#channel=gn&newsid=comos-{}&group=undefined&compress=0&ie=utf-8&oe=utf-8&page=1&page_size=3"
#news_url = 'http://news.sina.com.cn/c/2018-08-28/doc-ihikcahe7514629.shtml'
#news_id = news_url.split('/')[-1].rstrip('.shtml').lstrip('doc-i')



#comment_res = requests.get(comment_url.format(news_id)).text
#print(comment_res)


#jd = json.loads(comment_res)
#total_comment = jd['result']['count']['total']

#print(total_comment)
comment_url = "http://comment5.news.sina.com.cn/page/info?version=1&format=json&\
channel=gn&newsid=comos-{}&group=undefined&compress=0&ie=utf-8&oe=utf-8&page=1&page_size=3"
news_url = 'http://news.sina.com.cn/c/2018-08-28/doc-ihikcahe7514629.shtml'
#news_id = news_url.split('/')[-1].rstrip('.shtml').lstrip('doc-i')
"""


"""
函数名： getCommentCounts()
功能说明：从一个新闻newsurl中，获取该新闻的评论数。 注意，评论的评论的地址和新闻地址不一样。newsurl只用来获取新闻的ID号，用来在评论页面获取相应的评论。
输入： 一个新闻的newsurl
输出： 包含该新闻作者，标题，时间，内容，评论数的字典。

"""
def getCommentCounts(newsurl):
    import re
    #import json
    news_id =  re.search('doc-i(.+).shtml',news_url).group(1)
    comments = requests.get(comment_url.format(news_id))
    jd = json.loads(comments.text)
    
    return jd['result']['count']['total']

   

"""
函数名： getNewsDetail()
功能说明：从给到的新闻newsurl中，将该新闻的作者，标题，时间，内容，评论数获取，并存储为字典型， 并返回该字典
输入： 一个新闻的newsurl
输出： 包含该新闻作者，标题，时间，内容，评论数的字典。

"""
def getNewsDetail(newsurl):
    result = {}
    res =  requests.get(newsurl)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text)
    result['title'] = soup.select('.main-title')[0].text 
    result['newssource'] = soup.select('.date-source')[0].contents[-2].text
    result['dt'] = soup.select('.date-source')[0].contents[1].text 
    result['article'] = soup.select('.article')[0].text.strip() 
    result['editor'] = soup.select('.show_author')[0].text.lstrip('责任编辑：') 
    result['comments'] = getCommentCounts(newsurl)

    return result

"""
#print(getNewsDetail(news_url))

#import re
#m = re.search('doc-i(.+).shtml',news_url) #正则匹配，查找目标news_url， 匹配规则： 查找doc-i(.+).shtml'， 括号部分表示:.出现的所有文字， +出现的次数一次以上。
#print(m.group(1))  # group(0) 表示整个匹配的整体，包含doc-i和.shtml, group(1) 表示之包含匹配到的部分（括号中部分）



#china_url = "https://feed.sina.com.cn/api/roll/get?pageid=121&lid=1356&num=20&versionNumber=1.2.4&\
#             page=1&encode=utf-8&callback=feedCardJsonpCallback&_=1535523489635"
#china_url = "https://feed.sina.com.cn/api/roll/get?pageid=121&lid=1356&num=20&versionNumber=1.2.4&\
#             page=2&encode=utf-8&callback=feedCardJsonpCallback&_=1535523489635"

#res = requests.get(china_url)
#res.encoding = 'utf-8'
#print(res.text)
#进行strip是去掉javascript包裹的头尾，  但是在去掉头尾的时候，这里多去了}}和{, 所以将用链接符把她链接回去。
#s = res.text.lstrip('try{feedCardJsonpCallback(').rstrip(');}catch(e){};')
#ss = '{'+s+'}}'
#jd = json.loads(ss)
#print(jd)
#print(len(jd['result']['data']))
#for i in range(20):
#    print(jd['result']['data'][i]['url'])
#for context in jd['result']['data']:
#    print(context['url'])
#print(res.text)
#jd = json.loads(res.text.lstrip("try{feedCardJsonpCallback("))
#print(res.text)
#soup = BeautifulSoup(res.text)
#print(soup.select('.feed-card-content'))
"""

"""
函数名： getListLinks()
功能说明：将一个page url下的所有新闻的url解析出来，并调用getNewsDetail函数，获取该新闻的作者，标题，时间，内容，评论数(存储为字典型)， 将每个新闻的
         内容添加到列表中，并输出列表。
输入： 一个页面的url
输出： 该url下的所有新闻内容的列表。

"""
def getListLinks(url):
    newsDetails = []  #用于存放获取到的新闻内容   
    
    res = requests.get(url)
    
    #进行strip是去掉javascript包裹的头尾，  但是在去掉头尾的时候，这里多去了}}和{, 所以将用链接符把她链接回去。
    s = res.text.lstrip('try{feedCardJsonpCallback(').rstrip(');}catch(e){};')
    s = '{'+s+'}}'
    
    jd = json.loads(s) #调用json函数加载request get到的内容，解析为json格式。
    #print(jd)

    for content in jd['result']['data']:
        newsURL = content['url'] #这里就是解析得到的网页地址。
        #print(newsURL)
        newsDetails.append(getNewsDetail(newsURL))  #getNewsDetail(newsURL)将会返回获取到的新闻的一个字典。
    return newsDetails 

pageURL = "https://feed.sina.com.cn/api/roll/get?pageid=121&lid=1356&num=20&versionNumber=1.2.4&\
             page={}&encode=utf-8&callback=feedCardJsonpCallback&_=1535523489635"
comment_url = "http://comment5.news.sina.com.cn/page/info?version=1&format=json&\
channel=gn&newsid=comos-{}&group=undefined&compress=0&ie=utf-8&oe=utf-8&page=1&page_size=3"
         
news_total = []
for i in range(1, 3):
    pageURL = pageURL.format(i)
    #print(pageURL)
    news_total.extend(getListLinks(pageURL))

for content in news_total:
    print(content)

    










