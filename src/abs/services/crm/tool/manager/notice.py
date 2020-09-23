# coding=UTF-8


from abs.common.manager import BaseManager
from abs.services.crm.tool.store.notice import Notice
from infrastructure.utils.common.split_page import Splitor


class NoticeServer(BaseManager):

    @classmethod
    def search_all(cls, current_page, **search_info):
        """query 4 all notices, then split them"""
        if 'keywords' in search_info:
            keywords = search_info.pop('keywords')
            search_info.update({'content__contains': keywords})
        notice_qs = Notice.search(**search_info).order_by('-create_time')
        return Splitor(current_page, notice_qs)

    @classmethod
    def update(cls, notice_id, **update_info):
        """update notice info"""
        notice_obj = Notice.get_byid(notice_id)
        notice_obj.update(**update_info)
        return notice_obj

    @classmethod
    def delete(cls, notice_id):
        """delete notice by notice-id"""
        notice_obj = Notice.get_byid(notice_id)
        notice_obj.delete()
        return True

    @classmethod
    def add(cls, **notice_info):
        notice_obj = Notice.create(**notice_info)
        return notice_obj
