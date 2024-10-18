import asyncio
from pyppeteer import launch
from bs4 import BeautifulSoup

async def get_page_content(page):
    response = await page.content()
    soup = BeautifulSoup(response, "html.parser")
    return soup

async def main():
    browser = await launch(headless=False)
    page = await browser.newPage()
    
    await page.goto('https://exhibitors.informamarkets-info.com/event/CA2024/en-US/', waitUntil='networkidle0')

    await page.click("button.btn.dropdown-toggle.btn-default[data-id='cmbCountry']")

    await page.click("#divSearchFilter > div:nth-child(1) > div:nth-child(1) > div > div > ul > li:nth-child(20)")

    page_html = await get_page_content(page)

    url_element = page_html.select("#dtSearch > tbody > div > div > a.card-image")

    print(url_element)

    await asyncio.sleep(1000)

    # 브라우저 종료
    await browser.close()

# 비동기 함수 실행
asyncio.get_event_loop().run_until_complete(main())