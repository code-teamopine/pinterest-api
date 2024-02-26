from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time

driver, hrefsList, imgSrcList = webdriver.Chrome(service=Service(ChromeDriverManager().install())), [], []
driver.get("https://in.pinterest.com/")
time.sleep(6)


def mainScrapper(category):
    driver.get(f'https://in.pinterest.com/search/pins/?q={category}&rs=typed')
    time.sleep(5)

    def getHref():
        dataList = driver.find_elements(By.XPATH, """//div[@data-test-id="pinRepPresentation"]""")
        for data in dataList:
            dataSoup = BeautifulSoup(data.get_attribute('innerHTML'), "html.parser")
            aTag = dataSoup.find('a')
            if aTag:
                if "https://in.pinterest.com" + aTag['href'] not in hrefsList:
                    hrefsList.append("https://in.pinterest.com" + aTag['href'])

    getHref()
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(5)
    getHref()
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(5)
    getHref()
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(5)
    getHref()
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(5)
    getHref()
    
    for hrefData in hrefsList:
        driver.get(hrefData)
        divTag = None
        time.sleep(3)
        try:
            divTag = driver.find_element(By.XPATH, """//div[@data-test-id="closeup-image"]""")
        except Exception as e:
            print(hrefData)
        if divTag:
            divSoup = BeautifulSoup(divTag.get_attribute('innerHTML'), "html.parser")
            imgTag = divSoup.find('img')
            if imgTag:
                imgSrcList.append({"category": category, "imgSrc": imgTag['src'].replace("/236x/", "/600x/")})
                print(imgSrcList[-1])

    
driver.find_element(By.XPATH, """//div[@data-test-id="simple-login-button"]""").click()
driver.find_element(By.XPATH, """//input[@id="email"]""").send_keys("himanshujetani2211@gmail.com")
driver.find_element(By.XPATH, """//input[@id="password"]""").send_keys("Patidar1621@")
driver.find_element(By.XPATH, """//div[@data-test-id="registerFormSubmitButton"]""").click()
time.sleep(4)
mainScrapper('cars')
hrefsList = []
pd.DataFrame(imgSrcList).to_parquet('imageData.parquet', index=False)
driver.quit()
