#!/usr/bin/env python
# coding=utf-8

from BeautifulSoup import BeautifulSoup
import urllib2
import time 
import re
import db 

sql = db.MysqlHandler()
print sql.get_all_user_tel()
print type(sql.get_all_user_tel())
