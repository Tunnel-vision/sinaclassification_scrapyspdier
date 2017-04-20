# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json

class SinaspiderPipeline(object):
    def process_item(self, item, spider):
        sonUrls = item['sonUrls']
        #文件名为子链接ｕｒｌ中间部分，并将／替换为＿＇保存为．ｔｘｔ.格式
        filename = sonUrls[7:-6].replace('/','_')
        filename += '.txt'
        fp = codecs.open(item['subFilename']+'/'+filename,'w')
        fp.write(item['content'])
        fp.close()
        return item
