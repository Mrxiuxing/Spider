import requests
from lxml import etree
from bs4 import BeautifulSoup
import time
import os

url = 'https://www.mzitu.com/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
    'Referer': 'https://www.mzitu.com/',  # 因为网站有防盗链所有需要加上这条
}


# 获取所有系列url并添加至列表
def get_all_index_url():
    content = requests.get(url, headers=headers).content
    tree = etree.HTML(content)
    page = int(tree.xpath('//div[@class="nav-links"]/a[last()-1]/text()')[0])  # 共有多少页
    a_lists = []
    for p in range(1, page + 1):
        all_index_url = url + 'page/%s/' % p  # 获取首页所有系列的url
        content2 = requests.get(all_index_url, headers=headers).text
        tree2 = etree.HTML(content2)
        a_list = tree2.xpath('//div[@class="main"]/div/div[2]/ul/li/a//@href')  # 每一页又有多少系列
        for a in a_list:
            a_lists.append(a)
    return a_lists


# 获取所有系列页码并添加至列表中
def get_all_page():
    all_url = get_all_index_url()
    page_list = []
    for url in all_url:
        content = requests.get(url, headers=headers).text
        tree = etree.HTML(content)
        # 每一页又有多少页图片
        page = int(tree.xpath('//div[@class="pagenavi"]/a[last()-1]/span/text()')[0])
        page_list.append(page)
    return (page_list)


# 获取所有系列图片
def get_photo():
    url_list = get_all_index_url()
    page_list = get_all_page()
    length = len(page_list)
    for l in range(length):
        url = url_list[l]
        for p in range(int(page_list[l])):
            u = url + '/%s' % str(p + 1)
            content = requests.get(u, headers=headers).text
            tree = etree.HTML(content)
            try:
                photo_url = tree.xpath('//div[@class ="main-image"]/p/a/img//@src')[0]
                photo_name = tree.xpath('//h2[@class="main-title"]/text()')[0] + '.' + str(photo_url).split('.')[-1]

                print('正在下载--%s' % photo_name)
                photo = requests.get(photo_url, headers=headers).content
                dirname = '妹子图'
                if not os.path.exists(dirname):
                    os.mkdir(dirname)
                photo_path = os.path.join(dirname, photo_name)

                if not os.path.exists(photo_path):
                    with open(photo_path, 'wb') as f:
                        f.write(photo)
                        print('下载完成%s' % photo_name)
            except Exception as e:
                pass


if __name__ == "__main__":
    get_photo()
