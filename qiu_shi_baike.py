#coding:utf-8 
import urllib
import urllib2
import re
import thread 
import time 

#OOP就是在类树种爬取属性
class QSBK(object):
	# 初始化一些基本状态信息
	def __init__(self):
		self.pageIndex = 1 
		user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'
		self.headers = {'User-Agent':user_agent}
		# 存放每一页的段子
		self.stories = []
		self.enable = False 
	
	# 根据页面链接获取某页数据	
	def getPage(self,pageIndex):
		'''
			pageIndex正在读取当前页数
		'''
		try:
			url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
			request = urllib2.Request(url,headers=self.headers)
			response = urllib2.urlopen(request)
			#print response.read()
			pageCode = response.read().decode('utf-8')
			return  pageCode
		except urllib2.URLError,e:
			if hasattr(e,'code'):
				print "The server couldn/'t fultill the request"
				print "Error code:",e.code
			if hasattr(e,'reason'):
				print 'We failed to reach a server.'
				print 'Error code:',e.reason 

	# 使用正则解析当前页面数据				
	def getPageItems(self,pageIndex):
		pageCode = self.getPage(pageIndex) 
		if not pageCode:
			print "页面正在加载....."
			return None 
		pattern = re.compile(r'<div.*?author.*?>.*?<h2>(.*?)</h2>.*?<div.*?>(\d+)</div>.*?<div.*?content.*?>.*?<span>(.*?)</span>.*?<span.*?stats-vote.*?>.*?<i.*?number.*?>(\d+)</i>(.*?)</span>.*?(?:<a.*?qiushi_comments.*?>.*?<i.*?number.*?>(\d+)</i>(.*?)</a>)',re.S)
		items = re.findall(pattern,pageCode)
		# 存储每页段子
		pageStories = [] 
		for item in items:
			#item[0] 作者 item[1] 年龄
			#item[2] 内容
			#item[3] 好笑数 item[4]:好笑 
			#item[5] 评论数 item[6]:评论
			text = re.sub(r'<br/>',r'\n',item[2])
			pageStories.append([item[0].strip(),item[1],text.strip(),item[3],item[4].strip(),item[5],item[6].strip()])
		return pageStories

	# 加载并提取页面的内容，加入到列表中	
	def	loadPage(self):
		#如果当前未看的页数少于2页，则加载新一页
		if self.enable == True:
			if len(self.stories) < 2:
				#获取新一页
				pageStories = self.getPageItems(self.pageIndex)
				if pageStories:
					self.stories.append(pageStories)
					# 获取完之后页码索引加1,表示下次读取下一页
					self.pageIndex +=1

	# 调用该方法，每次敲回车输出一个段子
	def getOneStory(self,pageStories,page):
		for story in pageStories:
			input = raw_input()
			self.loadPage()
			if input == "Q":
				self.enable = False 
				return 
			print '-'*50 
			print story[0],story[1]
			print story[2]
			print story[3],story[4],story[5],story[6]
			print '-'*50,'\n'
			
	def start(self):
		print  u"正在读取糗事百科,按回车查看新段子，Q退出"
		#使变量为True,程序可以正常运行
		self.enable = True 
		#先加载一页内容
		self.loadPage()
		#局部变量，控制当前读取到第几页
		nowPage = 0
		while self.enable:
			if len(self.stories)>0:
				pageStories = self.stories[0]
				nowPage += 1
				del self.stories[0]
				self.getOneStory(pageStories,nowPage)

spider = QSBK()
spider.start()

