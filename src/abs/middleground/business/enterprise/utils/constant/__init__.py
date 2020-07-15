# coding=UTF-8


class GenderTypes(object):
    MAN = "man"
    WOMAN = "woman"
    UNKNOWN = "unknown"
    CHOICES = ((MAN, '男士'), (WOMAN, "女士"), (UNKNOWN, "未知"))


class EducationTypes(object):
    PRIMARY = "primary"
    MIDDLE = "middle"
    HIGH = "high"
    UNDERGRADUAYE = "undergraduate"
    COLLEGE = "college"
    MIDDLECOLLEGE = "middlecollege"
    MASTER = "master"
    DOCTOR = "doctor"
    OTHER = "other"
    CHOICES = ((PRIMARY, '小学'), (MIDDLE, "初中"), (HIGH, "高中"),
               (UNDERGRADUAYE, "本科"), (COLLEGE, "大专"), (MIDDLECOLLEGE, "中专"),
               (MASTER, "硕士"), (DOCTOR, "博士"), (OTHER, "其他"))
