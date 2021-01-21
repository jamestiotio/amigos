#!/usr/bin/python3
# -*- coding: utf-8 -*-

import constants
import re
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from typing import Dict, List


class DesignGroupStudentIDCrawler(scrapy.Spider):
    """
    Spider definition to crawl the student ID list of design groups on SUTD's eDimension page.
    Uses hybrid implementation of Scrapy and Selenium.
    """

    # Override attributes of superclass
    name = "designgroupstudentidbot"
    allowed_domains = [constants.EDIMENSION_GENERAL_URL, constants.EDIMENSION_LOGIN_URL]
    start_urls = [constants.EDIMENSION_PHOTO_ROSTER_URL]

    # Override method of superclass to yield a Request with the specified eDimension cookie parameter
    def start_requests(self):
        url = self.start_urls[0]

        # With the cookie that has been obtained through logging in and an automatic redirect to the desired URL, we begin collecting the corresponding data of student IDs
        yield scrapy.Request(
            url=url,
            cookies=self.edimension_cookie,
            callback=self.parse,
        )

    # Override method of superclass to return the response object (this method needs to be properly defined)
    def parse(self, response):
        # It is Scrapy's requirement for the parse() method to yield/return an iterable of Request and/or item objects
        yield {"output": response}


class DesignTeams:
    """
    Class of helper functions to scrape 03.007 Introduction to Design groups.
    """

    def __init__(self):
        # Define inner function to be called by the event signal listener (from the dispatcher)
        def crawler_results(signal, sender, item, response, spider):
            assert item["output"] == response
            self.teams = self.process(item["output"])

        # Use scrapy's dispatcher to get output from the spider
        dispatcher.connect(crawler_results, signal=scrapy.signals.item_scraped)

        # Initiate the logging in procedure
        self.login()

        # Use default settings
        process = CrawlerProcess(settings=scrapy.settings.Settings())

        process.crawl(
            DesignGroupStudentIDCrawler, edimension_cookie=self.edimension_cookie
        )

        # Blocking process until all crawling jobs are finished
        process.start()

    # Get an eDimension login cookie using Selenium, which is passed over to Scrapy for further usage and processing (separate this from the Scrapy spider class for better code management)
    def login(self):
        url = constants.EDIMENSION_PHOTO_ROSTER_URL

        # Use headless to not open a new browser window
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")

        # This requires the `geckodriver` binary executable to be present in the declared `PATH` system environment variable
        driver = webdriver.Firefox(options=options)

        # Clear and clean up prior login sessions
        driver.delete_all_cookies()

        # Begin procedure of logging in into eDimension
        driver.get(url)

        # Set global implicit wait time interval
        driver.implicitly_wait(10)

        # Explicit wait until the necessary element is available (which implies that page is ready)
        wait = WebDriverWait(driver, 5)
        wait.until(EC.presence_of_element_located((By.ID, "loginOptionsMobile")))

        agree_button_exists = False

        try:
            driver.find_element(By.ID, "agree_button")
            agree_button_exists = True
        except NoSuchElementException:
            pass

        # Click the `Agree & Continue` button to enable cookies for Blackboard, if it is present
        if agree_button_exists:
            driver.find_element_by_xpath('//*[@id="agree_button"]').click()

        # Click the `SUTD Network ID` login option button
        driver.find_element_by_xpath('//*[@id="loginOptionsMobile"]/div[2]').click()

        # Check if a 503 Service Unavailable response code is returned, and then refresh the page if necessary
        while driver.page_source == constants.EDIMENSION_ERROR_PAGE_SOURCE:
            driver.refresh()

        # Enter the provided eDimension's username and password into the corresponding input textboxes
        driver.find_element_by_xpath('//*[@id="userNameInput"]').send_keys(
            constants.EDIMENSION_USERNAME
        )
        driver.find_element_by_xpath('//*[@id="passwordInput"]').send_keys(
            constants.EDIMENSION_PASSWORD
        )

        # Click the `Sign in` button
        driver.find_element_by_xpath('//*[@id="submitButton"]').click()

        # This rarely happens, but it could potentially happen
        if driver.page_source == constants.EDIMENSION_ERROR_PAGE_SOURCE:
            raise RuntimeError(
                "Sorry! Something bad has happened. Please re-run the script after ensuring that there exists a stable Internet connection and after waiting for a while."
            )

        # Explicit wait until the necessary element is available (this is super important, since it implies a successful complete login, and otherwise, wrong cookies would be produced without this)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, "containerdiv")))

        # Store the cookie in a variable
        self.edimension_cookie = driver.get_cookies()

        # Graciously terminate and deactivate the WebDriver session to prevent memory leak
        driver.quit()

    # Process the output response object to return the whole accordion div separated into two parts: the h3 heading tag for the group numbers and the actual tabular content (roster tables stripped from their own container sections) of the student IDs
    def process(self, output) -> Dict[str, Dict[str, List[int]]]:
        result = {}

        # Strip some unnecessary whitespaces, newlines and tabs from the headers, as well as ignore the irrelevant headers ("All Students", "Others", "Teaching Assistants" and "Instructors")
        team_numbers = [
            header.strip()
            for header in output.css("h3.accordion-header::text").getall()[1::2]
        ][1:-3]

        # Grab the necessary relevant selector objects
        raw_student_id_values = output.xpath('//table[has-class("roster")]//tr')[1:-3]

        data = list(zip(team_numbers, raw_student_id_values))

        index = 0
        current_cohort_class = 0

        # We can do this processing here, since we can still use the corresponding selectors (instead of doing it using inflexible and ugly hard-coded regex and/or string-based slicings/selections)
        while index < len(data) - constants.DESIGN_NUM_OF_GROUPS[-1]:
            counter = 1

            if bool(re.search("^SC[0-9]{2}$", data[index][0].strip())):
                current_cohort = {}

                for team in data[
                    index
                    + 1 : index
                    + constants.DESIGN_NUM_OF_GROUPS[current_cohort_class]
                    + 1
                ]:
                    if bool(re.search("^SC[0-9]{2}-T[0-9]{2}$", team[0].strip())):
                        current_cohort[team[0]] = [
                            int(i)
                            for i in team[1].xpath(".//td//b[1]//text()").getall()
                        ]
                        counter += 1

                result[data[index][0]] = current_cohort

            current_cohort_class += 1
            index += counter

        return result