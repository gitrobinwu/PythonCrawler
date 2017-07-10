#coding: utf-8 

import urllib
import urllib2
import re

page =1 
url = 'http://www.qiushibaike.com/hot/page/' + str(page)
user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'
headers = {'User-Agent':user_agent}
try:
	request = urllib2.Request(url,headers=headers)
	response = urllib2.urlopen(request)
	#服务器发送特定头headers 
	print response.info()
	# 返回请求的真是url 
	print response.geturl() 
	content = response.read().decode('utf-8')
	# 非贪婪模式，也就是最近查找 
	#1,作者名 年龄大小
	#2,内容
	#3, 好笑数 
	#4, 评论数
	pattern = re.compile(r'<div.*?author.*?>.*?<h2>(.*?)</h2>.*?<div.*?>(\d+)</div>.*?<div.*?content.*?>.*?<span>(.*?)</span>.*?<span.*?stats-vote.*?>.*?<i.*?number.*?>(\d+)</i>(.*?)</span>.*?(?:<a.*?qiushi_comments.*?>.*?<i.*?number.*?>(\d+)</i>(.*?)</a>)',re.S)
	items = re.findall(pattern,content)
	'''
		半块儿砖头 35
		大爷九十多了，我跟他聊天说：“大爷，你的发型有点像座山雕。我祝您长命百岁！”大爷瞪我一眼说：“啥妖？你给我一边去，100不够…我这岁数有头发我就知足了。”这心态活该你长寿，呵呵…
		346  好笑 13  评论

	'''
	for author in items:
		print '-'*50 
		print author[0],author[1]
		print author[2]
		print author[3],author[4],author[5],author[6]
		print '-'*50,'\n'
	
except urllib2.URLError,e:
	if hasattr(e,'code'):
		print e.code
	if hasattr(e,'reason'):
		print e.reason 

	
