#!/usr/bin/env python
# coding=utf-8
import tornado.ioloop
import tornado.httpserver
import logging
from PyWapFetion import *
import os
import tornado.web
import db

user_info_list=[]

myfetion = Fetion('telnum' , 'pw')

class Add_User(tornado.web.RequestHandler ) :
    def get(self):
	if self.get_secure_cookie("name") == "network":
	    self.render("add_user.html")
	else :
	    self.redirect("/")

    def post( self):
	tel  = self.get_argument("tel").strip()
	new_user_id = "0" 
	try:
	    myfetion.addfriend(tel,'网络组飞信')
	except Exception as e:
	    myfetion.send2self("添加好友错误:"+ str(e) )
	try :
	    self.application.db.add_user( tel )
	except Exception as e:
	    myfetion.send2self("将数据插入数据库失败:"+str(e) )
	myfetion.logout()
	self.render("add_user.html")

class Login( tornado.web.RequestHandler ) :
    def get(self) :
	self.render("login.html")
    def post(self ):
	name = self.get_argument("name").strip()
	pw   = self.get_argument("pw").strip()
	if name == "network":
	    if pw == "network2013":
		try :
		    self.set_secure_cookie("name",name)
		    self.redirect("/add")
		except Exception as e:
		    print str(e)
	    else :
		self.render("login.html")
	else :
		self.render("login.html")


def get_user_info_list():
    return user_info_list
	
class Application ( tornado.web.Application ):
    def __init__(self):
	handlers = [
	    (r"/",Login ) ,
	    (r"/add" , Add_User) ,
	    (r"/login" , Login ) ,
        ]
        settings= dict(
            static_path   = os.path.join(os.path.dirname(__file__) , "statics" ) ,
            template_path = os.path.join(os.path.dirname(__file__) , "template") ,
            login_url     = "/",
	    cookie_secret = "sVgP3zdiS36r+rCKpS0IRtXaF1zgkEuliflY7hNcxKc=" ,
	)
	tornado.web.Application.__init__(self , handlers , **settings )
	self.db = db.MysqlHandler()

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(Application() )
    http_server.listen(12121)
    tornado.ioloop.IOLoop.instance().start()
