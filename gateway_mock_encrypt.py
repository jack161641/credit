#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import json
import urllib2
import time
import random, string
import base64
import argparse


class prpcrypt():
    def __init__(self, key, iv):
        self.key = key
        self.iv = iv
        self.mode = AES.MODE_CBC
        self.BS = AES.block_size
        # 补位
        self.pad = lambda s: s + (self.BS - len(s) % self.BS) * chr(self.BS - len(s) % self.BS)
        self.unpad = lambda s: s[0:-ord(s[-1])]

    def encrypt(self, text):
        a = (self.BS - len(text) % self.BS)
        b = chr(self.BS - len(text) % self.BS)
        text = self.pad(text)
        cryptor = AES.new(self.key, self.mode, self.iv)
        # 目前AES-128 足够目前使用
        ciphertext = cryptor.encrypt(text)
        # 把加密后的字符串使用base64编码
        return base64.b64encode(ciphertext)

    # 解密后，去掉补足的空格用strip() 去掉
    def decrypt(self, text):
        text = base64.b64decode(text)
        cryptor = AES.new(self.key, self.mode, self.iv)
        plain_text = cryptor.decrypt(text)
        return self.unpad(plain_text.rstrip('\0'))


class mock():
    def __init__(self, acct_id):
        key_len = 30
        self.url = 'http://credit.wanda.cn/credit-gw/service'
        self.headers = {'Content-type': 'application/json', 'X_WANDA_ACCT_ID': acct_id,
                        'Cache-Control': 'no-cache'}
        self.keylist = [random.choice(string.letters + string.digits) for i in range(key_len)]
        self.reqsn = "".join(self.keylist)
        self.reqtime = str(int(time.time())) + '000'

    def format(self, acct_id, acct_data):
        data = {"req_time": self.reqtime, "acct_id": acct_id, "inf_id": "P_C_B112", "prod_id": "P_C_B112",
                "request_sn": self.reqsn, "ext_data": {}, "req_data": acct_data}
        return data

    def send(self, data):
        req = urllib2.Request(self.url, data, self.headers)
        try:
            f = urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            print e.code
            print e.read()
        else:
            return f.read()


if __name__ == '__main__':
    #parser = argparse.ArgumentParser(description = 'Credit Gateway Mock Invoke')
    #parser.add_argument('-k','--key',action = 'store',help = 'Encrypt key',type = str)
    #parser.add_argument('-id','--id',action = 'store',help = 'Account id',type = str)
    #parser.add_argument('-data','--data',action = 'store',help = 'Resquest data',type = dict)
    #args = parser.parse_args()
    iv = "0000000000000000"
    #key = '5d8f090cb619624819a78e145266334a'
    #acct_id = "CREDIT_TEST_ACCTID"
    #acct_data = {"name": "陈浩", "idNo": "320105197603041412", "idType": "101", "reasonCode": "01",
    #             "mobile": "13924652748", "qq": "546344567@qq.com", "wechat": "dgfh0890",
    #             "weibo": "dgkhs0120@sina.com"}
    key = raw_input('please enter encrypt key:')
    acct_id = raw_input('please enter account id:')
    acct_data = input("please request data:")
    key = a2b_hex(key)
    req_data = mock(acct_id).format(acct_id, acct_data)
    req_data = json.dumps(req_data)
    print "请求原文:", req_data
    req_data = prpcrypt(key, iv).encrypt(req_data)
    print "请求密文:", req_data
    respon_data = mock(acct_id).send(req_data)
    print "响应密文:", respon_data
    respon_data = prpcrypt(key, iv).decrypt(respon_data)
    respon_data = json.loads(respon_data)
    print "响应原文:", respon_data
    if respon_data['retcode'] == '000000':
        print "调用成功"
    else:
        print "调用失败"

