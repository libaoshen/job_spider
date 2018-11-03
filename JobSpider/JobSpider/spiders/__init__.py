# coding:utf-8
# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import logging
from JobSpider.utils.redis import insert_into_job_spider
from JobSpider.spiders.zhilian_spider import ZhilianSpider
from JobSpider.spiders.wuyou_spider import WuyouSpider
from JobSpider.spiders.liepin_spider import LiepinSpider
from JobSpider.spiders.chinahr_spider import ChinahrSpider

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

# liepin
print('======Init insert start_url into redis[job_spider_start_urls_lp] start')
logging.info('======Init insert start_url into redis[job_spider_start_urls_lp] start')

for url in LiepinSpider.start_urls:
    insert_into_job_spider(url, 5)

print('======Init insert start_url into redis[job_spider_start_urls_lp] end')
logging.info('======Init insert start_url into redis[job_spider_start_urls_lp] end')

# chinahr
print('======Init insert start_url into redis[job_spider_start_urls_ch] start')
logging.info('======Init insert start_url into redis[job_spider_start_urls_ch] start')

for url in ChinahrSpider.start_urls:
    insert_into_job_spider(url, 7)

print('======Init insert start_url into redis[job_spider_start_urls_ch] end')
logging.info('======Init insert start_url into redis[job_spider_start_urls_ch] end')

print("======Init spider end")
logging.info("======Init spider end")
