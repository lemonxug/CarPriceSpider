# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy import create_engine
import pandas as pd


class CarpricespiderPipeline(object):

    def __init__(self):
        # pip install pymysql
        # pip install mysqlclient 未安装会报错
        self.engine = create_engine('mysql://root:root@localhost:3306/carprice?charset=utf8', echo=False)

    def process_item(self, item, spider):
        df = pd.DataFrame([item,])
        df.to_sql(name=spider.name, con=self.engine, if_exists='append', index=None, chunksize=10000)
        return item

    def close_spider(self, spider):#关闭爬虫时
        pass

import scrapy
import hashlib
from urllib.parse import quote


class ScreenshotPipeline(object):
    """Pipeline that uses Splash to render screenshot of
    every Scrapy item."""
    # http://localhost:8050/render.jpeg?url=https://dealer.autohome.com.cn/2027282/b_2319.html&render_all=1&wait=1
    SPLASH_URL = "http://localhost:8050/render.png?url={}&render_all=1&wait=5"
    SAVE_DIR = 'screenshot'

    def process_item(self, item, spider):
        spiders = [
                    'autohome_series',
                    # 'bitauto_specprice',
                   ]
        if spider.name in spiders:
            encoded_item_url = quote(item["priceUrl"])
            screenshot_url = self.SPLASH_URL.format(encoded_item_url)
            request = scrapy.Request(screenshot_url)
            dfd = spider.crawler.engine.download(request, spider)
            dfd.addBoth(self.return_item, item)
            return dfd
        return  item

    def return_item(self, response, item):
        if response.status != 200:
            # Error happened, return item.
            return item

        # Save screenshot to file, filename will be hash of url.
        url = item["priceUrl"]
        url_hash = hashlib.md5(url.encode("utf8")).hexdigest()
        filename = "{}.jpeg".format(url_hash)
        with open('{}/{}'.format(self.SAVE_DIR, filename), "wb") as f:
            f.write(response.body)

        # Store filename in item.
        item["screenshot_filename"] = filename
        return item


from scrapy.exceptions import DropItem

class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        # if spider.name == 'bitauto_dlr':
        if 'dlr' in spider.name:
            if item['dealerId'] in self.ids_seen:
                raise DropItem("Duplicate item found: %s" % item)
            else:
                self.ids_seen.add(item['dealerId'])
                return item
        else:
            return item