# coding=UTF-8

from ctypes import *
import os
import sys
import ftplib
import re

from tuoen.sys.utils.common.single import Single

class FtpHelper(Single):

    def _init(self, ip, port, username, pssword):
        self.ftp = ftplib.FTP()
        self.ftp.encoding = 'utf-8'  # 解决中文乱码问题
        self.ftp.connect(ip, port)
        # self.ftp.set_debuglevel(2)
        self.ftp.set_pasv(False)
        self.ftp.login(username, pssword)
        print("----------->>1", self.ftp.getwelcome())

    def ftp_download(self, LocalFile, RemoteFile, bufsize = 1024):
        print("==========LocalFile", LocalFile, RemoteFile)
        # 本地是否有此文件，来确认是否启用断点续传
        if not os.path.exists(LocalFile):
            with open(LocalFile, 'wb') as f:
                self.ftp.retrbinary('RETR %s' % RemoteFile, f.write, bufsize)
                f.close()
                # self.ftp.set_debuglevel(0)  # 关闭调试模式
                return True
        else:
            p = re.compile(r'\\', re.S)
            LocalFile = p.sub('/', LocalFile)
            localsize = os.path.getsize(LocalFile)
            with open(LocalFile, 'ab+') as f:
                self.ftp.retrbinary('RETR %s' % RemoteFile, f.write, bufsize, localsize)
                f.close()
                # self.ftp.set_debuglevel(0)  # 关闭调试模式
                return True


ftp_help = FtpHelper()
