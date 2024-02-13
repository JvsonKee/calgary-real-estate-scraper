from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from util import get_cookies, get_communities, scrape_community

def main():
    url = 'https://calgaryhomes.ca/'
    driver = webdriver.Chrome()
    driver.get(url)

    cookies = get_cookies(driver)
    if (cookies):
        cookies.click()

    property_list = []
    communities = get_communities(driver)
    
    for i in range(1,len(communities) + 1):
        scrape_community(driver, i, property_list)
        driver.find_element(By.XPATH, '//*[@id="logo"]').click()


    df = pd.DataFrame(property_list)
    df.to_csv('out.csv', index=False)


if __name__ == '__main__':
    main()
