# coding=UTF-8

'''
Created on 2016年8月22日

@author: Administrator
'''

import init_envt
from infrastructure.log.base import logger
from support.auto_test import AutoTest


class ResetDatabase(AutoTest):

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
    ResetDatabase().run()
