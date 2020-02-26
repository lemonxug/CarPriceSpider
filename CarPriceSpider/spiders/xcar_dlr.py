# -*- coding: utf-8 -*-
import scrapy
import time

class XcarSpider(scrapy.Spider):
    name = 'xcar_dlr'
    allowed_domains = ['xcar.com.cn', 'dealer.xcar.com.cn']
    start_urls = ['http://dealer.xcar.com.cn/d1000/22.htm']

    def parse(self, response):
        for p in response.xpath('//ul[@id="select_province"]/li')[2:]:
            pro =  {
                'provinceId':p.xpath('./@value').get(),
                'provinceName': p.xpath('./a/text()').get(),
            }
            # print(pro)
            # http://dealer.xcar.com.cn/d24/22.htm?type=1&page=1
            next_page = 'http://dealer.xcar.com.cn/d{}/22.htm?type=1&page=1'.format(pro['provinceId'])
            yield response.follow(next_page, callback=self.parse_dlr,
                                  cb_kwargs=dict(pro=pro))

    def parse_dlr(self, response, pro):
        for dlr in response.xpath('//ul[@class="dlists_list"]/li'):
            d = {
                'province': pro['provinceName'],
                'dealerId':dlr.xpath('./a/@href').get()[1:-1],
                'shortName':dlr.xpath('.//dl/dt/a/text()').get(),
                'address':dlr.xpath('.//dd[@class="site"]/span[2]/text()').get(),
                'dealerUrl':'http://dealer.xcar.com.cn{}'.format(dlr.xpath('./a/@href').get()),
                'crawlUrl':response.url,
                'crawlTime':time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            }
            # print(d)
            yield d
        next_page = response.xpath('//a[@class="page_down"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse_dlr, cb_kwargs=dict(pro=pro))
