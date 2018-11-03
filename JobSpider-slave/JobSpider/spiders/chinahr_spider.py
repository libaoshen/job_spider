# coding:utf-8

import sys
import re
import datetime
import scrapy
from scrapy.http.request import Request
from scrapy_redis.spiders import RedisSpider

from JobSpider.items import ChinahrSpiderItem

reload(sys)
sys.setdefaultencoding("utf-8")


class ChinahrSpider(RedisSpider):
    name = "chinahr"  # 爬虫名称
    allowed_domains = ["campus.chinahr.com"]  # 允许的域名
    redis_key = 'job_spider_request_ch'

    def parse(self, response):
        sweep_space = re.compile(r'[\s\n]*', re.S)

        url = response.url
        job_name = response.xpath(".//h1[@class='job-title']/text()").extract()[0] if response.xpath(".//h1[@class='job-title']/text()").extract() else None
        job_name = sweep_space.sub('', job_name)
        job_extra = response.xpath(".//div[@class='job-info']/text()").extract() if response.xpath(".//div[@class='job-info']/text()").extract() else None
        job_extra_1 = response.xpath(".//span[@class='release-date']/text()").extract()
        company_name = str(job_extra[1]).strip() if job_extra else None

        # company_type = response.xpath(".//div[@class='company-desc']/p[1]/text()").extract()[0] \
        #     if response.xpath(".//div[@class='company-desc']/p[1]/text()").extract() else None
        # company_type = company_type.split("：")[1]
        # company_scale = response.xpath(".//div[@class='company-desc']/p[2]/text()").extract()[0] \
        #     if response.xpath(".//div[@class='company-desc']/p[2]/text()").extract() else None
        # company_scale = company_scale.split("：")[1]
        # company_domain = response.xpath(".//div[@class='company-desc']/p[3]/a/text()").extract() \
        #     if response.xpath(".//div[@class='company-desc']/p[3]/a/text()").extract() else None

        # job_info = response.xpath(".//div[@class='cn']/p[@class='msg ltype']/@title").extract()
        # job_info = job_info[0] if job_info else None
        # job_info = str(job_info).split('|')
        # job_info_len = len(job_info)

        job_location = str(job_extra_1[1]).split('：')[1].strip() if job_extra_1 else None
        job_education = job_extra[0].strip() if job_extra else None
        job_hc = str(job_extra_1[2]).split('：')[1].strip() if job_extra_1 else None
        job_pub_time = str(job_extra_1[3]).split('：')[1].strip() if job_extra_1 else None
        # job_info = '.'.join(job_info)

        job_salary = response.xpath(".//strong[@class='job-salary']/text()").extract()[0] \
            if response.xpath(".//strong[@class='job-salary']/text()").extract() else None
        # job_type = response.xpath(".//div[@class='job-info']/span[@class='catagory']/text()").extract()[0] \
        #     if response.xpath(".//div[@class='job-info']/span[@class='catagory']/text()").extract() else None
        # job_attribute = job_info[4].xpath("text()").extract()[0] if job_info_len > 4 else None
        # job_dead_time = response.xpath(".//div[@class='time-info clearfix']/span[@class='dead-time']/text()").extract()[0]\
        #     if response.xpath(".//div[@class='time-info clearfix']/span[@class='dead-time']/text()").extract() else None
        job_is_dead = True if response.xpath(".//span[@class='company-name Fellip apply-btns']/text()").extract() else False

        # job_bright = ','.join(response.xpath(".//span[@class='sp4']/text()").extract()) if response.xpath(
        #     ".//span[@class='sp4']/text()").extract() else None

        job_description = response.xpath(".//div[@class='job-responsibility']").extract()[0] \
            if response.xpath(".//div[@class='job-responsibility']").extract() else None

        sweep_tag = re.compile(r'<[^>]+>', re.S)
        job_description = sweep_tag.sub('', job_description)
        job_description = str(job_description).strip()
        job_description = sweep_space.sub('', job_description)

        now = datetime.datetime.now()
        item = ChinahrSpiderItem(job_name=job_name, company_name=company_name, company_domain=None,
                               company_scale=None, company_type=None, job_is_dead=job_is_dead,
                               job_location=job_location, job_type=None, job_hc=job_hc, job_pub_time=job_pub_time,
                               job_attribute=None, job_education=job_education, job_description=job_description,
                               job_salary=job_salary,
                               gather_time='{}-{}-{} {}:{}:{}'.format(now.year, now.month, now.day, now.hour,
                                                                      now.minute, now.second), source=3, source_url=url)

        yield item
