# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import datetime

today = datetime.datetime.now()
print("====== [{}-{}-{} {}:{}:{}]JobSpider-slave start ======"
      .format(today.year, today.month, today.day, today.hour, today.minute, today.second))