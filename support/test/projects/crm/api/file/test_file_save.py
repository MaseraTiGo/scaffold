# coding=UTF-8

import os
import json

from support.common.testcase.api_test_case import APITestCase

class RegisterUpload(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_upload_file(self):
        cur_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(cur_path, 'test-01.png')
        files = {'test-01.png': open(file_path, 'rb')}
        api = "file.upload"
        result = self.access_file_api(api, files = files, role = "crm", store_type = "test")
