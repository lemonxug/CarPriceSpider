import scrapy
from scrapy.crawler import CrawlerProcess
from CarPriceSpider.CarPriceSpider.spiders.xcar_area import XcarAreaSpider


process = CrawlerProcess()
process.crawl(XcarAreaSpider)
# process.crawl(MySpider2)
process.start() # the script will block here until all crawling jobs are finished