# coding=UTF-8

'''
Created on 2016年8月23日

@author: Administrator
'''

# import python standard package

# import thread package

# import my project package

import smtplib

class EmailHelper(object):

    def __init__(self, account, passwd, title, content, _to, _from, host = 'smtp.qq.com', port = 465):
        self.account = account
        self.passwd = passwd
        self.host = host
        self._title = title
        self._content = content
        self._to = _to
        self._from = _from
        self.port = port

    @property
    def _body(self):
        return '\r\n'.join([
                                'From: %s' % self._from,
                                'To: %s' % (';'.join(self._to)) + ";",
#                                 'To: %s' % self._to,
                                'Subject: %s' % self._title,
                                "",
                                self._content
                            ])

    def __call__(self):
        server = smtplib.SMTP_SSL(self.host,self.port)
        server.set_debuglevel(1)
#         server.connect(self.host, self.port)
#         server.starttls()
        server.login(self.account, self.passwd)
        server.sendmail(self._from, self._to, self._body)
        server.quit()
        return True


if __name__ == "__main__":
    account = '237818280@qq.com'
    passwd = 'yrk654321'
    title = 'yangrongkai'
    content = 'test'
    _to = ['237818280@qq.com']
    _from = '237818280@qq.com'

    helper = EmailHelper(account, passwd, title, content, _to, _from)
    helper()
