'''
I need to get the urls of each code from scratch each time, as I think they change.

'''

import os

import selenium as se
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def helper(a, b):

    for i, l_a in enumerate(a):
        if b == l_a:
            return i
    return -1

def diff(a, b):

    t_b = b
    c_i = 0
    for c in a:

        t_i = helper(t_b, c)
        if t_i != -1 and (t_i > c_i or t_i == c_i):
            c_i = t_i
            t_b = t_b[:c_i] + t_b[c_i+1:]

    t_a = a
    c_i = 0
    for c in b:

        t_i = helper(t_a, c)
        if t_i != -1 and (t_i > c_i or t_i == c_i):
            c_i = t_i
            t_a = t_a[:c_i] + t_a[c_i+1:]

    return t_b + t_a

def clean_title(title: str) -> str:
    # Remove leading asterisk if present
    if title.startswith("*"):
        title = title[1:].lstrip()

    # Remove trailing "; and Appendix" if present
    suffix = "; and Appendix"
    if title.endswith(suffix):
        title = title[:-len(suffix)].rstrip()

    return title

TEXT_FILE_NAME = "Update_Text.txt"

options = webdriver.FirefoxOptions()
options.page_load_strategy = 'normal'
driver = webdriver.Firefox(options=options)
driverSecond = webdriver.Firefox(options=options)
#This page loads statically, no need to do any special stuff here.
driver.get("https://uscode.house.gov/currency/currency.shtml")
title = driver.title
text_box = driver.find_element(by=By.CLASS_NAME, value="pagesubhead")
box_text = text_box.text
print("Box value: ", box_text)
textFileRead = open(TEXT_FILE_NAME)
savedText = textFileRead.read()
print(savedText)
wereEqual = savedText == box_text
print("Were equal:", wereEqual)
textFileRead.close()
if True:#not wereEqual:
    print("Strings differ by", diff(savedText, box_text))
    print("Updating saved information, is now", box_text)
    with open(TEXT_FILE_NAME, "w") as textFileWrite:
        textFileWrite.write(box_text)
        textFileWrite.close()
        #Update all US Codes.  It's safe enough to assume they won't add more.
        driver.get("https://uscode.house.gov/browse.xhtml")
        iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "iframe"))
        )
        driver.switch_to.frame(iframe)
        for title_number in range(1, 55):
            
            element_name = f"USC-prelim-title{title_number}"
            #print(element_id)
            title_link = driver.find_element(by=By.NAME, value=element_name)
            titleFilename = f"{clean_title(title_link.text)}.txt"
            print("name", titleFilename)
            print("link", title_link.get_attribute('href'))
            titleLinkName = f"TITLE {title_number}"
            chapterUrl = f"https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title{title_number}-front&num=0&edition=prelim"
            driverSecond.get(chapterUrl)
            #please dump me the contents of this file
            print(driverSecond.find_element(By.XPATH, "/html/body").text)
            with open(titleFilename, "w") as titleFile:
                print()

#<a name="USC-prelim-title14" target="_top" href="/browse/prelim@title14&amp;edition=prelim" style="text-decoration: none;">*Title 14—Coast Guard</a>

## id "USC-prelim-title13:div"
#Save this value for future use.


driver.quit()

'''
text_box = driver.find_element(by=By.NAME, value="my-text")
submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")
text_box.send_keys("Selenium")
submit_button.click()
message = driver.find_element(by=By.ID, value="message")
text = message.text

'''