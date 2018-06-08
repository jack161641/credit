#!/usr/bin/env python
# -*- coding: utf-8 -*-

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


class elastic():
    def obtain(self,entity_name):
        es = Elasticsearch(
            ['10.214.0.134', '10.214.0.133'],
            http_auth=('elastic', 'elastic'),
        )
        now_time = int(time.time() * 1000)
        pre_time = int(time.time() * 1000 - 60 * 1000)
	print ("now_time = %s,pre_tiem = %s" %(now_time,pre_time))
        res = es.search(index="logstash-*", body={
            "query": {
                "bool": {
		   "must": [{"query_string": {"query": entity_name}},
                            {"range": {"@timestamp": { "gte": pre_time,"lte":now_time}}}]
                }
            }
         }
	)
	print type(res)	
	#for line in res['hit']['hit']:
	#   print line
	print json.dumps(res)
        print ("Got %d Hits:" % res['hits']['total'])
        for hit in res['hits']['hits']:
	#for hit in res:
	   created_time = time.strptime(hit["_source"]["created"], "%Y-%m-%dT%H:%M:%S.000Z")
           created_time = int((time.mktime(created_time) * 1000 + 60 * 60 * 8 * 1000) / 1000)
           geo_speed = (abs(hit["_source"]["geo_speed"]) / 1000) * 60 * 60
           print("%s %s %s %s %s" % (
           hit["_source"]["open_id"], created_time, hit["_source"]["geo_longitude"], hit["_source"]["geo_latitude"],
           geo_speed))
	   print "ok"
	   data=[hit["_source"]["open_id"],created_time,hit["_source"]["geo_longitude"],hit["_source"]["geo_latitude"],geo_speed]
#	print data
#    return res['hits']['hits']
if __name__ == '__main__':
    elastic().obtain('obAMY0b4kWtUao0LXCC5CbuqCyXg')

