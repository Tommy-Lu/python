# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 15:11:31 2018

@author: tommy
BeautifulSoup模块学习，练习。 
练习使用BeautifulSoup中基本功能，函数等。

"""

from bs4 import BeautifulSoup

html_sample = '\
<html>\
  <body>\
  <h1 id="title">Hello World</h1>\
  <a href="#" class="link">This is link1</a>\
  <a href="#link2" class="link">This is link2</a>\
  </body>\
</html>'

soup = BeautifulSoup(html_sample)  #使用beautifulsoup读入html，作为一个物件
print(type(soup))
print(soup.text)  #打印soup物件文字内容 , soup中的text能够将html中的tag标签去掉

#soup.select() # 取出特定标签元素 , 返回回传的是一个list,这里只有一个元素
header = soup.select('h1')  
print(header)    # 打印的是list
print(header[0]) #打印list中的内容
print(header[0].text)  #取出其中的内容文字部分
"""
以上3个print的输出分别为：
[<h1 id="title">Hello World</h1>]
<h1 id="title">Hello World</h1>
Hello World
"""


alink = soup.select('a')
print(alink)
for link in alink:   #这里a标签下有两个元素。
    print(link)
    print(link.text)
"""
以上输出分别为：
[<a class="link" href="#">This is link1</a>, <a class="link" href="#link2">This is link2</a>]
<a class="link" href="#">This is link1</a>
This is link1
<a class="link" href="#link2">This is link2</a>
This is link2
>>> 
"""

"""
获取含有特定CSS属性的元素
1, 使用select找出所有id为title的元素（id前面加#）
alink = soup.select('#title')
print(alink)
2, 使用select找出所有class为link的元素（class前面加.）
soup = BeautifulSoup(html_sample)
for link in soup.select('.link'):
  print(link)
"""


alink = soup.select('#title')
print(alink)
print(alink[0].text)
"""
[<h1 id="title">Hello World</h1>]
Hello World
"""


soup = BeautifulSoup(html_sample)
for link in soup.select('.link'):
  print(link)
  print(link.text)
"""
<a class="link" href="#">This is link1</a>
This is link1
<a class="link" href="#link2">This is link2</a>
This is link2
>>> 
"""

"""
获取所有a标签内的链接
使用select找出所有a tag的href链接
alink = soup.select('a')
for link in alink:
  print(link['href'])
"""
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`")
alink = soup.select('a')
for link in alink:
  print(link)
  print(link['href'])
"""
<a class="link" href="#">This is link1</a>
#
<a class="link" href="#link2">This is link2</a>
#link2
"""


