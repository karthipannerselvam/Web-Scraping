import requests
import pandas as pd
from bs4 import BeautifulSoup


url='https://www.scrapethissite.com/pages/simple/'
website=requests.get(url)
soup=BeautifulSoup(website.content,'html.parser')

row=soup.find_all('div',{'class':'container'})

country=soup.find_all('h3',{'class':'country-name'})
countries = [con.text.strip() for con in country]
capital=soup.find_all('span',{'class':'country-capital'})
capital = [con.text.strip() for con in capital]
population=soup.find_all('span',{'class':'country-population'})
population = [con.text.strip() for con in population]
area=soup.find_all('span',{'class':'country-area'})
area = [con.text.strip() for con in area]

df = pd.DataFrame(countries, columns=['Country'])
df['Capital'] = capital
df['Population'] = population
df['Area'] = area

df.to_excel('countries.xlsx', index=False)
