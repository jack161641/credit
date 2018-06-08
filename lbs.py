#!/usr/bin/env python
# -*- coding: utf-8 -*-


from datetime import datetime
from elasticsearch import Elasticsearch
import cx_Oracle
import os
import time
import datetime
import sys
import json
import urllib
import urllib2
import re
import time
import random, string



class data():
    def obtain(self):
        os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.AL32UTF8'

        dsn_tns = cx_Oracle.makedsn('10.214.2.71', 1530, 'efsdb')
        db = cx_Oracle.connect('datatech', 'bhu8(IJN', dsn_tns)
        cursor = db.cursor()
        cursor.execute("""select NAME,OPEN_ID from attd_users where UNITNAME like '%金融科技%'""")
        rows = cursor.fetchall()
        f = open('employee_fintech','w')
        for row in rows:
	    #print row[0],row[1]
            f.writelines(row[0]+' '+ row[1]+'\n')
        f.close()

class entity():
    def add(self, ak, service_id, entity_name, entity_desc):
        url = 'http://yingyan.baidu.com/api/v3/entity/add'
        headers = {'Content-type': 'application/x-www-form-urlencoded', 'Cache-Control': 'no-cache'}
        data = {"ak": ak, "service_id": service_id, "entity_name": entity_name, "entity_desc": entity_desc}
        data = urllib.urlencode(data)
        req = urllib2.Request(url, data, headers)
        try:
            f = urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            print e.code
            print e.read()
        else:
            return f.read()

    def update(self, ak, service_id, entity_name, entity_desc):
        url = 'http://yingyan.baidu.com/api/v3/entity/update'
        headers = {'Content-type': 'application/x-www-form-urlencoded', 'Cache-Control': 'no-cache'}
        data = {"ak": ak, "service_id": service_id, "entity_name": entity_name, "entity_desc": entity_desc}
        data = urllib.urlencode(data)
        req = urllib2.Request(url, data, headers)
        try:
            f = urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            print e.code
            print e.read()
        else:
            return f.read()

    def delete(self, ak, service_id, entity_name):
        url = 'http://yingyan.baidu.com/api/v3/entity/delete'
        headers = {'Content-type': 'application/x-www-form-urlencoded', 'Cache-Control': 'no-cache'}
        data = {"ak": ak, "service_id": service_id, "entity_name": entity_name}
        data = urllib.urlencode(data)
        req = urllib2.Request(url, data, headers)
        try:
            f = urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            print e.code
            print e.read()
        else:
            return f.read()


class track():
    def addpoint(self, ak, service_id, entity_name, latitude, longitude, loc_time, speed):
        url = 'http://yingyan.baidu.com/api/v3/track/addpoint'
        headers = {'Content-type': 'application/x-www-form-urlencoded', 'Cache-Control': 'no-cache'}
        data = {"ak": ak, "service_id": service_id, "entity_name": entity_name, "latitude": latitude,
                "longitude": longitude, "loc_time": loc_time, "coord_type_input": "wgs84", "speed": speed}
        data = urllib.urlencode(data)
        req = urllib2.Request(url, data, headers)
        try:
            f = urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            print e.code
            print e.read()
        else:
            return f.read()


class elastic():
    def obtain(entity_name):
        es = Elasticsearch(
            ['10.214.0.134', '10.214.0.133'],
            http_auth=('elastic', 'elastic'),
        )
        now_time = int(time.time() * 1000)
        pre_time = int(time.time() * 1000 - 60 * 1000)
        res = es.search(index="logstash-*", body={
            "query": {
                "bool": {
                    "must": [
                        {
                            "query_string": {
                                "query": entity_name,
                            }
                        },
                        {
                            "range": {
                                "@timestamp": {
                                    "gte": pre_time,
                                    "lte": now_time,
                                    "format": "epoch_millis"
                                }
                            }
                        }
                    ],
                    "must_not": []
                }
            }
        }
                        )
        # return res


if __name__ == '__main__':
    ak = '1ZlE1lZBaNn0ZiHhL81wSWScvtA0Cq7P'
    service_id = 149272
    #data().obtain()
    fileHandle = open('/root/python/employee_fintech')
    fileList = fileHandle.readlines()
    #   for fileLine in fileList:
    #       print fileLine.strip('\n')
    datas = [fileline.strip('\n') for fileline in fileList]
    #for index in range(len(datas)):
    #    print datas[index]

    for data in datas:
        entity_desc = data.split()[0]
        entity_name = data.split()[1]
        print "entity_desc = %s , entity_name = %s" % (entity_desc, entity_name)
        print entity().add(ak,service_id,entity_name,entity_desc)
    fileHandle.close()
