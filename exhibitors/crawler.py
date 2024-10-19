import asyncio
import os
import requests
from pyppeteer import launch
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def download_image(img_url, folder_path, file_name):
    try:
        response = requests.get(img_url)
        response.raise_for_status() 

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        safe_file_name = "".join([c if c.isalnum() else "_" for c in file_name]) + ".jpg"

        file_path = os.path.join(folder_path, safe_file_name)

        with open(file_path, 'wb') as img_file:
            img_file.write(response.content)

        print(f"Image saved to: {file_path}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download image: {e}")

async def get_page_content(page):
    response = await page.content()
    soup = BeautifulSoup(response, "html.parser")
    return soup

async def main():
    base_url = 'https://exhibitors.informamarkets-info.com'
    desktop_folder = os.path.join(os.path.expanduser("~"), "Desktop", "downloadedImages") 

    browser = await launch(headless=False)
    page = await browser.newPage()
    
    await page.goto('https://exhibitors.informamarkets-info.com/event/CA2024/en-US/', waitUntil='networkidle0')

    await page.click("button.btn.dropdown-toggle.btn-default[data-id='cmbCountry']")

    await page.click("#divSearchFilter > div:nth-child(1) > div:nth-child(1) > div > div > ul > li:nth-child(20)")

    page_html = await get_page_content(page)

    url_elements = page_html.select("#dtSearch > tbody > div > div > a.card-image")

    for element in url_elements:
        href = element['href']

        full_url = urljoin(base_url, href)

        await page.goto(full_url, waitUntil='networkidle0')

        new_page_html = await get_page_content(page)

        brand_img = new_page_html.select_one("#post-2 > div > div > div > div.container.brand > div.ExhibitorPageContent.row > div.col-xs-12.col-sm-6.col-md-4 > div:nth-child(1) > a > img")['src']
        brand_name = new_page_html.select_one("#post-2 > div > div > div > div.container.brand > div.ExhibitorPageContent.row > div.col-xs-12.col-sm-6.col-md-4 > div.name.flex-grow.sorting_1 > h4 > a").get_text(strip=True)
        brand_hall = new_page_html.select("#StandNo")[0].get_text(strip=True)
        brand_stand = new_page_html.select("#StandNo")[1].get_text(strip=True)
        brand_phone = new_page_html.select_one("#ContactPhone").get_text(strip=True)
        brand_url = new_page_html.select_one("#post-2 > div > div > div > div.container.brand > div.ExhibitorPageContent.row > div.col-xs-12.col-sm-6.col-md-4 > div.row-visit-website-button > a")["href"]

        print(brand_img)
        print(brand_name)
        print(brand_hall)
        print(brand_stand)
        print(brand_phone)
        print(brand_url)

        download_image(brand_img, desktop_folder, brand_name)

    await asyncio.sleep(1000)

    # 브라우저 종료
    await browser.close()

# 비동기 함수 실행
asyncio.get_event_loop().run_until_complete(main())