import scrapy
from Bili.items import BiliItem
import random
import time

class LycSpider(scrapy.Spider):
    name = 'lyc'
    allowed_domains = ['bilibili.com']
    start_urls = ['https://search.bilibili.com/all?keyword=大学课程&page=40']

    # 爬取的方法
    def parse(self, response):
        item = BiliItem()
        # 匹配
        for jobs_primary in response.xpath('//*[@id="all-list"]/div[1]/ul/li'):
            item['title'] = (jobs_primary.xpath('./a/@title').extract())[0]
            item['url'] = (jobs_primary.xpath('./a/@href').extract())[0]
            item['watchnum'] = (jobs_primary.xpath('./div/div[3]/span[1]/text()').extract())[0].replace("\n", "").replace(" ", "")
            item['dm'] = (jobs_primary.xpath('./div/div[3]/span[2]/text()').extract())[0].replace("\n", "").replace(" ", "")
            item['uptime'] = (jobs_primary.xpath('./div/div[3]/span[3]/text()').extract())[0].replace("\n", "").replace(" ", "")
            item['upname'] = (jobs_primary.xpath('./div/div[3]/span[4]/a/text()').extract())[0]


            # 不能使用return
            yield item

        # 获取当前页的链接
        url = response.request.url
        #page +1

        new_link = url[0:-1]+str(int(url[-1])+1)
        # 再次发送请求获取下一页数据
        yield scrapy.Request(new_link, callback=self.parse)
