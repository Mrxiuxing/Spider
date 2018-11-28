import urllib.request
from bs4 import BeautifulSoup
import time
import pymysql


# 拼接url并生成请求对象
def handle_request(url, keyword, page):
    url = url.format(keyword, page)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
    }
    request = urllib.request.Request(url=url, headers=headers)
    return request


# 解析并且保存内容
def parse_content(content, db, cursor):
    # 生成soup对象
    soup = BeautifulSoup(content, 'lxml')
    # 解析内容
    odiv = soup.find('div', id='resultList')
    div_list = odiv.find_all('div', class_='el')[1:]
    # 遍历列表 依此获取工作信息
    for div in div_list:
        # 得到职位名称
        jobname = div.select('.t1 > span > a')[0]['title']
        # 得到公司名称
        company = div.select('.t2 > a')[0]['title']
        # 得到工作地点
        area = div.select('.t3')[0].string
        # 薪资水平
        salary = div.select('.t4')[0].string
        # 发布时间
        publish_time = div.select('.t5')[0].string
        # 将这些信息放入字典
        item = {
            'jobname': jobname,
            'company': company,
            'area': area,
            'salary': salary,
            'publish_time': publish_time,
        }
        # 将数据写入数据库
        save_to_mysql(item, db, cursor)


def save_to_mysql(item, db, cursor):
    # 拼接sql语句
    sql = """insert into work(jobname, company, area, salary, publish_time) values('%s', '%s', '%s', '%s', '%s')""" % (
        item['jobname'], item['company'], item['area'], item['salary'], item['publish_time'])
    # 执行sql语句
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()


# 连接数据库, 返回游标
def connect_mysql():
    # 参数host='ip地址', port=端口, user='用户名', password='你的MySQL密码', db='你的数据库', charset='指定字符编码'
    db = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='xxxxxx', db='xxxxxx', charset='utf8')
    cursor = db.cursor()
    return db, cursor


def main():
    # 用户要爬取的关键字
    keyword = input("请输入要爬取的关键字：")
    # 输入起始页码
    start_page = int(input("请输入起始页码："))
    # 输入结束页码
    end_page = int(input("请输入结束页码："))
    # 最原始url
    url = 'https://search.51job.com/list/010000,000000,0000,00,9,99,{},2,{}.html'

    db, cursor = connect_mysql()

    # 循环爬取每一页的工作信息
    for page in range(start_page, end_page + 1):
        print('正在爬取%s页' % page)
        # 根据page和url拼接每一页url，并生成请求对象
        request = handle_request(url, keyword, page)
        # 发送请求得到响应
        content = urllib.request.urlopen(request).read().decode('gbk')
        # 解析响应
        parse_content(content, db, cursor)
        print('结束爬取%s页' % page)
        time.sleep(2)

    # 关闭数据库
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
