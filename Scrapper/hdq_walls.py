from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time

driver, hrefsList, imgSrcList = webdriver.Chrome(service=Service(ChromeDriverManager().install())), [], []
# driver.get("https://hdqwalls.com/category/nature-wallpapers/1440x2960/page/1")
# time.sleep(6)

def href_scrapper() -> None:
    div_tags_list = driver.find_elements(By.XPATH, """//div[@class="wall-resp col-lg-3 col-md-3 col-sm-4 col-xs-4 column_padding"]""")
    for div_tag in div_tags_list:
        divSoup = BeautifulSoup(div_tag.get_attribute('innerHTML'), "html.parser")
        a_tag = divSoup.find('a')
        if a_tag:
            hrefsList.append(a_tag['href'])

def image_scrapper() -> None:
    for href_link in hrefsList:
        driver.get(href_link)
        time.sleep(2)
        try:
            img = driver.find_element(By.XPATH, '''//img[@class="m_img_holder img-responsive center-block"]''')
        except Exception:
            img = None
        if img:
            imgSrcList.append({'category': 'cars', 'imgSrc': img.get_attribute('src')})

for i in range(38, 55):
    driver.get(f"https://hdqwalls.com/category/cars-wallpapers/1440x2960/page/{i}")
    time.sleep(6)
    href_scrapper()
image_scrapper()
driver.quit()
pd.DataFrame(imgSrcList).to_parquet('dataFiles/cars.parquet', index=False)
