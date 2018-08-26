# -*- coding:utf-8 -*-

import unittest
import os
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fontManager
import seaborn as sns
from pylab import mpl
import random
import csv
import codecs
import MySQLdb
import sys
from Ctrip_Spider_Init import connect_server

from warnings import filterwarnings
filterwarnings('error', category=MySQLdb.Warning)

reload(sys)
sys.setdefaultencoding("utf-8")  # Set system default encoding as UTF-8
doc_path = "G:\Program\Projects\Warcraft_Sipder\csv_test.csv"

conn, cur = connect_server()


def classify(n, interval):
    return '[%.1f,%.1f)' % (n*10//10, n*10//10+interval)


def city_top_10(min_price, max_price, min_rating, min_judge):
    cur.execute("select htl_state_data.id,htl_state_data.district,htl_price.price,htl_rating.rating,htl_judge.judge\
                from htl_state_data inner join htl_price on htl_state_data.id = htl_price.id \
                inner join htl_rating on htl_price.id = htl_rating.id\
                inner join htl_judge on htl_rating.id = htl_judge.id\
                where htl_price.price between %s and %s and htl_rating.rating > %s and htl_judge.judge > %s\
                order by htl_rating.rating DESC,htl_judge.judge DESC,htl_price.price ASC\
                limit 10", (min_price, max_price, min_rating, min_judge))
    htls = cur.fetchall()

    with codecs.open(doc_path, "wb") as top_10:
        top_10.write(codecs.BOM_UTF8)  # To display Chinese, avoid mess
        writer = csv.writer(top_10)

        if len(htls) > 0:
            for htl in htls:
                cur.execute("select htl_state_data.name from htl_state_data where htl_state_data.id = %s", (htl[0],))
                name = cur.fetchall()
                print name[0][0]+','+','.join(str(htl[i]) for i in xrange(5))
                writer.writerow([name[0][0], name[0][0], htl[2], "http://www.baidu.com"])
    top_10.close()

#     python -m SimpleHTTPServer 3000


def district_top_10(min_price, max_price, min_rating, min_judge):
    cur.execute("select distinct htl_state_data.district from htl_state_data")
    district = cur.fetchall()
    for dsrt in district:
        cur.execute("select htl_state_data.id,htl_state_data.district,htl_price.price,htl_rating.rating,htl_judge.judge\
                from htl_state_data inner join htl_price on htl_state_data.id = htl_price.id \
                inner join htl_rating on htl_price.id = htl_rating.id\
                inner join htl_judge on htl_rating.id = htl_judge.id\
                where htl_state_data.district like %s and htl_price.price between %s and %s and \
                htl_rating.rating > %s and htl_judge.judge > %s\
                order by htl_rating.rating DESC,htl_judge.judge DESC,htl_price.price ASC\
                limit 10", (dsrt[0], min_price, max_price, min_rating, min_judge))
        htls = cur.fetchall()

        if len(htls) > 0:
            for htl in htls:
                cur.execute("select htl_state_data.name from htl_state_data where htl_state_data.id = %s", (htl[0],))
                name = cur.fetchall()
                print name[0][0]+','+','.join(str(htl[i]) for i in xrange(5))


def district_details(district):
    original_df = pd.read_sql("select htl_state_data.id,htl_state_data.district,htl_price.price,htl_rating.rating,htl_judge.judge\
                from htl_state_data inner join htl_price on htl_state_data.id = htl_price.id \
                inner join htl_rating on htl_price.id = htl_rating.id\
                inner join htl_judge on htl_rating.id = htl_judge.id;", con=conn)

    lbl_price = ["{0}-{1}".format(i, i+99) for i in range(0, 10000, 100)]
    original_df['grp_price'] = pd.cut(original_df['price'], range(0, 10010, 100), right=True, labels=lbl_price)
    original_df['grp_price'] = original_df['grp_price'].astype('category')
    original_df['grp_price'].cat.set_categories(lbl_price)

    lbl_rating = ["{0}-{1}".format(i, i+0.5) for i in np.arange(0, 5, 0.5)]
    original_df['grp_rating'] = pd.cut(original_df['rating'], np.arange(0, 5.5, 0.5), right=True, labels=lbl_rating)
    original_df['grp_rating'] = original_df['grp_rating'].astype('category')
    original_df['grp_rating'].cat.set_categories(lbl_rating)

    lbl_judge = ["{0}-{1}".format(i, i+99) for i in range(0, 50000, 100)]
    original_df['grp_judge'] = pd.cut(original_df['judge'], range(0, 50100, 100), right=True, labels=lbl_judge)
    original_df['grp_judge'] = original_df['grp_judge'].astype('category')
    original_df['grp_judge'].cat.set_categories(lbl_judge)

    # print original_df.head(20)

    price = pd.cut(original_df['price'], [0, 1000, 10010], right=True)
    count_price = price.value_counts()
    all_price = pd.DataFrame(count_price, index=None)
    # plt_price.plot.bar()  # plt_price.plot(kind='bar')
    all_price.plot.pie(subplots=True, table=True, figsize=(6, 6),title='abc', legend=True, labels=['<1000', '>=1000'])
    # figsize is the size of shape
    # legend is to display legend on subplot
    # table is to use passed data from DataFrame to draw a table

    grp_price = original_df['grp_price'].value_counts()
    index_low_price = ["{0}-{1}".format(i, i+99) for i in range(0, 1000, 100)]
    low_price = pd.DataFrame(grp_price[:1000/100], index=index_low_price)
    low_price.plot(kind='bar', stacked=False)

    # # The number of hotel in each range of price
    # plt.bar(x_axis, data, width=0.5)

    # Example
    # count = original_df['price'].value_counts()
    # count.plot(kind='bar', stacked=True)
    # ts = pd.Series(count, index=None)
    # ts.plot()

    # Example_1
    # data = np.random.randint(1, 100, 30)
    # x = np.arange(len(data))
    # plt.bar(x, data, 0.8)

    # Example_2
    # data = np.random.randint(1, 11, 5)
    # x = np.arange(len(data))
    # plt.plot(x, data, color = 'r')
    # plt.bar(x, data, alpha = .5, color = 'g')

    # Example_3
    # x = [{i:random.randint(1,5)} for i in range(10)]
    # df = pd.DataFrame(x)
    # print df
    # df.plot(kind='bar', stacked=True)

    plt.show()

    # plt.figure(1)
    # width = 1
    # for i in range(len(count)):
    #     plt.bar(i*width,count[i],width)
    # plt.xlabel("x")
    # plt.ylabel("y")
    # plt.show()

    # district = unicode(district).encode('utf8')
    # result = original_df[original_df['district'] == district]
    # count = result = result['rating'].value_counts()
    # print count
    # result['cla'] = classify(result['rating'], 0.5)
    # print result

    # data = np.random.randint(1,11,5)
    # x = np.arange(len(data))
    # plt.bar(x,data,alpha=.5,color='g')
    # plt.show()


if __name__ == '__main__':
    # city_top_10(200, 300, 4.0, 2000)
    # district_top_10(200, 300, 4.0, 2000)
    dis = '西湖湖滨商圈'
    district_details(dis)
    # approximate_num(324)
    # print classify(4.2, 0.5)

    print 'Done'

