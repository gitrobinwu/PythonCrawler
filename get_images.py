#-*- coding:utf-8 -*- 
# 下载图片

import urllib
import urllib2 
import re
import os 

class Image(object):
	def __init__(self):
		# 初始化要打开的页索引
		self.pageIndex = 1  
		self.nowpage = 0
		# 要进行下载的每个页面的链接 
		# 整个页面整个页面的下载
		self.images = []

	# 返回指定索引的页面html 	
	def get_page(self,pageIndex):
		try:
			url = 'http://tieba.baidu.com/p/2460150866'
			values = {'pn':pageIndex} 
			user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'
			headers = {'User-Agent':user_agent}

			data=urllib.urlencode(values)
			request = urllib2.Request(url,data,headers)
			response = urllib2.urlopen(request)
			
			pagecode = response.read().decode('utf-8')
			return pagecode 
		except urllib2.URLError,e:
			if hasattr(e,'code'):
				print "The server couldn/'t fultill the request"
				print "Error code:",e.code
			if hasattr(e,'reason'):
				print 'We failed to reach a server.'
				print 'Error code:',e.reason 
	
	# 返回指定索引页面的所有图片链接			
	def get_img_list(self,pageIndex):
		pagecode = self.get_page(pageIndex)
		if not pagecode:
			print "页面正在加载....."
			return None 
		
		pattern = re.compile(r'<img.*?src="(.*?\.jpg)" pic_ext')
		img_list = re.findall(pattern,pagecode)
		pageimages = img_list[:] 
		return pageimages
		
	# 设置下载图片集合
	def getimages(self):
		if self.enable and len(self.images) <2:
			# 获取当前页面图片链接
			pageimages = self.get_img_list(self.pageIndex)
			if pageimages:
				self.images.append(pageimages)
				# 更新页面索引(后向指针)
				self.pageIndex += 1

	def load_imgs(self,pageimages):
		#设置图片下载路径
		path = os.getcwd()+'/imgs'+'/%s' % str(self.nowpage)
		if not os.path.exists(path):
			os.makedirs(path)

		x = 0
		def report_hook(count,block_size,total_size):
			per = 100.0*count*block_size/total_size
			if per>100: per=100
			print '%.2f%%' % per 

		for imgurl in pageimages:
			urllib.urlretrieve(imgurl,path+'/%s.jpg' % str(x),report_hook)
			x +=1 
			
	# 控制下载图片流程
	def start(self):
		self.enable = True
		
		# 初始化图片下载库
		self.getimages()
		while self.enable:
			# 返回要当前要进行下载的页面
			pageimages = self.images.pop(0)
			self.nowpage +=1 
			print u'正在下载第%d页图片' % self.nowpage + '.'*6 
			# 下载图片
			self.load_imgs(pageimages)

			input = raw_input()
			self.getimages()
			if input == 'Q':
				self.enable = False 
				return  
			
			
img = Image()
img.start() 



