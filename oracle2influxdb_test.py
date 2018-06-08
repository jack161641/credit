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
cursor.execute("""select l.product_id ,
t.product_name,
to_char(request_time, 'yyyy-mm-dd hh24:mi') as dt,
round(avg(to_number(substr(l.RESPONSE_TIME - l.REQUEST_TIME, 18, 2) ||
substr(l.RESPONSE_TIME - l.REQUEST_TIME, 21, 3)))) time_cost,
count(*)
from cpt_cst_request_log l, 
CPTDATA.T_ETL_PROD_TOPRANK T
where request_time<to_date(to_char(SYSDATE-1/24/60,'yyyy-mm-dd hh24:mi'),'yyyy-mm-dd hh24:mi:ss')   --过去1分钟
and   request_time>=to_date(to_char(SYSDATE-2/24/60,'yyyy-mm-dd hh24:mi'),'yyyy-mm-dd hh24:mi:ss')  --过去2分钟
and invoke_source in ('gateway','portlet','app')  --由网关发起
and t.amonth=to_char(add_months(sysdate,-1),'yyyy-mm') --取上个月的前十大
and l.product_id=t.product_id
group by l.product_id, t.product_name ,to_char(request_time, 'yyyy-mm-dd hh24:mi')
order by l.product_id, t.product_name ,to_char(request_time, 'yyyy-mm-dd hh24:mi')""")
rows = cursor.fetchall()
for row in rows:
	json_body=[{"measurement":row[0],"tags":{"product_name":row[1]},"fields":{"time_cost":row[3],"count":row[4]}}]
	print("Write points: %s" %(str(json_body).encode('utf-8')))
	#client.write_points(json_body)
cursor.close()
db.close()

