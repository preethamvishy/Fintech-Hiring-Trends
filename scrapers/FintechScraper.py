import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import chromedriver_binary

def scrape():
    driver = webdriver.Chrome()
    gs_target_url = 'https://globalcareers-goldmansachs.icims.com/jobs/search?pr=%s&searchCategory=44215&searchRelation=keyword_all'
    gs_targets = []
    gs_job_title_class_name = 'title'
    gs_job_desc_class_name = 'description'

    for i in range(0,32):
        gs_targets.append(gs_target_url % i)

    gs_titles = []
    gs_desc = []
    for target in gs_targets: 
        driver.get(target)
        driver.switch_to.frame(driver.find_element_by_id('icims_content_iframe'))
        for e in driver.find_elements_by_class_name(gs_job_title_class_name):
            gs_titles.append(e.text)
        for e in driver.find_elements_by_class_name(gs_job_desc_class_name):
            gs_desc.append(e.text)

    print(gs_titles)
    print(gs_desc)
    driver.quit()

scrape()