# coding=UTF-8

class TemplateStatus(object):

    DRAFT = "draft"
    WAIT = "wait"
    ADOPT = 'adopt'
    REFUSE = "refuse"

    CHOICES = (
        (DRAFT, "草稿"),
        (WAIT, "待审核"),
        (ADOPT, '通过'),
        (REFUSE, "拒绝"),
    )
