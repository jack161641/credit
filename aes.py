#!/usr/bin/env python
# -*- coding:utf-8 -*- 
 
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import base64
 
class prpcrypt():
    def __init__(self,key,iv):
        self.key = key
        self.iv  = iv
        self.mode = AES.MODE_CBC
        self.BS = AES.block_size
        #补位
        self.pad = lambda s: s + (self.BS - len(s) % self.BS) * chr(self.BS - len(s) % self.BS) 
	self.unpad = lambda s : s[0:-ord(s[-1])]
     
    def encrypt(self,text):
	a = (self.BS - len(text) % self.BS) 
	b =  chr(self.BS - len(text) % self.BS)
	#print "a: ", len(text)
	#print "b: ",b
        text = self.pad(text)
        print "text:",base64.b64encode(text)
        cryptor = AES.new(self.key,self.mode,self.iv)
        #目前AES-128 足够目前使用
        ciphertext = cryptor.encrypt(text)
        #把加密后的字符串转化为16进制字符串
        #return b2a_hex(ciphertext)
	return base64.b64encode(ciphertext)
     
    #解密后，去掉补足的空格用strip() 去掉
    def decrypt(self,text):
        cryptor = AES.new(self.key,self.mode, iv)
	plain_text = cryptor.decrypt(text)
        #plain_text  = cryptor.decrypt(a2b_hex(text))
        return self.unpad(plain_text.rstrip('\0'))
	#return plain_text

 
if __name__ == '__main__':
    iv = "0000000000000000"
    #ora = '''{"request_sn":"24ef5d41ac6d4fe184173d1d6e257b45","inf_id":"P_C_B040","acct_id":"CREDIT_TEST_ACCTID","prod_id":"P_C_B040","req_time":1490150022384,"req_data":{"cardNo":"211302198307040425","name":"张鸿羽"},"ext_data":null}'''
    ora = '''{"request_sn":"8263505e52d344efa2a19ab075e09db5","inf_id":"P_C_B040","acct_id":"CREDIT_TEST_ACCTID","prod_id":"P_C_B040","req_time":1490161136618,"req_data":{"cardNo":"211302198307040425","name":"张鸿羽"},"ext_data":null}'''
    #e2 = 'zqH82soWf5L3zktfbuREF/gGBh6dv0oxPWi43hkyAdLm+BXmzcTWYW8R2qTDwIWPLmnOLvbeUy7EGftAtNXRntp2Qmki5GDPj2kofkKBljyUzM4ADyyuIiSqn3sAGB3vlvieKoA2RBjJBPX3Y46YhWboDPRH7HLnwr1pxiKQ2mr8J9FEDDk8CD4qjQeptrEkCJt/MdKVDfgVgsTjauxlCJhG59vMkXpzyZaXAYD2VgH2tA+L61E/zktZur19zgraFUD7DEtqgkj0ct6I6PWzvNrHGydsPsd50JK04CnJrPzAqiIP6c+DOGEGTNtk8bbf='
    #e2 = 'L+Maa4wXBbzoWqz0zbawNGoAay80gsFiVw/RY0uE8+NoDYvrak55AR+6sHnI/qTQp750DVH40m1iO2rbDTthFt/cGYs3LSPHjj/mzjCDvY1wQWoIS4QOcHE4/+RiVlxc7/7rFdIpDSOIdCYqDUP4blV6KeEOZnGweOjeF1RK/QCWSRe+5d8ySrHu98J3IczwNLi8Rg0GlYfBPLXdzkYTszFDCiFZ17qTnywJ/WG9sldwpC473rpDhPE7QFagfOR5Q+rrpglaPIeRr/2TeMYEy/25GJpSDIOytr00h+oFYneSto43QaIwfeU6e3DYcwYpZ5GPRIWNVqZsF5gIBl7gnw=='
    e2 = 'L+Maa4wXBbzoWqz0zbawNGoAay80gsFiVw/RY0uE8+NoDYvrak55AR+6sHnI/qTQp750DVH40m1iO2rbDTthFt/cGYs3LSPHjj/mzjCDvY1wQWoIS4QOcHE4/+RiVlxc7/7rFdIpDSOIdCYqDUP4blV6KeEOZnGweOjeF1RK/QCWSRe+5d8ySrHu98J3IczwNLi8Rg0GlYfBPLXdzkYTszFDCiFZ17qTnywJ/WG9sldwpC473rpDhPE7QFagfOR5Q+rrpglaPIeRr/2TeMYEy/25GJpSDIOytr00h+oFYnfks7KEX/VEAgiWBt8muxDXPVLhXYY6jSW/PVXyVL/uBg=='
    key = a2b_hex('5d8f090cb619624819a78e145266334a')
    print "key:",key
    pc = prpcrypt(key, iv) #初始化密钥 和 iv
    import sys,os
    #fp = open("/tmp/test")
    #line = fp.readline()
    #line = line.strip('\n') 
    e = pc.encrypt(ora) #加密
    #e = pc.encrypt(sys.argv[1]) 
    e3 = base64.b64decode(e2)
    #print "e2 len:",len(e)
    #print "e3 len:",len(e3)
    #print "e3:",e3
    d = pc.decrypt(e3)#解密
    print "原文:",ora
    print "密文:",e
    print "解密:",d
    print "解密后长度:",len(d)

