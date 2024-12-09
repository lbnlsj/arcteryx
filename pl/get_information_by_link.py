import pandas as pd
import requests
import json
import re
import time
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def extract_product_json(html_content):
    try:
        pattern = r'__NEXT_DATA__" type="application/json">(.+?)</script>'
        match = re.search(pattern, html_content)
        if match:
            json_str = match.group(1)
            data = json.loads(json_str)
            product_data = json.loads(data['props']['pageProps']['product'])
            return {
                'name': product_data['name'],
                'variants': product_data['variants'],
                'colors': product_data['colourOptions']['options'],
                'sizes': product_data['sizeOptions']['options'] if product_data['sizeOptions'] else None
            }
    except:
        return None
    return None


def get_stock_info(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers, verify=False, timeout=10)
        if response.status_code == 200:
            return extract_product_json(response.text)
    except requests.exceptions.RequestException as e:
        print(f"Request failed for {url}: {str(e)}")
    except Exception as e:
        print(f"Error processing {url}: {str(e)}")
    return None


def main():
    # 读取CSV文件并去重
    df = pd.read_csv('data.csv')
    unique_urls = df['url'].unique()

    results = []
    for url in unique_urls:
        print(f"Processing {url}")
        info = get_stock_info(url)
        if info:
            # 创建颜色和尺码映射
            color_map = {c['value']: c['label'] for c in info['colors']}
            size_map = {s['value']: s['label'] for s in info['sizes']} if info['sizes'] else {}

            for variant in info['variants']:
                results.append({
                    'url': url,
                    'product_name': info['name'],
                    'color_id': variant['colourId'],
                    'color_name': color_map.get(variant['colourId'], ''),
                    'size_id': variant['sizeId'],
                    'size_name': size_map.get(variant['sizeId'], ''),
                    'inventory': variant['inventory'],
                    'price': variant['price']
                })
        time.sleep(0.1)  # 请求间隔0.1秒

    # 保存结果
    results_df = pd.DataFrame(results)
    results_df.to_csv('result.csv', index=False)
    print("Complete! Results saved to result.csv")


if __name__ == "__main__":
    main()