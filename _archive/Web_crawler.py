# -*- coding:utf-8 -*-

import urllib2
import re

# page = 2
# url = 'http://www.qiushibaike.com/8hr/page/' + str(page)
# url = "http://www.qiushibaike.com/8hr/page/2/?s=4877702"
# url = "http://man.cx/"
url = "http://www.qiushibaike.com/8hr/page/2/"

user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = {'User-Agent': user_agent}
try:
    request = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(request)
    content = response.read().decode('utf-8')
    # pattern = re.compile('<div.*?class="author.*?>.*?<a.*?</a>.*?<a.*?>(.*?)</a>.*?<div.*?class'+
    #                       '="content".*?title="(.*?)">(.*?)</div>(.*?)<div class="stats.*?class="number">(.*?)</i>', re.S)

    # pattern = re.compile('<p.*?style="margin-left:.*?11%;">(.*?)</p>', re.S)

    pattern = re.compile('<div.*?class="author clearfix">.*?<a href="/users/.*?title="(.*?)">(.*?)</a>', re.S)

    items = re.findall(pattern, content)
    for item in items:
    #     haveImg = re.search("img", item[3])
    #     if not haveImg:
        print item[0]
    # print "item0: "+items[0]
    # print response.read()
    # print response.read().decode('utf-8')
except urllib2.URLError, e:
    if hasattr(e, "code"):
        print e.code
    if hasattr(e, "reason"):
        print e.reason
else:
    print "OK"