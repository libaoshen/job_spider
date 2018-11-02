# coding:utf-8
# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import logging
from JobSpider.utils.redis import insert_into_job_spider
from JobSpider.spiders.zhilian_spider import ZhilianSpider
from JobSpider.spiders.wuyou_spider import WuyouSpider

# Init
print("======Init spider start")
logging.info("======Init spider start")

# zhilian
print('======Init insert start_url into redis[job_spider_start_urls_zl] start')
logging.info('======Init insert start_url into redis[job_spider_start_urls_zl] start')

for url in ZhilianSpider.start_urls:
    insert_into_job_spider(url, 1)

print('======Init insert start_url into redis[job_spider_start_urls_zl] end')
logging.info('======Init insert start_url into redis[job_spider_start_urls_zl] end')

# wuyou
print('======Init insert start_url into redis[job_spider_start_urls_wy] start')
logging.info('======Init insert start_url into redis[job_spider_start_urls_wy] start')

for url in WuyouSpider.start_urls:
    insert_into_job_spider(url, 3)

print('======Init insert start_url into redis[job_spider_start_urls_wy] end')
logging.info('======Init insert start_url into redis[job_spider_start_urls_wy] end')

print("======Init spider end")
logging.info("======Init spider end")
