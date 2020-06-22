# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

class SMSServer(object):

    @classmethod
    def send_verify_code(cls, code):
        print("[server - send_verify_code] : send verify code .....")
        return code
