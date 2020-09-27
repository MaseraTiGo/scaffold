# coding=UTF-8

class ReviewStatus(object):
    WAIT_POST = 'wait_post'
    WAIT_REVIEW = 'wait_review'
    PASS = 'pass'
    REJECTION = 'rejection'
    CHOICES = ((WAIT_POST, "待提交"), (WAIT_REVIEW, "待审核"), (PASS, "审核通过"), (REJECTION, "审核拒绝"))
