# coding=UTF-8

import os
from support.common.testcase.file_api_test_case import FileAPITestCase


class FileUpload(FileAPITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_upload_file(self):
        cur_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(cur_path, 'test-01.png')
        files = {'test-01.png': open(file_path, 'rb')}
        api = "file.upload"
        result = self.access_api(
            api,
            files=files,
            is_auth=False,
            role="crm",
            store_type="test"
        )
        self.assertTrue('file_paths' in result)
