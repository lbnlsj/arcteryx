import requests
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

    # 删除旧表（如果存在）以确保表结构正确
    cursor.execute('DROP TABLE IF EXISTS products')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            category TEXT,              
            pid TEXT,
            title TEXT,
            description TEXT,
            gender TEXT,
            price_ca REAL,
            discount_price_ca REAL,
            rating REAL,
            review_count INTEGER,
            is_new TEXT,
            is_pro TEXT,
            is_revised TEXT,            
            slug TEXT,
            thumb_image TEXT,
            hover_image TEXT,
            analytics_name TEXT,        
            variants TEXT,              
            colour_images_map_ca TEXT
        )
    ''')
    conn.commit()
    conn.close()


def save_products_to_db(products, category):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    for product in products:
        try:
            cursor.execute('''
                INSERT INTO products (
                    timestamp, category, pid, title, description, gender,
                    price_ca, discount_price_ca, rating, review_count,
                    is_new, is_pro, is_revised, slug, thumb_image, hover_image,
                    analytics_name, variants, colour_images_map_ca
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                timestamp,
                category,
                product.get('pid'),
                product.get('title'),
                product.get('description'),
                product.get('gender'),
                product.get('price_ca'),
                product.get('discount_price_ca'),
                product.get('rating'),
                product.get('review_count'),
                product.get('is_new'),
                product.get('is_pro'),
                product.get('is_revised'),
                product.get('slug'),
                product.get('thumb_image'),
                product.get('hover_image'),
                product.get('analytics_name'),
                json.dumps(product.get('variants', [])),
                json.dumps(product.get('colour_images_map_ca', []))
            ))
        except sqlite3.Error as e:
            logger.error(f"Database error: {e}")
            logger.error(f"Failed product data: {product}")

    conn.commit()
    conn.close()


def get_page_content(url):
    try:
        response = requests.get(url, impersonate="chrome")
        return response.text
    except Exception as e:
        logger.warning(f"Error fetching {url}: {e}")
        return None


def get_category_id(content):
    return re.findall('\"categoryId\":\"(.*?)\"', content)[0] if '"categoryId":"' in content else None


def get_products_data(category_id, url):
    try:
        # 从URL中提取wid参数
        wid_match = re.search(r'wid-(\w+)', url)
        wid = wid_match.group(1) if wid_match else 'kjyr4dq9'

        # 构造请求参数
        params = {
            'account_id': '7358',
            'domain_key': 'arcteryx',
            'fields': 'analytics_name,collection,colour_images_map,colour_images_map_ca,description,discount_price_ca,gender,hover_image,is_new,is_pro,is_revised,price_ca,pid,review_count,rating,slug,title,thumb_image',
            '_br_uid_2': 'uid=3912684450179:v=15.0:ts=1729444508809:hc=36',
            'ref_url': 'https://arcteryx.com/ca/en',
            'url': url,
            'request_id': str(int(time.time() * 1000)),
            'rows': '200',
            'start': '0',
            'view_id': 'ca',
            'query': category_id
        }

        response = requests.get(
            f'https://pathways.dxpapi.com/api/v2/widgets/keyword/{wid}',
            params=params,
            impersonate="chrome"
        )

        if response.status_code == 200:
            data = response.json()
            return data.get('response', {}).get('docs', [])
        return []

    except Exception as e:
        logger.error(f"Error fetching products data: {e}")
        return []


def crawl_products():
    setup_database()
    for category_url in CATEGORY_URLS:
        logger.info(f"Crawling category: {category_url}")
        page_content = get_page_content(category_url)

        if page_content:
            category_id = get_category_id(page_content)
            if category_id:
                products = get_products_data(category_id, category_url)
                if products:
                    save_products_to_db(products, category_url)
                    logger.success(f"Saved {len(products)} products from {category_url}")
                else:
                    logger.warning(f"No products found for category: {category_url}")
            else:
                logger.warning(f"No category ID found for: {category_url}")

        time.sleep(random.uniform(0.5, 2.0))


def main():
    crawl_products()


if __name__ == "__main__":
    main()