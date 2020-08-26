# coding=UTF-8
import os
import base64
import smtplib
import urllib.request
from settings import BASE_DIR
from abs.middleware.config import config_middleware


class EmailMiddleware(object):
    '''
    _sender = "orgdeer@cljykjhbwwgc.onexmail.com"
    _account = 'orgdeer@cljykjhbwwgc.onexmail.com'
    _passwd = 'zxcde321CL'
    _host = "smtp.exmail.qq.com"
    _port = 465
    '''

    def send_email(self, receivers, title, content = "", file_path = None):
        body_list = [
            'Content-Type: multipart/mixed; boundary= "===============email=="',
            'From: %s' % config_middleware.get_value("email", "sender"),
            'To: %s' % (';'.join(receivers)) + ";",
            'Subject: %s' % title,
            '',
            "--===============email==",
        ]
        if content:
            body_list.extend([
                'Content-Type:text/plain; charset="utf-8"',
                '',
                content,
                '',
                "--===============email==",
            ])
        if file_path:
            split_list = file_path.split("/")
            if len(split_list) > 0:
                file_name = split_list[-1]
                if "http" in file_path:
                    file = urllib.request.urlopen(file_path).read()
                else:
                    path = "{a}{b}".format(
                        a = BASE_DIR,
                        b = file_path
                    )
                    file = open(path, 'rb').read()
                body_list.extend([
                    'Content-Transfer-Encoding: base64',
                    'Content-Type:application/octet-stream',
                    'Content-Disposition:attachment; filename=%s' % file_name,
                    '',
                    base64.b64encode(file).decode('utf-8'),
                    '',
                    "--===============email==",
                ])
        body = '\r\n'.join(body_list)
        return self.send(receivers, body)


    def send(self, receivers, body):
        server = smtplib.SMTP_SSL(
            config_middleware.get_value("email", "host"),
            config_middleware.get_value("email", "port"),
        )
        server.login(
            config_middleware.get_value("email", "account"),
            config_middleware.get_value("email", "passwd"),
        )
        result = server.sendmail(
            config_middleware.get_value("email", "sender"),
            receivers,
            body.encode("utf-8")
        )
        server.quit()
        return True


email_middleware = EmailMiddleware()
