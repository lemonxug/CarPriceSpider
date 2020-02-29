# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy import Selector

class XcarSpider(scrapy.Spider):
    name = 'pcauto_brand'
    allowed_domains = ['pcauto.com.cn']
    start_urls = ['https://price.pcauto.com.cn/index/js/6_0/treedata-dn-html.js']

    def parse(self, response):
        # 指定response的解码格式
        doc = response.body.decode('gbk').split("innerHTML='")[1][:-2]
        sel = Selector(text=doc, type="html")
        for b in sel.xpath('//li[@class="closeChild"]/a'):
            brand =  {
                'brandId':b.xpath('./@id').re(r'_\w_(\d*)')[0],
                'brandName': b.xpath('./@title').get(),
                # https://price.pcauto.com.cn/shangjia/p5/nb7541/
                'brandUrl':'https://price.pcauto.com.cn/shangjia/p5/nb{}/'.format(
                    b.xpath('./@id').re(r'_\w_(\d*)')[0]),
                'crawlTime': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
            }
            # print(brand)
            yield brand