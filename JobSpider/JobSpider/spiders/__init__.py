# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
from JobSpider.utils.redis import insert_into_job_spider
from zhilian_spider import ZhilianSpider
print('======Init insert start_url into redis[job_spider_start_urls_zl] start')
for url in ZhilianSpider.start_urls:
    insert_into_job_spider(url, 1)
print('======Init insert start_url into redis[job_spider_start_urls_zl] end')