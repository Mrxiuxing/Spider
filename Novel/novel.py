import re
import requests
from lxml import etree
from bs4 import BeautifulSoup
import time


class NovelSpider:
    # 初始化
    def __init__(self):
        self.start_url = 'http://www.biquyun.com/16_16288/'  # 在笔趣阁搜索找到指定小说的url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
        }

    # 爬取传入url的网页
    def get_html(self, url):
        return requests.get(url=url, headers=self.headers).content

    # 获取小说所有章节的url
    def chapter_url_list(self):
        html = self.get_html(self.start_url)
        tree = etree.HTML(html)
        url_list = tree.xpath('//div/dl/dd/a/@href')
        novel_name = tree.xpath('//div[@class="box_con"]/div/div/h1/text()')[0]
        return url_list, novel_name

    def main(self):
        url_list, novel_name = self.chapter_url_list()
        # 遍历url拼接完整url
        count = 0
        for url in url_list:
            full_url = "http://www.biquyun.com" + url
            # print(full_url)
            novel_html = self.get_html(full_url)
            soup = BeautifulSoup(novel_html, 'lxml')
            content = soup.select("#content")[0].text
            tree = etree.HTML(novel_html)
            title = tree.xpath('//div[@class="bookname"]/h1/text()')[0]
            # 写入文件
            with open('{}.txt'.format(novel_name), 'a', encoding="utf") as f:
                f.write(title + "\n" + str(content) + '\n\n')
                count += 1
                # print("\r正在保存...{}当前进度: {:.2f}%".format(title, count * 100 / len(url_list)), end="")
                print("\r正在保存...{}\n当前进度: {:.2f}%".format(title, count * 100 / len(url_list)), end="")


if __name__ == "__main__":
    novel = NovelSpider()
    novel.main()
