# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# import json
import csv
import pymongo


# 以CSV文件存入
class Job51Pipeline(object):
    def __init__(self):
        self.csvwriter = csv.writer(open("51job.csv", "a", encoding='utf-8', newline=''), delimiter=',')
        self.csvwriter.writerow(["position_name", "company", "address", "salary", "time"])  # 指定列名

    # 以json文件存入
    # def process_item(self, item, spider):
    #     with open('51job.json', 'a') as f:
    #         json.dump(dict(item), f, ensure_ascii=False)
    #         f.write(',\n')
    #     return item

    # CSV
    def process_item(self, item, spider):
        self.csvwriter.writerow((item["position_name"], item["company"], item["address"], item["salary"], item["time"]))
        return item


# 存入MongoDB
class MongoPipeline(object):
    def __init__(self):
        client = pymongo.MongoClient('127.0.0.1', 27017)
        db = client['51Job_db']  # 指定库 （自动创建）
        self.post = db['51job']  # 指定表 （自定创建）

    def process_item(self, item, spider):
        postItem = dict(item)
        self.post.insert(postItem)
        return item
