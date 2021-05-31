# Import Module
from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
import os
from os import walk      
    
download_dir = os.path.expanduser('~/Downloads')
print('File being downloaded to:',download_dir)

def check_exists_by_xpath(driver,xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

def check_if_download_folder_has_unfinished_files():
    for (dirpath, dirnames, filenames) in walk(download_dir):
        return str(filenames)
  
  
# Open Chrome
driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
        
# Get the target URL
driver.get('https://support.hpe.com/hpesc/public/swd/detail?swItemId=MTX_c2f5e99173104d44827c78f6fb')
  
# Wait for 5 seconds to load the webpage completely
time.sleep(5)
  
# Find the button using text
# support hpe websites
if check_exists_by_xpath(driver,'//button[normalize-space()="Download"]'):
    driver.find_element_by_xpath('//button[normalize-space()="Download"]').click()
# intel websites
if check_exists_by_xpath(driver,'//a[normalize-space()="Download"]'):
    driver.find_element_by_xpath('//a[normalize-space()="Download"]').click()
    #driver.find_element_by_xpath('//a[normalize-space()="I accept the terms in the license agreement"]').click()

  
time.sleep(5)  # let the driver start downloading

file_list = check_if_download_folder_has_unfinished_files()
while 'Unconfirmed' in file_list or 'crdownload' in file_list:
    file_list = check_if_download_folder_has_unfinished_files()
    time.sleep(1)


time.sleep(5)
  
# Close the driver
driver.close()