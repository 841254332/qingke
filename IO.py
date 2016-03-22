# -*- coding: utf-8 -*-
__author__ = 'admin'


def save_to_db(sql, values):
    conn = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='1234', db='ped', charset='utf8')
    cur = conn.cursor()
    try:
        cur.execute(sql, values)
    except MySQLdb.Error, e:
        print e
    conn.commit()
    conn.close()


def save_to_mysql(sql):
    conn = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='1234', db='ped', charset='utf8')
    cur = conn.cursor()
    try:
        cur.execute(sql)
    except MySQLdb.Error, e:
        print e
    conn.commit()
    conn.close()


def get_data_from_sql(table):
    conn = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='1234', db='ped', charset='utf8')
    cur = conn.cursor()
    link_list = []
    try:
        cur.execute('SELECT * FROM ' + table + ' WHERE update_time !=\'2016-01-11\'')
        results = cur.fetchall()
        for link in results:
            if link[3] is None:
                link_list.append(link[1])
        return link_list
    except MySQLdb.Error, e:
        print "MySql Error %d: %s" % (e.args[0], e.args[1])


def get_data_from_db(sql, database):
    conn = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='1234', db=database, charset='utf8')
    cur = conn.cursor()
    try:
        cur.execute(sql)
        result = cur.fetchall()
        return result
    except MySQLdb.Error, e:
        print "MySql Error %d: %s" % (e.args[0], e.args[1])


