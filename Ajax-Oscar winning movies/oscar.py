import requests,pandas as pd 
from bs4 import BeautifulSoup

url='https://www.scrapethissite.com/pages/ajax-javascript/'
req=requests.get(url)
soup=BeautifulSoup(req.content,'html.parser')


years=[year.text for year in soup.find_all('a',{'class':'year-link'})]

datas=[]
for year in years:
    url1=f'https://www.scrapethissite.com/pages/ajax-javascript/?ajax=true&year={year}'
    res=requests.get(url1)
    datas.extend(res.json())

df=pd.DataFrame(datas)
df.to_excel('Ajax-Oscer.xlsx',index=False)