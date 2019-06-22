# -*- coding: utf-8 -*-
__auth__ = 'zone'
__date__ = '2019/6/17 下午11:47'
'''
公众号：zone7
小程序：编程面试题库
'''

import logging

module_logger = logging.getLogger("zone7Model.sub.module")


class SubOfMain(object):
    def __init__(self):
        self.logger = logging.getLogger("zone7Model.sub.module")
        self.logger.info("init sub class")

    def print_some_log(self):
        self.logger.info("sub class log is printed")


def som_function():
    module_logger.info("call function some_function")
