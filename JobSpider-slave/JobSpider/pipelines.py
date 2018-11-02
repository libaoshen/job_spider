# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from scrapy.exceptions import DropItem


class JobspiderPipeline(object):
    def __init__(self):
        self.file = open('jobs.json', 'wb')

    def process_item(self, item, spider):
        if item['job_name']:
            line = json.dumps(dict(item)) + "\n"
            self.file.write(line.decode('unicode_escape'))
            return item
        else:
            raise DropItem("Missing job_name in %s" % item)
