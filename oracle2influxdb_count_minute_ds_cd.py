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

dsn_tns = cx_Oracle.makedsn('10.214.2.71', 1530, 'efsdb')
db = cx_Oracle.connect('devro', 'SLI8fE05', dsn_tns)
cursor = db.cursor()
cursor.execute("""select trans_time,count(*) from
(
select to_char(g.create_date,'yyyymmdd hh24:mi') trans_time,trade_id
from cpdb_ds.t_ds_datasource_log_new@cpdb_cd2 g
where g.create_date>=to_date(to_char(sysdate-1/24/20,'yyyymmdd hh24mi')||'00','yyyymmdd hh24:mi:ss')
and g.create_date<to_date(to_char(sysdate-1/24/30,'yyyymmdd hh24mi')||'00','yyyymmdd hh24:mi:ss')
) cd_ds_log
group by trans_time""")
rows = cursor.fetchall()
for row in rows:
	json_body=[{"measurement":"count_minute_ds","tags":{"ds_name":"ds_cd"},"fields":{"count":row[1]}}]
	#print("Write points: {0}".format(json_body))
	client.write_points(json_body)
cursor.close()
db.close()

