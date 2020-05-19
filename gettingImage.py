import urllib
import requests
import os
from bs4 import BeautifulSoup
from selenium import webdriver

#open chrome
driver = webdriver.Chrome('./chromedriver')
driver.get('https://www.google.com/imghp?hl=en')

#target's name
target = "Kobe Bryant"
path = './dataset/{}_images'.format(target.replace(' ', '_'))
#type target's name as a google searching query
driver.find_element_by_xpath('/html/body/div/div[3]/div[2]/form/div[2]/div[1]/div[1]/div/div[2]/input').send_keys(target)
driver.find_element_by_xpath('//*[@id="sbtc"]/button').click()

url = driver.current_url

#retrieve web site's url
res = requests.get(url)

#get the HTML code from the web site
soup = BeautifulSoup(res.text, 'html.parser')
# print(soup.prettify())

#check if there is a target's directory
if not os.path.exists(path):
    os.makedirs(path)
    new_dir = path
else:
    new_dir = path
#get image urls and store them in the directory we have made above
for (i, img) in enumerate(soup.find_all('img')[1:]):
    imgUrl = img.get('src')
    #check if there is a same image
    if not os.path.exists(os.path.join(new_dir, target + str(i + 1))):
        with open(os.path.join(new_dir, target + str(i + 1) + ".png"), 'wb') as f:
            f.write(requests.get(imgUrl).content)
    
driver.quit()
