# -*- coding: utf-8 -*-
import scrapy
import json
import time


class AutohomeSpider(scrapy.Spider):
    name = 'bitauto_area'
    allowed_domains = ['bitauto.com']
    start_urls = ['https://cmsapi.bitauto.com/city/getcity.ashx?callback=City_Select._$JSON_callback.$JSON&requesttype=json&bizCity=1']

    def parse(self, response):
        s =  response.text.split('$JSON(')[1][:-2]
        area = json.loads(s)
        for c in area:
            city = {
                'bizCity': c['bizCity'],
                'centerCityId': c['centerCityId'],
                'cityId': c['cityId'],
                'cityLevel': c['cityLevel'],
                'cityName': c['cityName'],
                'CityPinyin': c['cityPinYin'],
                'domain': c['domain'],
                'natureType': c['natureType'],
                'navCityId': c['navCityId'],
                'parentId': c['parentId'],
                'regionId': c['regionId'],
                'regionName': c['regionName'],
                'shortName': c['shortName'],
                'crawlTime':time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            }
            # print(city)
            yield city

# https://autocall.bitauto.com/eilv3/das2.ashx?userid=100105214,100029486,100043574,100039883,100042675,100082590,100043319,&mediaid=10&source=bitauto