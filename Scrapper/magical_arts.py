from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time

driver, hrefsList, imgSrcList = webdriver.Chrome(service=Service(ChromeDriverManager().install())), [], []
driver.get("https://www.magicals.art/search/label/Cute%20Friends")
time.sleep(6)

def scrolller() -> None:
    try:
        all_data_a_list = driver.find_elements(By.XPATH, """//a[@class="thmb"]""")
        for a_tag in all_data_a_list:
            aSoup = BeautifulSoup(a_tag.get_attribute('innerHTML'), "html.parser")
            img_tag = aSoup.find('img')
            if img_tag:
                imgSrcList.append({"category": 'winter', "imgSrc": img_tag['data-src'].replace('w1620', 'w1440-h2560')})
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        driver.get(driver.find_element(By.XPATH, """//a[@class="olLnk"]""").get_attribute('href'))
        time.sleep(6)
    except Exception as e:
        print("\n\n", e, "\n\n")

scrolller()
scrolller()
scrolller()
scrolller()
scrolller()
scrolller()
scrolller()

driver.get("https://www.magicals.art/search/label/Night")
time.sleep(6)
scrolller()
scrolller()
scrolller()

driver.get("https://www.magicals.art/search/label/Old%20Couples")
time.sleep(6)
scrolller()
pd.DataFrame(imgSrcList).to_parquet('dataFiles/couple.parquet', index=False)
driver.quit()
