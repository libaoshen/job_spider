# coding:utf-8

import sys
import scrapy
from scrapy.http.request import Request
from JobSpider.utils.common import get_first_element,get_last_element
from JobSpider.utils.redis import insert_into_job_spider
from scrapy_redis.spiders import RedisSpider

reload(sys)
sys.setdefaultencoding("utf-8")


class ChinahrSpider(RedisSpider):
    name = "chinahr"  # 爬虫名称
    allowed_domains = ["campus.chinahr.com"]  # 允许的域名
    start_urls = ['http://campus.chinahr.com/qz/']
    redis_key = 'job_spider_start_urls_ch'

    def parse(self, response):
        # 获取下一页的url
        next_url = get_last_element(response.xpath(".//div[@class='pagination-bar']/a/@href").extract())
        # 获取详情页的url
        details_urls = response.xpath(".//a[@class='job-name Fellip']/@href").extract()

        # 下一页插入到redis的start_url list中
        if next_url and next_url != 'javascript:;':
            if details_urls:
                next_url = "https://" + self.allowed_domains[0] + next_url
                insert_into_job_spider(next_url.strip(), 7)
        # 详情页插入到redis的request list中
        for url in details_urls:
            url = "https://" + self.allowed_domains[0] + url
            insert_into_job_spider(url.strip(), 8)
