# -*- coding: utf-8 -*-
import scrapy
import time

class XcarSpider(scrapy.Spider):
    name = 'xcar_area'
    allowed_domains = ['xcar.com.cn', 'dealer.xcar.com.cn']
    start_urls = ['http://dealer.xcar.com.cn/d1000/22.htm']

    def parse(self, response):
        for p in response.xpath('//ul[@id="select_province"]/li')[2:]:
            pro =  {
                'provinceId':p.xpath('./@value').get(),
                'provinceName': p.xpath('./a/text()').get(),
            }
            print(pro)
            # http://dealer.xcar.com.cn/dealerdp_index.php?r=dealers/Ajax/selectCity&province_id=24&pbid=22
            next_page = 'http://dealer.xcar.com.cn/dealerdp_index.php?' \
                        'r=dealers/Ajax/selectCity&province_id={}&pbid=22'.format(pro['provinceId'])
            yield response.follow(next_page, callback=self.parse_city,
                                  cb_kwargs=dict(pro=pro))

    def parse_city(self, response, pro):
        for c in response.xpath('//li')[1:]:
            city = {
                'provinceId': pro['provinceId'],
                'provinceName': pro['provinceName'],
                'cityId': c.xpath('./@id').get(),
                'cityName': c.xpath('./@name').get(),
                'crawlTime': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            }
            yield city