# coding=UTF-8

from infrastructure.core.exception.business_error import BusinessError
from infrastructure.utils.common.split_page import Splitor
from abs.common.manager import BaseManager
from abs.services.crm.adsense.models import *
from django.db.models import *


class AdvertisementServer(BaseManager):

    @classmethod
    def search(cls, current_page, **search_info):
        ad_qs = cls.search_all(**search_info).order_by(
            'space__name', 'sort'
        )
        return Splitor(current_page, ad_qs)

    @classmethod
    def search_all(cls, **search_info):
        if 'name' in search_info:
            name = search_info.pop('name')
            search_info.update({
                'name__contains': name
            })
        return Advertisement.search(**search_info)

    @classmethod
    def create(cls, **ad_info):
        return Advertisement.search(**ad_info)

    @classmethod
    def bulk_create(cls, space_list, **ad_info):
        ad_list = []
        for space in space_list:
            ad_list.append(Advertisement(
                unique_number=Advertisement.generate_unique_number(),
                space=space,
                **ad_info
            ))
        return Advertisement.objects.bulk_create(ad_list)

    @classmethod
    def get(cls, ad_id):
        ad = Advertisement.get_byid(ad_id)
        if ad:
            return ad
        raise BusinessError('广告不存在')

    @classmethod
    def hung_enable_num(cls, space_list):
        mapping = {}
        for space in space_list:
            space.enable_num = 0
            mapping.update({
                space.label: space
            })
        ad_list = Advertisement.search(
            space__label__in=mapping.keys()
        ).values(
            'space__label'
        ).annotate(
            enable_num=Count("*")
        )
        for ad in ad_list:
            space = mapping.get(ad['space__label'])
            space.enable_num = ad['enable_num']


class SpaceServer(BaseManager):

    @classmethod
    def search(cls, current_page, **search_info):
        space_qs = cls.search_all(**search_info)
        return Splitor(current_page, space_qs)

    @classmethod
    def search_all(cls, **search_info):
        if 'name' in search_info:
            name = search_info.pop('name')
            search_info.update({
                'name__contains': name
            })
        return Space.search(**search_info)

    @classmethod
    def create(cls, **search_info):
        return Space.create(**search_info)

    @classmethod
    def get(cls, space_id):
        space = Space.get_byid(space_id)
        if space:
            return space
        raise BusinessError('广告位不存在')

    @classmethod
    def get_bylabel(cls, label):
        return Space.search(
            label=label
        ).first()
