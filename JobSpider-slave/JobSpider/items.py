# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JobspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class Item(scrapy.Item):
    # 职位信息来源
    # # 1 - 智联； 2 - 前程无忧；3 - 中华英才网；4 - 猎聘网
    source = scrapy.Field()
    # 职位来源Url
    source_url = scrapy.Field()
    job_name = scrapy.Field()  # 职位名
    company_name = scrapy.Field()  # 公司名
    company_domain = scrapy.Field()  # 公司领域
    company_scale = scrapy.Field()  # 公司规模
    company_type = scrapy.Field()  # 公司类型
    job_location = scrapy.Field()  # 工作地点
    job_type = scrapy.Field()  # 职位类别
    job_hc = scrapy.Field()  # 招聘人数
    job_pub_time = scrapy.Field()  # 发布时间
    job_attribute = scrapy.Field()  # 职位性质:全职，实习，兼职
    job_education = scrapy.Field()  # 学历要求
    job_description = scrapy.Field()  # 职位描述
    job_salary = scrapy.Field()  # 工资
    gather_time = scrapy.Field()  # 采集时间


class ZhilianSpiderItem(Item):
    pass


class WuyouSpiderItem(Item):
    job_bright = scrapy.Field()  # 职位亮点
    job_info = scrapy.Field()  # 笼统的职位信息


class LiepinSpiderItem(Item):
    job_dead_time = scrapy.Field()  # 职位截至时间


class ChinahrSpiderItem(Item):
    job_is_dead = scrapy.Field()  # 职位截至时间