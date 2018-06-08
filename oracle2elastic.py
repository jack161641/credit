#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

import cx_Oracle
import os
import sys
from datetime import datetime
from elasticsearch import Elasticsearch

es = Elasticsearch(
    ['10.214.0.111', '10.214.0.133'],
    http_auth=('elastic', 'elastic'),
)
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.AL32UTF8'

dsn_tns = cx_Oracle.makedsn('10.214.2.71', 1530, 'efsdb')
db = cx_Oracle.connect('datatech', 'bhu8(IJN', dsn_tns)
cursor = db.cursor()
cursor.execute("""select * from attd_geo_track order by created desc""")
rows = cursor.fetchall()

print rows
for row in rows:
#	print row
	doc = {
	'id': row[0],
	'open_id': row[1],
	'client_time': row[2],
	'geo_distance': row[3],
	'geo_latitude': row[4],
	'geo_longitude': row[5],
	'geo_speed': row[6],
	'geo_accuracy': row[7],
	'geo_altitude': row[8],
	'geo_verticalaccuracy': row[9],
	'geo_horizonaccuracy': row[10],
	'device_model': row[11],
	'device_weixin_version': row[12],
	'device_system_version': row[13],
	'device_network_type': row[14],
	'created': row[15],
}
#	print doc
	
#	res = es.index(index="geo-trace", doc_type='external', body=doc)
cursor.close()
db.close()
