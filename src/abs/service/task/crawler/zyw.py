# coding=UTF-8

import json
import urllib.request
from pyquery import PyQuery as pq
from infrastructure.utils.common.dictwrapper import DictWrapper
from model.store.model_role import SourceType
from abs.service.task.crawler.base import BaseCrawler


class ZYW(BaseCrawler):
    _root_path = 'http://www.zxdyw.com'
    _domain_mapping = None

    def get_domains(self):
        mapping = {}
        url = '{}{}'.format(self._root_path, '/csfz/')
        p = pq(url=url)
        level_list = p('#cl1 dl')
        for level_obj in level_list.items():
            span_list = level_obj.find('span')
            cat = span_list.eq(0).find('strong').text()
            ct_main = span_list.eq(1)
            dd_list = ct_main.find('dd').not_('.citymore')
            for dd_obj in dd_list.items():
                a_obj = dd_obj.find('a').eq(0)
                domain = a_obj.attr('href')
                city = a_obj.text()
                mapping[domain] = '{}-{}'.format(cat, city)

            more_list = ct_main.find('em dd a')
            for a_obj in more_list.items():
                domain = a_obj.attr('href')
                city = a_obj.text()
                mapping[domain] = '{}-{}'.format(cat, city)

        return mapping

    def get_shop_infos(self, shop_infos):
        page = pq(url=shop_infos.url, opener=lambda link, **kw:
                       urllib.request.urlopen(link).read().decode("utf-8"))
        infor_board = page.find('.s_major')
        if infor_board:
            phone, name = infor_board.find('.s_tel').text().split(' ')
            address = infor_board.find('.s_add span').text()
            organization = DictWrapper({
                'name': shop_infos.name,
                'site': shop_infos.url,
                'city': shop_infos.city,
                'industry': '装修',
                'source': SourceType.ZYW,
                'address': address,
            })
            operator = DictWrapper({
                'name': name,
                'phone': phone,
            })
            return organization, operator
        else:
            print("error : {}".format(shop_infos))
            return None, None

    def get_next_shop_url(self, domain_info):
        hot_len = domain_info.find('span.ico_hot').size()
        new_len = domain_info.find('span.ico_new').size()
        all_len = domain_info.find('.m_main ul li').size()
        if all_len == (hot_len + new_len):
            paginator_obj = domain_info.find('.paginator')
            a_obj = paginator_obj.find('a').eq(-2)
            url = a_obj.attr('href')
            return url
        return None

    def get_shop_tasks(self, addr, domain_info):
        def _get_shop_task(ele_list):
            shop_tasks = []
            for ele_obj in ele_list:
                shop_info = ele_obj.parents('li:first').find('span.l_txt')
                a_obj = shop_info.find('.li_tle b a')
                shop_name = a_obj.text()
                shop_url = a_obj.attr('href')
                if shop_name and shop_url:
                    shop_tasks.append(DictWrapper({
                        'url': shop_url,
                        'city': addr,
                        'name': shop_name
                    }))
            return shop_tasks

        shop_tasks = []
        hot_list = domain_info.find('span.ico_hot').items()
        if hot_list:
            shop_tasks.extend(_get_shop_task(hot_list))

        new_list = domain_info.find('span.ico_new').items()
        if new_list:
            shop_tasks.extend(_get_shop_task(new_list))
        return shop_tasks

    def get_shop_urls(self, domain_mapping):
        all_tasks = []
        # domain_mapping = {"http://wh.zxdyw.com/": "湖北-武汉"}
        for root_url, addr in domain_mapping.items():
            url = "{}{}".format(root_url, '/zsgs/')
            domain_info = pq(url=url)
            shop_tasks = self.get_shop_tasks(addr, domain_info)
            all_tasks.extend(shop_tasks)
            next_url = self.get_next_shop_url(domain_info)

            while next_url is not None:
                url = "{}{}".format(root_url, next_url)
                next_domain_info = pq(url=url)
                shop_tasks = self.get_shop_tasks(addr, next_domain_info)
                all_tasks.extend(shop_tasks)
                next_url = self.get_next_shop_url(next_domain_info)

        return all_tasks

    def get_name(self):
        return "装一网爬虫任务"

    def generate_tasks(self, task_group):
        self._domain_mapping = self.get_domains()
        shop_parms_list = self.get_shop_urls(self._domain_mapping)
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
