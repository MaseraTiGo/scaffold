# coding=UTF-8

import time
import init_envt

from analysis.macroscopical import run
from abs.middleware.data import import_transaction_middleware,\
        import_rebate_middleware, import_register_middleware, \
        import_buyinfo_middleware

class TestPerformance(object):

    def run(self):
        """
        import_transaction_middleware.exec_transaction()
        run("import_transaction_middleware.exec_transaction()",
            "transaction_profile_{}".format(time.time()))
        """

        """
        import_rebate_middleware.exec_rebate()
        run("import_rebate_middleware.exec_rebate()",
            "rebate_profile_{}".format(time.time()))
        """

        """
        import_register_middleware.exec_register()
        run("import_register_middleware.exec_register()",
            "rebate_profile_{}".format(time.time()))
        """

        """
        import_buyinfo_middleware.exec_buyinfo()
        run("import_register_middleware.exec_register()",
            "rebate_profile_{}".format(time.time()))
        """

if __name__ == "__main__":
    TestPerformance().run()
