# -*- coding: utf-8 -*-
__auth__ = 'zone'
__date__ = '2019/6/16 下午3:23'
'''
公众号：zone7
小程序：编程面试题库
'''

# import logging
# import sys
#
# try:
#     level_msg = sys.argv[1]
#     if level_msg == "--debug":
#         log_level = logging.DEBUG
#     else:
#         log_level = logging.INFO
# except Exception as e:
#     log_level = logging.DEBUG
# log_level = logging.DEBUG
#
#
# logging.basicConfig(level=log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)
#
# logger.info("Log level info")
# logger.debug("Log level debug")
# logger.warning("Log level warning")



import logging

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler("log.txt")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.info("Log level info")
logger.debug("Log level debug")
logger.warning("Log level warning")
