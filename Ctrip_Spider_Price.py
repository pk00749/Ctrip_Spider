# -*- coding:utf-8 -*-

import MySQLdb
from Ctrip_Spider_Init import load_url
from Ctrip_Spider_Init import connect_server
from Ctrip_Spider_Init import get_amount_pages
from Ctrip_Spider_Init import base_url
from warnings import filterwarnings
filterwarnings('error', category=MySQLdb.Warning)


conn, cur = connect_server()
curURL = base_url


def create_table():
    try:
        cur.execute("drop table if exists htl_price")
        cur.execute("create table if not exists htl_price(no int unsigned not null auto_increment,id mediumint unsigned not null,\
    date timestamp,price float,primary key(no))")
        pass
    except MySQLdb.Warning, w:
        print "Warning:%s" % str(w)
    except MySQLdb.Error, e:
        print "Error %d:%s" % (e.args[0], e.args[1])


def spider_price(detail_page):
    page_soup = load_url(curURL, detail_page)

    hotel_list = page_soup.find(id="hotel_list")
    hotel_detail = hotel_list.find_all("div", attrs={"class": "searchresult_list"}, limit=25)
    hotels = len(hotel_detail)

    for htl in range(0, hotels):
        if hotel_detail[htl]["id"] != "hoteltuan":
            htlid = float(hotel_detail[htl]['id'])
            price = float(hotel_detail[htl].find("span", attrs={"class": "J_price_lowList"}).string)

            cur.execute("insert into htl_price (id,date,price) values (%s,sysdate(),%s)", (htlid, price))


if __name__ == '__main__':
    soup = load_url(curURL, 1)
    max_page = get_amount_pages(soup)
    # create_table()
    for page in range(1, max_page):
        spider_price(page)

    conn.commit()
    conn.close()

    print('Price Done')
