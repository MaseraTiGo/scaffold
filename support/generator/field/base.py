# coding=UTF-8

import random
import datetime
from infrastructure.utils.common.single import Single


class BaseHelper(Single):

    _count = 0

    def get_count(self):
        return self._count

    def calc(self, *args, **kwargs):
        raise NotImplementedError('Please imporlement this interface in subclass')

    def generate(self, *args, **kwargs):
        self._count += 1
        return self.calc(*args, **kwargs)


class BaseDateHelper(BaseHelper):

    def calc_attrs(self, is_direction = False, years = 0, days = 0):
        cur_time = datetime.date.today()

        cur_year = cur_time.year
        start, end = cur_year, cur_year
        if years:
            start, end = (cur_year, cur_year + years) \
                    if is_direction \
                        else (cur_year - years, cur_year)

        month = random.randint(1, 12)
        date = random.randint(1, 30) if month != 2 else \
                random.randint(1, 28)
        if days:
            delta = datetime.timedelta(days = random.randint(0, days))
            date_time = cur_time + delta if is_direction else cur_time - delta
            month = date_time.month
            date = date_time.day

        year = random.randint(start, end)
        return year, month, date

