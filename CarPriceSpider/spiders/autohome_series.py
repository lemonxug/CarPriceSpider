# -*- coding: utf-8 -*-
import scrapy
import json
import time

class AutohomeSeriesSpider(scrapy.Spider):
    name = 'autohome_series'
    allowed_domains = ['autohome.com', 'dealer.autohome.com.cn']

    def start_requests(self):
        brandid = getattr(self, 'brandid', None)
        if brandid is None:
            brandid = 62 # 若未指定brandid，设置为62-起亚
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
                        yield scrapy.Request(next_page, callback=self.parse_dealer)
                        # yield response.follow(next_page, self.parse_dealer)

    def parse_dealer(self, response):
        # response.xpath('//ul[@class="list-box"]/li')
        for dlrid in response.xpath('//ul[@class="list-box"]/li/@id').extract():
            # https://dealer.autohome.com.cn/handler/other/getdata?__action=dealerlq.getdealerserieslist&dealerId=121722&seriesId=0&factoryId=0
            next_page = 'https://dealer.autohome.com.cn/handler/other/getdata?__action=dealerlq.getdealerserieslist&dealerId=' + dlrid
            yield scrapy.Request(next_page, callback=self.parse_series)

    def parse_series(self, response):
        dealerseries = json.loads(response.text)
        for s in dealerseries['result'][0]['seriesInfoList']:
            yield {
                'brandId': s['brandId'],
                'url':response.url,
                # https://dealer.autohome.com.cn/15813/b_4505.html
                'priceUrl':'https://dealer.autohome.com.cn/{}/b_{}.html'.format(s['dealerId'],s['seriesId'] ),
                'dealerId':s['dealerId'],
                'seriesId': s['seriesId'],
                'seriesName': s['seriesName'],
                'seriesImg': s['seriesImg'],
                'specCount': s['specCount'],
                'carBody': s['carBody'],
                'emission': s['emission'],
                'transmission': s['transmission'],
                'maxOriginalPrice': s['maxOriginalPrice'],
                'minOriginalPrice': s['minOriginalPrice'],
                'dealerMaxPrice': s['dealerMaxPrice'],
                'dealerMinPrice': s['dealerMinPrice'],
                'crawlTime': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            }



