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
cursor.execute("""select to_char(g.request_time,'mm-dd hh24:mi') amin,count(1) cnt
from cpt_cst_request_log g
where g.invoke_source in ('gateway','portlet','app') 
and request_time<to_date(to_char(SYSDATE-1/24/60,'yyyy-mm-dd hh24:mi'),'yyyy-mm-dd hh24:mi:ss')   --过去1分钟
and request_time>=to_date(to_char(SYSDATE-2/24/60,'yyyy-mm-dd hh24:mi'),'yyyy-mm-dd hh24:mi:ss')  --过去2分钟
group by to_char(g.request_time,'mm-dd hh24:mi')
order by to_char(g.request_time,'mm-dd hh24:mi')""")
rows = cursor.fetchall()
for row in rows:
	json_body=[{"measurement":"count_minute","tags":{"product_name":"count"},"fields":{"count":row[1]}}]
	#print("Write points: {0}".format(json_body))
	client.write_points(json_body)
cursor.close()
db.close()

