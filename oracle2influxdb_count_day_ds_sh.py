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

dsn_tns = cx_Oracle.makedsn('10.214.2.71', 1530, 'efsdb')
db = cx_Oracle.connect('devro', 'SLI8fE05', dsn_tns)
cursor = db.cursor()
cursor.execute("""select sysdate-1 ,count(*)
from cpdb_ds.t_ds_datasource_log_new@kqcd_cpdb_app g
where g.create_date>=to_date(to_char(sysdate-1,'yyyymmdd')||'00:00:00','yyyymmdd hh24:mi:ss')
and g.create_date<to_date(to_char(sysdate,'yyyymmdd')||'00:00:00','yyyymmdd hh24:mi:ss')""")
rows = cursor.fetchall()
for row in rows:
        day_date = row[0].strftime('%m-%d')
        json_body=[{"measurement":"count_day_ds","tags":{"ds_day":day_date},"fields":{"day":day_date,"ds_name":"上海","count":row[1]}}]
	#print("Write points: {0}".format(json_body))
	client.write_points(json_body)
cursor.close()
db.close()

