# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class BiliItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #pass
    # 视频标题
    title = scrapy.Field()
    # 链接
    url = scrapy.Field()
    # 观看量
    watchnum = scrapy.Field()
    # 弹幕数
    dm = scrapy.Field()
    # 上传时间
    uptime = scrapy.Field()
    # 作者
    upname = scrapy.Field()
