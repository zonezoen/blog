# -*- coding: utf-8 -*-
__auth__ = 'zone'
__date__ = '2019/6/17 下午11:47'
'''
公众号：zone7
小程序：编程面试题库
'''

import logging

module_logger = logging.getLogger("mainModule.sub")


class SubModuleClass(object):
    def __init__(self):
        self.logger = logging.getLogger("mainModule.sub.module")
        self.logger.info("creating an instance in SubModuleClass")

    def doSomething(self):
        self.logger.info("do something in SubModule")
        a = []
        a.append(1)
        self.logger.debug("list a = " + str(a))
        self.logger.info("finish something in SubModuleClass")


def som_function():
    module_logger.info("call function some_function")
