#!/usr/bin/env python
# encoding: utf-8
import re
from urllib import request

# 构建基本因素：url  user-agent
url = 'http://www.jianshu.com'
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}

# 发起请求
req = request.Request(url, headers=headers)
resp = request.urlopen(req)
# print(resp.read().decode())

# 解析数据
result = re.findall(r'<a class="title" target="_blank" href=".*?">(.*?)</a>.*?<p class="abstract">(.*?)</p>', resp.read().decode(), re.S)
for title, abstract in result:
    print(title)
    print(abstract)
