# -*- coding: utf-8 -*-
import scrapy
import json
import time
import math

class BiautoDlrSpider(scrapy.Spider):
    name = 'bitauto_dlr'
    allowed_domains = ['bitauto.com', 'dealer.bitauto.com']
    start_urls = ['https://dealer.bitauto.com/nanjing/kia/?BizModes=0']

    def parse(self, response):
        for p in response.xpath('//div[@id="header-city-select"]//ul/li'):
            pro = {
                'provinceUrl':'https://dealer.bitauto.com{}'.format(p.xpath('./a/@href').get()),
                'provinceName':p.xpath('./a/text()').get(),
                'provinceCount':p.xpath('.//span/text()').get()[1:-1],
            }
            pages = math.ceil(int(pro['provinceCount'])/10) +1
            for page in range(1, pages):
                next_page = '{}&page={}'.format(pro['provinceUrl'], str(page))
                yield scrapy.Request(next_page, callback=self.parse_dlr, cb_kwargs=dict(pro=pro))

    def parse_dlr(self, response, pro):
        # https://dealer.bitauto.com/jiangsu/kia/?BizModes=0
        for dlr in response.xpath('//div[@class="row dealer-list"]'):
            d = {
                'province': pro['provinceName'],
                'city':dlr.xpath('.//div[@class="row"]//p[@class="add"]/text()').get().split(' ')[0],
                'district': dlr.xpath('.//div[@class="row"]//p[@class="add"]/text()').get().split(' ')[1],
                'dealerId':dlr.xpath('.//span[@class="tel400atr"]/@id').get(),
                'shortName':dlr.xpath('.//a[@target="_blank"]/text()').get(),
                'address':dlr.xpath('.//p[@class="add"]/span/text()').getall()[1],
                'dealerUrl':dlr.xpath('.//a[@target="_blank"]/@href').get(),
                'crawlUrl':response.url,
                'crawlTime':time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            }
            yield d
