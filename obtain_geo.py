#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

from datetime import datetime
from elasticsearch import Elasticsearch
import time
import datetime
import sys
import json
import urllib
import urllib2
import re
import time
import math

def bd_encrypt(gg_lon, gg_lat):
    x_pi = 3.14159265358979324 * 3000.0 / 180.0
    x = gg_lon
    y = gg_lat
    z = math.sqrt(x * x + y * y) + 0.00002 * math.sin(y * x_pi)
    theta = math.atan2(y, x) + 0.000003 * math.cos(x * x_pi)
    bd_lon = z * math.cos(theta) + 0.0065
    bd_lat = z * math.sin(theta) + 0.006
    return bd_lon,bd_lat

def obtain(ak, service_id, entity_name):
    es = Elasticsearch(
        ['10.214.0.134', '10.214.0.133'],
        http_auth=('elastic', 'elastic'),
    )


    now_time = int(time.time() * 1000)
    pre_time = int(time.time() * 1000 - 60 * 1000)
    res = es.search(index="kaoqin-*", body={
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
    print ("Got %d Hits:" % res['hits']['total'])
    for hit in res['hits']['hits']:
        created_time = time.strptime(hit["_source"]["created"], "%Y-%m-%dT%H:%M:%S.000Z")
        created_time = int((time.mktime(created_time) * 1000 + 60 * 60 * 8 * 1000) / 1000)
	#created_time = time.strptime(hit["_source"]["created"],"%B %dth %Y, %H:%M:%S.%f")
	#created_time = int(time.mktime(created_time))
        geo_speed = (abs(hit["_source"]["geo_speed"]) / 1000) * 60 * 60
	bd_lon = hit["_source"]["geo_longitude"] 
        bd_lat = hit["_source"]["geo_latitude"] 
        #print("%s %s %s %s %s" % (
        #hit["_source"]["open_id"], created_time, hit["_source"]["geo_longitude"], hit["_source"]["geo_latitude"],
        #geo_speed))
        url = 'http://yingyan.baidu.com/api/v3/track/addpoint'
        headers = {'Content-type': 'application/x-www-form-urlencoded', 'Cache-Control': 'no-cache'}
        data = {"ak": ak, "service_id": service_id, "entity_name": entity_name,
                "latitude": bd_lat, "longitude": bd_lon,
                "loc_time": created_time,
                "coord_type_input": "gcj02", "speed": geo_speed}
        data = urllib.urlencode(data)
        #print data
        req = urllib2.Request(url, data, headers)
        try:
            f = urllib2.urlopen(req)
            #print f.read()
        except urllib2.HTTPError, e:
            print e.code
            print e.read()
        else:
            return f.read()

if __name__ == '__main__':
    ak = '1ZlE1lZBaNn0ZiHhL81wSWScvtA0Cq7P'
    service_id = 149272
    fileHandle = open('/root/python/employee_fintech')
    fileList = fileHandle.readlines()
    datas = [fileline.strip('\n') for fileline in fileList]
    for data in datas:
        entity_desc = data.split()[0]
        entity_name = data.split()[1]
        print "entity_desc = %s , entity_name = %s" % (entity_desc, entity_name)
        print obtain(ak, service_id, entity_name)
    fileHandle.close()

