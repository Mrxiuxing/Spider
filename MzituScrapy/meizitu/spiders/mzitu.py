# -*- coding: utf-8 -*-
import scrapy
from meizitu.items import MeizituItem


class MzituSpider(scrapy.Spider):
    name = 'mzitu'

    # 初始请求
    def start_requests(self):
        start_url = "https://www.mzitu.com/"
        yield scrapy.Request(url=start_url, callback=self.parse)

    # 所有系列
    def parse(self, response):
        for series in response.xpath('//div[@class="postlist"]'):
            url = series.xpath('./ul/li/a/@href').extract_first(' ')
            if url:
                yield scrapy.Request(url, callback=self.parse_info)

        next_series = response.xpath('//div[@class="nav-links"]/a[last()]/@href').extract_first(' ')
        if next_series:
            yield scrapy.Request(url=next_series, callback=self.parse)

    # 获取系列所有图片
    def parse_info(self, response):
        item = MeizituItem()
        item["image_url"] = response.xpath('//div[@class="main-image"]/p/a/img/@src').extract_first()
        item["image_name"] = response.xpath('//h2[@class="main-title"]/text()').extract_first()
        yield item

        next_page = response.xpath('//div[@class="pagenavi"]/a[last()]/@href').extract_first()
        if next_page:
            yield scrapy.Request(next_page, callback=self.parse_info, meta={}, dont_filter=True)
