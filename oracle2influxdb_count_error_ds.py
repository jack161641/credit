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
cursor.execute("""select ds_id,ds_name,to_char(create_date, 'yyyy-mm-dd hh24:mi') as dt,state_code,state_msg,
round(avg(total_cost)) time_cost,count(1) cnt
from (
select g.ds_id,s.ds_name,g.create_date,g.total_cost,h.prod_id,g.state_code,g.state_msg
from cpdb_ds.t_ds_datasource_log_new@cpdb_cd2 g,cpdb_mk.t_etl_datasource_idname@cpdb_cd2 s,
cpdb_app.t_sys_req_header@cpdb_cd2 h,cptdata.T_ETL_PROD_TOPRANK@ZHENGXIN c
where g.ds_id = s.ds_id and h.trade_id = g.trade_id and h.prod_id = c.product_id
and g.create_date >= to_date(to_char(SYSDATE-2/24/60,'yyyy-mm-dd hh24:mi'),'yyyy-mm-dd hh24:mi:ss')  --过去2分钟
and g.create_date < to_date(to_char(SYSDATE-1/24/60,'yyyy-mm-dd hh24:mi'),'yyyy-mm-dd hh24:mi:ss')   --过去1分钟
and ((g.state_code = '01' and g.state_msg like '%异常%' ) or g.state_code = '02')
union all
select g.ds_id,s.ds_name,g.create_date,g.total_cost,h.prod_id,g.state_code,g.state_msg
from cpdb_ds.t_ds_datasource_log_new@kqcd_cpdb_app g,cpdb_mk.t_etl_datasource_idname@kqcd_cpdb_app s,
t_sys_req_header@kqcd_cpdb_app h,cptdata.T_ETL_PROD_TOPRANK@ZHENGXIN c
where g.ds_id = s.ds_id and h.trade_id = g.trade_id and h.prod_id = c.product_id
and g.create_date >= to_date(to_char(SYSDATE-2/24/60,'yyyy-mm-dd hh24:mi'),'yyyy-mm-dd hh24:mi:ss')  --过去2分钟
and g.create_date < to_date(to_char(SYSDATE-1/24/60,'yyyy-mm-dd hh24:mi'),'yyyy-mm-dd hh24:mi:ss')   --过去1分钟
and ((g.state_code = '01' and g.state_msg like '%异常%' ) or g.state_code = '02')
) group by ds_id,ds_name,to_char(create_date, 'yyyy-mm-dd hh24:mi'),state_code,state_msg""")
rows = cursor.fetchall()
for row in rows:
	json_body=[{"measurement":"ds_error","tags":{"ds_id":row[0]},"fields":{"ds_name":row[1],"state_code":row[3],"state_msg":row[4],"time_cost":row[5],"count":row[6]}}]
	#print("Write points: {0}".format(json_body))
	client.write_points(json_body)
cursor.close()
db.close()

