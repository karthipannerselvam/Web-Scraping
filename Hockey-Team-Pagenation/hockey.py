import pandas as pd,requests
from bs4 import BeautifulSoup

page,datas=1,[]

while True:
    url=f'https://www.scrapethissite.com/pages/forms/?page_num={page}&per_page=100'
    req=requests.get(url)
    soup=BeautifulSoup(req.content,'html.parser')

    trs=soup.find_all('tr',{'class':'team'})
    if trs:
        for tr in trs:
            data={td.get('class')[0]: td.text.strip() for td in tr.find_all('td')}
            datas.append(data)
        page+=1
    else:
        break

df=pd.DataFrame(datas)
df.to_excel('Hockey-Pagenation.xlsx',index=False)

