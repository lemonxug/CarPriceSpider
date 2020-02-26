# -*- coding: utf-8 -*-
import scrapy
import json
import time


class AutohomeSpider(scrapy.Spider):
    name = 'autohome_area'
    allowed_domains = ['autohome.com']
    start_urls = ['https://www.autohome.com.cn/yancheng/#pvareaid=2113623'] # 查询起亚各地区经销商数量

    def parse(self, response):
        s =  response.xpath('//script/text()').re(r'areaJson = (.*), allAreaJson')[0]
        area = json.loads(s)
        for p in area:
            for c in p['City']:
                city = {
                    'Province': p['Name'],
                    'ProvinceId': p['Id'],
                    'ProvincePinyin': p['Pinyin'],
                    'City': c['Name'],
                    'CityId': c['Id'],
                    'CityPinyin': c['Pinyin'],
                    'OldCityId': c['OldCityId'],
                    'crawlTime':time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

                }
                # print(city)
                yield city
