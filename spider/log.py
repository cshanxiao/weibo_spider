# -*- coding: utf8 -*-
u'''
@summary: 日志模块
@author: Administrator
@date: 2015年9月3日
'''
import logging

from spider.global_cnf import LOG_LEVEL, LOG_FORMAT, LOG_DATEFMT, \
    LOG_FILENAME, LOG_FILEMODE

log_levels = {"NOTSET": logging.NOTSET,
              "DEBUG": logging.DEBUG,
              "INFO": logging.INFO,
              "WARNING": logging.WARNING,
              "ERROR": logging.ERROR,
              "CRITICAL": logging.CRITICAL
              }

logging.basicConfig(level=log_levels[LOG_LEVEL],
                    format=LOG_FORMAT,
                    datefmt=LOG_DATEFMT,
                    filename=LOG_FILENAME,
                    filemode=LOG_FILEMODE
                    )


