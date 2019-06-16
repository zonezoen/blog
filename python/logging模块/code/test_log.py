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


#
# import logging
#
# logger = logging.getLogger(__name__)
# logger.setLevel(level=logging.INFO)
# handler = logging.FileHandler("log.txt")
# handler.setLevel(logging.INFO)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)
# logger.addHandler(handler)
#
# logger.info("Log level info")
# logger.debug("Log level debug")
# logger.warning("Log level warning")



# import json
# import logging.config
# import os
#
#
# def setup_logging(default_path="log_cfg.json", default_level=logging.INFO, env_key="LOG_CFG"):
#     path = default_path
#     value = os.getenv(env_key, None)
#     if value:
#         path = value
#     if os.path.exists(path):
#         with open(path, "r") as f:
#             config = json.load(f)
#             logging.config.dictConfig(config)
#     else:
#         logging.basicConfig(level=default_level)
#
#
# def func():
#     logging.info("start func")
#
#     logging.info("exec func")
#
#     logging.info("end func")
#
#
# if __name__ == "__main__":
#     setup_logging(default_path="log_cfg.json")
#     func()



import yaml
import logging.config
import os

def setup_logging(default_path = "logging.yaml",default_level = logging.INFO,env_key = "LOG_CFG"):
    path = default_path
    value = os.getenv(env_key,None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path,"r") as f:
            config = yaml.load(f)
            logging.config.dictConfig(config)
    else:
        logging.basicConfig(level = default_level)

def func():
    logging.info("start func")

    logging.info("exec func")

    logging.info("end func")

if __name__ == "__main__":
    setup_logging(default_path = "log_cfg.yaml")
    func()