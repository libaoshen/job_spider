# coding:utf-8

import sys
import re
import datetime
import scrapy
from scrapy.http.request import Request
from scrapy_redis.spiders import RedisSpider

from JobSpider.items import LiepinSpiderItem

reload(sys)
sys.setdefaultencoding("utf-8")


class LiepinSpider(RedisSpider):
    name = "liepin"  # 爬虫名称
    allowed_domains = ["liepin.com"]  # 允许的域名
    redis_key = 'job_spider_request_lp'

    def parse(self, response):
        sweep_space = re.compile(r'[\s\n]*', re.S)

        url = response.url
        job_name = response.xpath(".//div[@class='job-brief wrap']/div[@class='job-title "
                                  "clearfix']/h1/@title").extract()[0] if response.xpath(
            ".//div[@class='job-brief wrap']/div[@class='job-title clearfix']/h1/@title").extract() else None
        job_name = sweep_space.sub('', job_name)
        company_name = response.xpath(".//div[@class='company-desc']/a[1]/text()").extract()[0] \
            if response.xpath(".//div[@class='company-desc']/a[1]/text()").extract() else None

        company_type = response.xpath(".//div[@class='company-desc']/p[1]/text()").extract()[0] \
            if response.xpath(".//div[@class='company-desc']/p[1]/text()").extract() else None
        company_type = company_type.split("：")[1]
        company_scale = response.xpath(".//div[@class='company-desc']/p[2]/text()").extract()[0] \
            if response.xpath(".//div[@class='company-desc']/p[2]/text()").extract() else None
        company_scale = company_scale.split("：")[1]
        company_domain = response.xpath(".//div[@class='company-desc']/p[3]/a/text()").extract() \
            if response.xpath(".//div[@class='company-desc']/p[3]/a/text()").extract() else None

        # job_info = response.xpath(".//div[@class='cn']/p[@class='msg ltype']/@title").extract()
        # job_info = job_info[0] if job_info else None
        # job_info = str(job_info).split('|')
        # job_info_len = len(job_info)

        job_location = response.xpath(".//div[@class='job-info']/span[@class='where']/text()").extract()[0]\
            if response.xpath(".//div[@class='job-info']/span[@class='where']/text()").extract() else None
        # job_education = job_info[2].strip() if job_info_len > 1 else None
        # job_hc = job_info[3].strip() if job_info_len > 2 else None
        job_pub_time = response.xpath(".//div[@class='time-info clearfix']/span[@class='create-time']/text()").extract()[0] \
            if response.xpath(".//div[@class='time-info clearfix']/span[@class='create-time']/text()").extract() else None
        # job_info = '.'.join(job_info)

        job_salary = response.xpath(".//div[@class='job-info']/span[@class='salary']/text()").extract()[0] \
            if response.xpath(".//div[@class='job-info']/span[@class='salary']/text()").extract() else None
        job_type = response.xpath(".//div[@class='job-info']/span[@class='catagory']/text()").extract()[0] \
            if response.xpath(".//div[@class='job-info']/span[@class='catagory']/text()").extract() else None
        job_hc = response.xpath(".//div[@class='job-info']/span[@class='num']/text()").extract()[0] \
            if response.xpath(".//div[@class='job-info']/span[@class='num']/text()").extract() else None
        # job_attribute = job_info[4].xpath("text()").extract()[0] if job_info_len > 4 else None
        job_dead_time = response.xpath(".//div[@class='time-info clearfix']/span[@class='dead-time']/text()").extract()[0]\
            if response.xpath(".//div[@class='time-info clearfix']/span[@class='dead-time']/text()").extract() else None

        # job_bright = ','.join(response.xpath(".//span[@class='sp4']/text()").extract()) if response.xpath(
        #     ".//span[@class='sp4']/text()").extract() else None

        job_description = response.xpath(".//div[@class='job-desc']/p").extract()[0] \
            if response.xpath(".//div[@class='job-desc']/p").extract() else None

        sweep_tag = re.compile(r'<[^>]+>', re.S)
        job_description = sweep_tag.sub('', job_description)
        job_description = str(job_description).strip()
        job_description = sweep_space.sub('', job_description)

        now = datetime.datetime.now()
        item = LiepinSpiderItem(job_name=job_name, company_name=company_name, company_domain=company_domain,
                               company_scale=company_scale, company_type=company_type, job_dead_time=job_dead_time,
                               job_location=job_location, job_type=job_type, job_hc=job_hc, job_pub_time=job_pub_time,
                               job_attribute=None, job_education=None, job_description=job_description,
                               job_salary=job_salary,
                               gather_time='{}-{}-{} {}:{}:{}'.format(now.year, now.month, now.day, now.hour,
                                                                      now.minute, now.second), source=4, source_url=url)

        yield item
