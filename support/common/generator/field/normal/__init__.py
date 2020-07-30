# coding=UTF-8

import random
import datetime
from infrastructure.utils.common.single import Single
from support.common.generator.field.base import BaseHelper, BaseDateHelper
from support.common.generator.field.data.address import ADDRES_TEMPLATES
from support.common.generator.field.data.name import NAME_LIST
from support.common.generator.field.data.school import SHOOL_LIST
from support.common.generator.field.data.major import MAJOR_LIST


class NameHelper(BaseHelper):

    def get_enume(self):
        return NAME_LIST

    def calc(self):
        return random.choice(self.get_enume())


class NumberHelper(BaseHelper):

    def calc(self):
        return "BQ" + str(self.get_count()).rjust(5, '0')


class ThirdPayIDHelper(BaseHelper):

    def calc(self):
        return "TPD" + str(self.get_count()).rjust(8, '0')


class GoodsNumberHelper(BaseHelper):

    def calc(self):
        return "SP" + str(self.get_count()).rjust(5, '0')


class OrderNumberHelper(BaseHelper):

    def calc(self):
        return "OR" + str(self.get_count()).rjust(8, '0')

class WorkNumberHelper(BaseHelper):

    def calc(self):
        return "WN" + str(self.get_count()).rjust(8, '0')


class PhoneHelper(BaseHelper):
    _count = 0

    def get_enume(self):
        return [134, 135, 136, 137, 138, 139, 150, 151, \
            152, 158, 159, 157, 182, 187, 188, 130, 131, \
                132, 155, 156, 185, 186, 133, 153, 180, 189]

    def calc(self):
        return str(random.choice(self.get_enume()) * 100000000 + self.get_count())


class QQHelper(BaseHelper):

    def calc(self):
        return str(random.randint(0, 1000) * 1000000 + random.randint(0, 1000000))


class AmountHelper(BaseHelper):

    def calc(self):
        return random.randint(1, 999999)


class DateHelper(BaseDateHelper):

    def calc(self, is_direction=False, years=0, days=0):
        year, month, date = self.calc_attrs(is_direction, years, days)
        fmt_time = datetime.date(
            year,
            month,
            date,
        )
        return fmt_time
        # return datetime.datetime.strftime(fmt_time, "%Y-%m-%d")


class DateTimeHelper(BaseDateHelper):

    def calc(self, is_direction=False, years=0, days=0):
        year, month, date = self.calc_attrs(is_direction, years, days)
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)

        fmt_time = datetime.datetime(
            year,
            month,
            date,
            hour,
            minute,
            second
        )
        return fmt_time
        # return datetime.datetime.strftime(fmt_time, "%Y-%m-%d %H:%M:%S")


class BankCardHelper(BaseHelper):

    def calc(self):
        bank_list = (
            ('中国工商银行', "ICBC"),
            ('中国邮政储蓄银行', "PSBC"),
            ('中国农业银行', "ABC"),
            ('中国银行', "BOC"),
            ('中国建设银行', "CCB"),
            ('中国交通银行', "COMM"),
            ('招商银行', "CMB"),
        )
        bank_name, bank_code = random.choice(bank_list)
        bank_number = str(random.randint(10000000, 99999999)) + str(random.randint(10000000, 99999999))
        return bank_name, bank_code, bank_number


class LogisticsCompanyHelper(BaseHelper):

    def calc(self):
        name = random.choice(['顺风', '圆通', '天天'])
        return name


class LogisticsNumberHelper(BaseHelper):

    def calc(self):
        return "SF" + str(random.randint(0, 9999999)).rjust(7, '0')


class EmailHelper(BaseHelper):

    def calc(self):
        return str(random.randint(100000, 99999999)) + "@" \
               + random.choice(["163", "qq", "google", "wangyi"]) + "."\
                    + random.choice(['cn', 'com'])


class ContractHelper(BaseHelper):

    def calc(self):
        return "BQ" + str(random.randint(0, 10000)).rjust(5, '0')


class IdentificationHelper(BaseHelper):

    def calc(self):
        return str(random.randint(100000, 999999)) \
                + str(random.randint(1950, 2018)) \
                    + str(random.randint(1, 12)).rjust(2, "0") \
                        + str(random.randint(1, 12)).rjust(2, "0") \
                            + str(self.get_count())[:4].rjust(4, '0')


class CityHelper(BaseHelper):

    def calc(self):
        if not hasattr(self, '_enume'):
            self._enume = list(set(['-'.join([data[0], data[1]]) for data in ADDRES_TEMPLATES]))
        return random.choice(self._enume)


class AddressHelper(BaseHelper):

    def calc(self):
        if not hasattr(self, '_enume'):
            self._enume = [ ('-'.join([data[0], data[1]]), data[3]) for data in ADDRES_TEMPLATES]
        return random.choice(self._enume)


class SchoolHelper(BaseHelper):

    def calc(self):
        school = random.choice(SHOOL_LIST)
        name = school[0]
        content = school[1]
        province = school[2]
        city = school[3]
        return name, content, province, city


class MajorHelper(BaseHelper):

    def calc(self):
        major = random.choice(MAJOR_LIST)
        name = major[0]
        content = major[1]
        return name, content

