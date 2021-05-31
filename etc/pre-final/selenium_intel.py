from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
from os import walk      
    
def wait_for_downloads():
    # print("Waiting for downloads", end="")
    # print(os.listdir(os.getcwd()))
    while any([filename.endswith(".crdownload") for filename in 
               os.listdir(os.getcwd() + r"\downloads")]):
        time.sleep(2)

def check_exists_by_xpath(driver,xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

def check_exists_by_xpath(driver,xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


def check_exe(download_button):
    if(".exe" in download_button.get_attribute("href")):
        return True
    return False


url = "https://downloadcenter.intel.com/download/29227/Chipset-INF-Utility"

if ("downloads" not in os.listdir(os.getcwd())):
    os.mkdir(os.getcwd() + r"\downloads")

chromeOptions = webdriver.ChromeOptions()
# chromeOptions.add_argument("--headless")
# chromeOptions.add_argument("--no-sandbox")
# chromeOptions.add_argument("--disable-dev-shm-usage")
prefs = {'safebrowsing.enabled': 'false', "download.default_directory" : os.getcwd() + r"\downloads"}
chromeOptions.add_experimental_option("prefs", prefs)
# chromeOptions.add_argument("download.default_directory=C:\\Users\\naikp\\Desktop\\HP-CTY")
# driver = webdriver.Chrome(executable_path=r"C:\\chromedriver.exe", chrome_options=chromeOptions)
driver = webdriver.Chrome(executable_path=os.getcwd() + r"\chromedriver.exe", chrome_options=chromeOptions)

driver.get(url)

time.sleep(5)

if check_exists_by_xpath(driver,'//span[contains(text(),"A newer version of this software is available, which includes functional and security updates.")]'):
    logFile = open("log.txt", "a")
    logFile.write("{} contains a newer version of the required driver. The version specified in the release note could not be found.\n".format(url))
    logFile.close()

downloadButtons = driver.find_elements_by_xpath('//a[normalize-space()="Download"]')


if(len(downloadButtons) == 0):
    if check_exists_by_xpath(driver,'//input[contains(text(),"I accept the terms in the license agreement")]'):
    # time.sleep(1)
    # driver.find_element_by_xpath('//a[normalize-space()="I accept the terms in the license agreement"]').click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//input[normalize-space()="I accept the terms in the license agreement"]'))).click()
    else:
        logFile = open("log.txt", "a")
        logFile.write("{} contains a newer version of the required driver. However, the version specified in the release note has been downloaded\n".format(url))
        logFile.close()
elif(len(downloadButtons) == 1):
    downloadButtons[0].click()
    if check_exists_by_xpath(driver,'//a[contains(text(),"I accept the terms in the license agreement")]'):
        # time.sleep(1)
        # driver.find_element_by_xpath('//a[normalize-space()="I accept the terms in the license agreement"]').click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//a[normalize-space()="I accept the terms in the license agreement"]'))).click()
        print("CLIKED")

else:
    exe_btns = filter(check_exe, downloadButtons)
    for i in exe_btns:
        i.click()
        if check_exists_by_xpath(driver,'//a[contains(text(),"I accept the terms in the license agreement")]'):
            # time.sleep(1)
            # driver.find_element_by_xpath('//a[normalize-space()="I accept the terms in the license agreement"]').click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//a[normalize-space()="I accept the terms in the license agreement"]'))).click()

time.sleep(5)

wait_for_downloads()
# print(downloadButtons)

time.sleep(5)

driver.close()




