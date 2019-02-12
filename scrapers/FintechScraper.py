import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import chromedriver_binary
import urlparse
import csv
import re

def scrape():
    driver = webdriver.Chrome()
    gs_target_url = 'https://careers-goldmansachs.icims.com/jobs/search?pr=%s&searchRelation=keyword_all&schemaId=&o='
    
    last_page = get_number_of_pages(get_last_url(driver, gs_target_url % 1))
    
    gs_job_title_class_name = 'title'
    gs_job_desc_class_name = 'description'
    gs_jobs = []
    

    for i in range(0, int(last_page[0]) + 1):
        target = gs_target_url % i
        driver.get(target)
        driver.switch_to.frame(driver.find_element_by_id('icims_content_iframe'))

        for title in driver.find_elements_by_class_name(gs_job_title_class_name):
            for job in title.find_elements_by_tag_name('a'):
                gs_jobs.append(job.get_attribute('href'))

    job_list = scrape_jobs(driver, gs_jobs)
    export_to_csv(job_list)
    
def get_last_url(driver, first):
    driver.get(first)
    driver.switch_to.frame(driver.find_element_by_id('icims_content_iframe'))
    last_url = driver.find_elements_by_class_name('iCIMS_Paging')[-1].find_elements_by_tag_name('a')[-1].get_attribute('href')
    return last_url

def get_number_of_pages(url):
    parsed = urlparse.urlparse(url)
    return urlparse.parse_qs(parsed.query)['pr']

def scrape_jobs(driver, job_urls):
    job_list = []
    for job in job_urls:
        try:
            driver.get(job)
            driver.switch_to.frame(driver.find_element_by_id('icims_content_iframe'))
            jobdict = {}

            jobdict['Job Title'] = driver.find_element_by_id('iCIMS_Header').text.encode("utf-8")
            for dl in driver.find_elements_by_tag_name('dl'):
                key = dl.find_elements_by_class_name('iCIMS_JobHeaderField')[0].text.encode("utf-8")
                val = dl.find_elements_by_class_name('iCIMS_JobHeaderData')[0].text.encode("utf-8")
                jobdict[key] = val

            jobdict['Job Responsibilities'] =  re.sub('[^A-Za-z]+', ' ', driver.find_elements_by_class_name('iCIMS_Expandable_Text')[0].text.encode("utf-8").lower())
            location = driver.find_elements_by_class_name('left')[0]
            jobdict['Location'] = location.find_elements_by_tag_name('span')[1].text.encode("utf-8")
            job_list.append(jobdict)
            # append_to_csv(jobdict)
        except:
            print('error')
            continue

    return job_list

def export_to_csv(job_list):
    keys = job_list[0].keys()
    with open('gs_jobs.csv', 'wb') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(job_list)


def append_to_csv(jobdict):
    keys = jobdict.keys()
    with open('gs_jobs.csv', 'a') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writerow(jobdict)

scrape()