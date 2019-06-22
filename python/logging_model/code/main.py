# -*- coding: utf-8 -*-
__auth__ = 'zone'
__date__ = '2019/6/17 下午11:46'
'''
公众号：zone7
小程序：编程面试题库
'''
import os

print(os.getcwd())
import sys
import logging

sys.path.append(os.getcwd())
from python.logging_model.code import sub_of_main

logger = logging.getLogger("zone7Model")
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler("log.txt")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(formatter)

logger.addHandler(handler)
logger.addHandler(console)

sub = sub_of_main.SubOfMain()
logger.info("main module log")
sub.print_some_log()



