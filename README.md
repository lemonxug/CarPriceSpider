# CarPriceSpider
该项目利用scrapy框架开发，用于爬取各汽车垂媒网站上各车型的经销商报价。

# 爬取网站
|  网站   | 状态  |
|  ----  | ----  |
| 汽车之家  | ok |
| 易车网  | ok |
| 爱卡汽车  | ok |
| 太平洋汽车  | todo |

# 使用
## 安装相关库
```bash
# pip安装scrapy
>pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pip
>pip install -i https://pypi.tuna.tsinghua.edu.cn/simple scrapy

# 新建工程
startproject CarPriceSpider
# 新建爬虫
scrapy genspider autohome autohome.com
```

## 快速导出数据
```bash
# 列出所有爬虫
>scrapy list

# 运行指定爬虫,导出数据为csv格式
>scrapy crawl autohome_area -o area.csv

# 上述csv文件用Excel可能打不开，可使用cache目录下的csv2xlsx.py转化格式（需安装pandas库）
>python csv2xlsx.py area.csv

```
## 使用mysql
启动mysql数据库
```bash
# 使用docker启动mysql，具体
>docker run -d --rm --name mysql -v /D/mysql:/var/lib/mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=root  mysql

# 使用docker启动phpmyadmin
>docker run -d --rm --name phpmyadmin -p 8080:80 --link mysql:db phpmyadmin/phpmyadmin
```
修改pipelines.py文件
```python
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
```
修改settings.py文件启用上述Pipeline
```python
ITEM_PIPELINES = {
   'CarPriceSpider.pipelines.CarpricespiderPipeline': 320,
   }
```
启动后爬虫会使用爬虫名自动创建数据库表，非常方便

## 启用截图
启动splash
```bash
# 启动splash，访问地址：http://localhost:8050/
docker run -itd -p 8050:8050 --rm scrapinghub/splash

```
修改pipelines.py文件
```python
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
```
修改settings.py文件启用上述Pipeline
```python
ITEM_PIPELINES = {
    'CarPriceSpider.pipelines.CarpricespiderPipeline': 320,
    'CarPriceSpider.pipelines.ScreenshotPipeline':300,
   }
```



