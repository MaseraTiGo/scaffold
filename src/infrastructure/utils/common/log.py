# coding=utf-8

import os
import logging
import logging.config

logging.config.fileConfig(os.path.join(os.path.dirname(__file__), "log.conf"))
log = logging.getLogger("infile")
log.info("="*40 + "microbrain start" + "="*40)