# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BossItem(scrapy.Item):
    position_name = scrapy.Field()  # 职位名称
    city = scrapy.Field()  # 城市
    experience = scrapy.Field()  # 经验
    education = scrapy.Field()  # 教育程度
    company_name = scrapy.Field()  # 公司名称
    company_scale = scrapy.Field()  # 公司规模
    company_industry = scrapy.Field()  # 公司所处行业
    company_website = scrapy.Field()  # 公司网站
    position_description = scrapy.Field()  # 职位描述
    company_introduction = scrapy.Field()  # 公司介绍
    full_company_name = scrapy.Field()  # 公司全名
    work_address = scrapy.Field()  # 工作地址
