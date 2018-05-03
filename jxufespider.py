# -*- coding: utf-8 -*-
import scrapy
import os
import re

class jxufespider(scrapy.Spider):
    name = "jxufespider"
    allowed_domains = ["movie.douban.com"]
    start_urls = (
        'https://movie.douban.com/subject/1291546/reviews?start=0',
    )

    save_path='..\\doubanAssess\\' #create director for downloaded pages
    if not os.path.exists(save_path):
        os.system('md '+save_path)
    urls = {} # save the urls of downloaded pages
    def parse(self, response):
	#	if 'start' not in response.url:
		filename = self.save_path + re.sub('https:|\/|\?','',response.url) #write downloaded pages
		with open(filename, 'wb') as f:
			f.write(response.body)
				
		title = response.xpath('//title/text()').extract()
		print ' '.join(title)
		
	# based on the observation of webpages
	#suppose all interest urls are in the path /ul/li,such as
	# <ul>
	# <li class="first"><a href="http://business.sohu.com" target="_blank">财经</a></li>
		nextLink = response.xpath('//span[@class="next"]/a/@href')
		for sel in response.xpath('//div[@class="main-bd"]/h2/a/@href')+nextLink:
			url=sel.extract()
			if 'start' in url:
				url= 'https://movie.douban.com/subject/1291546/reviews'+url
		#	links = sel.xpath('h2/a/@href').extract()
		#	for url in links:
		#	for url in sel:
			if url not in self.urls:
				self.urls[url]=''
				print url
				yield scrapy.Request(url, callback=self.parse) #根据获取的URL，再次抓取
						
