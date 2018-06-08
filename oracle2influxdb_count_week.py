#!/usr/bin/python2.7
# -*- coding:utf-8 -*- 

import cx_Oracle
import os
import sys
import time
import datetime
from influxdb import InfluxDBClient

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.AL32UTF8'
#reload(sys)
#sys.setdefaultencoding('utf8')

client = InfluxDBClient('localhost',8086,'root',',','mydb')
dsn_tns = cx_Oracle.makedsn('10.214.2.65', 1521, 'zhengxin')
db = cx_Oracle.connect('devro', 'nzaWq3XA', dsn_tns)
cursor = db.cursor()
cursor.execute("""select TRUNC(min(g.request_time)) mindate,TRUNC(max(g.request_time)) maxdate,to_char(g.request_time,'iw'),count(1) cnt
from cpt_cst_request_log g
where g.invoke_source in ('gateway','portlet','app')
and g.request_time >= trunc(sysdate)-7
group by to_char(g.request_time,'iw')""")
rows = cursor.fetchall()
#print rows
for row in rows:
	week_date=row[0].strftime('%m/%d')+'-'+row[1].strftime('%m/%d')
	json_body=[{"measurement":"count_week","tags":{"week":week_date},"fields":{"count":row[3]}}]
	#print("Write points: {0}".format(json_body))
	client.write_points(json_body)
cursor.close()
db.close()

