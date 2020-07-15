# coding=UTF-8

import random

from abs.middleground.business.enterprise.models import Enterprise


class EnterpriseServer(object):

    @classmethod
    def create(cls, **enterprise_infos):
        enterprise = Enterprise.create(**enterprise_infos)
        return enterprise

    @classmethod
    def get(cls, enterprise_id):
        enterprise = Enterprise.get_byid(enterprise_id)
        return enterprise

    @classmethod
    def search(cls, current_page, **search_info):
        enterprise_qs = Enterprise.search(**search_info)
        return enterprise_qs

    @classmethod
    def update(cls, enterprise_id, **enterprise_infos):
        enterprise = cls.get(enterprise_id)
        enterprise.update(**enterprise_infos)
        return enterprise
