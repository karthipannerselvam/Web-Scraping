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
chrome_options.headless = True
chrome_options.add_argument('--headless')
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

def scrape_links():
    links = set()
    has_more_places = True

    while has_more_places:
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        places = browser.find_elements(By.CLASS_NAME, 'hfpxzc')

        if not places:
            break

        for place in places:
            link = place.get_attribute('href')
            if link:
                links.add(link)

        # Scroll down to load more places
        prev_length = len(places)
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        places = browser.find_elements(By.CLASS_NAME, 'hfpxzc')

        if len(places) == prev_length:
            has_more_places = False

    return links

def scrape_gmb_data(links):
    data = []
    cnt=0

    for link in links:
        browser.get(link)
        time.sleep(5)
        soup = BeautifulSoup(browser.page_source, 'html.parser')

        try:
            name = soup.find('h1', class_='DUwDvf lfPIob').text if soup.find('h1', class_='DUwDvf lfPIob') else ''
            address = soup.find('div', class_='Io6YTe fontBodyMedium kR99db').text if soup.find('div', class_='Io6YTe fontBodyMedium kR99db') else 'Address not found'
            phone_elem = soup.find('button', {'data-tooltip': 'Copy phone number'})
            phone = phone_elem.find('div', class_='Io6YTe fontBodyMedium kR99db').text if phone_elem else 'Phone number not found'
            url_elem = soup.find('a', {'data-tooltip': 'Open website'})
            url = url_elem.get('href') if url_elem else 'url not found'
            hours_div = soup.find('span', class_='ZDu9vd')
            hours = ''
            if hours_div:
                spans = hours_div.find_all('span')
                if spans:
                    hours = spans[-1].text.strip()

            review_elem = soup.find('button', {'class': 'HHrUdb fontTitleSmall rqjGif'})
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

            cnt += 1
            print(f"Processed {cnt}/{len(links)}: {name}")


        except Exception as e:
            print(f"Error extracting data: {e}")

    return data

# Locations to scrape
locations = ["banglore", "chennai", "delhi","pune","mumbai","kolkata","hydrabad","new york","San Francisco","ahmedabad","atlanta","kerala","Pennsylvania","New Jersey","los angles","texas","london","chicago","las vegas","san diego","orland","jaipur","mysore","coimbatore","Australia","Manchester","Massachusetts","Colorado"]
all_data = []

for location in locations:
    search_escape_rooms(location)
    links = scrape_links()
    location_data = scrape_gmb_data(links)
    all_data.extend(location_data)

df = pd.DataFrame(all_data)

# Save to CSV
df.to_csv('gmb_data.csv', index=True)

# Save to JSON
with open('gmb_data.json', 'w') as f:
    json.dump(all_data, f, indent=4)

print("Data saved to gmb_data.csv and gmb_data.json")
browser.quit()
