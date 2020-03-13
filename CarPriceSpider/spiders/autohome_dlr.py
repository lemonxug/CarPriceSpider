# -*- coding: utf-8 -*-
import scrapy
import json
import time
# from CarPriceSpider.items import AutohomeDealerItem

class AutohomeDlrSpider(scrapy.Spider):
    name = 'autohome_dlr'
    allowed_domains = ['autohome.com', 'dealer.autohome.com.cn']

    def start_requests(self):
        brandid = getattr(self, 'brandid', None)
        if brandid is None:
            brandid = 62 # 若未指定brandid，设置为62-起亚
        # https://dealer.autohome.com.cn/DealerList/GetAreasAjax?provinceId=0&cityId=340200&brandid=62&manufactoryid=0&seriesid=0&isSales=0
        url = 'https://dealer.autohome.com.cn/DealerList/GetAreasAjax?brandid={}'.format(str(brandid))
        yield scrapy.Request(url, self.parse, cb_kwargs=dict(brandid = str(brandid)))

    def parse(self, response, brandid):
        areas = json.loads(response.text)
        #  areas['AreaInfoGroups'][0]['Values'][0]['Cities'][0]['Pinyin']
        for firstchar in areas['AreaInfoGroups']:
            for province in firstchar['Values']:
                for city in province['Cities']:
                    if city['Count'] > 0:
                        # https://dealer.autohome.com.cn/yancheng/0/62/0/0/1/0/0/0.html
                        next_page = 'https://dealer.autohome.com.cn/'+city['Pinyin']+'/0/{}/0/0/1/0/0/0.html'.format(brandid)
                        request = scrapy.Request(next_page,
                                                 callback=self.parse_dealer,
                                                 cb_kwargs=dict(brandid=brandid,
                                                                province=province['Name'],
                                                                city=city['Name']))
                        yield request

    def parse_dealer(self, response, province, city, brandid):
        # response.xpath('//ul[@class="list-box"]/li')
        for dlr in response.xpath('//ul[@class="list-box"]/li'):
            yield {
                'brandId': brandid,
                'province':province,
                'city': city,
                'dealerId':dlr.xpath('./@id').extract_first(),
                'shortName':dlr.xpath('.//a[@class="link"]//span/text()').extract_first(),
                '400phone':dlr.xpath('.//span[@class="tel"]/text()').extract_first(),
                'address':dlr.xpath('.//span[@class="info-addr"]/text()').extract_first(),
                'dealerUrl':'https:' + dlr.xpath('.//a[@class="link"]/@href').extract_first(),
                'crawlTime':time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            }



