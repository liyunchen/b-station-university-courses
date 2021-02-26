# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv

class BiliPipeline:

    def __init__(self):
        #打开文件，指定方式为写，利用第3个参数把csv写数据时产生的空行消除
        self.f = open("lyc大学课程.csv", "a", newline="")
        # 设置文件第一行的字段名，注意要跟spider传过来的字典key名称相同
        self.fieldnames = ["title", "url","watchnum","dm","uptime","upname"]
        # 指定文件的写入方式为csv字典写入，参数1为指定具体文件，参数2为指定字段名
        self.writer = csv.DictWriter(self.f, fieldnames=self.fieldnames)
        # 写入第一行字段名，因为只要写入一次，所以文件放在__init__里面
        self.writer.writeheader()

    def process_item(self, item, spider):
        # print("title:", item['title'][0])
        # print("url:", item['url'][0])
        # print("watchnum:", item['watchnum'][0].replace("\n","").replace(" ",""))
        # print("dm:", item['dm'][0].replace("\n", "").replace(" ", ""))
        # print("uptime:", item['uptime'][0].replace("\n", "").replace(" ", ""))
        # print("upname:", item['upname'][0])

        print("title:", item['title'])
        print("url:", item['url'])
        print("watchnum:", item['watchnum'])
        print("dm:", item['dm'])
        print("uptime:", item['uptime'])
        print("upname:", item['upname'])


        # 写入spider传过来的具体数值
        self.writer.writerow(item)
        # 写入完返回
        return item

    def close(self, spider):
        self.f.close()
