# -*- coding: utf-8 -*-
__auth__ = 'zone'
__date__ = '2019/6/16 下午3:23'
'''
公众号：zone7
小程序：编程面试题库
'''


import yaml
import logging.config
import os


def set_log_cfg(default_path="log_cfg.yaml", default_level=logging.INFO, env_key="LOG_CFG"):
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, "r") as f:
            config = yaml.load(f)
            logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


def record_some_thing():
    logging.info("Log level info")
    logging.debug("Log level debug")
    logging.warning("Log level warning")


if __name__ == "__main__":
    set_log_cfg(default_path="log_cfg.yaml")
    record_some_thing()
