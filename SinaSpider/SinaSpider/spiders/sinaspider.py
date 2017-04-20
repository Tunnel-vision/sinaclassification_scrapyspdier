# -*- coding: utf-8 -*-
import scrapy
import os
from SinaSpider.items import SinaItem
class SinaspiderSpider(scrapy.Spider):
    name = "sinaspider"
    allowed_domains = ["sina.com.cn"]
    start_urls = (
            'http://news.sina.com.cn/guide/',
             # "http://news.sina.com.cn/guide/"
    )

    def parse(self, response):
        items = []
        #网站的大标题,url
        parentTitle = response.xpath('//div[@class="clearfix"]/h3/a/text()').extract()
        parentUrls = response.xpath('//div[@class="clearfix"]/h3/a/@href').extract()
        #网站的子类url,标题
        subTitle = response.xpath('//div[@class="clearfix"]/ul/li/a/text()').extract()
        subUrls = response.xpath('//div[@class="clearfix"]/ul/li/a/@href').extract()
        for i in range(0,len(parentTitle)):
            parentFilename = "./Data/" + parentTitle[i]
            if (not os.path.exists(parentFilename)):
                os.makedirs(parentFilename)

            for j in range(0,len(subUrls)):
                item = SinaItem()
                #保存大类的ｔｉｔｌｅ和ｕｒｌｓ
                item['parentTitle'] = parentTitle[i]
                item['parentUrls'] = parentUrls[i]
                #检查小类的ｕｒｌ是否以同类的大类ｕｒｌ开头，是测返回ｔｒｕｅ
                if_belong = subUrls[j].startswith(item['parentUrls'])
                if(if_belong):
                    subFilename = parentFilename + '/' +subTitle[j]
                    if(not os.path.exists(subFilename)):
                        os.makedirs(subFilename)

                    #存储小类的ｕｒｌ和ｔｉｔｌｅ，和Ｆｉｌｅｎａｍｅ字段数据
                    item['subUrls'] = subUrls[j]
                    item['subTitle'] = subTitle[j]
                    item['subFilename'] = subFilename
                    items.append(item)
                #发送每个小类的子链接url的ｒｅｑｕｅｓｔ,的得到response对象
                for item in items:
                    yield scrapy.Request(url=item['subUrls'],meta={'meta_1':item},callback=self.second_parse)

    def second_parse(self,response):
        meta_1 = response.meta['meta_1']
        #取出小类里的所有的子链接
        sonUrls = response.xpath('//a/@href').extract()
        items = []
        for i in range(0,len(sonUrls)):
            if_belong = sonUrls[i].endswith('.shtml') and sonUrls[i].startswith(meta_1['parentUrls'])
            #如果属于本大类，获取字段值放在同一个ｉｔｅｍ里面便于传输
            if(if_belong):
                item = SinaItem()
                item['parentTitle'] = meta_1['parentTitle']
                item['parentUrls'] = meta_1['parentUrls']
                item['subUrls'] = meta_1['subUrls']
                item['subTitle'] = meta_1['subTitle']
                item['subFilename'] = meta_1['subFilename'] 
                item['sonUrls'] = sonUrls[i]
                items.append(item)
        for item in items:
            yield scrapy.Request(url=item['sonUrls'],meta={'meta_2':item},callback=self.detail_parse)

    def detail_parse(self,response):
        item = response.meta['meta_2']
        content = ""
        head = response.xpath('//h1[@id="main_title"]/text()')
        content_list = response.xpath('//div[@id="artibody"]/p/text()').extract()
        #将ｐ标签里的文本内容合并到一起
        for content_one in content_list:
            content += content_one
        item['head'] = head
        item['content'] =content
        yield item

        
