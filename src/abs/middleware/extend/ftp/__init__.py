# coding=UTF-8

from tuoen.settings import FTP_CONF
from tuoen.sys.utils.common.single import Single
from tuoen.abs.middleware.extend.ftp.helper import ftp_help


class FtpMiddleware(Single):

    def _get_ip(self):
        # return config_middleware.get_value("ftp", "ip")
        return FTP_CONF.get('host')

    def _get_port(self):
        # return int(config_middleware.get_value("ftp", "port"))
        return int(FTP_CONF.get('port'))

    def _get_username(self):
        # return config_middleware.get_value("ftp", "username")
        return FTP_CONF.get('user')

    def _get_password(self):
        # return config_middleware.get_value("ftp", "password")
        return FTP_CONF.get('pass')

    def prepare_ftp(self):
        ftp_help._init(self._get_ip(), self._get_port(), self._get_username(), self._get_password())

    def download_txt(self, txtpath, localfile):
        try:
            self.prepare_ftp()
            ftp_help.ftp_download(localfile, txtpath)
            return True
        except Exception as e:
            print("---->>>>>ee", e)
            return False

    def download_merchant_txt(self, name, localfile):
        txtpath = "meradd_{txt_name}.txt".format(txt_name = name)
        return self.download_txt(txtpath, localfile)

    def download_transaction_txt(self, name, localfile):
        txtpath = "trans_{txt_name}.txt".format(txt_name = name)
        return self.download_txt(txtpath, localfile)


ftp_middleware = FtpMiddleware()
