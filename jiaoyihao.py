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


def obtain(number):
    es = Elasticsearch(
        ['10.214.0.134', '10.214.0.133'],
        http_auth=('elastic', 'elastic'),
    )

    str_search= number + " AND " + "code"
    res = es.search(index="logstash-*", body={
        "query": {
            "bool": {
                "must": [ {"query_string": { "query": str_search }},
			  {"match_phrase": { "fields.filename": {"query": "app-wanda-credit-ds.log"}}}
			]
                    }
		}
    }
    )
    if (res['hits']['total'] == 0):
	return "Message is not found"
    #print ("Got %d Hits:" % res['hits']['total'])
    for hit in res['hits']['hits']:
         #print  "logmessage",hit["_source"]["logmessage"]
	 if (hit["_source"]["logmessage"].find('success') <> -1 ):
             index_start = hit["_source"]["logmessage"].find('success')
             res_mes = json.loads(hit["_source"]["logmessage"][index_start-2:])
	     #print "res_mes", res_mes
             return  "code:%s desc:%s" % (res_mes['data']['code'], res_mes['data']['desc'])
         elif (hit["_source"]["logmessage"].find('code') <> -1 ):
	     index_start = hit["_source"]["logmessage"].find('code')
             res_mes = json.loads(hit["_source"]["logmessage"][index_start-2:])
	     #print "res_mes", res_mes
	     return "code:%s message:%s" % (res_mes['code'], res_mes['msg'])
	 else:
	     return "Response is not regular pattern"
if __name__ == '__main__':
       number=sys.argv[1]
       print obtain(number)

