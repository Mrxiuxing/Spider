# -*- coding: utf-8 -*-
import scrapy
from fund.items import FundItem


class EastmoneySpider(scrapy.Spider):
    name = 'eastmoney'
    allowed_domains = ['fund.eastmoney.com']
    start_urls = ['http://fund.eastmoney.com/allfund.html']

    def parse(self, response):
        urls = response.xpath('//*[@id="code_content"]/div/ul/li/div/a[1]/@href')
        for url in urls:
            url = response.urljoin(url.extract())
            yield scrapy.Request(url,callback=self.parse_info)
            # print(url)

    def parse_info(self, response):
        item = FundItem()
        try:
            item['code'] = response.xpath('//*[@class="fundcodeInfo"]/span[1]/text()').extract()[0]    # 基金代码
        except:
            item['code'] = response.xpath('//*[@class="fundDetail-tit"]/div/span[2]/text()').extract()[0]
        item['name'] = response.xpath('//*[@class="fundDetail-tit"]/div[1]/text()').extract()[0]     # 基金名称
        item['service_Charge'] = response.xpath('//*[@class="buyWayStatic"]/div[5]/span[2]/span[2]/text()').extract_first('暂停申购')   # 手续费
        item['purchase_amount'] = response.xpath('//*[@id="moneyAmountTxt"]/@data-placeholder').extract_first('暂停申购')    # 起购金额
        try:
            item['recent1Month'] = response.xpath('//*[@class="dataItem01"]/dd[2]/span[2]/text()').extract()[0]     # 最近一月
            item['recent3Month'] = response.xpath('//*[@class="dataItem02"]/dd[2]/span[2]/text()').extract()[0]     # 最近三月
            item['recent6Month'] = response.xpath('//*[@class="dataItem03"]/dd[2]/span[2]/text()').extract()[0]     # 最近六月
            item['recent1Year'] = response.xpath('//*[@class="dataItem01"]/dd[3]/span[2]/text()').extract()[0]     # 最近一年
            item['recent3Year'] = response.xpath('//*[@class="dataItem02"]/dd[3]/span[2]/text()').extract()[0]    # 最近三年
            item['from_Build'] = response.xpath('//*[@class="dataItem03"]/dd[3]/span[2]/text()').extract()[0]    # 成立以来
        except:
            item['recent1Month'] = response.xpath('//*[@class="dataItem01"]/dd[1]/span[2]/text()').extract()[0]
            item['recent3Month'] = response.xpath('//*[@class="dataItem02"]/dd[1]/span[2]/text()').extract()[0]
            item['recent6Month'] = response.xpath('//*[@class="dataItem03"]/dd[1]/span[2]/text()').extract()[0]
            item['recent1Year'] = response.xpath('//*[@class="dataItem01"]/dd[2]/span[2]/text()').extract()[0]
            item['recent3Year'] = response.xpath('//*[@class="dataItem02"]/dd[2]/span[2]/text()').extract()[0]
            item['from_Build'] = response.xpath('//*[@class="dataItem03"]/dd[2]/span[2]/text()').extract()[0]
        item['type'] = response.xpath('//*[@class="infoOfFund"]/table/tr[1]/td[1]/a/text()').extract()[0]
        item['fund_scale'] = response.xpath('//*[@class="infoOfFund"]/table/tr[1]/td[2]/text()').extract()[0].split("：")[1]    # 基金规模
        item['establishment_date'] = response.xpath('//*[@class="infoOfFund"]/table/tr[2]/td[1]/text()').extract()[0].split("：")[1]    # 成立日期
        item['company'] = response.xpath('//*[@class="infoOfFund"]/table/tr[2]/td[2]/a/text()').extract()[0]    # 公司
        yield item
