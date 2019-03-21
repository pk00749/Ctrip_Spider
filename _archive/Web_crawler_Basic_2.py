# -*-coding=utf-8-*-
import urllib2
import urllib
# values = {"username":"pk00749","password":"8130hupu"}
# data = urllib.urlencode(values)
# url = "http://passport.hupu.com/pc/login?project=nba&from=pc"
url = "http://www.qiushibaike.com/8hr/page/2/?s=4877702"
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = {'User-Agent': user_agent}
# request = urllib2.Request(url, data)
# request = urllib2.Request(url)
request = urllib2.Request(url, headers=headers)
try:
    response = urllib2.urlopen(request)
    # print response.read()
except urllib2.URLError, error:  # The parent of HTTPError is URLError
    if hasattr(error, "code"):
        print error.code
    if hasattr(error, "reason"):
        print error.reason
else:
    print "OK"

# print 'http header: \n', response.info()
# print 'http status:', response.getcode()
# print 'url:', response.geturl()
# http://passport.hupu.com/pc/login