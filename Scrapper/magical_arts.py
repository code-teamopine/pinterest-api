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
    # all_data_a_list = 
    pass
