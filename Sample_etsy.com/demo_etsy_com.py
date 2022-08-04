import re

import pandas as pd
import textract
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import requests
import shutil
import os.path
import sys
import docx2txt
from dateutil.parser import parse
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import urllib.request
driver = webdriver.Chrome(ChromeDriverManager().install())
url = 'https://www.etsy.com/shop/JACKSPIRITdesigns'
action = ActionChains(driver)
title_list=[]
pricing_list=[]
pics_list=[]
description_list=[]
added_price_list=[]
image_list=[]

items=[]

driver.get(url)
time.sleep(5)
item_list=driver.find_element_by_xpath('//div[@class="responsive-listing-grid wt-grid wt-grid--block justify-content-flex-start wt-mb-xs-3 appears-ready"]')
a = item_list.find_elements_by_tag_name('a')
for x in a:
    link = x.get_attribute('href')
    print(link)
    if link.startswith('https://www.etsy.com/'):
        items.append(link)
time.sleep(3)
print(items)

url_list=list(set(items))
len_1 = len(url_list)
print(url_list)
count=1
for za in url_list:
    try:
        print(za)
        driver.get(za)
        time.sleep(5)
        print(count)
        image_name='image_'+str(count)+'.jpg'
        image_list.append(image_name)
        title=driver.find_element_by_xpath('//h1[@class="wt-text-body-03 wt-line-height-tight wt-break-word"]')
        title=title.text
        print(title)
        title_list.append(title)
        price=driver.find_element_by_xpath('//p[@class="wt-text-title-03 wt-mr-xs-2"]')
        price=price.text
        print(price,'price text')
        price_ee=price.replace(',','')
        price=int(price_ee.replace('₹ ',''))
        price_usd=price*0.013
        price=float("{:.2f}".format(price_usd))
        print(price)
        price_info='$'+str(price)
        pricing_list.append(price_info)
        added_price=price+((price*46)/100)
        added_price=float("{:.2f}".format(added_price))
        print(added_price,'added price')
        added_price_info='$'+str(added_price)
        added_price_list.append(added_price_info)
        description=driver.find_element_by_xpath('//*[@id="wt-content-toggle-product-details-read-more"]/p')
        description=description.text
        print(description)
        description_list.append(description)

        pics_url=driver.find_element_by_xpath('//ul[@class="wt-list-unstyled wt-overflow-hidden wt-position-relative carousel-pane-list"]/li[1]/img')
        pics_url=pics_url.get_attribute('src')
        print(pics_url,'pics url')
        # pics_name=title+'.jpg'
        img_content = requests.get(pics_url).content
        with open(image_name, 'wb') as fh:
            fh.write(img_content)
        time.sleep(5)
    except Exception as e:
        print(e)
        pass
    count+=1
final_list=[title_list,pricing_list,added_price_list,description_list]
df = pd.DataFrame(
    {'Image': image_list,
     'Title': title_list,
     'Pricing': pricing_list,
     'Added_price': added_price_list,
     'Description': description_list
    })
print(df)
df.to_csv('sample_data2.csv')



