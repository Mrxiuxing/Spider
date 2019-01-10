import time
import random
import scrapy
from Boos.items import BoosItem


class JobSpider(scrapy.Spider):
    name = 'BoosSpider'
    allowed_domains = ['www.zhipin.com']
    start_urls = ['https://www.zhipin.com/c101010100/h_101010100/?query=python&page=1']

    def parse(self, response):
        all_detail = response.xpath('//div[@class="job-primary"]')
        for detail in all_detail:
            detail_url = detail.xpath('./div/h3[@class="name"]/a/@href').extract_first(' ')
            yield response.follow('https://www.zhipin.com' + detail_url, callback=self.parse_detail)
            time.sleep(random.uniform(5, 10))

        next_page = response.xpath('//div[@class="page"]/a[last()]/@href').extract()[0]
        if next_page is not None:
            yield response.follow('https://www.zhipin.com' + next_page, callback=self.parse)
            time.sleep(random.uniform(5, 10))

    def parse_detail(self, response):
        item = BoosItem()
        try:
            item['position_name'] = response.xpath('//div[@class="name"]/h1/text()').extract_first()
            item['city'] = response.xpath('//div[1]/div/div/div[2]/p/text()[1]').extract_first()[3:]
            item['experience'] = response.xpath('//div[1]/div/div/div[2]/p/text()[2]').extract_first()[3:]
            item['education'] = response.xpath('//div/div/div/div[2]/p/text()[3]').extract_first()[3:]
            item['company_name'] = response.xpath('//div[1]/div/div/div[3]/h3/a/text()').extract_first()
            item['company_scale'] = response.xpath(
                '//*[@id="main"]/div[1]/div/div/div[3]/p[1]/text()[2]').extract_first()
            item['company_industry'] = response.xpath('//div/div/div/div/p[1]/a/text()').extract_first()
            item['company_website'] = response.xpath('//div/div/div/div[3]/p[2]/text()').extract_first()
            item['position_description'] = "".join(
                response.xpath('//div[@class="job-sec"]/div[@class="text"]/text()').extract_unquoted()).strip().strip(
                "[]")
            item['company_introduction'] = response.xpath('//div[3]/div/div[2]/div[3]/div[3]/div/text()') \
                .extract_first().strip()
            item['full_company_name'] = response.xpath('//div/div/div/div/div[5]/div[1]/text()').extract_first().strip()
            item['work_address'] = response.xpath('//div/div/div/div/div[6]/div/div[1]/text()').extract_first()
        except Exception as e:
            pass
        yield item
