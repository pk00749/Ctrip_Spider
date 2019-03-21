# -*- coding:utf-8 -*-
# encoding: utf-8
import unittest
import os
import urllib
import urllib2
from selenium import webdriver
from bs4 import BeautifulSoup
import xlsxwriter
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fontManager
import seaborn as sns
from pylab import mpl

curURL = 'http://hotels.ctrip.com/hotel/hangzhou17#ctm_ref=hod_hp_sb_lst'
print curURL

user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = {'User-Agent': user_agent}
request = urllib2.Request(curURL, headers=headers)
response = urllib2.urlopen(request)
soup = BeautifulSoup(response.read())

hotel_list = soup.find(id="hotel_list")
# print hotel_list.prettify
# hotel = hotel_list.find_all("li",attrs={"class":"searchresult_info_name"})
hotel = hotel_list.find_all("h2", attrs={"class": "searchresult_name"})
hotelAddress = hotel_list.find_all("p", attrs={"class": "searchresult_htladdress"})
htlPrice = hotel_list.find_all("span", attrs={"class": "J_price_lowList"})
numOfHotel = len(hotel_list.find_all("h2", attrs={"class": "searchresult_name"}))
htlValue = hotel_list.find_all("span", attrs={"class": "hotel_value"})
htlJudgement = hotel_list.find_all("span", attrs={"class": "hotel_judgement"})

p = re.compile("\d+")

workbook = xlsxwriter.Workbook('demo_1.xlsx')
worksheet = workbook.add_worksheet()

price = []
ID = []
value = []
name = []
distinct = []

for i in range(0, numOfHotel):
    worksheet.write(i+1, 0, hotel[i].span.string)
    worksheet.write(i+1, 1, hotel[i].span.next_sibling.string)
    worksheet.write(i+1, 2, hotelAddress[i].a.string)
    worksheet.write(i+1, 3, hotelAddress[i].a.previous_element.string)
    worksheet.write(i+1, 4, float(htlPrice[i].string))
    worksheet.write(i+1, 5, float(htlValue[i].string))
    worksheet.write(i+1, 6, float(p.findall(htlJudgement[i].string)[0]))

    price.append(float(htlPrice[i].string))
    ID.append(float(hotel[i].span.string))
    value.append(float(htlValue[i].string))
    name.append(hotel[i].span.next_sibling.string)
    distinct.append(hotelAddress[i].a.string)

print "done"
workbook.close()


myfont = fontManager.FontProperties(fname='C:/Windows/Fonts/msyh.ttf')
mpl.rcParams['axes.unicode_minus'] = False

df = pd.DataFrame({
    'Distinct': distinct,
    'Price': price,
    'Value': value
})


# Method 1
df2 = df.groupby('Distinct').sum()
df2.plot()
ax = df2.plot()
ax.set_xticklabels(distinct, fontproperties=myfont)
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

plt.show()





# workbook = xlsxwriter.Workbook('demo_1.xlsx')
# worksheet = workbook.add_worksheet()
#
# row_num = len(list)
# print row_num
# for i in range(1, row_num):
#     if i == 1:
#         tag_pos = 'A%s' % i
#         worksheet.write_row(tag_pos, 'test')
#     else:
#         con_pos = 'A%s' % i
#         content = list[i-1] # -1是因为被表格的表头所占
#         worksheet.write_row(con_pos, content)
# workbook.close()
