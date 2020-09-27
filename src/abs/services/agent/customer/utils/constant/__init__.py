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
    MIDDLE = 'middle'
    HIGH = 'hign'
    MIDDLECOLLEGE = 'middlecollege'
    COLLEGE = 'college'
    UNSERGRADUATE = 'undergraduate'
    MASTER = 'master'
    DOCTOR = 'doctor'
    OTHER = 'other'
    CHOICES = ((PRIMARY, '小学'), (MIDDLE, '初中'),
               (MIDDLECOLLEGE, "中专"), (COLLEGE, '大专'),
               (HIGH, '高中'), (UNSERGRADUATE, '本科'),
               (MASTER, '硕士'), (DOCTOR, '博士'),
               (OTHER, '其他'))


class IntentionTypes(object):
    NO = 'no'
    LOW = 'low'
    MIDDLE = 'middle'
    HIGH = 'high'
    UNKNOWN = 'unknown'
    CHOICES = ((NO, '无意向'), (LOW, '低意向'),
               (MIDDLE, '中意向'), (HIGH, '高意向'),
               (UNKNOWN, '未知'))


class MessageStatus(object):
    READ = 'read'
    UNREAD = 'unread'
    CHOICES = ((READ, "已读"), (UNREAD, "未读"))
