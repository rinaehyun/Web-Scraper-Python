from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import urllib.request

driver = webdriver.Chrome()
driver.get("https://www.google.com/imghp?hl=en&ogbl")
agree=driver.find_element_by_css_selector('#L2AGLb')
agree.click()
elem = driver.find_element_by_name("q")
elem.send_keys("BTS jimin")
elem.submit()
images=driver.find_elements_by_css_selector('.rg_i.Q4LuWd')
count = 0
for image in images:
    image.click()
    time.sleep(3)
    imgTag=driver.find_element_by_css_selector('.n3VNCb').get_attribute("alt")
    if '| Twitter' in imgTag:
        imgUrl=driver.find_element_by_css_selector('.n3VNCb').get_attribute("src")
        urllib.request.urlretrieve(imgUrl, str(count) + '.jpg')
    else:
        print('count')
    count = count + 1
driver.close()
