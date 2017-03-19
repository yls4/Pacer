import urllib2
import time
import csv
import sys
import os
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from _io import open
from _ast import Str
from locale import str
from test.test_iterlen import len
from pip._vendor.distlib.compat import raw_input
from mimify import File

court_number_regex = "[0-9]{2}-[0-9]{5}-[a-zA-Z0-9]{5}"
court_number_regex2 = "[0-9]{2}-[0-9]{5}"
creditor_number_regex = "([0-9]+)"
cr_regex = "(cr)"
case_type_string = "Case type:"
chapter_string = "Chapter:"
asset_string = "Asset:"
vol_string = "Vol:"
judge_string = "Judge:"
date_filed_string = "Date filed:"
date_of_last_filing_string = "Date of last filing:"

inputPath = os.getcwd() + "/output/"
print "Enter output folder name"
o = raw_input()
outputPath = os.getcwd() + "/" + o + "/"
if not os.path.exists(outputPath):
    os.mkdir(outputPath)
print outputPath
print "Enter QR_Code"
qr_code = raw_input()

print "Please wait..."

# Gets output Folder
driver = webdriver.Firefox()
main_window = driver.current_window_handle
counter = 0
data = open(outputPath + "source" + str(counter) + qr_code + ".txt", 'w')

for file in os.listdir(inputPath):
    if file.endswith(".html"):
        driver.find_element_by_css_selector('body').send_keys(Keys.CONTROL + 't')
        print "Parsing through: " + file
        driver.get("file:///" + inputPath + file)

        # Reads main data
        if len(driver.find_elements_by_css_selector('center')) != 0:
            main_data = driver.find_element_by_css_selector('center').text
        else:
            print "Could not find main_data for " + file
            continue
        
        if len(driver.find_elements_by_tag_name("b")) != 0:
            case_number = driver.find_elements_by_tag_name("b")[0].text
        else:
            print "Could not find case_number for " + file
            continue
        
        if len(main_data.split(case_number)) >= 2:
            if len(main_data.split(case_number)[1].split(case_type_string)) != 0:
                name = main_data.split(case_number)[1].split(case_type_string)[0].strip()
            else:
                print "Could not find name for " + file
                continue
        else:
            print "Could not find name for " + file
            continue

        if len(main_data.split(case_type_string)) >= 2:
            if len(main_data.split(case_type_string)[1].split(chapter_string)) != 0:
                case_type = (main_data.split(case_type_string))[1].split(chapter_string)[0].strip()
            else:
                print "Could not find case_type for " + file
                continue
        else:
            print "Could not find case_type for " + file
            continue
        
        if len(main_data.split(chapter_string)) >= 2:
            if len(main_data.split(chapter_string)[1].split(asset_string)) != 0:
                chapter = (main_data.split(chapter_string))[1].split(asset_string)[0].strip()
            else:
                print "Could not find chapter for " + file
                continue
        else:
            print "Could not find chapter for " + file
            continue
        
        if len(main_data.split(asset_string)) >= 2:
            if len(main_data.split(asset_string)[1].split(vol_string)) != 0:
                asset = (main_data.split(asset_string))[1].split(vol_string)[0].strip()
            else:
                print "Could not find asset for " + file
                continue
        else:
            print "Could not find asset for " + file
            continue
            
        if len(main_data.split(vol_string)) >= 2:
            if len(main_data.split(vol_string)[1].split(judge_string)) != 0:
                vol = (main_data.split(vol_string))[1].split(judge_string)[0].strip()
            else:
                print "Could not find vol for " + file
                continue
        else:
            print "Could not find vol for " + file
            continue
            
        if len(main_data.split(judge_string)) == 2:
			judge = (main_data.split(judge_string))[1].split(date_filed_string)[0].strip()
        else:
			judge = "None"
        
        if len(main_data.split(date_filed_string)) >= 2:
            if len(main_data.split(date_filed_string)[1].split(date_of_last_filing_string)) != 0:
                date_filed = (main_data.split(date_filed_string))[1].split(date_of_last_filing_string)[0].strip()
            else:
                print "Could not find date_filled_string for " + file
                continue
        else:
            print "Could not find date_filled_string for " + file
            continue
        
        if len(main_data.split(date_of_last_filing_string)) >= 2:
            if len(main_data.split(date_of_last_filing_string)[1].split("Creditors")) != 0:
                date_of_last_filing = (main_data.split(date_of_last_filing_string))[1].split("Creditors")[0].strip()
            else:
                print "Could not find date_of_last_filing for " + file
                continue
        else:
            print "Could not find date_of_last_filing for " + file
            continue
 
        #print "Case Number: " + case_number
        #print "Name: " + name
        #print "Case type: " + case_type
        #print "Chapter: " + chapter
        #print "Asset: " + asset
        #print "Vol: " + vol
        #print "Judge: " + judge
        #print "Date Filed: " + date_filed
        #print "Date of last filing: " + date_of_last_filing
        
        # Reads creditor data
        tables = driver.find_elements_by_css_selector("table")
        if len(tables) != 0:
            table = tables[0]
            rows = table.find_elements_by_xpath(".//tr")
        else:
            print "Empty file for " + file
            continue
        #cells = rows[0].find_elements_by_xpath(".//td")
        #cell = cells[0]
        #print cell.text
        #for row in rows:
            #cells = row.find_elements_by_tag_name("td")
            #if (len(cells) > 0):
                #cell = cells[0]
                #print cell.text
        # Generates letter
        output = ""
        for row in rows:
            cells = row.find_elements_by_xpath(".//td")
            if len(cells) > 0:
				output += cells[0].text + unicode(chr(12)) + "\n\nNotice of Recent Bankruptcy Filing\n\nDetails:\n\n" + case_number + " " + name + "\nCase type: " + case_type + " Chapter: " + chapter + " Asset: " + asset + " Vol: " + vol + " Judge: " + judge + "\nDate filed: " + date_filed + " Date of last filing: " + date_of_last_filing + unicode(chr(12))
            else:
				output += "No creditors"
        driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')
        time.sleep(1)
        data.write(output)
        counter += 1
        

print "Finished letter generation"
driver.close()
