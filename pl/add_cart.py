from curl_cffi import requests
# import requests
import re
import time

URI = 'https://arcteryx.com/api/mcgql'
session = requests.Session()


def get_product_page():
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-encoding': 'gzip, deflate, br, zstd', 'accept-language': 'en-US,en;q=0.9', 'priority': 'u=0, i',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"', 'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"', 'sec-fetch-dest': 'document', 'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none', 'sec-fetch-user': '?1', 'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'}
    response = session.get('https://arcteryx.com/us/en/shop/micon-32-backpack?sub-cat=daypacks&sub_categories=Daypacks',
                           headers=headers)
    print(re.search('<title>.*?</title>', response.text)[0])
    return True


def t():
    get_product_page()
    # 创建卡片
    data = {
        "query": "query getCart($cartId: String!) { cart(cart_id: $cartId) { email id total_quantity items { id quantity arc_original_country_price is_available prices { price { value currency } discounts { label amount { value currency } } } product { sku slug name marketingname marketingnameenglish productcollectioncode is_returnable isfootwear gendercode isnewsizing } ... on ConfigurableCartItem { configured_variant { sku upc color_data size_data quantity_available productimage } } } applied_coupons { code } discount_notice prices { grand_total { value currency } subtotal_excluding_tax { value currency } subtotal_including_tax { value currency } merged_taxes { amount { value currency } label percent } discounts { label amount { value currency } } } } }",
        "variables": {"cartId": "aMwJDn9xDw4CnxUPDO0TSSjEYF3ZiOiv"}}
    # 添加商品
    # data = {
    #     "query": "mutation addConfigurableProductsToCart( $cartId: String! $preSku: String! $preParentSku: String! $quantity: Float! ) { addConfigurableProductsToCart( input: { cart_id: $cartId cart_items: [{ parent_sku: $preParentSku, data: { quantity: $quantity, sku: $preSku } }] } ) { cart { email id total_quantity items { id quantity arc_original_country_price is_available prices { price { value currency } discounts { label amount { value currency } } } product { sku slug name marketingname marketingnameenglish productcollectioncode is_returnable isfootwear gendercode isnewsizing } ... on ConfigurableCartItem { configured_variant { sku upc color_data size_data quantity_available productimage } } } discount_notice applied_coupons { code } prices { grand_total { value currency } subtotal_excluding_tax { value currency } subtotal_including_tax { value currency } merged_taxes { amount { value currency } label percent } discounts { label amount { value currency } } } } } }",
    #     "variables": {"cartId": "70KgV5rfNJylMupToGa1inYtq2wmIinC", "preParentSku": "X000007518",
    #                   "preSku": "X000007518008", "quantity": 1}}
    st = int(time.time() * 1000)
    headers = {'accept': '*/*', 'accept-encoding': 'gzip, deflate, br, zstd', 'accept-language': 'en-US,en;q=0.9',
               'content-length': '1104', 'content-type': 'application/json',
               # 'cookie': '_pxhd=12458dc57fe7f880635f2ba179a5ad2b57c40f69c7447d307d30020a8029a074:1c501cbc-a991-11ef-a7e3-bf30dde3db9e; _vid=fc712293-b46b-4c80-83f9-80fd4c3e4588; enableClickAndCollectCA=true; enableClickAndCollectUS=true; enableEnhancedAssets=true; _pxvid=1cc49662-a991-11ef-897e-12d4254d0e1d; s_ecid=MCMID%7C40321520137041527420777044221788066483; AMCVS_DFBF2C1653DA80920A490D4B%40AdobeOrg=1; AMCV_DFBF2C1653DA80920A490D4B%40AdobeOrg=179643557%7CMCIDTS%7C20051%7CMCMID%7C40321520137041527420777044221788066483%7CMCAID%7CNONE%7CMCOPTOUT-1732369820s%7CNONE%7CMCAAMLH-1732967420%7C3%7CMCAAMB-1732967420%7Cj8Odv6LonN4r3an7LhD3WZrU1bUpAkFkkiY1ncBR96t2PTI%7CMCSYNCSOP%7C411-20058%7CvVersion%7C5.5.0; _hjSessionUser_33114=eyJpZCI6IjAyZjQyODI4LTA2MjYtNTYxOC04MzQ4LTE0N2U4NGZlMGRkNiIsImNyZWF0ZWQiOjE3MzIzNjI2MjEyMzYsImV4aXN0aW5nIjp0cnVlfQ==; _hjSession_33114=eyJpZCI6ImMxZGZjMzhjLTdjYTUtNDY2Zi04ODcwLTMzZmE3MjY4ZDJjNCIsImMiOjE3MzIzNjI2MjEyMzcsInMiOjEsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MX0=; OptanonAlertBoxClosed=2024-11-23T11:50:22.840Z; country=ca; language=en; _fbp=fb.1.1732362625224.835676887652721833; s_cc=true; _pin_unauth=dWlkPU1qaGxaRFUyTmpJdE1EUm1OeTAwTlRBd0xUazRaR0V0WmprM09UZGtNR0U0T0Roaw; _gcl_au=1.1.852808159.1732362626; _gid=GA1.2.986209617.1732362626; IR_gbd=arcteryx.com; _evga_a7e2={%22uuid%22:%223a6442ff807f8942%22}; IR_PI=2200940c-a991-11ef-9cd5-fb242484c82e%7C1732362627499; bounceClientVisit4468v=N4IgNgDiBcIBYBcEQM4FIDMBBNAmAYnvgIYBOAxggKakCeAHgHTkD2AtkecUVQHadkEIADQhSMECJABLFAH0A5izkoqKFNJa8YAM2JhVo2Yogq1Grbv2qAvkA; _tt_enable_cookie=1; _ttp=j_66bCmYB7JnLgh_yvFiqX0ObgT.tt.1; _scid=WTAPyAdR2UJpbtd7lZANvYJFy0Nsah7v; _ScCbts=%5B%5D; OptanonConsent=isGpcEnabled=0&datestamp=Sat+Nov+23+2024+19%3A50%3A30+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=202410.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=17293613-a310-47a3-bd62-0005d7caf91e&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&intType=1&geolocation=US%3BWA&AwaitingReconsent=false; _sctr=1%7C1732291200000; enableOutletFlashSaleModal=false; BVBRANDID=72155afb-b4f2-4b5c-a31f-c892ef0a0ca6; BVBRANDSID=d29f7734-1d1a-41f7-a845-dbb492531811; _sfid_836c={%22anonymousId%22:%223a6442ff807f8942%22%2C%22consents%22:[]}; __olapicU=1732362722025; prevPageType=product-page; forterToken=079e71820b704e528ec4981390710e47_1732362766096__1i_21ck; facebookConversionGuid={%22viewContentGuid%22:%22f90ddbbf-c546-a29e-6c23-7ca0aca22c0b%22%2C%22pageViewGuid%22:%22f914f873-3878-a8db-284d-bfd28ba2b737%22%2C%22addToCartGuid%22:%22bbc9e430-ecca-65b9-bafe-79db36c819e0%22}; _scid_r=Y7APyAdR2UJpbtd7lZANvYJFy0Nsah7vUIga_Q; _br_uid_2=uid%3D3808822159356%3Av%3D15.0%3Ats%3D1732362724313%3Ahc%3D2; _ga_84KZ7F7FWP=GS1.1.1732362626.1.1.1732362767.10.0.0; _ga=GA1.2.940640004.1732362626; IR_24493=1732362766381%7C5531554%7C1732362766381%7C%7C; _uetsid=20b24690a99111ef879b19d83af03282; _uetvid=20b28c10a99111ef9f8fa34e823697d5; _rdt_uuid=1732362626009.b47cdb31-d3a3-4ff0-b970-e6d7b3e88903; private_content_version=5a8e8d3f29e6e2821cc4b6da82f930db; KP_UIDz-ssn=02TsxPFAzvtqTm7CLcJytWaaAOq1Tf7NHKyOaH1QS5vpJcrPe0GWjY2JjJnsz3USodYkpZQ666eVw3rmkdBs8iReOw8rQSiDQMHPZKlvQA6bjiDb9keJI6dRgFuNaaw0wyRtGROzoKYBR6eqDYubhUFuhfim9WizbKIgWIje8D; KP_UIDz=02TsxPFAzvtqTm7CLcJytWaaAOq1Tf7NHKyOaH1QS5vpJcrPe0GWjY2JjJnsz3USodYkpZQ666eVw3rmkdBs8iReOw8rQSiDQMHPZKlvQA6bjiDb9keJI6dRgFuNaaw0wyRtGROzoKYBR6eqDYubhUFuhfim9WizbKIgWIje8D; CartCount-OUTDOOR=0; _ga_N8XJLJFM2Z=GS1.1.1732362625.1.1.1732363208.35.0.0; bounceClientVisit4468=N4Igzg7gbiBcBmBDANmApgGhAEwJbbhAHYBOAVgAYKiAWCgZgDYmAOGxsygJhCynzgBGIvS5MujLiTqCuNFnzig0UNACcA+sgD2Ac11psG3ADs4SVJhABjRGoAuGqCgCuaOBSxgXAIwC2uPb2hhraJmCB7ggo6Fi4AA7q1mjx9rhh5jFoAL5Y8FD2QiJikkREgliI2kJYyPGEABZB8WAApPQAgq1cAGLdPXbWwWoAngAeAHTW2n79tv1oJnN2hZVgNSBQ8TCw9FgEsDi8IGqEx9YFRaLikiReArCCCiC61qe7dyB+HrWXj8VMUSCTw2RB+eKIXC6cJKEBcFiCEgUQSMWFQHZcX6Ff7XUrw2qIfgHYS4iRSGRyZ7IRBXEpcIj4kCEjbwMA0nF0hnPRDrR6Vap8kDadkAbRJnPhAF04gKKiAIBdaeIRCCFUrSvQKLk4QikRI0TsQcg-uLAVxgdlLUA; s_sq=arctprod%3D%2526c.%2526a.%2526activitymap.%2526page%253Dproduct%25257Cneutral%25257Cmicon-32-backpack%2526link%253DAdd%252520to%252520cart%2526region%253Dcontent%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c%2526pid%253Dproduct%25257Cneutral%25257Cmicon-32-backpack%2526pidt%253D1%2526oid%253DfunctionBf%252528%252529%25257B%25257D%2526oidt%253D2%2526ot%253DSUBMIT',
               'origin': 'https://arcteryx.com', 'priority': 'u=1, i',
               'referer': 'https://arcteryx.com/ca/en/shop/micon-32-backpack?sub-cat=daypacks&sub_categories=Daypacks',
               'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
               'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"macOS"', 'sec-fetch-dest': 'empty',
               'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-origin', 'store': 'arcteryx_en',
               'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
               'x-country-code': 'ca', 'x-is-checkout': 'false', 'x-jwt': '',
               # workTime 大概比st晚15s左右 都是北京时间 rst比st快54ms
               'x-kpsdk-cd': '{"workTime":' + str(
                   st + 15 * 1000 - 56) + ',"id":"54f28d997a376fa123aef1234bc02f12","answers":[2,1],"duration":0.2,"d":-54,"st":' + str(
                   st) + ',"rst":' + str(st - 54) + '}', 'x-kpsdk-ct': ''}
    response = requests.post(URI, headers=headers, json=data, proxies={'https': 'http://127.0.0.1:7890'})
    print()


if __name__ == '__main__':
    t()
