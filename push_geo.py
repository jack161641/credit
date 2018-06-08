#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import urllib
import urllib2
import re
import time
import string

    def push_geo():
        url = 'http://yingyan.baidu.com/api/v3/track/addpoints'
        headers = {'Content-type': 'application/x-www-form-urlencoded',
                        'Cache-Control': 'no-cache'}

    def send(self):
        data = {"req_time": reqtime, "acct_id": "credit-cdtest", "inf_id": "P_C_B112", "prod_id": "P_C_B112",
                "req_data": {"name": "陈浩", "idNo": "320105197603041412", "idType": "101", "reasonCode": "01",
                             "mobile": "13924652748", "qq": "546344567@qq.com", "wechat": "dgfh0890",
                             "weibo": "dgkhs0120@sina.com"}, "request_sn": self.reqsn, "ext_data": {}}
        data = json.dumps(data)
        req = urllib2.Request(self.url, data, self.headers)
        try:
            f = urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            print e.code
            print e.read()
        else:
            return f.read()
