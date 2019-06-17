# -*- coding: utf-8 -*-
__auth__ = 'zone'
__date__ = '2019/6/17 下午11:15'
'''
公众号：zone7
小程序：编程面试题库
'''
# 写入文件
import logging

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler("info.log")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.info("Log level info")
logger.debug("Log level debug")
logger.warning("Log level warning")


# 写入文件，同时输出到屏幕

import logging
logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)
handler = logging.FileHandler("info.log")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

console = logging.StreamHandler()
console.setLevel(logging.INFO)

logger.addHandler(handler)
logger.addHandler(console)

logger.info("Log level info")
logger.debug("Log level debug")
logger.warning("Log level warning")