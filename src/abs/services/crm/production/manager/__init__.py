# coding=UTF-8

from infrastructure.core.exception.business_error import BusinessError
from infrastructure.utils.common.split_page import Splitor

from abs.common.manager import BaseManager
from abs.middleground.business.enterprise.manager import EnterpriseServer
from abs.middleground.business.production.manager import ProductionServer \
     as mg_ProductionServer


class ProductionServer(BaseManager):

    @classmethod
    def add(cls, brand_id, **add_info):
        company = EnterpriseServer.get_crm__company()
        production = mg_ProductionServer.generate(
            company_id = company.id,
            brand_id = brand_id,
            **add_info
        )
        return production

    @classmethod
    def get(cls, production_id):
        production = mg_ProductionServer.get(
            production_id
        )
        return production

    @classmethod
    def search(cls, current_page, **search_info):
        company = EnterpriseServer.get_crm__company()
        spliter = mg_ProductionServer.search(
            current_page,
            company.id,
            **search_info
        )
        return spliter

    @classmethod
    def search_all(cls, **search_info):
        company = EnterpriseServer.get_crm__company()
        production_qs = mg_ProductionServer.search_all(
            company_id = company.id,
            **search_info
        )
        return production_qs

    @classmethod
    def update(cls, production_id, **update_info):
        production = mg_ProductionServer.update(
            production_id,
            **update_info
        )
        return production


    @classmethod
    def hung_production(cls, obj_list):
        obj_list = mg_ProductionServer.hung_production(
           obj_list
        )
        return obj_list


class BrandServer(BaseManager):

    @classmethod
    def add(cls, **brand_info):
        company = EnterpriseServer.get_crm__company()
        brand = mg_ProductionServer.generate_brand(
            company_id = company.id,
            **brand_info
        )
        return brand

    @classmethod
    def get(cls, brand_id):
        brand = mg_ProductionServer.get_brand(
            brand_id
        )
        return brand

    @classmethod
    def search(cls, current_page, **search_info):
        company = EnterpriseServer.get_crm__company()
        spliter = mg_ProductionServer.search_brand(
            current_page,
            company.id,
            **search_info
        )
        return spliter

    @classmethod
    def search_all(cls, **search_info):
        company = EnterpriseServer.get_crm__company()
        production_qs = mg_ProductionServer.search_all_brand(
            company.id,
            **search_info
        )
        return production_qs

    @classmethod
    def update(cls, brand_id, **update_info):
        brand = mg_ProductionServer.update_brand(
            brand_id,
            **update_info
        )
        return brand

    @classmethod
    def remove(cls, brand_id):
        mg_ProductionServer.delete_brand(
            brand_id,
        )
        return True