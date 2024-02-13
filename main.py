from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from util import scrape_community

property_list = []

driver = webdriver.Chrome()

url = 'https://calgaryhomes.ca/'

driver.get(url)

cookies = driver.find_element(By.CLASS_NAME, 'close-icon')

if (cookies):
    cookies.click()

community_list = driver.find_element(By.XPATH, '//*[@id="feature-deck"]/div/div')
communities = community_list.find_elements(By.TAG_NAME, 'article')

for i in range(1,len(communities) + 1):
    
    scrape_community(driver, i, property_list)

    driver.find_element(By.XPATH, '//*[@id="logo"]').click()


df = pd.DataFrame(property_list)
df.to_csv('out.csv', index=False)