# coding=UTF-8


class DurationTypes(object):
    ONE_YEAR = 'one_year'
    ONE_HALF_YEAR = 'one_half_year'
    TWO_YEAR = 'two_year'
    TWO_HALF_YEAR = 'two_half_year'
    FIVE_YEAR = 'five_year'
    OTHER = 'other'
    CHOICES = ((ONE_YEAR, '1年'), (ONE_HALF_YEAR, '1.5年'),
               (TWO_YEAR, '2年'), (TWO_HALF_YEAR, '2.5年'),
                (FIVE_YEAR, '5年'), (OTHER, '其它'))


class CategoryTypes(object):
    UNDERGRADUATE = 'undergraduate'
    SPECIALTY = 'specialty'
    HIGHCOST = 'highcost'
    GRADUATE = 'graduate'
    QUALIFICATION = 'qualification'
    OTHER = 'other'
    CHOICES = ((UNDERGRADUATE, '专升本'), (SPECIALTY, '高起专'),
               (HIGHCOST, '高起本'), (GRADUATE, '考研'),
               (QUALIFICATION, '资格证'),
               (OTHER, '其它'))
