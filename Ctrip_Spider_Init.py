# -*- coding:utf-8 -*-

import urllib2
from bs4 import BeautifulSoup
import MySQLdb

base_url = 'http://hotels.ctrip.com/hotel/hangzhou17/p'


def connect_server():
    conn = MySQLdb.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='81302137',
        db='hotels',
        charset='utf8'
    )
    cur = conn.cursor()
    return conn, cur


def load_url(page_url, page_number):
    url = page_url + str(page_number)
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = {'User-Agent': user_agent}
    request = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(request)
    page_soup = BeautifulSoup(response.read())
    print 'Downloading page %d, url: ' % page_number + url
    return page_soup


def get_amount_pages(page_soup):
    amount = page_soup.find(id="lblAmount").string
    print 'Total number of hotel: '+amount

    pages = page_soup.find("div", attrs={"class": "c_page_list layoutfix"}).find(rel="nofollow").string
    print 'Total number of page: '+pages
    pages = int(pages)
    return pages
