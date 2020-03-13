# -*- coding: utf-8 -*-
import scrapy
import time

class PcautoDlrSpider(scrapy.Spider):
    name = 'pcauto_dlr'
    allowed_domains = ['pcauto.com.cn']
    start_urls = ['https://price.pcauto.com.cn/shangjia/c2/nb12/']

    def parse(self, response, provinceName='北京'):

        for dlr in response.xpath('//div[@id="listTmmd"]//li'):
            if '4S' in dlr.xpath('.//p[1]/span[2]/text()').get():
                d = {
                    'province': provinceName,
                    'city':dlr.xpath('.//span[@class="smoke"]/text()').get(),
                    'dealerId':dlr.xpath('.//p[1]/a/@href').re('/(\d*)/')[1],
                    'shortName':dlr.xpath('.//p[1]/a/strong/text()').get(),
                    'dealerName': dlr.xpath('.//p[1]/a/@title').get(),
                    'address':dlr.xpath('.//p[4]/span[2]/@title').get(),
                    'dealerUrl':'https:{}'.format(dlr.xpath('.//p[1]/a/@href').get(),),
                    'crawlUrl':response.url,
                    'crawlTime':time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                }
                # print(d)
                yield d

        next_page = response.xpath('//a[@class="next"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse, cb_kwargs=dict(provinceName=provinceName))

        for p in response.xpath('//div[@id="J-cityItem"]//a')[1:]:
            provinceName=p.xpath('./text()').get()
            # https: // price.pcauto.com.cn / shangjia / c2 / nb12 /
            next_page = 'https:{}'.format(p.xpath('./@href').get())
            if 'pcauto' in next_page:
                # print(next_page)
                yield response.follow(next_page, callback=self.parse,
                                      cb_kwargs=dict(provinceName=provinceName))
