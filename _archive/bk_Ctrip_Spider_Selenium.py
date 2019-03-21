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


#useful
chromedriver = "C:\Program Files\Google\Chrome\Application\chromedriver.exe"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)

driver.get("http://hotels.ctrip.com/hotel/848702.html#ctm_ref=hod_sr_lst_dl_n_2_1")

# setDatElement = driver.find_element_by_xpath("//*[@id='txtCity']")
# setDatElement.clear()
# setDatElement.send_keys("乌鲁木齐")

setDatElement = driver.find_element_by_xpath("//input[@id='txtCheckIn']")
setDatElement.clear()
setDatElement.send_keys("2016-12-10")

setDatElement = driver.find_element_by_xpath("//input[@id='txtCheckOut']")
setDatElement.clear()
setDatElement.send_keys("2016-12-11")

setDatElement = driver.find_element_by_xpath(("//*[@id='btnSearch']"))
setDatElement.click()

# setDatElement = driver.find_element_by_xpath(("//*[@id='downHerf']"))
# setDatElement.click()

curURL = driver.current_url
print curURL


#base_wrap3->base_main3->hotel_list
#span.parent -> a
#print soup.a['title']

#print soup.contents


#htl_name_grade = driver.find_elements_by_xpath('//*[@id="hotel_list"]/*/ul/li/div/a')
# for detail in htl_name_grade:
#     print detail.get_attribute('title')
#     list.extend(detail.get_attribute('title'))
#


# assert "Python" in driver.title
# elem = driver.find_element_by_name("q")
# elem.send_keys("selenium")
# elem.send_keys(Keys.RETURN)
# assert "Google" in driver.title

#useful
# driver.close()
# driver.quit()

