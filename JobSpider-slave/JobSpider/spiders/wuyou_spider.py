# coding:utf-8

import sys
import re
import datetime
import scrapy
from scrapy.http.request import Request
from scrapy_redis.spiders import RedisSpider

from JobSpider.items import WuyouSpiderItem

reload(sys)
sys.setdefaultencoding("utf-8")


class ZhilianSpider(RedisSpider):
    name = "wuyou"  # 爬虫名称
    allowed_domains = ["51job.com"]  # 允许的域名
    redis_key = 'job_spider_request_wy'

    def parse(self, response):
        sweep_space = re.compile(r'[\s\n]*', re.S)

        url = response.url
        job_name = response.xpath(".//div[@class='cn']/h1/@title").extract()[0] if response.xpath(
            ".//div[@class='cn']/h1/@title").extract() else None
        job_name = sweep_space.sub('', job_name)
        company_name = response.xpath(".//div[@class='cn']/p[@class='cname']/a/@title").extract()[0] if response.xpath(
            ".//div[@class='cn']/p[@class='cname']/a/@title").extract() else None
        company_info = response.xpath(".//div[@class='tCompany_sidebar']/div[1]/div[@class='com_tag']/p/@title").extract()
        company_type = company_info[0] if len(company_info) > 1 else None
        company_scale = company_info[1] if len(company_info) > 1 else None
        company_domain = company_info[2] if len(company_info) > 1 else None
        job_info = response.xpath(".//div[@class='cn']/p[@class='msg ltype']/@title").extract()
        job_info = job_info[0] if job_info else None
        job_info = str(job_info).split('|')
        job_info_len = len(job_info)

        job_location = job_info[0].strip() if job_info_len > 0 else None
        # job_education = job_info[2].strip() if job_info_len > 1 else None
        # job_hc = job_info[3].strip() if job_info_len > 2 else None
        # job_pub_time = job_info[4].strip() if job_info_len > 3 else None
        job_info = '.'.join(job_info)

        job_salary = response.xpath(".//div[@class='cn']/strong/text()").extract()[0] if response.xpath(
            ".//div[@class='cn']/strong/text()").extract() else 0
        # job_type = job_info[1].xpath("text()").extract()[0] if job_info_len > 1 else None
        # job_attribute = job_info[4].xpath("text()").extract()[0] if job_info_len > 4 else None

        job_bright = ','.join(response.xpath(".//span[@class='sp4']/text()").extract()) \
            if response.xpath(".//span[@class='sp4']/text()").extract() else None


        job_description = response.xpath(".//div[@class='bmsg job_msg inbox']").extract()[0] if response.xpath(
            ".//div[@class='bmsg job_msg inbox']").extract() else None

        sweep_tag = re.compile(r'<[^>]+>', re.S)
        job_description = sweep_tag.sub('', job_description)
        job_description = str(job_description).strip()
        job_description = sweep_space.sub('', job_description)

        now = datetime.datetime.now()
        item = WuyouSpiderItem(job_name=job_name, company_name=company_name, company_domain=company_domain, company_scale=company_scale,
                               company_type=company_type, job_info=job_info, job_location=job_location, job_type=None, job_hc=None,
                               job_pub_time=None, job_attribute=None, job_education=None,
                               job_description=job_description, job_salary=job_salary, job_bright=job_bright,
                               gather_time='{}-{}-{} {}:{}:{}'.format(now.year, now.month, now.day, now.hour,
                                                                      now.minute, now.second), source=2, source_url=url)

        yield item
