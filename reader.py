from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import urllib2
import time
import csv
import sys
import os
from pip._vendor.distlib.compat import raw_input
from _io import open
from locale import str
from test.test_iterlen import len


#print "Enter url of district site in EXACTLY this format: https://ecf.txnb.uscourts.gov"
#filename = raw_input()
if os.path.isfile("urls.txt") == False:
    sys.exit()

print "Enter username"
username = raw_input()
print "Enter password"
password = raw_input()
print "Enter date 1 in format: Month/Day/Year"
date1 = raw_input()
print "Enter date 2 in format: Month/Day/Year"
date2 = raw_input()
print "Enter Chapter/Lead BK case"
chapter = raw_input()

print "\nConfirm if the following data is correct (restart the program if it isn't)"
#print "Filename: " + filename
print "Username: " + username
print "Date 1: " + date1
print "Date 2: " + date2
print "Chapter/Lead BK Case: " + chapter
raw_input("Press Enter to continue...\n")

print "The following urls will be visited:\n"
file = open("urls.txt", 'r')
for line in file:
    print line,
    if 'str' in line:
        break
raw_input("\nPress Enter to continue...")
print "Please wait..."

# Creates output folder
if not os.path.exists(os.getcwd() + "/output"):
    os.mkdir(os.getcwd() + "/output")

page_num = 0

driver = webdriver.Firefox()

file = open("urls.txt", 'r')
for line in file:
    try:
        time.sleep(2)
        print "Now parsing through: " + line,
        line = line.strip()
        
        driver.get(line + "/cgi-bin/iquery.pl")
        main_window = driver.current_window_handle
        
        #Login
        if len(driver.find_elements_by_name("login")) != 0:
            elem = driver.find_element_by_name("login")
            elem.send_keys(username)
            time.sleep(1)
            elem = driver.find_element_by_name("key")
            elem.send_keys(password)
            time.sleep(1)
            elem.send_keys(Keys.RETURN)
            time.sleep(5)
        
        #Inputs query data
        if len(driver.find_elements_by_name("filed_from")) != 0:
            elem = driver.find_element_by_name("filed_from")
            elem.send_keys(date1)
            time.sleep(1)
            elem = elem = driver.find_element_by_name("filed_to")
            elem.send_keys(date2)
            time.sleep(1)
            elem.send_keys(Keys.RETURN)
            time.sleep(5)
        elif len(driver.find_elements_by_name("Qry_filed_from")) != 0:
            print "\nThis district uses a different template"
            break
            elem = driver.find_element_by_name("Qry_filed_from")
            elem.send_keys(date1)
            time.sleep(1)
            elem = elem = driver.find_element_by_name("Qry_filed_to")
            elem.send_keys(date2)
            time.sleep(1)
            elem = driver.find_element_by_name("button1")
            elem.send_keys(Keys.RETURN)
            time.sleep(5)
        
        # Checks the rows, saves data in rows with correct leading number
        #if len(driver.find_elements_by_css_selector("tr.rowBackground1")) != 0:
        rowType1 = driver.find_elements_by_css_selector("tr.rowBackground1")
        rowType2 = driver.find_elements_by_css_selector("tr.rowBackground2")
        rows = rowType1 + rowType2
        for row in rows:
            link = row.find_elements_by_tag_name("td")[0].find_elements_by_tag_name("a")
            cell = row.find_elements_by_tag_name("td")[2]
            if (cell.text == chapter):
                # Opens link in new tab
                link[0].send_keys(Keys.CONTROL + Keys.RETURN)
                driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB)
                driver.switch_to_window(main_window)
                time.sleep(2)
                if not len(driver.find_elements_by_link_text("Creditor")) == 0:
                    creditor_link = driver.find_element_by_link_text("Creditor")
                elif not len(driver.find_elements_by_link_text("Creditors")) == 0:
                    creditor_link = driver.find_element_by_link_text("Creditors")
                elif not len(driver.find_elements_by_link_text("Creditor (Not the Matrix)")) == 0:
                    creditor_link = driver.find_element_by_link_text("Creditor (Not the Matrix)")
                elif not len(driver.find_elements_by_link_text("Creditor (Not a Mailing Matrix)")) == 0:
                    creditor_link = driver.find_element_by_link_text("Creditor (Not a Mailing Matrix)")
                elif not len(driver.find_elements_by_link_text("Creditors...")) == 0:
                    creditor_link = driver.find_element_by_link_text("Creditors...")    
                #elif not len(driver.find_elements_by_link_text("List of Creditors")) == 0:
                    #creditor_link = driver.find_element_by_link_text("List of Creditors")
                creditor_link.send_keys(Keys.RETURN)
                time.sleep(4)
                if not len(driver.find_elements_by_link_text("List of Creditors and Parties")) == 0:
                    list_creds = driver.find_element_by_link_text("List of Creditors and Parties")
                    list_creds.send_keys(Keys.RETURN)
                driver.find_elements_by_name("button1")[0].send_keys(Keys.RETURN)
                time.sleep(4)
                
                # Saves page source        
                data = open(os.getcwd() + "/output/source" + str(page_num) + ".html", 'w')
                page_num += 1
                data.write(driver.page_source)
                data.close()
                time.sleep(2)
                driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')
                driver.switch_to_window(main_window)
                time.sleep(1)
    except:
        print "Error on " + line
        continue
    #else:
        #table = driver.find_element_by_tag_name('table')
        #refs = table.find_elements_by_xpath(".//tbody/tr/td/a")
        #for ref in refs:
            
   
print "\nFinished data collection"     
driver.close()