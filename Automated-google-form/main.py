import time
from selenium import webdriver

web=webdriver.Chrome()
web.get('https://forms.gle/WT68aV5UnPajeoSc8')
time.sleep(2)

sname = 'Karthi'
name=web.find_element('xpath','//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
name.send_keys(sname)
snum='9363655025'
num=web.find_element('xpath','//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
num.send_keys(snum)
semail='karthipannerselvam173@gmail.com'
email=web.find_element('xpath','//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
email.send_keys(semail)
saddress='Boys hostel, Bannari Amman Institute of Technology'
address=web.find_element('xpath','//*[@id="mG61Hd"]/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[1]/div[2]/textarea')
address.send_keys(saddress)
spincode='638401'
pincode=web.find_element('xpath','//*[@id="mG61Hd"]/div[2]/div/div[2]/div[5]/div/div/div[2]/div/div[1]/div/div[1]/input')
pincode.send_keys(spincode)
sdob='17-03-2005'
dob=web.find_element('xpath',
                     '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[6]/div/div/div[2]/div/div/div[2]/div[1]/div/div[1]/input')
dob.send_keys(sdob)

sgender = 'Male'
gender=web.find_element('xpath','//*[@id="mG61Hd"]/div[2]/div/div[2]/div[7]/div/div/div[2]/div/div[1]/div/div[1]/input')
gender.send_keys(sgender)
scode='GNFPYC'
code=web.find_element('xpath','//*[@id="mG61Hd"]/div[2]/div/div[2]/div[8]/div/div/div[2]/div/div[1]/div/div[1]/input')
code.send_keys(scode)
submit=web.find_element\
    ('xpath','//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
submit.click()
time.sleep(15)

