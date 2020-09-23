# coding=UTF-8

class FeedType(object):

    FUNCTION_ERROR = "function_error"
    OPTIMIZATION_PROPOSAL = "optimization_proposal"
    COMPLAINT_PROPOSAL = "complaint_proposal"
    OTHER = "other"

    CHOICES = (
        (FUNCTION_ERROR, "功能异常"),
        (OPTIMIZATION_PROPOSAL, "优化建议"),
        (COMPLAINT_PROPOSAL, "投诉建议"),
        (OTHER, "其它反馈")
    )


class FeedStatus(object):

    WAIT_SOLVE = "wait_solve"
    RESOLVED = "resolved"
    CLOSED = "closed"

    CHOICES = (
        (WAIT_SOLVE, "待解决"),
        (RESOLVED, "已解决"),
        (CLOSED, "已关闭"),
    )


class MessageStatus(object):
    READ = 'read'
    UNREAD = 'unread'
    CHOICES = ((READ, "已读"), (UNREAD, "未读"))

