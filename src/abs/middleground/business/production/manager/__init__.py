# coding=UTF-8

from infrastructure.core.exception.business_error import BusinessError
from infrastructure.utils.common.split_page import Splitor

from abs.common.manager import BaseManager
from abs.middleground.business.production.models import Brand,Production


class ProductionServer(BaseManager):

    @classmethod
    def get(cls,production_id):
        production=Production.get_byid(production_id)
        if production is None:
            raise BusinessError("产品不存在")
        return production

    @classmethod
    def search(cls,current_page,company_id,**search_info):
        production_qs=Production.query(
            **search_info
        ).filter(
            company_id=company_id
        )
        splitor=Splitor(current_page,production_qs)
        return splitor

    @classmethod
    def generate(cls,company_id,brand_id,**production_info):
        brand=cls.get_brand(brand_id)
        production=Production.create(
            company_id=company_id,
            brand=brand,
            **production_info
        )
        return production

    @classmethod
    def update(cls,production_id,**production_info):
        production=cls.get(production_id)
        production.update(
            **production_info
        )
        return True

    @classmethod
    def delete(cls,product_id):
        product=cls.get(brand_id)
        # 未添加判断是否可删除的条件
        product.delete()
        return True

    @classmethod
    def generate_brand(cls,company_id,**brand_info):
        cls.is_brand_exsited(company_id,brand_info["name"])
        brand=Brand.create(
            company_id=company_id,
            **brand_info
        )
        return brand

    @classmethod
    def get_brand(cls,brand_id):
        brand=Brand.get_byid(
            brand_id,
        )
        return brand

    @classmethod
    def search_brand(cls,current_page,company_id,**search_info):
        brand_qs=Brand.query(
            **search_info
        ).filter(
            company_id=company_id
        ).order_by("-create_time")
        splitor=Splitor(current_page,brand_qs)
        return splitor

    @classmethod
    def update_brand(cls,brand_id,**brand_info):
        brand=cls.get_brand(brand_id)
        if brand is None:
            raise BusinessError("未知的品牌")
        cls.is_brand_exsited(brand.company_id,brand_info["name"],brand)
        brand.update(
            **brand_info
        )
        return brand

    @classmethod
    def is_brand_exsited(cls,company_id,name,brand=None):
        brand_qs=Brand.query(
            company_id=company_id,
            name=name
        )
        if brand is not None:
            brand_qs=brand_qs.exclude(id=brand.id)
        if brand_qs.count()>0:
            raise BusinessError("品牌名称重复")

    @classmethod
    def delete_brand(cls,brand_id):
        brand=cls.get_brand(brand_id)
        if brand is None:
            raise BusinessError("未知的品牌")
        product_qs=Production.query(
            brand=brand
        )
        if product_qs.count()>0:
            raise BusinessError("此品牌存在产品无法删除")
        brand.delete()
        return True
