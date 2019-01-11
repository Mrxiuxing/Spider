import csv
import json
import pymongo


# 以CSV文件存入
class CSVPipeline(object):

    def __init__(self):
        self.csvwriter = csv.writer(open("Boos_job.csv", "a", encoding='utf-8', newline=''), delimiter=',')
        self.csvwriter.writerow(["position_name", "city", "experience", "education", "company_name", "company_scale",
                                 "company_industry", "company_website", "position_description", "company_introduction",
                                 "full_company_name", "work_address"])  # 指定列名

    def process_item(self, item, spider):
        self.csvwriter.writerow(
            (item["position_name"], item["city"], item["experience"], item["education"], item["company_name"],
             item["company_scale"], item["company_industry"], item["company_website"], item["position_description"],
             item["company_introduction"], item["full_company_name"], item["work_address"])
        )
        return item


# 以JSON形式储存
class JSONPipeline(object):
    def process_item(self, item, spider):
        with open('%s.json' % spider.name, 'a', encoding='utf-8') as f:
            json.dump(dict(item), f, ensure_ascii=False)
            f.write(',\n')
        return item


# 存入MongoDB
class MongoPipeline(object):
    def __init__(self):
        client = pymongo.MongoClient('127.0.0.1', 27017)
        db = client['Boos_db']  # 指定库 （自动创建）
        self.post = db['Boos_job']  # 指定表 （自定创建）

    def process_item(self, item, spider):
        postItem = dict(item)
        self.post.insert(postItem)
        return item
