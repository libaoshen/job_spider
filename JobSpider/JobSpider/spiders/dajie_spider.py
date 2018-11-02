# coding:utf-8

import sys
import scrapy
from scrapy.http.request import Request
from JobSpider.utils.common import get_first_element
from JobSpider.utils.redis import insert_into_job_spider
from scrapy_redis.spiders import RedisSpider

reload(sys)
sys.setdefaultencoding("utf-8")


class DajieSpider(RedisSpider):
    name = "dajie"  # 爬虫名称
    allowed_domains = ["dajie.com"]  # 允许的域名
    start_urls = ['https://so.dajie.com/job/search?keyword=']
    redis_key = 'job_spider_start_urls_dj'

    def parse(self, response):
        # 获取下一页的url
        next_url = get_first_element(response.xpath(".//li[@class='bk']/a/@href").extract())
        # 获取详情页的url
        details_urls = response.xpath(".//div[@id='resultList']/div[@class='el']/p[@class='t1 ']/span/a/@href").extract()

        # 下一页插入到redis的start_url list中
        if next_url:
            if details_urls:
                insert_into_job_spider(next_url, 3)
        # 详情页插入到redis的request list中
        for url in details_urls:
            if url.startswith('https://jobs.51job.com'):
                insert_into_job_spider(url, 4)
