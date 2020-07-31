# coding=UTF-8

from infrastructure.core.exception.business_error import BusinessError
from infrastructure.utils.common.split_page import Splitor

from abs.common.manager import BaseManager
from abs.middleground.business.merchandise.models import Merchandise, \
        Specification, SpecificationValue


class MerchandiseServer(BaseManager):

    @classmethod
    def _hung_specification_value(cls, specification_list):
        specification_mapping = {}
        for specification in specification_list:
            specification.specification_value_list = []
            specification_mapping.update({
                specification.id: specification
            })

        for specification_value in SpecificationValue.query().filter(
            specification__in=specification_mapping.values()
        ):
            specification = specification_mapping.get(
                specification_value.specification.id
            )
            specification.specification_value_list.append(
                specification_value
            )
        return specification_list

    @classmethod
    def _hung_specification(cls, merchandise_list):
        merchandise_mapping = {}
        for merchandise in merchandise_list:
            merchandise.specification_list = []
            merchandise_mapping.update({
                merchandise.id: merchandise
            })

        specification_list = []
        for specification in Specification.query().filter(
            merchandise__in=merchandise_mapping.values()
        ):
            merchandise = merchandise_mapping[specification.merchandise_id]
            merchandise.specification_list.append(
                specification
            )
            specification_list.append(specification)

        cls._hung_specification_value(specification_list)
        return merchandise_list

    @classmethod
    def hung_merchandise(cls, obj_list):
        merchandise_list = Merchandise.query().filter(
            id__in=[obj.merchandise_id for obj in obj_list]
        )
        mapping = {}
        for merchandise in merchandise_list:
            mapping.update({
                merchandise.id: merchandise
            })
        for obj in obj_list:
            merchandise = mapping.get(obj.merchandise_id)
            obj.merchandise = merchandise
        cls._hung_specification(merchandise_list)
        return obj_list

    @classmethod
    def search_id_list(cls, company_id, **search_info):
        if 'title' in search_info:
            title = search_info.pop('title')
            search_info.update({'title__contains': title})
        return list(Merchandise.query(
            company_id=company_id
        ).filter(
            **search_info
        ).values_list(
            'id',
            flat=True
        ))

    @classmethod
    def get(cls, merchandise_id):
        merchandise = Merchandise.get_byid(merchandise_id)
        if merchandise is None:
            raise BusinessError("商品不存在")
        cls._hung_specification([merchandise])
        return merchandise

    @classmethod
    def search(cls, current_page, company_id, **search_info):
        merchandise_qs = Merchandise.query(
            company_id=company_id
        ).filter(
            **search_info
        )
        spliter = Splitor(current_page, merchandise_qs)
        cls._hung_specification(spliter.get_list())
        return spliter

    @classmethod
    def search_all(cls, company_id, **search_info):
        merchandise_qs = Merchandise.query(
            company_id=company_id
        ).filter(
            **search_info
        )
        return merchandise_qs

    @classmethod
    def generate(
        cls,
        company_id,
        production_id,
        title,
        video_display,
        slideshow,
        detail,
        pay_types,
        pay_services,
        market_price,
        despatch_type,
        remark,
    ):
        merchandise = Merchandise.get_bytitle(
            company_id,
            title
        )
        if merchandise is not None:
            raise BusinessError("商品已存在，不能创建")

        merchandise = Merchandise.create(
            company_id=company_id,
            production_id=production_id,
            title=title,
            video_display=video_display,
            slideshow=slideshow,
            detail=detail,
            pay_types=pay_types,
            pay_services=pay_services,
            market_price=market_price,
            despatch_type=despatch_type,
            remark=remark,
        )
        return merchandise

    @classmethod
    def update(cls, merchandise_id, **update_info):
        merchandise = cls.get(merchandise_id)
        merchandise.update(
            **update_info
        )
        return merchandise

    @classmethod
    def remove(cls, merchandise_id):
        specification_qs = Specification.query(
            merchandise_id=merchandise_id
        )
        SpecificationValue.query(
            specification__in=list(specification_qs)
        ).delete()
        specification_qs.delete()
        Merchandise.query(
            id=merchandise_id
        ).delete()

    @classmethod
    def generate_specification(
        cls,
        merchandise_id,
        show_image,
        sale_price,
        stock,
        remark,
        attribute_list
    ):
        merchandise = cls.get(merchandise_id)
        specification = Specification.create(
            merchandise=merchandise,
            show_image=show_image,
            sale_price=sale_price,
            stock=stock,
            remark=remark
        )
        for attribute in attribute_list:
            SpecificationValue.create(
                category=attribute['category'],
                attribute=attribute['attribute'],
                specification=specification
            )
        return specification

    @classmethod
    def get_specification_list(cls, specification_id_list):
        specification_list = list(
            Specification.query().filter(
                id__in=specification_id_list
            )
        )
        cls._hung_specification_value(specification_list)
        return specification_list

    @classmethod
    def get_specification(cls, specification_id):
        specification = Specification.get_byid(
            specification_id
        )
        if specification is None:
            raise BusinessError("系统不存在该规格")
        cls._hung_specification_value([specification])
        return specification

    @classmethod
    def update_specification(
        cls,
        specification_id,
        show_image,
        sale_price,
        stock,
        remark
    ):
        specification = cls.get_specification(specification_id)
        specification.update(
            show_image=show_image,
            sale_price=sale_price,
            stock=stock,
            remark=remark
        )
        return True

    @classmethod
    def remove_specification(cls, specification_id):
        SpecificationValue.query(specification_id=specification_id).delete()
        Specification.query(id=specification_id).delete()
