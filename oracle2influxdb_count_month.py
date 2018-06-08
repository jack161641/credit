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
#year=int(datetime.date.today().strftime("%Y"))
year=int(datetime.date.today().year)
client = InfluxDBClient('localhost',8086,'root',',','mydb')
dsn_tns = cx_Oracle.makedsn('10.214.2.65', 1521, 'zhengxin')
db = cx_Oracle.connect('devro', 'nzaWq3XA', dsn_tns)
cursor = db.cursor()
cursor.execute("""select to_char(g.request_time,'mm'),count(1) cnt
from cpt_cst_request_log g
where g.invoke_source in ('gateway','portlet','app')
and g.request_time >= add_months(trunc(last_day(sysdate))+1,-2)
group by to_char(g.request_time,'mm')""")
rows = cursor.fetchall()
#print rows
for row in rows:
	month=int(row[0])
	t=datetime.date(year,month,1)
	month_date=t.strftime('%Y%m')
        json_body=[{"measurement":"count_month","tags":{"month":month_date},"fields":{"count":row[1]}}]
	#print("Write points: {0}".format(json_body))
	client.write_points(json_body)
cursor.close()
db.close()

