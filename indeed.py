from selenium import webdriver
from openpyxl import load_workbook, Workbook
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import sys


def indeed_info(job_title, location, e_name, t, count, driver):
    try:
        count = int(count)  # Ensure 'count' is an integer
    except Exception as e:
        print(e)
        return

    try:
        wb = load_workbook(e_name)  # Load the Excel workbook
        sheet = wb.active  # Select the active sheet
    except Exception as e:
        print(f"Error loading workbook: {e}")
        return 0

    c_m = 0
    try:
        driver.get(
            f"https://de.indeed.com/jobs?q={job_title}&l={location}&from=searchOnDesktopSerp&hl=de&fromage={t}"
        )  # Open the Indeed job search page
        nav_element = driver.find_element(
            By.CSS_SELECTOR, 'nav[role="navigation"]')
        # Count the number of navigation elements (pages)
        c_m = len(nav_element.find_elements(By.CSS_SELECTOR, "li"))
    except (NoSuchElementException, Exception) as e:
        print(e)
        return

    c = 0

    for page in range(0, c_m):  # Iterate through each page of search results
        try:
            driver.get(
                f"https://de.indeed.com/jobs?q={job_title}&l={location}&fromage={t}&start={page*10}"
            )  # Open the job search results for the current page
            e = driver.find_element(By.ID, "mosaic-jobResults")
            li_elements1 = e.find_element(By.ID, "mosaic-provider-jobcards")
            li_elements2 = li_elements1.find_element(
                By.CSS_SELECTOR, "ul.css-zu9cdh")
            li_elements3 = li_elements2.find_elements(
                By.CSS_SELECTOR, "li.css-5lfssm")  # Get all job postings on the page
        except (NoSuchElementException, TimeoutException, WebDriverException) as e:
            print(f"Error while loading page or finding elements: {e}")
            continue

        for job_element in li_elements3:  # Iterate through each job posting
            info = []
            if c == count // 3:  # Stop if the count limit is reached
                return
            try:
                job_title2 = job_element.find_element(
                    By.CSS_SELECTOR, "a.jcs-JobTitle").text  # Get the job title
                info.append(job_title2)
                company_name = job_element.find_element(By.CLASS_NAME, "company_location").find_element(
                    By.CSS_SELECTOR, "[data-testid='company-name']"
                ).text  # Get the company name
                info.append(company_name)
                location2 = job_element.find_element(By.CLASS_NAME, "company_location").find_element(
                    By.CSS_SELECTOR, "[data-testid='text-location']"
                ).text  # Get the job location
                info.append(location2)
                try:
                    description = job_element.find_element(
                        By.CLASS_NAME, "css-9446fg").text  # Get the job description
                    info.append(description)
                except NoSuchElementException as e:
                    print(f"Error while extracting job info: {e}")
                    info.append("------")
                link = job_element.find_element(
                    By.CSS_SELECTOR, "a.jcs-JobTitle").get_attribute('href')  # Get the job link
                info.append(link)
            except NoSuchElementException as e:
                print(f"Error while extracting job info: {e}")

            try:
                if info[3] == "":
                    info[3] = "Didn't find any information"
                if info[0] != '' or info[1] != '' or info[2] != '':
                    try:
                        # Append job info to the Excel sheet
                        sheet.append(info)
                        wb.save(e_name)  # Save the workbook
                        c += 1
                    except Exception as e:
                        print(f"Error saving workbook: {e}")
                        continue
            except:
                print("Some error in indeed")
