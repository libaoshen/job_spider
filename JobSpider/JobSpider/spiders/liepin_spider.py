# coding:utf-8

import sys
import scrapy
from scrapy.http.request import Request
from JobSpider.utils.common import get_first_element
from JobSpider.utils.redis import insert_into_job_spider
from scrapy_redis.spiders import RedisSpider

reload(sys)
sys.setdefaultencoding("utf-8")


class LiepinSpider(RedisSpider):
    name = "liepin"  # 爬虫名称
    allowed_domains = ["campus.liepin.com"]  # 允许的域名
    start_urls = ['https://campus.liepin.com/sojob/']
    redis_key = 'job_spider_start_urls_lp'

    def parse(self, response):
        # 获取下一页的url
        next_url = get_first_element(response.xpath(".//div[@class='pagerbar']/a[7]/@href").extract())
        # 获取详情页的url
        details_urls = response\
            .xpath(".//ul[@class='super-jobs job-lists']/li/div/p[@class='job-name']/span/a/@href").extract()

        # 下一页插入到redis的start_url list中
        if next_url:
            if details_urls:
                insert_into_job_spider(next_url.strip(), 5)
        # 详情页插入到redis的request list中
        for url in details_urls:
            if url.startswith('https://campus.liepin.com'):
                insert_into_job_spider(url.strip(), 6)
