import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import json

# Setup
url = 'https://www.google.com/maps'
path = r'C:\Users\hp\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe'

chrome_options = Options()
service = Service(path)
browser = webdriver.Chrome(service=service, options=chrome_options)

def search_escape_rooms(location):
    browser.get(url)
    place = browser.find_element(By.XPATH, '//*[@id="searchboxinput"]')
    place.clear()
    place.send_keys(f'escape rooms in {location}')
    submit = browser.find_element(By.XPATH, '//*[@id="searchbox-searchbutton"]')
    submit.click()
    time.sleep(5)

def scrape_gmb_data():
    data = []
    visited_links = set()

    while len(data) < 50:
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        places = browser.find_elements(By.CLASS_NAME, 'hfpxzc')

        if not places:
            print("No more places found")
            break

        for place in places:
            if len(data) >= 50:
                break

            link = place.get_attribute('href')
            if link not in visited_links:
                visited_links.add(link)

                try:
                    place.click()
                    time.sleep(5)
                    detail_soup = BeautifulSoup(browser.page_source, 'html.parser')

                    name = detail_soup.find('h1', class_='DUwDvf lfPIob').text if detail_soup.find('h1', class_='DUwDvf lfPIob') else ''
                    address = detail_soup.find('div', class_='Io6YTe fontBodyMedium kR99db').text if detail_soup.find('div', class_='Io6YTe fontBodyMedium kR99db') else 'Address not found'
                    phone_elem = detail_soup.find('button', {'data-tooltip': 'Copy phone number'})
                    phone = phone_elem.find('div', class_='Io6YTe fontBodyMedium kR99db').text if phone_elem else 'Phone number not found'
                    url_elem = detail_soup.find('a', {'data-tooltip': 'Open website'})
                    url = url_elem.get('href') if url_elem else 'url not found'
                    hours_div = detail_soup.find('span', class_='ZDu9vd')
                    hours = ''
                    if hours_div:
                        spans = hours_div.find_all('span')
                        if spans:
                            hours = spans[-1].text.strip()

                    review_elem = detail_soup.find('button', {'class': 'HHrUdb fontTitleSmall rqjGif'})
                    reviews_text = 'review not found'
                    if review_elem:
                        spans = review_elem.find('span')
                        if spans:
                            reviews_text = spans.text.strip()

                    data.append({
                        'name': name,
                        'address': address,
                        'phone number': phone,
                        'url': url,
                        'hours': hours,
                        'reviews': reviews_text,
                        'links': link
                    })
                    browser.back()
                    time.sleep(5)

                except Exception as e:
                    print(f"Error extracting data: {e}")
                    browser.back()
                    time.sleep(5)

        # Scroll down to load more places
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)

    return data

search_escape_rooms("india")
scraped_data = scrape_gmb_data()

if len(scraped_data) < 100:
    print("Not enough data in India, searching in America...")
    search_escape_rooms("america")
    more_data = scrape_gmb_data()
    scraped_data.extend(more_data[:100 - len(scraped_data)])  # Ensure total data is 100

df = pd.DataFrame(scraped_data)

# Save to CSV
df.to_csv('gmb_data.csv', index=False)

# Save to JSON
with open('gmb_data.json', 'w') as f:
    json.dump(scraped_data, f, indent=4)

print("Data saved to gmb_data.csv and gmb_data.json")
browser.quit()
