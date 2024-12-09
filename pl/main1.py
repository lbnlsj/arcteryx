# import requests
from bs4 import BeautifulSoup
import time
import random
import sqlite3
import datetime
import json
import re
from bs4 import BeautifulSoup
from loguru import logger
from lxml import etree
from curl_cffi import requests

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
BASE_URL = "https://arcteryx.com"
category = []
ERROR_SLEEP_TIME = 8

# response = requests.get('https://ui-components.arcteryx.com/ca/zh/outdoorHeader.js', impersonate="chrome", proxies={'https': 'http://127.0.0.1:7890'})
response = requests.get('https://ui-components.arcteryx.com/ca/zh/outdoorHeader.js', impersonate="chrome")

if response.status_code != 200:
    logger.error('Error getting outdoor list. Program will exit later...')
    input()
    exit()

category_data = list(
    set([d.replace("href:\"", "").replace('"', "") for d in re.findall(r'href:"/c.*?"', response.text)]))
if len(category_data) == 0:
    logger.error('No outdoor category found.')
    input()
    exit()

CATEGORY_URLS = ['https://arcteryx.com/ca/en' + d for d in category_data if d.count('/') > 2]

DB_FILE = 'arcteryx_products.db'


def setup_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            timestamp TEXT,
            email_address TEXT,
            product_name TEXT,
            product_skuid TEXT,
            color TEXT,
            size TEXT,
            quantity INTEGER,
            shipping_id TEXT,
            country TEXT
        )
    ''')
    conn.commit()
    conn.close()


def save_products_to_db(products, email):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    for product in products:
        try:
            cursor.execute('''
                INSERT INTO products (timestamp, email_address, product_name, product_skuid, color, size, quantity, shipping_id, country)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (timestamp, email, product['name'], product['skuid'], product['color'], product['size'], 1, '', 'ca'))
        except sqlite3.Error as e:
            print(f"Database error: {e}")
    conn.commit()
    conn.close()


def get_page_content(url):
    try:
        response = requests.get(url, impersonate="chrome")
        # response = requests.get(url, impersonate="chrome", proxies={'https': 'http://127.0.0.1:7890'})
        return response.text
    except Exception as e:
        logger.warning(f"Error fetching {url}: {e}")
        return None


def get_category_id(content):
    return re.findall('\"categoryId\":\"(.*?)\"', content)[0] if '"categoryId":"' in content else None


def crawl_products():
    setup_database()
    for category_url in CATEGORY_URLS:
        print(f"Crawling category: {category_url}")
        page_content = get_page_content(category_url)

        if page_content:
            category_id = get_category_id(page_content)
            # 应该编写一个爬虫参数，接口get https://pathways.dxpapi.com/api/v2/widgets/keyword/kjyr4dq9? ... 请参考我上传的资料的格式，只需要修改query参数的值为category_id,并且也需要使用代理然后返回结果将结果入库

        time.sleep(random.uniform(0.5, 2.0))


def main():
    crawl_products()


if __name__ == "__main__":
    main()
