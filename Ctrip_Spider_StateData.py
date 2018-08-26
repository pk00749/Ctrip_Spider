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


def create_table():
    try:
        cur.execute("drop table if exists htl_state_data")
        cur.execute("create table if not exists htl_state_data (no int unsigned not null auto_increment,city varchar(50),\
        id mediumint unsigned not null,date timestamp,name varchar(50),address varchar(200),district varchar(50),\
        primary key(no,id))engine=InnoDB default charset='utf8'")
    except MySQLdb.Warning, w:
        print "Warning: %s" % str(w)
    except MySQLdb.Error, e:
        print "Error %d:%s" % (e.args[0], e.args[1])
    except MySQLdb.IntegrityError, interror:
        print "Integrity Error %d:%s" % (interror.args[0], interror.args[1])


def spider_state_data(detail_page):
    page_soup = load_url(curURL, detail_page)
    hotel_list = page_soup.find(id="hotel_list")
    hotel_detail = hotel_list.find_all("div", attrs={"class": "searchresult_list"}, limit=25)
    hotels = len(hotel_detail)

    for htl in range(0, hotels):
        if hotel_detail[htl]["id"] != "hoteltuan":
            htlid = float(hotel_detail[htl]['id'])
            names = hotel_detail[htl].find("h2", attrs={"class": "searchresult_name"})
            name = unicode(names.span.next_sibling.string) # Convert NavigableString to unicode
            addresses = hotel_detail[htl].find("p", attrs={"class": "searchresult_htladdress"})
            address = unicode(addresses.contents[0])
            address = address[0:str(address).find(u'。')]

            if addresses.a is None:
                district = 'No District'
            else:
                district = unicode(addresses.a.string)

            cur.execute("insert into htl_state_data (city,id,date,name,address,district) values\
             (%s,%s,sysdate(),%s,%s,%s)", ('hangzhou', htlid, name.encode('utf8'),\
                                           address.encode('utf8'), district.encode('utf8')))
            # Convert unicode to String by encode function

    conn.commit()

    print "Received"


def city_list(city, province):
    cur.execute("drop table if exists htl_city")
    cur.execute("create table htl_city(no int unsigned not null auto_increment,city varchar(50),\
                province varchar(50),district varchar(50), district_id smallint unsigned not null,primary key(no))")

    cur.execute("select distinct htl_state_data.district from htl_state_data")
    district = cur.fetchall()
    n = 0
    for dsrt in district:
        n += 1
        cur.execute("insert ignore into htl_city (city,province,district, district_id) values (%s,%s,%s,%s)",\
                    (city, province, dsrt[0], n))


if __name__ == '__main__':
    soup = load_url(curURL, 1)
    max_page = get_amount_pages(soup)
    cur.execute("start transaction")
    # create_table()

    # for page in range(1, max_page):
    #     spider_state_data(page)

    city_list('hangzhou', 'zhejiang')

    cur.close()
    conn.commit()
    conn.close()

    print 'State Data Done'
