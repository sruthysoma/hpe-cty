from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import sys
from os import walk      


def find_1(driver):
    element = driver.find_elements_by_id('Windows Client')
    if element:
        return element
    else:
        return False

def find_2(driver):
    element = driver.find_elements_by_id('10 1809')
    if element:
        return element
    else:
        return False

def find_3(driver):
    element = driver.find_elements_by_id('10 (1809)')
    if element:
        return element
    else:
        return False

def find_4(driver):
    element = driver.find_element_by_xpath("//a[contains(@href,'download')]")
    if element:
        return element
    else:
        return False

# def find_5(driver):
#     element = driver.find_elements_by_id('Windows Client')
#     if element:
#         return element
#     else:
#         return False

def wait_for_downloads():
    while any([filename.endswith(".crdownload") for filename in 
               os.listdir(os.getcwd() + r"\downloads")]):
        time.sleep(2)

def check_exists_by_xpath(driver,xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


def get_file_name_without_extension(url):
    try:
        return url[url.rindex('/')+1:url.rindex('.')]
    except:
        print()

def get_file_name(url):
    try:
        return url[url.rindex('/')+1:]
    except:
        print()

def get_extension(url):
    try:
        return url[url.rindex('.')+1:]
    except:
        print()

def click_download(driver,selenium_obj,url,logFile):
    selenium_obj.click()
    try:
        if check_exists_by_xpath(driver,'//a[contains(text(),"I accept the terms in the license agreement")]'):
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//a[normalize-space()="I accept the terms in the license agreement"]'))).click()
            if check_exists_by_xpath(driver,'//a[contains(text(),"X")]'):
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//a[normalize-space()="X"]'))).click()
    except:
        print("Timeout")
    logFile.write("\nDownloading from "+url)

def check_exe(download_button):
    if(".exe" in download_button.get_attribute("href")):
        return True
    return False

# url = "https://www.hpe.com/global/swpublishing/MTX-681cfe595a184e1b856f245d2b"
# logFile = open(os.getcwd() + r"\log.txt", "a") 

def download_from_url(url,logFile):
    chromeOptions = webdriver.ChromeOptions()
    #chromeOptions.add_argument("headless")
    chromeOptions.add_experimental_option('excludeSwitches', ['enable-logging'])
    prefs = {'safebrowsing.enabled': 'false', "download.default_directory" : os.getcwd() + r"\downloads"}
    chromeOptions.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(os.getcwd() + r"\chromedriver.exe", chrome_options=chromeOptions)
    driver.get(url)
    time.sleep(5)




    if("mellanox" in url):
        i_frame=[]
        j_frame=[]  
        downloadButtons=driver.find_elements_by_tag_name("iframe")
        for i in downloadButtons:
            if("downloader4" in i.get_attribute("src")):
                i_frame.append(i)
        url_1 = i_frame[0].get_attribute("src")
        driver.get(i_frame[0].get_attribute("src"))
        element = WebDriverWait(driver, 10).until(find_1)
        webdriver.ActionChains(driver).click(element.pop()).perform()
        element = WebDriverWait(driver, 10).until(find_2)
        webdriver.ActionChains(driver).click(element.pop()).perform()
        element = WebDriverWait(driver, 10).until(find_4)
        webdriver.ActionChains(driver).click(element).perform()

        logFile.write("\nDownloading from "+url_1)

        driver.back()

        downloadButtons=driver.find_elements_by_tag_name("iframe")
        for i in downloadButtons:
            if("downloader6" in i.get_attribute("src")):
                j_frame.append(i)

        url_2 = j_frame[0].get_attribute("src")
        driver.get(j_frame[0].get_attribute("src"))
        element = WebDriverWait(driver, 10).until(find_1)
        webdriver.ActionChains(driver).click(element.pop()).perform()
        element = WebDriverWait(driver, 10).until(find_3)
        webdriver.ActionChains(driver).click(element.pop()).perform()
        element = WebDriverWait(driver, 10).until(find_4)
        webdriver.ActionChains(driver).click(element).perform()
        logFile.write("\nDownloading from "+url_2)
        wait_for_downloads()
        driver.close()

    else:
        downloadButtons = []
        if driver.find_elements_by_xpath('//button[normalize-space()="Download"]'):
            downloadButtons = driver.find_elements_by_xpath('//button[normalize-space()="Download"]')
        elif driver.find_elements_by_xpath('//a[normalize-space()="Download"]'):
            downloadButtons = driver.find_elements_by_xpath('//a[normalize-space()="Download"]')


        # MULTIPART DOWNLOAD
        if check_exists_by_xpath(driver,'//span[contains(text(),"Multi-part download")]'):
            if(len(downloadButtons)>1):
                for i in range(len(downloadButtons)):
                    click_download(driver,downloadButtons[i],url,logFile)


        # NEWER VERSION EXISTS
        if check_exists_by_xpath(driver,'//span[contains(text(),"newer version")]'):
            logFile.write("\n{} contains a newer version of the required driver. The version specified in the release note could not be found.".format(url))

        # No download button
        if(len(downloadButtons) == 0):
            if check_exists_by_xpath(driver,'//input[contains(text(),"I accept the terms in the license agreement")]'):
            # time.sleep(1)
            # driver.find_element_by_xpath('//a[normalize-space()="I accept the terms in the license agreement"]').click()
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//input[normalize-space()="I accept the terms in the license agreement"]'))).click()
                logFile.write("\nDownloading from "+url)
            else:
                logFile.write("\n{}No downloads available.".format(url))

        # One download button
        elif(len(downloadButtons) == 1):
            click_download(driver,downloadButtons[0],url,logFile)

        else:
            # EXE, ZIP, WIN32, WIN64
            to_download = []
            for i in downloadButtons:
                to_download.append([i.get_attribute("href"),i])

            dc = {}
            for i in to_download:
                ext = get_extension(i[0])
                if ext not in dc.keys():
                    dc[ext] = []
                dc[ext].append([get_file_name_without_extension(i[0]),i[1]])

            for i in dc.keys():
                if i=='exe':
                    for j in dc[i]:
                        if 'zip' in dc.keys():
                            if not any(j[0] in x for x in dc['zip']):
                                click_download(driver,j[1], url, logFile)
                                #print("Download zip",get_file_name(j[1].get_attribute('href')))
                            #else:
                                #print("Download zip version of",j[0])
                                
                        else:
                            click_download(driver,j[1], url, logFile)
                            #print("Download",get_file_name(j[1].get_attribute('href')))
                else:
                    for j in dc[i]:
                        click_download(driver,j[1], url, logFile)
                        #print("Download",get_file_name(j[1].get_attribute('href')))

        time.sleep(5)

        wait_for_downloads()

        time.sleep(5)

        driver.close()




