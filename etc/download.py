# Import Module
import pyautogui as pg
from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
import os
from os import walk      
pg.FAILSAFE = False

def check_exists_by_xpath(driver,xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

def check_if_download_folder_has_unfinished_files():
    for (dirpath, dirnames, filenames) in walk(download_dir):
        return str(filenames)



def download(url):
    download_dir = os.path.expanduser('~/Downloads')
    print('File being downloaded to:',download_dir)

    driver = webdriver.Chrome(executable_path=r"C:\\chromedriver.exe")
    driver.maximize_window()
            
    # Get the target URL
    driver.get(url)
    
    # Wait for 5 seconds to load the webpage completely
    time.sleep(5)

    
























    
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
driver = webdriver.Chrome(executable_path=r"C:\\chromedriver.exe")
driver.maximize_window()
        
# Get the target URL
driver.get('https://downloadcenter.intel.com/download/29227/Chipset-INF-Utility')
  
# Wait for 5 seconds to load the webpage completely
time.sleep(5)
  
# Find the button using text
# support hpe websites
#if check_exists_by_xpath(driver,'//button[normalize-space()="Download"]'):
 #   driver.find_element_by_xpath('//button[normalize-space()="Download"]').click()
# intel websites
# if check_exists_by_xpath(driver,'//a[normalize-space()="Download"]'):
#     downloadBtn = driver.find_element_by_xpath('//a[normalize-space()="Download"]')
#     downloadBtn.click()
#     termsBtn = driver.find_element_by_xpath('//a[normalize-space()="I accept the terms in the license agreement"]')
#     print("Element is visible? " + str(termsBtn.is_displayed()))
#     time.sleep(5)  # let the driver start downloading
#     termsBtn.click()

#     file_list = check_if_download_folder_has_unfinished_files()
#     while 'Unconfirmed' in file_list or 'crdownload' in file_list:
#         file_list = check_if_download_folder_has_unfinished_files()
#         time.sleep(1)


#     time.sleep(5)
    
#     # Close the driver
#     driver.close()



    # print(d)

    # #x,y=pg.position()
    
    # #print('X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4))
    # pg.click(d['x']+100,d['y']+300)
    # pg.PAUSE=2
    # pg.moveRel(300,-30)
    # pg.click()
    
    #pg.click()
    
    #pg.click(str(d['x']).rjust(4)+100,str(d['y']).rjust(4)+350,'left')
    #pg.PAUSE=5
    #pg.click(d['x'],d['y'],button='left')
    # e=driver.find_element_by_xpath('//a[normalize-space()="I accept the terms in the license agreement"]').location
    #pg.click(e['x'],e['y'],button='left')



    #driver.find_element_by_xpath('//a[normalize-space()="I accept the terms in the license agreement"]').click()

  
