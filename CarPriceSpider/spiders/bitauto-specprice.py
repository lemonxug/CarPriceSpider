# -*- coding: utf-8 -*-
import scrapy
import json
import time
import math

class AutohomeSpider(scrapy.Spider):
    name = 'bitauto_specprice'
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
            dlrid = dlr.xpath('.//span[@class="tel400atr"]/@id').get()
            next_page = 'https://dealer.bitauto.com/{}/cars.html'.format(dlrid)
            yield response.follow(next_page, callback=self.parse_series, cb_kwargs=dict(dlrid=dlrid))

    def parse_series(self, response, dlrid):
        for s in response.xpath('//dl[@class="brands end"]//dd/p'):
            seriesName = s.xpath('./a/@title').get()
            seriesUrl = s.xpath('./a/@href').get()
            seriesId = s.xpath('./a/@href').re(r'(\d*).html')[0]
            next_page = 'https://dealer.bitauto.com{}'.format(seriesUrl)
            yield response.follow(next_page,
                                  callback=self.parse_spec,
                                  cb_kwargs=dict(dlrid=dlrid, seriesName=seriesName, seriesId=seriesId))

    def parse_spec(self, response, dlrid, seriesName, seriesId):
        seriesImg = response.xpath('//a[@class="carpic"]/img/@src').get()
        dealerPriceRange = response.xpath('//div[@class="car_top"]//em[@class="imp"]/text()').get()
        factoryPriceRange = response.xpath('//div[@class="car_top"]//span[@class="c99"]/text()').get()[1:-1]
        groupName = ''
        for tr in response.xpath('//div[@class="car_price"]//tr'):
            if tr.xpath('./th[@class="fw"]/text()').get():
                groupName = tr.xpath('./th[@class="fw"]/text()').get().strip()
            else:
                specprice = {
                    'dealerId':dlrid,
                    'specId': tr.xpath('./td[1]/a/@href').re(r'(\d*).html')[0],
                    'specName': tr.xpath('./td[1]/a/@title').get(),
                    'specUrl': 'https://dealer.bitauto.com{}'.format(tr.xpath('./td[1]/a/@href').get()),
                    'factoryPriceRange': factoryPriceRange,
                    'dealerPriceRange': dealerPriceRange,
                    'groupName': groupName,
                    'seriesId': seriesId,
                    'seriesName':seriesName,
                    'seriesImg': seriesImg,
                    'factoryPrice':tr.xpath('./td[2]/text()').get().strip(),
                    'discount': tr.xpath('./td[3]/em/text()').get().strip(),
                    'dealerPrice':tr.xpath('./td[4]/a/text()').get().strip(),
                    'crawlUrl':response.url,
                    'crawlTime':time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                }
                # print(specprice)
                yield specprice
