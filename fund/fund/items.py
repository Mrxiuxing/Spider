# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FundItem(scrapy.Item):
    code = scrapy.Field()    # 基金代码
    name = scrapy.Field()    # 基金名称
    service_Charge = scrapy.Field()    # 手续费
    purchase_amount = scrapy.Field()    # 起购金额
    recent1Month = scrapy.Field()  # 最近一月
    recent3Month = scrapy.Field()  # 最近三月
    recent6Month = scrapy.Field()  # 最近六月
    recent1Year = scrapy.Field()  # 最近一年
    recent3Year = scrapy.Field()  # 最近三年
    from_Build = scrapy.Field()  # 成立以来
    type = scrapy.Field()    # 基金类型
    fund_scale = scrapy.Field()    # 基金规模
    establishment_date = scrapy.Field()    # 成立日
    company = scrapy.Field()    # 基金公司
