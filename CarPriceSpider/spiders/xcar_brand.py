# -*- coding: utf-8 -*-
import scrapy
import time

class XcarSpider(scrapy.Spider):
    name = 'xcar_brand'
    allowed_domains = ['xcar.com.cn']
    start_urls = ['http://dealer.xcar.com.cn/']

    def parse(self, response):
        for b in response.xpath('//dd[@class="brands"]//a'):
            brand =  {
                'brandId':b.xpath('./@href').re(r'(\d*).htm')[0],
                'brandName': b.xpath('./text()').get(),
                'brandUrl':'http://dealer.xcar.com.cn{}'.format(b.xpath('./@href').get()),
                'crawlTime': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
            }
            print(brand)
            yield brand