# -*- coding:utf-8 -*-

import MySQLdb
import sys
from Ctrip_Spider_Init import load_url
from Ctrip_Spider_Init import get_amount_pages
from Ctrip_Spider_Init import connect_server
from Ctrip_Spider_Init import base_url
from warnings import filterwarnings
filterwarnings('error', category=MySQLdb.Warning)

reload(sys)
sys.setdefaultencoding("utf-8")  # 首先设置系统的默认编码为utf-8

conn, cur = connect_server()
curURL = base_url


def spider_state_data(detail_page):
    page_soup = load_url(curURL, detail_page)
    hotel_list = page_soup.find(id="hotel_list")
    hotel_detail = hotel_list.find_all("div", attrs={"class": "searchresult_list"}, limit=25)
    hotels = len(hotel_detail)

    for htl in range(0, hotels):
        if hotel_detail[htl]["id"] != "hoteltuan":
            htlid = float(hotel_detail[htl]['id'])
            names = hotel_detail[htl].find("h2", attrs={"class": "searchresult_name"})
            name = unicode(names.span.next_sibling.string)
            addresses = hotel_detail[htl].find("p", attrs={"class": "searchresult_htladdress"})
            address = unicode(addresses.contents[0])
            address = address[0:str(address).find(u'。')]
            print type(names.span.next_sibling.string)
            print type(unicode(names.span.next_sibling.string))
            print type(name.encode('utf8'))

    print "Received"


if __name__ == '__main__':

    for page in range(1, 2):
        spider_state_data(page)

    conn.commit()
    conn.close()

    print 'State Data Done'
