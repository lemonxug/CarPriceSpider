# -*- coding: utf-8 -*-
import scrapy
import time

class XcarSpider(scrapy.Spider):
    name = 'xcar_specprice'
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
            dlrid = dlr.xpath('./a/@href').get()[1:-1]
            # http://dealer.xcar.com.cn/55972/price_1_1.htm
            next_page = 'http://dealer.xcar.com.cn/{}/price_1_1.htm'.format(dlrid)
            yield response.follow(next_page, callback=self.parse_series, cb_kwargs=dict(dlrid=dlrid))
        next_page = response.xpath('//a[@class="page_down"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse_dlr, cb_kwargs=dict(pro=pro))

    def parse_series(self, response, dlrid):
        for s in response.xpath('//div[@class="pars_list"]//ul/li'):
            seriesName = s.xpath('./a/text()').get()
            seriesUrl =  'http://dealer.xcar.com.cn{}'.format(s.xpath('./a/@href').get())
            # http://dealer.xcar.com.cn/55972/price_s3535_1_1.htm
            seriesId = s.xpath('./a/@href').re(r'_s(\d*)_1_1.htm')[0]
            # http://dealer.xcar.com.cn/55972/price_s3535_1_1.htm
            next_page = seriesUrl
            yield response.follow(next_page,
                                  callback=self.parse_spec,
                                  cb_kwargs=dict(dlrid=dlrid, seriesName=seriesName, seriesId=seriesId))

    def parse_spec(self, response, dlrid, seriesName, seriesId):
        seriesImg = 'http{}'.format(response.xpath('//div[@class="car_t"]//img/@src').get())
        dealerPriceRange = response.xpath('//span[@class="price_z"]/text()').get().strip()
        factoryPriceRange = response.xpath('//span[@class="price_z"]/i/text()').get()[1:-1]
        groupName = ''
        for tr in response.xpath('//div[@class="price_list"]//table//tr'):
            if tr.xpath('./th[@class="car_xin_th"]/text()').get():
                groupName = tr.xpath('./th[@class="car_xin_th"]/text()').get()
            else:
                specprice = {
                    'dealerId':dlrid,
                    'specId': tr.xpath('./td[1]/a/@href').re(r'm(\d*).htm')[0],
                    'specName': tr.xpath('./td[1]/a/text()').get(),
                    'specUrl': 'http://dealer.xcar.com.cn{}'.format(tr.xpath('./td[1]/a/@href').get()),
                    'factoryPriceRange': factoryPriceRange,
                    'dealerPriceRange': dealerPriceRange,
                    'groupName': groupName,
                    'seriesId': seriesId,
                    'seriesName':seriesName,
                    'seriesImg': seriesImg,
                    'factoryPrice':tr.xpath('./td[2]/text()').get().strip(),
                    'discount': tr.xpath('./td[3]/i/text()').get().strip(),
                    'dealerPrice':tr.xpath('./td[4]/i/text()').get().strip(),
                    'crawlUrl':response.url,
                    'crawlTime':time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                }
                # print(specprice)
                yield specprice

