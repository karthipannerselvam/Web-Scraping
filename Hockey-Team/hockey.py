import requests
from bs4 import BeautifulSoup
import pandas as pd 

url='https://www.scrapethissite.com/pages/forms/'

website=requests.get(url)
soup=BeautifulSoup(website.content,'html.parser')

table=soup.find('table',{'class':'table'})
row=table.find_all('th')
Heading = [con.text.strip() for con in row]
name=table.find_all('td',{'class':'name'})
name = [con.text.strip() for con in name]
year=table.find_all('td',{'class':'year'})
year = [con.text.strip() for con in year]
wins=table.find_all('td',{'class':'wins'})
wins = [con.text.strip() for con in wins]
losses=table.find_all('td',{'class':'losses'})
losses = [con.text.strip() for con in losses]
otlosses=table.find_all('td',{'class':'ot-losses'})
OTLosses = [con.text.strip() for con in otlosses]
winper=table.select('td.pct.text-success, td.pct.text-danger')
WinPercentage = [con.text.strip() for con in winper]
gf=table.find_all('td',{'class':'gf'})
GoalsFor = [con.text.strip() for con in gf]
ga=table.find_all('td',{'class':'ga'})
GoalsAgainst = [con.text.strip() for con in ga]
points=table.select('td.diff.text-success, td.diff.text-danger')
Points = [con.text.strip() for con in points]

df=pd.DataFrame(columns=Heading)

df['Team Name']=name
df['Year']=year
df['Wins']=wins
df['Losses']=losses
df['OT Losses']=OTLosses
df['Win %']=WinPercentage
df['Goals For (GF)']=GoalsFor
df['Goals Against (GA)']=GoalsAgainst
df['+/-']=Points

df.to_excel('Hockey-team.xlsx', index=False)