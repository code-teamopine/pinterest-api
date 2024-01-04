from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time

driver, hrefsList, imgSrcList = webdriver.Chrome(service=Service(ChromeDriverManager().install())), [], []
driver.get("https://wallspic.com/album/motorcycles/1440x2960")
time.sleep(6)

def scrolller() -> None:
    all_data_a_list = driver.find_elements(By.XPATH, """//a[@class="gallery_fluid-column-block"]""")
    for data_div in all_data_a_list:
        if data_div.get_attribute('href') not in hrefsList:
            hrefsList.append(data_div.get_attribute('href'))
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(5)

def image_scrapper() -> None:
    for href_link in hrefsList:
        driver.get(href_link)
        time.sleep(4)
        div_tag = None
        try:
            div_tag = driver.find_element(By.XPATH, """//div[@class="wallpaper__image__desktop"]""")
        except Exception as e:
            print(e, href_link)
        if div_tag:
            divSoup = BeautifulSoup(div_tag.get_attribute('innerHTML'), "html.parser")
            imgTag = divSoup.find('img')
            if imgTag:
                print(imgTag['src'])
                imgSrcList.append({"category": 'motorcycles', "imgSrc": imgTag['src']})

scrolller()
scrolller()
scrolller()
scrolller()
scrolller()
image_scrapper()
pd.DataFrame(imgSrcList).to_parquet('dataFiles/motorcycles.parquet', index=False)
driver.quit()
