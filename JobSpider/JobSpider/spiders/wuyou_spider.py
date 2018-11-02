# coding:utf-8

import sys
import scrapy
from scrapy.http.request import Request
from JobSpider.utils.common import get_first_element
from JobSpider.utils.redis import insert_into_job_spider
from scrapy_redis.spiders import RedisSpider

reload(sys)
sys.setdefaultencoding("utf-8")


class WuyouSpider(RedisSpider):
    name = "wuyou"  # 爬虫名称
    allowed_domains = ["51job.com"]  # 允许的域名
    start_urls = ['https://search.51job.com/list/000000,000000,0000,00,9,99,%2520,2,1.html?lang=c&stype='
                  '&postchannel=0100&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&provi'
                  'desalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&addr'
                  'ess=&line=&specialarea=00&from=&welfare=']
    redis_key = 'job_spider_start_urls_wy'

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
