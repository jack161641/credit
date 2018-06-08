#!/usr/bin/python2.7
# -*- coding:utf-8 -*- 

import cx_Oracle
import os
import sys
from influxdb import InfluxDBClient

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
#os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.AL32UTF8'
#os.environ['NLS_LANG'] = 'AMERICAN_AMERICA.AL32UTF8' 
reload(sys)
sys.setdefaultencoding('utf8')

#client = InfluxDBClient('localhost',8086,'root',",")
cardno_entry = '$45CA30662C7F368F11D6DCA7BDF2F1901A48A0E6792BE92F'
dsn_tns = cx_Oracle.makedsn('10.214.2.71', 1530,'efsdb' )
db = cx_Oracle.connect('devro', 'SLI8fE05', dsn_tns)
cursor = db.cursor()
cursor.execute("""select 
t.cardno ,t.name ,t.pair_similarity ,h.acct_id ,
h.req_time ,
y.file_name||'.jpg' ,
replace(y.file_path,'/opt/netdata/Creditdata','/u01/data/sata2/pics_cd') 
from cpdb_ds.t_ds_yitu_auth_result@kqcd_cpdb_ds t ,cpdb_app.t_sys_req_header@kqcd_cpdb_app h,
cpdb_app.t_sys_file_factory@kqcd_cpdb_app y
where t.cardno = '%s'
and t.photo_id is not null
and t.trade_id = h.trade_id and y.id = t.photo_id
and h.acct_id in ('coc_act_app_user','coc_kyh_user','coc_zyt_user','coc_kyh2_user')
and t.pair_similarity >= 66
union all 
select 
t.cardno ,t.name ,t.pair_similarity ,h.acct_id ,
h.req_time ,
y.file_name||'.jpg' ,
replace(y.file_path,'/opt/netdata/Creditdata','/u01/data/sata2/pics_cd') 
from cpdb_ds.t_ds_yitu_auth_result@kqcd_cpdb_ds t ,cpdb_app.t_sys_req_header@kqcd_cpdb_app h,
cpdb_app.t_sys_file_factory@kqcd_cpdb_app y,cpdb_ds.t_ds_yitu_auth_photo@kqcd_cpdb_ds p
where t.cardno = '%s'
and t.photo_id is null and t.trade_id = p.trade_id
and t.trade_id = h.trade_id and y.id = p.photo_id
and h.acct_id in ('coc_act_app_user','coc_kyh_user','coc_zyt_user','coc_kyh2_user')
and t.pair_similarity >= 66""" %(cardno_entry,cardno_entry))
#sql = "select zx_encrypt(%s) from dual",cardno
#cursor.execute("""select id,open_id,client_time,geo_distance,geo_latitude,geo_longitude,geo_speed,geo_accuracy,geo_altitude,geo_verticalaccuracy,geo_horizonaccuracy,device_model,device_weixin_version,device_system_version,device_network_type,created from attd_geo_track where client_time >=to_date(to_char(SYSDATE-1/24/10,'yyyy-mm-dd hh24:mi'),'yyyy-mm-dd hh24:mi:ss')""")
#cursor.execute("""select  NAME,OPEN_ID from attd_users where UNITNAME like '%数据科技%'""")
#cursor.execute("""select l.product_id ,
#t.product_name,
#to_char(request_time, 'yyyy-mm-dd hh24:mi') as dt,
#round(avg(to_number(substr(l.RESPONSE_TIME - l.REQUEST_TIME, 18, 2) ||
#substr(l.RESPONSE_TIME - l.REQUEST_TIME, 21, 3)))) time_cost,
#count(*)
#from cpt_cst_request_log l, 
#CPTDATA.T_ETL_PROD_TOPRANK T
#where request_time>=to_date(to_char(SYSDATE-1/24/10,'yyyy-mm-dd hh24:mi'),'yyyy-mm-dd hh24:mi:ss') --前6分钟
#and request_time<to_date(to_char(SYSDATE-1/24/60,'yyyy-mm-dd hh24:mi'),'yyyy-mm-dd hh24:mi:ss') --前1分钟
#and invoke_source ='gateway' --由网关发起
#and t.amonth=to_char(add_months(sysdate,-1),'yyyy-mm') --取上个月的前十大
#and l.product_id=t.product_id
#group by l.product_id, t.product_name ,to_char(request_time, 'yyyy-mm-dd hh24:mi')
#order by l.product_id, t.product_name ,to_char(request_time, 'yyyy-mm-dd hh24:mi')""")
rows = cursor.fetchall()
#print 'rows_range:',range(rows)
#print rows[0]
for row in rows:
	print row
cursor.close()
db.close()

