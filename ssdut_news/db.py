#!/usr/bin/env python
# coding=utf-8

import torndb
import sys
import logging 

reload(sys)
sys.setdefaultencoding('utf-8')

logging.basicConfig( filename = "db.log" ,filemode='a' , leval = logging.INFO)


class MysqlHandler( ) :
    def __init__( self ) :
        try : 
            self.db = torndb.Connection( 'localhost' , 'long_ssdut' , user='xxx' , password='xxx' )
        except Exception as e : 
            logging.INFO(e)

    def get_news( self ) :
        exe = "select * from news"
        return self.db.get(exe)

    def save_news( self , news ) :
        exe = "delete from news"
	news = str(news)
	print "save_news"
        self.db.execute_lastrowid(exe)
        exe = "insert into news values( %s )"
        self.db.execute_lastrowid(exe , news)
    
    def add_user( self , user_id ) :
	exe = "insert into user(tel) values(%s)"
	self.db.execute_lastrowid(exe , user_id)

    def get_all_user_tel(self ) :
	exe = "select * from user"
	return self.db.query(exe )
