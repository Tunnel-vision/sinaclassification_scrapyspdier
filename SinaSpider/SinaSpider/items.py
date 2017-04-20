# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class SinaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #大类的名称he url
    parentTitle = scrapy.Field()
    parentUrls = scrapy.Field()
    #小类的名称和url
    subTitle = scrapy.Field()
    subUrls = scrapy.Field()
    #小类的目录存储路径
    subFilename = scrapy.Field()
    #小类下的子链接
    sonUrls = scrapy.Field()
    #文章的标题和内容
    head = scrapy.Field()
    content = scrapy.Field()
