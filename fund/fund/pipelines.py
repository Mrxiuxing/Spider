# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv
from fund.items import FundItem


class ToCSVPipeline(object):
    def __init__(self):
        self.f = open("fund.csv", "a", encoding='utf-8', newline="")
        # 设置表头，要跟spider传过来的字典key名称相同
        self.fieldnames = ["code", "name", "service_Charge", "purchase_amount", "recent1Month", "recent3Month", "recent6Month",
                           "recent1Year", "recent3Year", "from_Build", "type", "fund_scale", "establishment_date", "company"]
        self.writer = csv.DictWriter(self.f, fieldnames=self.fieldnames)
        self.writer.writeheader()

    def process_item(self, item, spider):
        self.writer.writerow(item)
        return item

    def close(self, spider):
        self.f.close()
