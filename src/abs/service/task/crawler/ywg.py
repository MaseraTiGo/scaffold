# coding=UTF-8

import json
import hashlib
import urllib.request
from pyquery import PyQuery as pq
from infrastructure.utils.common.dictwrapper import DictWrapper
from model.store.model_task import TaskGroup, Task
from model.store.model_role import Organization, Operator, SourceType
from abs.service.task.crawler.base import BaseCrawler


class YWG(BaseCrawler):
    _root_path = 'http://www.yiwugou.com'

    def get_all_shop_category(self):
        category_list = []
        p = pq(url=self._root_path)
        level_list = p('.nav-class-bord ul li')
        for level_obj in level_list.items():
            addr_str = level_obj.find('.market-qukuai a').eq(0).text()
            layer_list = level_obj.find('.nav-erji-bord .louc')
            for layer_obj in layer_list.items():
                layer_str = layer_obj.find('h2').text()
                a_list = layer_obj.find('a')
                for a_obj in a_list.items():
                    link = self.generate_url(a_obj.attr('href')\
                             .strip().replace('product_list', 'shop_list'))
                    category_list.append((addr_str, layer_str, a_obj.text(), link))
                    print(addr_str, layer_str, a_obj.text(), link)
        return category_list

    def get_next_shop_pages(self, page):
        search_bar = page.find('.bord_list_page')
        next_page = search_bar.find('.page_next_yes')
        if next_page:
            return pq(url=self.generate_url(next_page.attr('href')))
        return None

    def get_shop_infos(self, shop_infos):
        url = shop_infos.url
        page = pq(url=url, opener=lambda link, **kw:
                       urllib.request.urlopen(link).read().decode("utf-8"))
        infor_board = page.find('.shop_introduce')
        if infor_board:
            shop = infor_board.find('.temp-company-v span').text().split(' ')[0]
            name = infor_board.find('.ico-shop-01').text()
            phone = infor_board.find('.ico-shop-02').text()
            tel = infor_board.find('.ico-shop-03').text()
            wx = infor_board.find('.ico-shop-05').text()
            title_list = infor_board.find('.c999').text().split(' ')
            content_list = infor_board.find('.con').text().split(' ')
            other = dict(zip(title_list, content_list))
            relative = infor_board.find('.jyhname').text()
            organization = DictWrapper({
                'name': shop,
                'site': url,
                'address': "{} {}".format(shop_infos.address, shop_infos.layer),
                'category': shop_infos.category,
                'city': "浙江-义务",
                'industry': '小商品',
                'source': SourceType.YWG,
                'other': json.dumps(other),
                'relative': relative,
            })
            operator = DictWrapper({
                'name': name,
                'phone': phone,
                'tel': tel,
                'wx': wx,
                'phone': phone,
            })
            return organization, operator
        else:
            raise Exception("error : {}".format(url))

    def get_shop_urls(self, page):
        shop_list = page.find('.pro_list_company_img')
        shop_url_list = []
        for shop in shop_list.items():
            a_obj = shop.find('p span a')
            url = self.generate_url(a_obj.attr('href'))
            shop_url_list.append(url)
            print('\t', url)
        return shop_url_list

    def get_name(self):
        return "义乌购爬虫任务"

    def generate_tasks(self, task_group):
        category_list = self.get_all_shop_category()
        task_list = []
        for addr, layer, category, first_page_url in category_list:
            category_page = pq(url=first_page_url)
            next_page = category_page
            while next_page is not None:
                shop_url_list = self.get_shop_urls(next_page)
                cur_task_list = self.store_tasks(task_group, addr, layer, category, shop_url_list)
                task_list.extend(cur_task_list)
                next_page = self.get_next_shop_pages(next_page)
        return task_list

    def execute_task(self, group, task):
        exec_parms = DictWrapper(json.loads(task.exec_parms))
        organization, operator = self.get_shop_infos(exec_parms)
        if organization and operator:
            organization = self.create_customer_infos(organization, operator)
            return organization
        return None
