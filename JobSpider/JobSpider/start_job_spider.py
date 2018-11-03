# coding:utf-8

import logging

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# 启动爬虫脚本
if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    # 爬虫名称, 可以启动多个爬虫
    # process.crawl('zhilian')
    # process.crawl('wuyou')
    # process.crawl('liepin')
    process.crawl('chinahr')
    process.start()
