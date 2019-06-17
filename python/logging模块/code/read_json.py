# -*- coding: utf-8 -*-
__auth__ = 'zone'
__date__ = '2019/6/17 下午11:57'
'''
公众号：zone7
小程序：编程面试题库
'''

import json
import logging.config
import os


def set_log_cfg(default_path="log_cfg.json", default_level=logging.INFO, env_key="LOG_CFG"):
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, "r") as f:
            config = json.load(f)
            logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


def record_some_thing():
    logging.info("Log level info")
    logging.debug("Log level debug")
    logging.warning("Log level warning")


if __name__ == "__main__":
    set_log_cfg(default_path="log_cfg.json")
    record_some_thing()
