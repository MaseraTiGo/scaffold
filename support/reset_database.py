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
start_file = join(base_dir, "manage.py")


class AutoTest(object):

    def _config(self):
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_settings")

    def _execute_ddl_sql(self, sql, database):
        import pymysql
        conn = pymysql.connect(
            host=database['HOST'],
            port=int(database['PORT']),
            user=database['USER'],
            passwd=database['PASSWORD']
        )
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
        except Exception as e:
            print('------>>>>>>>>    ', e)
        cursor.close()

    def _create_testdb(self):
        from test_settings import DATABASES
        self._delete_testdb()
        for _, database in DATABASES.items():
            db_name = database['NAME']
            sql = "CREATE DATABASE {db_name} DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;".format(db_name=database['NAME'])
            self._execute_ddl_sql(sql, database)

    def _delete_testdb(self):
        from test_settings import DATABASES
        for _, database in DATABASES.items():
            sql = "DROP DATABASE IF EXISTS {db_name};".format(
                db_name=database['NAME']
            )
            self._execute_ddl_sql(sql, database)

    def _sync_db_struct(self):
        from django.core.management import execute_from_command_line
        from test_settings import DATABASES
        for label, database in DATABASES.items():
            argv = [start_file, 'migrate', "--database={}".format(label)]
            execute_from_command_line(argv)

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


if __name__ == "__main__":
    AutoTest().run()
