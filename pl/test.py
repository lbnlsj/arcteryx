from playwright.async_api import async_playwright
import asyncio


async def run():
    async with async_playwright() as p:
        # 启动浏览器
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # 访问网页
        await page.goto("https://arcteryx.com/ca/en/shop/venta-glove?sub-cat=gloves&sub_categories=Gloves")

        # 截图
        # await page.screenshot(path="example.png")

        # 关闭浏览器
        await browser.close()


# 执行异步任务
asyncio.run(run())
