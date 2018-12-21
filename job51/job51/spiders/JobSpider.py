# -*- coding: utf-8 -*-
import scrapy
from job51.items import Job51Item


class JobspiderSpider(scrapy.Spider):
    name = 'JobSpider'
    allowed_domains = ['51job.com']

    def start_requests(self):
        start_requests = "https://search.51job.com/list/010000,000000,0000,00,9,99,python,2,1.html"
        yield scrapy.Request(url=start_requests, callback=self.parse_job_info)

    def parse(self, response):
        next_page = response.xpath('//div/ul/li[@class="bk"][2]/a/@href').extract_first(' ')
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse_job_info)

    def parse_job_info(self, response):
        item = Job51Item()
        for echo in response.xpath('//div[@class="el"]')[4:]:
            item["position_name"] = echo.xpath('./p/span/a/@title').extract_first()
            item["company"] = echo.xpath('./span[@class="t2"]/a/text()').extract_first()
            item["address"] = echo.xpath('./span[@class="t3"]/text()').extract_first()
            item["salary"] = echo.xpath('./span[@class="t4"]/text()').extract_first()
            item["time"] = echo.xpath('./span[@class="t5"]/text()').extract_first()
            yield item
        yield scrapy.Request(url=response.url, callback=self.parse, meta={}, dont_filter=True)
