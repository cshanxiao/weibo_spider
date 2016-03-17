# -*- coding: utf8 -*-
u'''
@summary:
@author: Administrator
@date: 2015年9月3日
'''

import ConfigParser
cnf = ConfigParser.ConfigParser()
cnf.read("./config.ini")

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_PWD = None

MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_PWD = "root"

LOG_LEVEL = "DEBUG"
LOG_FORMAT = "%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s"
LOG_DATEFMT = "%Y-%m-%d %H:%M:%S"
LOG_FILENAME = None
LOG_FILEMODE = "W"

SPIDER_TIMEOUT = 30


# 读取配置文件里面参数
REDIS_HOST = cnf.get("redis", "host").strip()
REDIS_PORT = cnf.getint("redis", "port")
REDIS_PWD = cnf.get("redis", "pwd").strip()
if not REDIS_PWD:
    REDIS_PWD = None

MYSQL_HOST = cnf.get("mysql", "host").strip()
MYSQL_PORT = cnf.getint("mysql", "port")
MYSQL_USER = cnf.get("mysql", "user").strip()
MYSQL_PWD = cnf.get("mysql", "pwd").strip()

LOG_LEVEL = cnf.get("log", "level").strip()
LOG_FORMAT = cnf.get("log", "format", raw=True).strip()
LOG_DATEFMT = cnf.get("log", "datefmt", raw=True).strip()
LOG_FILENAME = cnf.get("log", "filename").strip()
if not LOG_FILENAME:
    LOG_FILENAME = None
LOG_FILEMODE = cnf.get("log", "filemode").strip()

SPIDER_TIMEOUT = cnf.getint("spider", "timeout")
SPIDER_NAME = cnf.get("spider", "name").strip()

ISO_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"








