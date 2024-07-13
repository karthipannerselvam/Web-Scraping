import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import  BeautifulSoup
url = 'https://www.youtube.com/@nikoo28/videos'
path = r'C:\Users\hp\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe'

chrome_options = Options()
chrome_options.headless = True
chrome_options.add_argument('--headless')
service = Service(path)
browser = webdriver.Chrome(service=service, options=chrome_options)


browser.get(url)


soup=BeautifulSoup(browser.page_source, 'html.parser')

title=soup.find_all('yt-formatted-string', {'id': 'video-title'})


metadata_lines = soup.find_all('div', {'id': 'metadata-line'})

view_counts = []
for metadata in metadata_lines:
    spans = metadata.find_all('span')
    if spans:
        view_counts.append(spans[0].text.strip())


data = []
for tit, view in zip(title, view_counts):
    data.append({
        'Title': tit.text.strip(),
        'Views': view
    })

df=pd.DataFrame(data)
df.to_excel('NikilLohiaYT.xlsx',index=True)
browser.close()
