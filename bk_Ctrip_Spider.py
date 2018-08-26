# -*- coding:utf-8 -*-
# encoding: utf-8
import unittest
import os
import urllib
import urllib2
from selenium import webdriver
from bs4 import BeautifulSoup
import xlsxwriter
import xlrd
from xlutils.copy import copy
import xlwt
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fontManager
import seaborn as sns
from pylab import mpl
import MySQLdb
import sys

reload(sys)
sys.setdefaultencoding("utf-8")# 首先设置系统的默认编码为utf-8

conn = MySQLdb.connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='81302137',
    db='hotels',
    charset='utf8'
)
cur = conn.cursor()
p = re.compile("\d+")


curURL = 'http://hotels.ctrip.com/hotel/hangzhou17/p'
doc = 'G:\Program\Projects\Web crawler\demo_1.xls'


def load_url(page_url, page_number):
    url = page_url + str(page_number)
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = {'User-Agent': user_agent}
    request = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(request)
    page_soup = BeautifulSoup(response.read())
    print 'Downloading page %d, url: ' % page_number + url
    return page_soup


def spider(detail_page, result):
    page_soup = load_url(curURL, detail_page)

    hotel_list = page_soup.find(id="hotel_list")
    hotel_detail = hotel_list.find_all("div", attrs={"class": "searchresult_list"}, limit=25)
    hotels = len(hotel_detail)

    pre_workbook = xlrd.open_workbook(result)
    cur_workbook = copy(pre_workbook)
    cur_worksheet = cur_workbook.get_sheet(0)
    print hotels
    for htl in range(0, hotels):
        if hotel_detail[htl]["id"] != "hoteltuan":
            ID = float(hotel_detail[htl]['id'])
            names = hotel_detail[htl].find("h2", attrs={"class": "searchresult_name"})
            name = unicode(names.span.next_sibling.string)
            addresses = hotel_detail[htl].find("p", attrs={"class": "searchresult_htladdress"})
            address = unicode(addresses.contents[0])
            address = address[0:str(address).find(u'。')]

            price = float(hotel_detail[htl].find("span", attrs={"class": "J_price_lowList"}).string)
            value = hotel_detail[htl].find("div", attrs={"class": "searchresult_judge_box"})

            cur_worksheet.write((page-1)*25+htl, 0, ID)
            # print 'http://hotels.ctrip.com/'+hotel[0].a.get('href') #Take href
            cur_worksheet.write((page-1)*25+htl, 1, name)  # here can't save as excel if encode as utf8
            cur_worksheet.write((page-1)*25+htl, 2, address)

            if addresses.a is None:
                district = 'No District'
            else:
                district = addresses.a.string
            cur_worksheet.write((page-1)*25+htl, 3, district)

            cur_worksheet.write((page-1)*25+htl, 4, price)

            if value.span.string is None:
                tmp_values = 0
                tmp_judges = 0
            else:
                tmp_values = float(value.span.string)
                tmp_judge = value.span.next_sibling.next_sibling
                tmp_judges = float(p.findall(tmp_judge.next_sibling.next_sibling.next_sibling.string)[0])

            cur_worksheet.write((page-1)*25+htl, 5, tmp_values)
            cur_worksheet.write((page-1)*25+htl, 6, tmp_judges)

            cur.execute("insert into hotel_1 (id, name,address,price) values (%s,%s,%s,%s)", (ID, name.encode('utf8'),\
                                                                                     address.encode('utf8'), price))
    cur_workbook.save(result)


def get_amount_pages(page_soup):
    amount = page_soup.find(id="lblAmount").string
    print 'Total number of hotel: '+amount

    pages = soup.find("div", attrs={"class": "c_page_list layoutfix"}).find(rel="nofollow").string
    print 'Total number of page: '+pages
    pages = int(pages)
    return pages

if __name__ == '__main__':
    soup = load_url(curURL, 1)
    max_page = get_amount_pages(soup)

    cur.execute("drop table if exists hotel_1")
    cur.execute("create table hotel_1(id mediumint ,name varchar(50),address varchar(200),price smallint)")
    # ENGINE=MYISAM DEFAULT CHARSET=gbk")

    for page in range(1, 2):
        spider(page, doc)

    # cur.execute("create table hotel(no smallint not null auto_increment,id int,name varchar(20),\
    # address varchar(50),district varchar(50),price int,value int,judge int, update_date date)")
    # no
    # id
    # name
    # address
    # district
    # price
    # value
    # judge
    # update_date
    cur.close()
    conn.commit()
    conn.close()

print 'Done'


# workbook = xlsxwriter.Workbook('demo_1.xls')
# worksheet = workbook.add_worksheet()

# print "Data captured"
# workbook.close()
#

# myfont = fontManager.FontProperties(fname='C:/Windows/Fonts/msyh.ttf')
# mpl.rcParams['axes.unicode_minus'] = False
#
# df = pd.DataFrame({
#     'Distinct': distinct,
#     'Price': price,
#     'Value': value
# })
#
#
# # Method 1
# df2 = df.groupby('Distinct').sum()
# ax = df2.plot()
# ax.set_xticklabels(distinct, fontproperties=myfont)
# ---------------

# Method 2
# df = pd.DataFrame(price, index=distinct, columns=['Price']).groupby(distinct).sum()
# ax = df.plot()
# ax.set_xticklabels(distinct, fontproperties=myfont)
# ---------------

# Method 3
# fig = plt.figure()
# ax1 = fig.add_subplot(111)
# ax1.set_title("Hotel")
#
# ax1.plot(df['Price'], color='red')
# ax1.set_ylabel('Price', color='red')
# # ax1.set_ylim([0, 1000])
# # ax1.set_xticks(ID)
# ax1.set_xticklabels(df['Distinct'], fontproperties=myfont)
#
# ax2 = ax1.twinx()  # this is the important function
# ax2.plot(df['Value'], color='blue')
# ax2.set_ylabel('Values', color='blue')
# ax2.set_ylim([0, 5])
# ---------------
# print 'Graph created!'
# plt.show()