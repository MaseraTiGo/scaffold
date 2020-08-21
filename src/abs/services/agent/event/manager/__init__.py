# coding=UTF-8
import datetime

from infrastructure.core.exception.business_error import BusinessError
from infrastructure.utils.common.split_page import Splitor

from abs.common.manager import BaseManager

from abs.services.agent.event.models import TrackEvent, StaffOrderEvent


class TrackEventServer(BaseManager):

    @classmethod
    def create(cls, **info):
        track = TrackEvent.create(**info)
        return track

    @classmethod
    def search(cls, current_page, **search_info):
        track_qs = cls.search_all(**search_info).\
                   order_by("-create_time")
        splitor = Splitor(current_page, track_qs)
        return splitor

    @classmethod
    def search_all(cls, **search_info):
        track_qs = TrackEvent.search(**search_info)
        return track_qs


class StaffOrderEventServer(BaseManager):

    @classmethod
    def create(cls, **info):
        event = StaffOrderEvent.create(**info)
        return event
