#!/usr/bin/python2.7
# -*- coding:utf-8 -*- 

import cx_Oracle
import os
import sys
import time
from influxdb import InfluxDBClient

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.AL32UTF8'
#reload(sys)
#sys.setdefaultencoding('utf8')

client = InfluxDBClient('localhost',8086,'root',',','mydb')

dsn_tns = cx_Oracle.makedsn('10.214.2.65', 1521, 'zhengxin')
db = cx_Oracle.connect('devro', 'nzaWq3XA', dsn_tns)
cursor = db.cursor()
cursor.execute("""
select TRUNC(g.request_time) ADATE,count(1) cnt
from cpt_cst_request_log g
where g.invoke_source in ('gateway','portlet','app') 
and g.request_time >= trunc(sysdate)
group by trunc(g.request_time)""")
rows = cursor.fetchall()
for row in rows:
	json_body=[{"measurement":"count_today","tags":{"product_name":"current"},"fields":{"count":row[1]}}]
	#print("Write points: {0}".format(json_body))
	client.write_points(json_body)
cursor.close()
db.close()

