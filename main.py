from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd

property_list = []

def get_price(listing, listing_id):
    price = listing.find_element(By.XPATH, f'//*[@id="{listing_id}"]/div[2]/hgroup/h3/span').text
    return price.replace('$', '').replace(',', '')

def get_address(listing, listing_id):
    address = listing.find_element(By.XPATH, f'//*[@id="{listing_id}"]/div[2]/hgroup/h3').text
    splitted_address = address.split('-')
    return splitted_address[0].strip()

def get_type(listing, listing_id):
    r_type = listing.find_element(By.XPATH, f'//*[@id="{listing_id}"]/div[2]/div[1]/div').text
    r_type = r_type.split(',')
    return r_type[1].strip()

def get_beds(listing, listing_id):
    beds = listing.find_element(By.XPATH, f'//*[@id="{listing_id}"]/div[2]/div[1]/ul/li[1]/b').text
    return beds

def get_baths(listing, listing_id):
    baths = listing.find_element(By.XPATH, f'//*[@id="{listing_id}"]/div[2]/div[1]/ul/li[2]/b').text
    return baths

def get_area(listing, listing_id):
    area = listing.find_element(By.XPATH, f'//*[@id="{listing_id}"]/div[2]/div[1]/ul/li[3]/b').text
    return area.replace(',', '')

def get_dom(listing, listing_id):
    try:
        dom =listing.find_element(By.XPATH, f'//*[@id="{listing_id}"]/div[2]/div[1]/ul/li[4]/b')
    except NoSuchElementException:
        return ""
    return dom.text

def get_link(listing, listing_id):
    link = listing.find_element(By.XPATH, f'//*[@id="{listing_id}"]/div[1]/a')
    return link.get_attribute('href')

def scrape_listings(listings, community):
    for listing in listings:
        listing_id = listing.get_attribute("id")

        address = get_address(listing, listing_id)
        price = get_price(listing, listing_id)
        r_type = get_type(listing, listing_id)
        beds = get_beds(listing, listing_id)
        baths = get_baths(listing, listing_id)
        area = get_area(listing, listing_id)
        dom = get_dom(listing, listing_id)
        link = get_link(listing, listing_id)

        listing_item = {
            'address': address,
            'community': community,
            'price': price,
            'type': r_type,
            'beds': beds,
            'baths': baths,
            'area': area,
            'dom': dom,
            'link': link
        }

        property_list.append(listing_item)


driver = webdriver.Chrome()

url = 'https://calgaryhomes.ca/'

driver.get(url)

cookies = driver.find_element(By.CLASS_NAME, 'close-icon')

if (cookies):
    cookies.click()

community = driver.find_element(By.XPATH, '//*[@id="feature-deck"]/div/div/article[8]/a')
community_name = community.text
community.click()

while (True):
    listings_list = driver.find_element(By.CLASS_NAME, 'articleset')
    listings = driver.find_elements(By.TAG_NAME, 'article')

    scrape_listings(listings, community_name)

    try:
        next = driver.find_element(By.CLASS_NAME, 'next')
    except NoSuchElementException:
        break;
    next.click()

    
df = pd.DataFrame(property_list)
df.to_csv('out.csv', index=False)