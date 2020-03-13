    # -*- coding: utf-8 -*-
import scrapy
import json
import time


class AutohomeBrandSpider(scrapy.Spider):
    name = 'autohome_brand'
    allowed_domains = ['autohome.com', 'car.autohome.com.cn']
    start_urls = ['https://car.autohome.com.cn/AsLeftMenu/As_LeftListNew.ashx?typeId=1']

    def parse(self, response):
        for b in response.xpath('//li'):
            yield {
                'brandId': b.xpath('./@id').get()[1:],
                'brandName': b.xpath('.//a/text()').get(),
                'brandUrl': 'https://car.autohome.com.cn/{}'.format(b.xpath('.//a/@href').get()),
                'crawlTime': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            }

