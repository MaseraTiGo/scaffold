# coding=UTF-8


class SourceTypes(object):
    CREATE = 'create'
    ASSIGN = 'assign'
    SYS = 'sys'
    OTHER = 'other'
    CHOICES = ((CREATE, '创建'), (ASSIGN, '分配'),
               (SYS, '系统分配'), (OTHER, '其他'))


class EducationTypes(object):
    PRIMARY = 'primary'
    SECONDARY = 'secondary'
    TECHNICALSECONDARY = 'technicalsecondary'
    HIGHSCHOOL = 'highschool'
    JUNIORCOLLEGE = 'juniorcollege'
    UNSERGRADUATE = 'undergraduate'
    MASTER = 'master'
    DOCTOR = 'doctor'
    OTHER = 'other'
    CHOICES = ((PRIMARY, '小学'), (SECONDARY, '初中'),
               (TECHNICALSECONDARY, "中专"), (JUNIORCOLLEGE, '大专'),
               (HIGHSCHOOL, '高中'), (UNSERGRADUATE, '本科'),
               (MASTER, '硕士'), (DOCTOR, '博士'),
               (OTHER, '其他'))