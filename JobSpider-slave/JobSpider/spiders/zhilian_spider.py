# coding:utf-8

import sys
import re
import scrapy
from scrapy.http.request import Request
from scrapy_redis.spiders import RedisSpider

from JobSpider.items import ZhilianSpiderItem

reload(sys)
sys.setdefaultencoding("utf-8")


class ZhilianSpider(RedisSpider):
    name = "zhilian"  # 爬虫名称
    allowed_domains = ["xiaoyuan.zhaopin.com"]  # 允许的域名
    redis_key = 'job_spider_request_zl'

    def parse(self, response):
        sweep_space = re.compile(r'[\s\n]*', re.S)

        url = response.url
        job_name = response.xpath(".//h1[@id='JobName']/text()").extract()[0] if response.xpath(".//h1[@id='JobName']/text()").extract() else None
        job_name = sweep_space.sub('', job_name)
        company_name = response.xpath(".//li[@id='jobCompany']/a/text()").extract()[0] if response.xpath(".//li[@id='jobCompany']/a/text()").extract() else None
        company_info = response.xpath(".//li[@class='cJobDetailInforWd2']")
        company_domain = company_info[0].xpath("@title").extract()[0] if len(company_info) > 1 else None
        company_scale = company_info[1].xpath("text()").extract()[0] if len(company_info) > 1 else None

        company_type = response.xpath(".//ul[@class='cJobDetailInforTopWrap clearfix c3']/li[last()]/text()").extract()[
            0] if response.xpath(".//ul[@class='cJobDetailInforTopWrap clearfix c3']/li[last()]/text()").extract() else None
        job_info = response.xpath(
            ".//ul[@class='cJobDetailInforBotWrap clearfix c3']/li[@class='cJobDetailInforWd2 marb']")
        job_info_len = len(job_info)
        job_location = job_info[0].xpath("text()").extract()[0] if job_info_len > 0 else None
        job_location = sweep_space.sub('', job_location)
        job_type = job_info[1].xpath("text()").extract()[0] if job_info_len > 1 else None
        job_hc = job_info[2].xpath("text()").extract()[0] if job_info_len > 2 else None
        job_pub_time = job_info[3].xpath("text()").extract()[0] if job_info_len > 3 else None
        job_attribute = job_info[4].xpath("text()").extract()[0] if job_info_len > 4 else None
        job_education = job_info[5].xpath("text()").extract()[0] if job_info_len > 5 else None

        job_description = response.xpath(".//div[@class='cJob_Detail f14']").extract()[0] \
            if response.xpath(".//div[@class='cJob_Detail f14']").extract() else None

        sweep_tag = re.compile(r'<[^>]+>', re.S)
        job_description = sweep_tag.sub('', job_description)
        job_description = str(job_description).strip()
        job_description = sweep_space.sub('', job_description)

        item = ZhilianSpiderItem(job_name=job_name, company_name=company_name, company_domain=company_domain,
                                 company_scale=company_scale, company_type=company_type, job_location=job_location,
                                 job_type=job_type, job_hc=job_hc, job_pub_time=job_pub_time,
                                 job_attribute=job_attribute, job_education=job_education,
                                 job_description=job_description,source=1,source_url=url)

        yield item
