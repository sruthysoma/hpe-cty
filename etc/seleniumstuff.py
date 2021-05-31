from selenium import webdriver
import time
from os import walk

download_dir = "C:\\Users\\naikp\\Downloads"

def check_if_download_folder_has_unfinished_files():
    for (dirpath, dirnames, filenames) in walk(download_dir):
        return str(filenames)
  
# set webdriver path here it may vary
# Its the location where you have downloaded the ChromeDriver
driver = webdriver.Chrome(executable_path=r"C:\\chromedriver.exe")
  
# Get the target URL
driver.get('https://downloadcenter.intel.com/download/29227/Chipset-INF-Utility')
  
# Wait for 5 seconds to load the webpage completely
time.sleep(5)
  
# Find the button using text
# driver.find_element_by_xpath('//button[normalize-space()="Download"]').click()

driver.find_element_by_xpath("//span[contains(text(),'A newer version of this software is available, which includes functional and security updates.')]").click()


time.sleep(5)  # let the driver start downloading

file_list = check_if_download_folder_has_unfinished_files()
while 'Unconfirmed' in file_list or 'crdownload' in file_list:
    file_list = check_if_download_folder_has_unfinished_files()
    time.sleep(1)


time.sleep(5)
  
# Close the driver
driver.close()