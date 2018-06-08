#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import cx_Oracle
import sys
import os
import urllib2
import random, string
import json
import urllib
import threading

def obtain_account_status():
    os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
    dsn_tns = cx_Oracle.makedsn('10.214.2.71', 1530, 'efsdb')
    pool = cx_Oracle.SessionPool('devro','SLI8fE05',dsn_tns,2,5,1,threaded = True)
    conn = pool.acquire()
    cursor = conn.cursor()
    cursor.arraysize = 25000
    #cursor.execute("""select mobile from CFSUN.tmp_scf_sms where rownum <= 1 AND isauth is NULL""")
    while True:
	cursor.execute("""select mobile from CFSUN.tmp_scf_sms where  isauth is NULL""")
        rows = cursor.fetchmany()
        #print "rows:",rows[0]
        if not rows:
            break
	for row in rows:
            #print "row:",row
            mobile_number = cursor.callfunc("zx_decrypt",str,(row))
	    #print "mobile_number:",mobile_number
            account = account_search(mobile_number)
            account = json.loads(account)
	    #print "respond:",account
	    #print "respond_loginAccount:",account['loginAccountList'][0]
            try:
                status = account['loginAccountList'][0]
	        print "respond_status:",status
            except:
                status = 999
            else:
                 status = status['loginStatus']
	    mobile_number_str=row[0]
	    bind_val = [] 
	    bind_val = [status,mobile_number_str]
	    #print "update statement:update CFSUN.tmp_scf_sms set isauth = %d where mobile = %s" %(bind_val[0],bind_val[1])
	    cursor.execute("""update CFSUN.tmp_scf_sms set isauth = :1 where mobile = :2""", bind_val )
            cursor.execute("""commit""")
    cursor.close()
    db.close()

def update(status,mobile):
    dsn_tns = cx_Oracle.makedsn('10.214.2.71', 1530, 'efsdb')
    db = cx_Oracle.connect('devro', 'SLI8fE05', dsn_tns)
    status = int(status)
    mobile = '$4381AD6517EF215247F2C5072172C1A7'
    print("status: %d mobile: %s" %(status,mobile))
    cursor = db.cursor()
    #cursor.execute("""select * from CFSUN.tmp_scf_sms  where mobile = '%s'""" %(mobile,))
    cursor.execute("""update CFSUN.tmp_scf_sms set isauth = 1 where mobile = '%s'""" %(mobile,))
    cursor.execute("""commit""")
    #rows = cursor.fetchall()
    #print rows
    cursor.close()
    db.close()

def account_search(mobile_number):
    key_len = 9
    url = 'http://10.214.65.20:8080/v1/query/login_account/exist'
    headers = {'Content-type': 'application/json'}
    keylist = [random.choice(string.digits) for i in range(key_len)]
    reqsn = "".join(keylist)
    data = {
        "reqHeader": {"accessToken": "775AC-SNMSD-K13LG-TD8OZ-XSP7C", "appId": "wandacredit", "entityId": "wandacredit",
                      "reqId": reqsn, "sessionId": reqsn}, "loginName": mobile_number}
    data = json.dumps(data)
    req = urllib2.Request(url, data, headers)
    try:
        f = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        print e.code
        print e.read()
    else:
        return f.read()

if __name__ == '__main__':
    thread = threading.Thread(None,obtain_account_status)
    thread.start()
    #status = sys.argv[1]
    #mobile = sys.argv[2]	
    #update(status,mobile)

