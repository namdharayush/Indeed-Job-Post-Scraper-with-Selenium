import time
import os
import re

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from fake_useragent import UserAgent
import random
from datetime import datetime, timedelta
from indeed_mongo import Indeed_Mongo

class IndeedScraper:

    def __init__(self):
        self.chrome_options = Options()

        # if site has been block due to heavily request same user-agent or proxies so please change the user-agent.

        # self.ua= UserAgent()
        # self.user_agent = self.ua.random
        # print(self.user_agent)
        # self.chrome_options.add_argument(f'--user-agent={self.user_agent}')
        self.service = Service()
        self.main_url = 'https://in.indeed.com/'
        self.driver = self.start_driver(self.main_url)
        self.output_file = 'indeed.csv'
        self.mongo_client = Indeed_Mongo()
        self.mongo_client.clear_all_jobs_14_or_above()
        self.next_page_link = ''

    def start_driver(self,url):
        driver = webdriver.Chrome(options=self.chrome_options, service=self.service)
        driver.maximize_window()
        driver.get(url)
        return driver

    def scrape(self):
        keywords = {'web developer': [''], 'python developer': ['mumbai', 'pune', 'delhi'], 'full stack developer': ['chennai', 'banglore', 'gurgaon']} # Keywords and locations for job search
        for keyword in keywords.keys():
            try:
                # Wait until the keyword input field is located
                input_search_by_keyword = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH,"//input[@id='text-input-what']")))
                time.sleep(1)
                # Enter the keyword
                input_search_by_keyword.send_keys(keyword)
                time.sleep(1)
                # Loop through each location for the current keyword
                for keyword_wise_locations in keywords[keyword]:
                    try:
                        # Wait until the location input field is located
                        input_search_by_location = WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, "//input[@id='text-input-where']")))
                        input_search_by_location.send_keys(keyword_wise_locations)
                        # Scrape the job page
                        self.job_page_scrape()
                        # If location is not empty
                        if keywords[keyword] != ['']:
                            # Wait until the location input field is located and click it
                            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@id='text-input-where']"))).click()
                            # Clear the location input field
                            clear_input_where_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                            (By.XPATH, '//button[@aria-label="Clear location input"]'))).click()

                    except Exception as e:
                        print(e)
                time.sleep(1)
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@id='text-input-what']"))).click()
                time.sleep(1)
                clear_input_what_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[@aria-label="Clear what input"]'))).click()

            except Exception as e:
                print(e)


    #Try to close the email signup modal if it appears
    def close_email_model(self):

        try:
            close_email = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//button[@aria-label='close']"))).click()
        except:
            pass
    def job_page_scrape(self):
        try:
            search_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, "//button[@class='yosegi-InlineWhatWhere-primaryButton']"))).click()
        except Exception as e:
            print(e)

        time.sleep(random.uniform(1,3))

        try:
            date_posted = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//button[@id='filter-dateposted']")))
            date_posted.click()
        except Exception as e:
            time.sleep(2)
            try:
                date_posted = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//button[@id='filter-dateposted']")))
                date_posted.click()
            except:
                print(e)
        try:
            date_select = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//ul[@id='filter-dateposted-menu']/li[4]/a"))).click()
        except Exception as e:
            print(e)
        self.close_email_model()
        time.sleep(1)
        try:
            self.all_jobs_for_while()
        except Exception as e:
            print("Site blocked due to too many requests. Please try again later or change the user agent.")

    def retries_mechanism(self,retries_count,max_retries):
        retries_count += 1
        time.sleep(20)
        self.driver.close()
        time.sleep(2)
        self.driver = self.start_driver(self.next_page_link)  # Reinitialize the driver
        self.driver.get(self.next_page_link)
        self.close_email_model()
        self.all_jobs_for_while()
    def all_jobs_for_while(self):
        retries_count = 0
        max_retries = 5
        while True:
            try:
                self.close_email_model()
                all_jobs = self.driver.find_elements(By.XPATH, "//div[@class='job_seen_beacon']")
                if not all_jobs:
                    raise Exception("CAPTCHA or No Jobs Found")
            except:
                if retries_count == max_retries:
                    return
                self.retries_mechanism(retries_count,max_retries)
                continue

            for job in all_jobs:
                try:
                    job_id = job.find_element(By.XPATH, ".//a").get_attribute('id').split("_")[1]
                except:
                    job_id = ''
                if self.mongo_client.check_job_exists(job_id):
                    print("This Job Id Exists  : " , job_id)
                    continue
                try:
                    company = job.find_element(By.XPATH, './/span[@data-testid="company-name"]').text
                except:
                    company = ''
                try:
                    job_link = job.find_element(By.XPATH, ".//a").get_attribute('href')
                except:
                    job_link = ''
                try:
                    job_posted = job.find_element(By.XPATH,
                                                  './/span[@data-testid="myJobsStateDate"] | .//span[@data-testid="myJobsState"]').text.split(
                        '\n')[1]
                    today_date = datetime.today()
                    if 'just posted' in job_posted.lower():
                        job_posted = today_date.strftime('%d/%m/%Y')
                    else:
                        match = re.search(r'(\d+) day', job_posted)
                        if match:
                            days_ago = int(match.group(1))
                            target_date = today_date - timedelta(days=days_ago)
                            job_posted = target_date.strftime('%d/%m/%Y')
                        else:
                            job_posted = ''
                except:
                    job_posted = ''
                try:
                    job.click()
                except:
                    if retries_count == max_retries:
                        return
                    self.retries_mechanism(retries_count, max_retries)
                    break
                time.sleep(1)
                try:
                    title = self.driver.find_element(By.XPATH,"//div[contains(@class,'jobsearch-JobInfoHeader-title')]//h2/span").text.split('\n')[0]
                except:
                    title = ''
                try:
                    salary = self.driver.find_element(By.XPATH,"//h3[contains(text(),'Pay')]/following-sibling::div//div[contains(@class,'js-match-insights-provider-tvvxwd')][1]").text
                except:
                    salary = ''
                try:
                    job_type = self.driver.find_elements(By.XPATH,"//h3[contains(text(),'Job type')]/following-sibling::div//div[contains(@class,'js-match-insights-provider-tvvxwd')][2]")
                    job_type = [x.text for x in job_type]
                    if not ''.join(job_type).strip():
                        job_type = self.driver.find_elements(By.XPATH,"//h3[contains(text(),'Job type')]/following-sibling::div//div[contains(@class,'js-match-insights-provider-tvvxwd')][1]")
                        job_type = [x.text for x in job_type]
                except:
                    job_type = ''
                try:
                    shift_schedule = self.driver.find_elements(By.XPATH,
                   "//h3[contains(text(),'Shift and schedule')]/following-sibling::div//div[contains(@class,'js-match-insights-provider-tvvxwd')][2]")
                    shift_schedule = [x.text for x in shift_schedule]
                    if not ''.join(shift_schedule).strip():
                        shift_schedule = self.driver.find_elements(By.XPATH,
                   "//h3[contains(text(),'Shift and schedule')]/following-sibling::div//div[contains(@class,'js-match-insights-provider-tvvxwd')][1]")
                        shift_schedule = [x.text for x in shift_schedule]
                except:
                        shift_schedule = ''
                try:
                    apply_link = self.driver.find_element(By.XPATH,"//div[@id='applyButtonLinkContainer']//button").get_attribute('href')
                except:
                    apply_link = 'apply through indeed'
                try:
                    benefits = self.driver.find_element(By.XPATH,"//h2[@id='benefitsSectionTitle']/following-sibling::div//ul/li").text
                except:
                    benefits = ''
                try:
                    location = self.driver.find_element(By.XPATH, "//div[@id='jobLocationText']//span").text
                except:
                    location = ''
                try:
                    jds_data = {}
                    job_descriptions = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_all_elements_located((By.XPATH, "//div[@id='jobDescriptionText']//ul")))
                    for jd in job_descriptions:
                        try:
                            jd_key = jd.find_element(By.XPATH, 'preceding-sibling::p[1]').text
                            if len(jd_key) > 50 or jd_key.lower() in ['schedule:', 'job type:', 'salary:', 'pay:'] or len(''.join(jd_key).split(':')) > 2 :
                                continue
                        except:
                            continue
                        jd_value = [x.text for x in jd.find_elements(By.XPATH, './li')]
                        if not jd_value or not jd_key:
                            continue
                        jds_data[jd_key[0:len(jd_key) - 1]] = jd_value
                except:
                    jds_data = ''
                data = {
                    'job_id': job_id,
                    'company' : company,
                    'apply_link' : apply_link,
                    'job_link': job_link,
                    'job_posted': job_posted,
                    'title': title,
                    'salary': salary,
                    'job_type': job_type,
                    'shift_schedule': shift_schedule,
                    'benefits': benefits,
                    'location': location,
                    'description': jds_data,

                }
                self.create_csv(data)
            try:
                next_page = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//a[@data-testid="pagination-page-next"]')))
                self.next_page_link = next_page.get_attribute('href')
                next_page.click()
                retries_count = 0
                time.sleep(3)
            except:
                break

    def create_csv(self, data):
        df = pd.DataFrame([data])
        if os.path.exists(self.output_file):
            df.to_csv(self.output_file, header=False, index=False, mode='a')
        else:
            df.to_csv(self.output_file, header=True, index=False, mode='a')
        self.mongo_client.insert_data(data)

    def create_excel(self,data):
        df = pd.DataFrame([data])
        if os.path.exists(self.output_file):
            with pd.ExcelWriter(self.output_file, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
                sheet = writer.sheets.get('Sheet1')
                start_row = sheet.max_row if sheet else 0
                df.to_excel(writer, startrow=start_row, index=False, header=False)
        else:
            df.to_excel(self.output_file, index=False , header=True)

if __name__ == '__main__':
    webscrapper = IndeedScraper()
    webscrapper.scrape()
