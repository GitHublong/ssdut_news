#!/usr/bin/env python
# coding=utf-8

from BeautifulSoup import BeautifulSoup
import urllib2
import time 
import db
import re
from PyWapFetion import *


SqlHandler = db.MysqlHandler()
# make a dict-list
def get_info(  ):
    url = 'http://ssdut.dlut.edu.cn/index.php/News/student.html'
    content = urllib2.urlopen(url).read()
    soup = BeautifulSoup( content , fromEncoding="utf-8" )
    paraText = soup.html.body.contents[5].contents[1].contents[5].contents[2]
    i = 0
    dict = {}
    list = []
    while i < 12 :
        dict['title']   = paraText.contents[i+3].a.contents[0]
        dict['time']    = paraText.contents[i+3].contents[5].contents[0]
        dict['source']  = paraText.contents[i+3].contents[7].contents[0].contents[0]
	dict['url']     = str( paraText.contents[i+3].a)[9:35]
	list.append(dict)
        dict = {}
        i += 1
    return list

def get_contents ( url ) :
    content_url = "http://ssdut.dlut.edu.cn"+url
    content = urllib2.urlopen(content_url).read()
    soup = BeautifulSoup( content , fromEncoding = "utf-8" )
    paraText = soup.html.body.contents[5].contents[1].contents[5].contents[2].contents[7].td
    str_content = str( paraText )
    
    repl_str = "<td class=\"content\">"
    str_content = re.sub(repl_str,'',str_content)
    
    repl_str = "<a href=\""
    str_content = re.sub(repl_str,'(表格请自行上网下载)',str_content)
    
    repl_str = "/Attachments/file/*\w*.\w*\""
    str_content = re.sub(repl_str,'',str_content)
    
    repl_str = "target=\"\w*\">/\w*/\w*/\w*.\w*</a>"
    str_content = re.sub( repl_str,'',str_content )

    repl_str = "<br />"
    str_content = re.sub(repl_str,'\n',str_content)
    
    repl_str = "&nbsp;"
    str_content = re.sub(repl_str,'',str_content)
    
    repl_str = "</td>" 
    str_content = re.sub(repl_str,'',str_content)
   
    repl_str = "<.*?>"
    str_content = re.sub( repl_str ,'',str_content ) 
    
    repl_str = "\s*\s"
    str_content = re.sub(repl_str , '\n' ,str_content )

    return  str_content
     

def release_news( news ):
    release_news = "网络组飞信端(消息以学院网为准):\n标题:"+news['title'] +" \n 时间:" + news['time'] + "\n 来源: "+ news['source'] + " \n 正文: " + news['content']
    myfetion = Fetion('xxxx','xxxx')
    
    try:
        myfetion.send2self( release_news )
    except Exception as e :
	pass
    try:
	user_info_list = SqlHandler.get_all_user_tel( )
    except Exception as e :
	myfetion.send2self("获取号码失败:"+str(e) )
    tel_list =[]
    
    for tel in user_info_list :
	#tel_list.append(tel['tel'])
        try:
    	    myfetion.send(tel['tel'] , release_news)
    	except Exception as e:
	    myfetion.send2self("发送消息失败:"+str(e) )

    myfetion.logout

#从数据库获取到上次最新的消息,返回title就行了

def BaseHandler(  ):
    new_list   = get_info()
    try :
    	old_new_title = str( SqlHandler.get_news()['title'] )
    except Exception :
	old_new_title = "" 
    flag = 0
    dict = {} 
    for news in new_list :
        if news['title'] != old_new_title :
	    news['content'] = get_contents( str(news['url']) ) 
            release_news( news )
            if flag == 0 :
                SqlHandler.save_news( news['title'] )
            flag += 1
	else :
	    break

def loop( ):
    while True :
        BaseHandler( )
        time.sleep(60)



if __name__ =="__main__" :
    loop( )
