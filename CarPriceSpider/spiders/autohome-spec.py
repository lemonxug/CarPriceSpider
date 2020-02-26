# -*- coding: utf-8 -*-
import scrapy
import json
import time

class AutohomeSpider(scrapy.Spider):
    name = 'autohome_spec'
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
            next_page = 'https://dealer.autohome.com.cn/handler/other/getdata?__action=dealerlq.getdealerserieslist&dealerId={}'.format(dlrid)
            request =  scrapy.Request(next_page, callback=self.parse_series,
                                      cb_kwargs=dict(dlrid=dlrid))
            yield request


    def parse_series(self, response, dlrid):
        dealerseries = json.loads(response.text)
        for s in dealerseries['result'][0]['seriesInfoList']:
            # https://dealer.autohome.com.cn/handler/other/getdata?__action=dealerlq.getdealerspeclist&dealerId=121722&seriesId=2886
            next_page = 'https://dealer.autohome.com.cn/handler/other/\
            getdata?__action=dealerlq.getdealerspeclist&dealerId={}&seriesId={}'.format(dlrid, str(s['seriesId']))
            request = scrapy.Request(next_page, callback=self.parse_spec,
                                      cb_kwargs=dict(dlrid=dlrid, seriesId=s['seriesId'], brandid=s['brandId']))
            yield request

    def parse_spec(self, response, dlrid, seriesId, brandid):
        dealerspecs = json.loads(response.text)
        for g in dealerspecs['result']:
            for s in g['list']:
                yield {
                        'brandId': brandid,
                        'url':response.url,
                        'dealerId':dlrid,
                        'seriesId': seriesId,
                        'groupName': g['groupName'],
                        'specId': s['specId'],
                        'specName': s['specName'],
                        'dealerMaxPrice': s['dealerMaxPrice'],
                        'dealerMinPrice': s['dealerMinPrice'],
                        'fctMaxPrice': s['fctMaxPrice'],
                        'fctMinPrice': s['fctMinPrice'],
                        'priceTime': s['priceTime'],
                        'saleState': s['saleState'],
                        'newsId': s['newsId'],
                        'crawlTime': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    }
# https://dealer.autohome.com.cn/handler/other/getdata?__action=dealerlq.getreferencepricebyspecid&specId=43134&newsId=481229580&dealerId=2016913