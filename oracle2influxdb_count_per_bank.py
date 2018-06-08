#!/usr/bin/python2.7
# -*- coding:utf-8 -*- 

import cx_Oracle
import os
import sys
import time
import datetime
from influxdb import InfluxDBClient
import json

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.AL32UTF8'
#reload(sys)
#sys.setdefaultencoding('utf8')

client = InfluxDBClient('localhost',8086,'root',',','mydb')

dsn_tns = cx_Oracle.makedsn('10.214.2.71', 1530, 'efsdb')
db = cx_Oracle.connect('devro', 'SLI8fE05', dsn_tns)
cursor = db.cursor()
cursor.execute("""select ds_id,ds_name,to_char(create_date, 'yyyy-mm-dd hh24:mi') as dt,bank_name,
round(avg(total_cost)) time_cost,count(1) cnt ,sum(case when state_code <> '00' then 1 else 0 end) error_cnt
from (
select g.ds_id,s.ds_name,g.create_date,g.total_cost,g.state_code,(case when g.biz_code2 like '%工商%' then '工商银行'
 else case when g.biz_code2 like '%农业%' then '农业银行'
 else case when g.biz_code2 like '%中国银行%' then '中国银行'
 else case when g.biz_code2 like '%建设%' then '建设银行'
 else case when g.biz_code2 like '%交通%' then '交通银行'
 else case when g.biz_code2 like '%邮储%' or g.biz_code2 like '%邮政储蓄%' then '邮储银行'
 else case when g.biz_code2 like '%浦发%' then '浦发银行'
 else case when g.biz_code2 like '%兴业%' then '兴业银行'
 else case when g.biz_code2 like '%中信%' then '中信银行'
 else case when g.biz_code2 like '%光大%' then '光大银行'
 else case when g.biz_code2 like '%广发%' then '广发银行'
 else case when g.biz_code2 like '%平安%' then '平安银行'
 else case when g.biz_code2 like '%华夏%' then '华夏银行'
 else case when g.biz_code2 like '%民生%' then '民生银行'
 else case when g.biz_code2 like '%招商%' then '招商银行'
 else case when g.biz_code2 like '%华夏%' then '华夏银行'
else '其他银行' end end end end end end end end end end end end end end end end) bank_name
from cpdb_ds.t_ds_datasource_log_new@cpdb_cd2 g,cpdb_mk.t_etl_datasource_idname@cpdb_cd2 s
where g.ds_id = s.ds_id
and s.ds_id in ('ds_xyan_AuthenBankCardNew','ds_yinxing_AuthenBankCard','ds_xyan_AuthenBankCard',
'ds_juhe_AuthenBankCard3','ds_juhe_AuthenBankCard4','ds_mas_cardAuth','ds_jixin_AuthenBankCard')
and g.create_date >= to_date(to_char(SYSDATE-2/24/60,'yyyy-mm-dd hh24:mi'),'yyyy-mm-dd hh24:mi:ss')  --过去2分钟
and g.create_date < to_date(to_char(SYSDATE-1/24/60,'yyyy-mm-dd hh24:mi'),'yyyy-mm-dd hh24:mi:ss')   --过去1分钟
union all
select g.ds_id,s.ds_name,g.create_date,g.total_cost,g.state_code,(case when g.biz_code2 like '%工商%' then '工商银行'
 else case when g.biz_code2 like '%农业%' then '农业银行'
 else case when g.biz_code2 like '%中国银行%' then '中国银行'
 else case when g.biz_code2 like '%建设%' then '建设银行'
 else case when g.biz_code2 like '%交通%' then '交通银行'
 else case when g.biz_code2 like '%邮储%' or g.biz_code2 like '%邮政储蓄%' then '邮储银行'
 else case when g.biz_code2 like '%浦发%' then '浦发银行'
 else case when g.biz_code2 like '%兴业%' then '兴业银行'
 else case when g.biz_code2 like '%中信%' then '中信银行'
 else case when g.biz_code2 like '%光大%' then '光大银行'
 else case when g.biz_code2 like '%广发%' then '广发银行'
 else case when g.biz_code2 like '%平安%' then '平安银行'
 else case when g.biz_code2 like '%华夏%' then '华夏银行'
 else case when g.biz_code2 like '%民生%' then '民生银行'
 else case when g.biz_code2 like '%招商%' then '招商银行'
 else case when g.biz_code2 like '%华夏%' then '华夏银行'
else '其他银行' end end end end end end end end end end end end end end end end) bank_name
from cpdb_ds.t_ds_datasource_log_new@kqcd_cpdb_app g,cpdb_mk.t_etl_datasource_idname@kqcd_cpdb_app s
where g.ds_id = s.ds_id
and g.create_date >= to_date(to_char(SYSDATE-2/24/60,'yyyy-mm-dd hh24:mi'),'yyyy-mm-dd hh24:mi:ss')  --过去2分钟
and g.create_date < to_date(to_char(SYSDATE-1/24/60,'yyyy-mm-dd hh24:mi'),'yyyy-mm-dd hh24:mi:ss')   --过去1分钟
) group by ds_id,ds_name,to_char(create_date, 'yyyy-mm-dd hh24:mi'),bank_name""")
rows = cursor.fetchall()
for row in rows:
        json_body=[{"measurement":"count_per_bank","tags":{"bank_name":row[3],"ds_id":row[0]},"fields":{"bank_name":row[3],"ds_id":row[0],"ds_name":row[1],"time_cost":row[4],"count":row[5],"error_count":row[6]}}]
	#print (json.dumps(json_body,ensure_ascii=False))
	client.write_points(json_body)
cursor.close()
db.close()

