# -*- coding: utf-8 -*-
import scrapy
import time
import json
from scrapy import Selector

class PcautoAreaSpider(scrapy.Spider):
    name = 'pcauto_area'
    allowed_domains = ['pcauto.com.cn']
    start_urls = ['https://www.pcauto.com.cn/global/1603/intf8771.js']

    def parse(self, response):
        doc = response.body.decode('gbk')
        sel = Selector(text=doc, type="html")
        s = sel.xpath('//text()').re('var areaData = (.*)')[0][:-1]
        area = json.loads(s)
        for p in area:
            for c in p['citys']:
                city = {
                    'Province': p['pro'],
                    'ProCode': p['proCode'],
                    'ProvinceId': p['proId'],
                    'City': c['name'],
                    'CityId': c['cityId'],
                    'CityPinyin': c['pinyin'],
                    'CityUrl':'https:{}'.format(c['siteUrl']),
                    'CityCode': c['cityCode'],
                    'crawlTime':time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                }
                # print(city)
                yield city