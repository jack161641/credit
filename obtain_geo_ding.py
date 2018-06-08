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


def obtain():
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
                            "query": "obAMY0b4kWtUao0LXCC5CbuqCyXg",
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
    #print "res = ",json.dumps(res)
    print("Got %d Hits:" % res['hits']['total'])
    point = []
    i = 0
    for hit in res['hits']['hits']:
        created_time = time.strptime(hit["_source"]["created"], "%Y-%m-%dT%H:%M:%S.000Z")
        created_time = int((time.mktime(created_time) * 1000 + 60 * 60 * 8 * 1000) / 1000)
        geo_speed = (abs(hit["_source"]["geo_speed"]) / 1000) * 60 * 60
        #print("%s %s %s %s %s" % (
        #hit["_source"]["open_id"], created_time, hit["_source"]["geo_longitude"], hit["_source"]["geo_latitude"],
        #geo_speed))
	point.append({"entity_name":"obAMY0b4kWtUao0LXCC5CbuqCyXg","latitude":hit["_source"]["geo_latitude"],
                      "longitude":hit["_source"]["geo_longitude"],"loc_time":created_time,
                      "coord_type_input":"wgs84","speed":geo_speed})
	#print "%d point = %s" % (i,point)
	#i = i + 1
    print "point = ", point
    url = 'http://yingyan.baidu.com/api/v3/track/addpoints'
    headers = {'Content-type': 'multipart/form-data', 'Cache-Control': 'no-cache'}
    data = {"ak":"1ZlE1lZBaNn0ZiHhL81wSWScvtA0Cq7P","service_id":"149272","point_list":point}
    data = {"point_list":point}
    #data =  {"ak":"1ZlE1lZBaNn0ZiHhL81wSWScvtA0Cq7P","service_id":"149272","point_list": {"entity_name":"obAMY0b4kWtUao0LXCC5CbuqCyXg","latitude":hit["_source"]["geo_latitude"],"longitude":hit["_source"]["geo_longitude"],"loc_time":created_time,"coord_type_input":"wgs84","speed":geo_speed}}
    data = json.dumps(data)
    #data = urllib.urlencode("ak":"1ZlE1lZBaNn0ZiHhL81wSWScvtA0Cq7P","service_id":"149272","point_list":data)
    print "data = ",data
    req = urllib2.Request(url,data,headers)
    try:
        f = urllib2.urlopen(req)
        print f.read()
    except urllib2.HTTPError, e:
        print e.code
        print e.read()
    else:
        return f.read()

if __name__ == '__main__':
     obtain()
