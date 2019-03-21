# -*- coding:utf-8 -*-

import MySQLdb
from Ctrip_Spider_Init import load_url
from Ctrip_Spider_Init import get_amount_pages
from Ctrip_Spider_Init import connect_server
from Ctrip_Spider_Init import base_url
from warnings import filterwarnings
filterwarnings('error', category=MySQLdb.Warning)

conn, cur = connect_server()
curURL = base_url


def create_table():
    try:
        cur.execute("drop table if exists htl_rating")
        cur.execute("create table htl_rating(no int unsigned not null auto_increment,id mediumint unsigned not null,\
    date timestamp,rating float,primary key(no))")
        pass
    except MySQLdb.Warning:
        print("Warning:%s" % str(w))
    except MySQLdb.Error:
        print("Error %d:%s" % (e.args[0], e.args[1]))


def spider_rating(detail_page):
    page_soup = load_url(curURL, detail_page)

    hotel_list = page_soup.find(id="hotel_list")
    hotel_detail = hotel_list.find_all("div", attrs={"class": "searchresult_list"}, limit=25)
    hotels = len(hotel_detail)

    for htl in range(0, hotels):
        if hotel_detail[htl]["id"] != "hoteltuan":
            htlid = float(hotel_detail[htl]['id'])

            tmp_value = hotel_detail[htl].find("div", attrs={"class": "searchresult_judge_box"})

            if tmp_value.span.string is None:
                value = 0
            else:
                value = float(tmp_value.span.string)

            cur.execute("insert into htl_rating (id,date,rating) values (%s,sysdate(),%s)", (htlid, value))


if __name__ == '__main__':
    soup = load_url(curURL, 1)
    max_page = get_amount_pages(soup)
    # create_table()
    for page in range(1, max_page):
        spider_rating(page)

    conn.commit()
    conn.close()

    print('Value Done')
