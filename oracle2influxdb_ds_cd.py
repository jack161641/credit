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
cursor.execute("""select ds_id,ds_name,to_char(create_date, 'yyyy-mm-dd hh24:mi') as dt,
round(avg(total_cost)) time_cost,count(1) cnt ,sum(case when state_code <> '00' then 1 else 0 end) error_cnt
from (
select g.ds_id,s.ds_name,g.create_date,g.total_cost,h.prod_id,g.state_code
from cpdb_ds.t_ds_datasource_log_new@cpdb_cd2 g,cpdb_mk.t_etl_datasource_idname@cpdb_cd2 s,
cpdb_app.t_sys_req_header@cpdb_cd2 h,cptdata.T_ETL_PROD_TOPRANK@ZHENGXIN c
where g.ds_id = s.ds_id and h.trade_id = g.trade_id and h.prod_id = c.product_id
and g.create_date >= to_date(to_char(SYSDATE-2/24/60,'yyyy-mm-dd hh24:mi'),'yyyy-mm-dd hh24:mi:ss')  --过去2分钟
and g.create_date < to_date(to_char(SYSDATE-1/24/60,'yyyy-mm-dd hh24:mi'),'yyyy-mm-dd hh24:mi:ss')   --过去1分钟
) group by ds_id,ds_name,to_char(create_date, 'yyyy-mm-dd hh24:mi')""")
rows = cursor.fetchall()
for row in rows:
	json_body=[{"measurement":row[0],"tags":{"ds_name":row[1]},"fields":{"cd_time_cost":row[3],"cd_count":row[4]}}]
	#print("Write points: {0}".format(json_body))
	client.write_points(json_body)
cursor.close()
db.close()

