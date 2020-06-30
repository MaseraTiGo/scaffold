# coding=UTF-8

'''
Created on 2016年8月22日

@author: Administrator
'''

# import python standard package
import os
import sys
import smtplib
import unittest
import importlib
import threading

# import thread package

# import my project package
import init_envt
from infrastructure.log.base import logger

join = os.path.join

base_dir = init_envt.BASE_DIR
api_test_dir = join(join(join(base_dir, 'support'), 'test'), 'projects')
start_file = join(base_dir, "manage.py")

account = '237818280@qq.com'
passwd = 'honpfnthtvbybigh'
title = '这是一个测试'
_to = ['237818280@qq.com']
_from = '237818280@qq.com'


def send_email(content):

    class EmailHelper(object):

        def __init__(self, account, passwd, title, content, _to, _from, host='smtp.qq.com', port=465):
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
            server = smtplib.SMTP_SSL(self.host, self.port)
#             server.set_debuglevel(1)
            server.login(self.account, self.passwd)
            server.sendmail(self._from, self._to, self._body.encode("utf-8"))
            server.quit()
            return True

    return EmailHelper(account, passwd, title, content, _to, _from)()


def load():
    module_names = []
    for root, dirs, files in os.walk(api_test_dir):
        for file in files:
            if file.startswith("test_") and file.endswith(".py"):
                file_path = os.path.join(root, file)
                file_path = os.path.splitext(file_path)[0]
                module_name = file_path.replace(base_dir, "").replace(os.sep, '.')[1:]
                module_names.append(module_name)

#     module_names = module_names[-1:]
    modules = map(importlib.import_module, module_names)
    load = unittest.defaultTestLoader.loadTestsFromModule
    return unittest.TestSuite(map(load, modules))


class AutoTest(object):

    def _config(self):
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_settings")

    def _sync_db_struct(self):
        from django.core.management import execute_from_command_line
        argv = [start_file, 'migrate']
        execute_from_command_line(argv)

    def _runserver(self):
        from test_settings import TEST_PORT
        from django.core.management import execute_from_command_line
        argv = [start_file, 'runserver', '0.0.0.0:{}'.format(TEST_PORT), '--noreload']
        execute_from_command_line(argv)

    def _start_server(self):
        thread = threading.Thread(target=self._runserver)
        thread.setDaemon(True)
        thread.start()
        import time
        time.sleep(3)

    def _generate_result(self, program):
        failures = program.result.failures
        errors = program.result.errors
        total = program.result.testsRun

        result = ["自动化脚本检测错误报告: 总运行数= {total}, 失败数量={fail}, 脚本出错数量={error}"\
                  .format(total=total, fail=len(failures), error=len(errors))]
        split_line = '-' * 40
        if program.result.failures:
            failures_list = ["/ ========================= api failures  ========================= \ "]
            failures_list.append(('\n\n{line}\n\n'.format(line=split_line)).join([fail[1] for fail in failures]))
            failures_list.append("\ =========================  end failures  ========================= / ")
            result.extend(failures_list)

        result.append("")
        if errors:
            error_list = ["/ =========================  test code error  ========================= \ "]
            error_list.append(('\n\n{line}\n\n'.format(line=split_line)).join([error[1] for error in errors]))
            error_list.append("\ =========================  end error  ========================= / ")
            result.extend(error_list)

        return '\n'.join(result)

    def _execute_ddl_sql(self, sql):
        import pymysql
        from test_settings import DATABASES
        default_db = DATABASES['test']
        conn = pymysql.connect(host=default_db['HOST'], port=int(default_db['PORT']), user=default_db['USER'], passwd=default_db['PASSWORD'])
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
        except Exception as e:
            print('------>>>>>>>>    ', e)
        cursor.close()

    def _create_testdb(self):
        from test_settings import DATABASES
        self._delete_testdb()
        default_db = DATABASES['test']
        self._execute_ddl_sql("CREATE DATABASE {db_name} DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;"\
                             .format(db_name=default_db['NAME']))

    def _delete_testdb(self):
        from test_settings import DATABASES
        default_db = DATABASES['test']
        self._execute_ddl_sql("DROP DATABASE IF EXISTS {db_name};".format(db_name=default_db['NAME']))

    def _init_data(self):
        import init_manager
        init_manager.InitManager().run()

    def run(self):
        logger.info('-------------- auto test start --------------')
        logger.info('create test database...')
        self._create_testdb()
        logger.info('change to start server of config file...')
        self._config()
        logger.info('sync table struct...')
        self._sync_db_struct()
        logger.info('init server data...')
        self._init_data()
        logger.info('start server...')
        self._start_server()
        logger.info('excute test case...')
        program = unittest.TestProgram(defaultTest="load", exit=False)
        logger.info('get test result...')
        result = self._generate_result(program)
        if result:
            logger.info('send email...')
            send_email(result)
        logger.info('delete database...')
        self._delete_testdb()
        logger.info('-------------- auto test end --------------')
        return result


if __name__ == "__main__":
    AutoTest().run()
