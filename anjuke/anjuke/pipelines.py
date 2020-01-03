# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime

import pymongo

from anjuke.items import Anjuke_fy_rent2, Anjuke_xq_sale


class AnjukePipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPipeline(object):
    def __init__(self, host='localhost', port=27017, db='main', user=None, password=None):
        self.mongo_db = pymongo.MongoClient(
            host=host,
            port=port
        )[db]
        if user:
            self.mongo_db.authenticate(user, password)

    @classmethod
    def from_crawler(cls, engine):
        return cls(
            host=engine.settings.get('MONGO_HOST'),
            port=engine.settings.get('MONGO_PORT'),
            db=engine.settings.get('MONGO_DB'),
            user=engine.settings.get('MONGO_USER'),
            password=engine.settings.get('MONGO_PWD')
        )

    def process_item(self, item, spider):
        collection_name = item.__class__.__name__
        item['create_time'] = datetime.now()
        if collection_name == Anjuke_fy_rent2.__name__:
            if self.mongo_db[collection_name].find_one({'link': item['link']}) is None:
                self.mongo_db[collection_name].insert(dict(item))
        elif collection_name == Anjuke_xq_sale.__name__:
            if self.mongo_db[collection_name].find_one({'url': item['url']}) is None:
                self.mongo_db[collection_name].insert(dict(item))
        else:
            self.mongo_db[collection_name].insert(dict(item))
        return item
