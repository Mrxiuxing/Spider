import time
import pymongo
from selenium import webdriver
from pyquery import PyQuery as pq
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LagouSpider:
    # 初始化
    def __init__(self):
        self.data = list()
        self.isEnd = False
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        self.browser = webdriver.Chrome(chrome_options=chrome_options)
        self.wait = WebDriverWait(self.browser, 10)
        self.browser.get('https://www.lagou.com/')
        # 首页弹窗模拟点击
        index_tab = self.browser.find_element_by_xpath('//*[@id="changeCityBox"]/ul/li[1]/a')
        index_tab.click()
        input_search = self.browser.find_element_by_id('search_input')    # 搜索框
        input_search.send_keys('Python')    # 在搜索框输入职位名称
        time.sleep(1)
        button = self.browser.find_element_by_class_name('search_button')    # 搜索按钮
        button.click()    # 模拟点击
        client = pymongo.MongoClient('localhost')
        db = client.lagou
        self.collection = db.Python

    # 解析网页数据
    def parse_page(self):
        try:
            doc = pq(self.browser.page_source)
            items = doc('#s_position_list .item_con_list .con_list_item').items()
            for item in items:
                money_experience_educational = item.find('.position .p_bot .li_b_l').text().split(' ')
                product = [{
                    "position": item.find('.p_top .position_link h3').text(),
                    "city": item.find('.position .p_top .add em').text(),
                    "money": money_experience_educational[0],
                    "experience": money_experience_educational[1],
                    "educational": money_experience_educational[3],
                    "company": item.find('.company .company_name a').text(),
                }]
                self.data.extend(product)
        except:
            time.sleep(3)
            self.parse_page()

    # 翻页操作
    def turn_page(self):
        if pq(self.browser.page_source)('.pager_container span:last-child').attr('class') != 'pager_next pager_next_disabled':
            pager_next = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'pager_next')))
            pager_next.click()
            time.sleep(2)
        else:
            self.isEnd = True

    # 职位详情页弹窗
    def body_btn(self):
        try:
            body_btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.body-btn')))
            if body_btn:
                body_btn.click()
                time.sleep(3)
        except:
            pass

    # 储存至MongoDB
    def save_to_mongo(self):
        try:
            for item in self.data:
                if self.collection.update_one(item, {"$setOnInsert": item}, True):
                    pass
            print('储存到MongoDB成功')
        except Exception:
            print('储存到MongoDB失败')

    # 爬取数据
    def crawl(self):
        while not self.isEnd:
            page = self.browser.find_element_by_class_name('pager_is_current').text
            print('正在爬取第 ' + page + ' 页 ...')
            try:
                showData = self.browser.find_element_by_css_selector('[class="body-container showData"]')
            except:
                showData = False
            if showData:
                self.body_btn()
            self.parse_page()
            self.turn_page()
        self.browser.close()
        self.save_to_mongo()
        print('爬取结束')


if __name__ == '__main__':
    obj = LagouSpider()
    obj.crawl()