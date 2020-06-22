# coding=UTF-8

import json
import urllib.request
from pyquery import PyQuery as pq
from selenium import webdriver
from infrastructure.utils.common.dictwrapper import DictWrapper
from model.store.model_role import SourceType
from abs.service.task.crawler.base import BaseCrawler


class QCC(BaseCrawler):
    _root_path = 'http://www.qichacha.com'

    @property
    def browser(self):
        if not hasattr("_browser"):
            self._browser = webdriver.Chrome()
        return self._browser

    def login(self):
        browser = self.browser
        url = "{}{}".format(self._root_path, '/user_login')
        browser.get(url)

        account_element = browser.find_element_by_id('nameNormal')
        account_element.send_keys("15527703115")

        password_element = browser.find_element_by_id('pwdNormal')
        password_element.send_keys("yangrongkai123")

        self._login_verify(browser)

        password_element = browser.find_element_by_id('pwdNormal')
        return 

    def get_name(self):
        return "企查查爬虫任务"

    def generate_tasks(self, task_group):
        self.login()
        return []
        print(" ======  count ({})   ========".format(len(shop_parms_list)))
        task_list = self.store_tasks(task_group, shop_parms_list)
        return task_list

    def execute_task(self, group, task):
        exec_parms = DictWrapper(json.loads(task.exec_parms))
        organization, operator = self.get_shop_infos(exec_parms)
        if organization and operator:
            organization = self.create_customer_infos(organization, operator)
            return organization
        return None
