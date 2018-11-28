import urllib.request
from bs4 import BeautifulSoup
import time
import redis


# 拼接url
def handle_request(url, keyword, page):
    url = url.format(keyword, page)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    }
    request = urllib.request.Request(url=url, headers=headers)
    return request


# 解析并保存内容
def parse_content(content, r):
    # 生成soup对象
    soup = BeautifulSoup(content, 'lxml')
    # 解析内容
    odiv = soup.find('div', id='resultList')
    div_list = odiv.find_all('div', class_='el')[1:]
    # 遍历获取工作的每个信息
    for div in div_list:
        # 得到职位名称
        jobname = div.select('.t1 > span > a')[0]['title']
        # 得到公司名称
        company = div.select('.t2 > a')[0]['title']
        # 得到工作地点
        area = div.select('.t3')[0].string
        # 得到薪资水平
        salary = div.select('.t4')[0].string
        # 得到发布时间
        publish_time = div.select('.t5')[0].string
        # 将这些信息都放到字典中
        item = {
            'jobname': jobname,
            'company': company,
            'area': area,
            'salary': salary,
            'publish_time': publish_time
        }
        # 将item字典写到redis中
        string = str(item)
        r.lpush('work', string)


def main():
    # 让用户输入要爬取的关键字
    keyword = input('请输入要爬取的关键字：')
    # 输入起始页码和结束页码
    start_page = int(input('请输入起始页码：'))
    end_page = int(input('请输入结束页码：'))
    # 最原始的url就是
    url = 'https://search.51job.com/list/010000,000000,0000,00,9,99,{},2,{}.html'

    # 链接redis
    r = redis.Redis(host='127.0.0.1', port=6379, db=0)
    # 循环取每一页的工作信息
    for page in range(start_page, end_page + 1):
        print('正在爬取第%s页。。。。。。' % page)
        # 根据page和url拼接每一页的url，并且生成请求对象
        request = handle_request(url, keyword, page)
        # 发送请求，得到响应
        content = urllib.request.urlopen(request).read().decode('gbk')
        # 保存到数据库中
        parse_content(content, r)
        print('结束爬取第%s页' % page)
        time.sleep(3)


if __name__ == "__main__":
    main()
