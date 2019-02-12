import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import chromedriver_binary
import urlparse

def scrape():
    driver = webdriver.Chrome()
    gs_target_url = 'https://globalcareers-goldmansachs.icims.com/jobs/search?pr=%s&searchCategory=44215&searchRelation=keyword_all'
    
    last_page = get_number_of_pages(get_last_url(driver, gs_target_url % 1))
    
    gs_job_title_class_name = 'title'
    gs_job_desc_class_name = 'description'
    gs_titles = []
    gs_desc = []

    for i in range(0, int(last_page[0]) + 1):
        target = gs_target_url % i
        driver.get(target)
        driver.switch_to.frame(driver.find_element_by_id('icims_content_iframe'))
        for e in driver.find_elements_by_class_name(gs_job_title_class_name):
            gs_titles.append(e.text)
        for e in driver.find_elements_by_class_name(gs_job_desc_class_name):
            gs_desc.append(e.text)

    print(gs_titles)
    print(gs_desc)
    driver.quit()

def get_last_url(driver, first):
    driver.get(first)
    driver.switch_to.frame(driver.find_element_by_id('icims_content_iframe'))
    last_url = driver.find_elements_by_class_name('iCIMS_Paging')[-1].find_elements_by_tag_name('a')[-1].get_attribute('href')
    return last_url

def get_number_of_pages(url):
    parsed = urlparse.urlparse(url)
    return urlparse.parse_qs(parsed.query)['pr']

scrape()