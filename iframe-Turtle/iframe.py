import requests,pandas as pd 
from bs4 import BeautifulSoup

url='https://www.scrapethissite.com/pages/frames/'
req=requests.get(url)
soup=BeautifulSoup(req.content,'html.parser')

frame='https://www.scrapethissite.com'+soup.find('iframe',{'id':'iframe'}).get('src')
res=requests.get(frame)
soup=BeautifulSoup(res.content,'html.parser')
divs=soup.find_all('div',{'class':'turtle-family-card'})


datas=[]
for div in divs:
    image=div.find('img').get('src')
    family_name=div.find('h3').text
    learn='https://www.scrapethissite.com'+div.find('a').get('href')
    res=requests.get(learn)
    soup=BeautifulSoup(res.content,'html.parser')
    details=soup.find('p',{'class':'lead'}).text.strip()
    data={
        'Image':image,
        'Family Name':family_name,
        'More':details
    }
    datas.append(data)

df=pd.DataFrame(datas)
df.to_excel('iframe.xlsx',index=False)