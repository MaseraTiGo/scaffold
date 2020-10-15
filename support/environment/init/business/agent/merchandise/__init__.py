# coding=UTF-8

from src.abs.services.agent.contract.utils.constant import TemplateStatus
from support.common.maker import BaseLoader


class MerchandiseLoader(BaseLoader):

    def generate(self):
        return [
            {
                'title': '人生巅峰',
                'slideshow': '["http://orgdeer.oss-cn-hangzhou.aliyuncs.com/source/goods/20200825144740.jpeg"]',
                'video_display': '-',
                'market_price': 88888888,
                'description': '有了高起专， 下得火海上得山。',
                'detail': '["http://orgdeer.oss-cn-hangzhou.aliyuncs.com/source/goods/20200825144740.jpeg"]',
                'pay_types': '',
                'pay_services': '',
                'despatch_type': 'eduction_contract',
                'remark': '自从上了高起专， 吃饭也有劲了，走路也利索了， 一口气下一楼， 不费劲',
            },
            {
                'title': '巅峰人生',
                'slideshow': '["http://orgdeer.oss-cn-hangzhou.aliyuncs.com/source/goods/20200825144740.jpeg"]',
                'video_display': '-',
                'market_price': 666666,
                'description': '有了学历敲门砖，从此不把他人酸',
                'detail': '["http://orgdeer.oss-cn-hangzhou.aliyuncs.com/source/goods/20200825144740.jpeg"]',
                'pay_types': '',
                'pay_services': '',
                'despatch_type': 'eduction_contract',
                'remark': ' 吃饭也有劲了，走路也利索了， 一口气下一楼， 不费劲',
            },
            {
                'title': '极乐世界',
                'slideshow': '["http://orgdeer.oss-cn-hangzhou.aliyuncs.com/source/goods/20200825144740.jpeg"]',
                'video_display': '-',
                'market_price': 7777777,
                'description': '天若有情天亦老，越早报名越是好。',
                'detail': '["http://orgdeer.oss-cn-hangzhou.aliyuncs.com/source/goods/20200825144740.jpeg"]',
                'pay_types': '',
                'pay_services': '',
                'despatch_type': 'eduction_contract',
                'remark': '吃饭也有劲了，走路也利索了， 一口气下一楼， 不费劲',
            }
        ]
