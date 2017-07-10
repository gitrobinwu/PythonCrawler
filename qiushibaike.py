#coding: utf-8 

import urllib
import urllib2

page =1 
url = 'http://www.qiushibaike.com/hot/page/' + str(page)
user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'
headers = {'User-Agent':user_agent}
try:
	request = urllib2.Request(url,headers=headers)
	response = urllib2.urlopen(request)
	#服务器发送特定头headers 
	print response.info()
	print response.geturl() 
except urllib2.URLError,e:
	if hasattr(e,'code'):
		print e.code
	if hasattr(e,'reason'):
		print e.reason 

	
