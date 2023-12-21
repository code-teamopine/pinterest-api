from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time

class Scrapper:
    __slots__ = "driver", "url"
    
    def __init__(self) -> None:
        self.url, self.driver = "https://www.magicals.art/search/label/Cute%20Friends", webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.get(self.url)
        time.sleep(8)

    def select_main_div(self) -> None:
        main_div = self.driver.find_element(By.XPATH, """//div[@id="main-widget"]""")
        a_tags_list = main_div.find_elements(By.XPATH, """//a[@class="thmb"]""")
        for a_tag in a_tags_list:
            print(a_tag)

    def __del__(self) -> None:
        self.driver.quit()

scrapper_obj = Scrapper()
scrapper_obj.select_main_div()
del scrapper_obj
