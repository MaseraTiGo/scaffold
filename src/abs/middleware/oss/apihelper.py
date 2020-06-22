# coding=UTF-8

'''
Created on 2016年8月24日

@author: Administrator
'''

# import python standard package

# import thread package
import oss2

# import my project package


access_key_id = 'LTAIZOIZXlWJV3C5'
access_key_secret = 'HRHgNkqSncPbuf7AGzRcAMSDjewECy'

endpoint = "http://oss-cn-beijing.aliyuncs.com"

class OSSAPI(object):

    def __init__(self):
        # self.auth = None
        self.auth = oss2.Auth(access_key_id, access_key_secret)
        self._register = {}

    def get_bucket(self, bucket_name):
        if bucket_name not in self._register:
            bucket = oss2.Bucket(self.auth, endpoint, bucket_name)
            self._register[bucket_name] = bucket
            # self._register[bucket_name] = None
        return self._register[bucket_name]

    def put_object(self, store_name, content, bucket_name):
        backet = self.get_bucket(bucket_name)
        if backet:
            result = backet.put_object(store_name, content)
            return result.resp.response.url
        raise Exception("backet error for oss")


if __name__ == "__main__":
    oss = OSSAPI()
    bucket_name = 'bq-crm-resouce'
    store_name = 'QQ截图20180803191412.png'
    with open(store_name, 'rb') as f:
        url = oss.put_object("通讯头像/{store}".format(store = store_name), f, bucket_name)
        print(url)
