# -*- coding: utf-8 -*-
import scrapy
import time
import json

class XcarSpider(scrapy.Spider):
    name = 'pcauto_specprice'
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
                # https://price.pcauto.com.cn/dealer/interface/dealer_free_info_json.jsp?m=getSgByDealer&did=111410&pageNo=1&pageSize=20&sort=1
                next_page = 'https://price.pcauto.com.cn/dealer/interface/dealer_free_info_json.jsp?m=getSgByDealer' \
                            '&did={}&pageNo=1&pageSize=20&sort=1'.format(d['dealerId'])
                yield response.follow(next_page, callback=self.parse_series, cb_kwargs=dict(dealer=d))

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

    def parse_series(self, response, dealer):
        series = json.loads(response.text)
        for s in series['data']:
            serial = {
                'serialGroupId':s['serialGroupId'],
                'baiPhoto': s['baiPhoto'],
                'name': s['name'],
                'pl': s['pl'],
                'bsx': s['bsx'],
                'qdfs': s['qdfs'],
                'photo': s['photo'],
                'kind': s['kind'],
                'maxPrice': s['priceRange']['maxPrice'],
                'minPrice': s['priceRange']['minPrice'],
                'crawlUrl': response.url,
                'crawlTime': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            }
            # print(serial)
            # https://price.pcauto.com.cn/dealer/interface/base/get_dealer_models.jsp?dealerId=111410&sgId=4553
            next_page = 'https://price.pcauto.com.cn/dealer/interface/base/get_dealer_models.jsp' \
                        '?dealerId={}&sgId={}'.format(dealer['dealerId'], serial['serialGroupId'])
            yield response.follow(next_page, callback=self.parse_spec, cb_kwargs=dict(dealer=dealer, serial=serial))

    def parse_spec(self, response, dealer, serial):
        groups = json.loads(response.text)
        for k, v in groups.items():
            for g in v:
                specprice = {
                    'dealerId': dealer['dealerId'],
                    'specId': g['modelDescId'],
                    'specName':g['name'],
                    'serialId': g['serialId'],
                    'modelParameterId': g['modelParameterId'],
                    'priceType': g['priceType'],
                    'groupName': k,
                    'seriesId': serial['serialGroupId'],
                    'seriesName': serial['name'],
                    'price':g['price'],
                    'dealerPrice': g['dealerPrice'],
                    'tid': g['id'],
                    'crawlUrl': response.url,
                    'crawlTime': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    }
                # print(specprice)
                yield specprice