# coding=UTF-8


class DurationTypes(object):
    ONE_YEAR = 'one_year'
    ONE_HALF_YEAR = 'one_half_year'
    TWO_YEAR = 'two_year'
    TWO_HALF_YEAR = 'two_half_year'
    OTHER = 'other'
    CHOICES = ((ONE_YEAR, '1年'), (ONE_HALF_YEAR, '1.5年'),
               (TWO_YEAR, '2年'), (TWO_HALF_YEAR, '2.5年'),
               (OTHER, '其它'))
