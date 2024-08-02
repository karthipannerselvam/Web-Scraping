import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import json
# Setup
url = 'https://www.google.com/maps'
path = r'C:\Users\hp\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe'

chrome_options = Options()
# chrome_options.headless = True
# chrome_options.add_argument('--headless')
service = Service(path)
browser = webdriver.Chrome(service=service, options=chrome_options)

browser.get(url)

place = browser.find_element(By.XPATH, '//*[@id="searchboxinput"]')
place.send_keys('escape rooms')
submit = browser.find_element(By.XPATH, '//*[@id="searchbox-searchbutton"]')
submit.click()
time.sleep(10)


def scrape_gmb_data():
    data = []
    visited_links = set()

    while len(data) < 5:
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        places = browser.find_elements(By.CLASS_NAME, 'hfpxzc')

        for place in places:
            if len(data) >= 5:
                break

            link = place.get_attribute('href')
            if link not in visited_links:
                visited_links.add(link)

                try:
                    place.click()

                    time.sleep(5)
                    detail_soup = BeautifulSoup(browser.page_source, 'html.parser')

                    name = detail_soup.find('h1', class_='DUwDvf lfPIob').text if detail_soup.find('h1',
                                                                                                       class_='DUwDvf lfPIob') else ''
                    address = detail_soup.find('div', class_='Io6YTe fontBodyMedium kR99db').text if detail_soup.find('div', class_='Io6YTe fontBodyMedium kR99db') else 'Address not found'

                    phone_elem = detail_soup.find('button', {'data-tooltip': 'Copy phone number'})
                    phone = phone_elem.find('div', class_='Io6YTe fontBodyMedium kR99db').text if phone_elem else 'Phone number not found'

                    url_elem = detail_soup.find('a', {'data-tooltip': 'Open website'})
                    url = url_elem.find('div',
                                            class_='Io6YTe fontBodyMedium kR99db').text if url_elem else 'url not found'

                    hours_div = detail_soup.find('span', class_='ZDu9vd')
                    hours = ''
                    if hours_div:
                        spans = hours_div.find_all('span')
                        if spans:
                            hours = spans[-1].text.strip()

                    review_elem = detail_soup.find('button', {'class': 'HHrUdb fontTitleSmall rqjGif'})
                    if review_elem:
                        spans = review_elem.find('span')
                        reviews_text = spans.text.strip() if spans else 'review not found'
                    else:
                        reviews_text = 'review not found'

                    data.append({
                        'name': name,
                        'address':address,
                        'phone number':phone,
                        'url':link,
                        'hours':hours,
                        'reviews':reviews_text,
                        'links': url


                    })
                    browser.back()

                except Exception as e:
                    print(f"Error extracting data: {e}")



        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(5)

    return data


scraped_data = scrape_gmb_data()
print(pd.DataFrame(scraped_data))


with open('gmb_data.json', 'w') as f:
    json.dump(scraped_data, f, indent=4)

print("Data saved to gmb_data.json")
browser.quit()
