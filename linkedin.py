from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from openpyxl import load_workbook, Workbook
from selenium.webdriver.chrome.options import Options
import time


def linkedin_info(job_title, location, e_name, t, count):
    try:
        count = int(count)  # Ensure 'count' is an integer
    except Exception as e:
        print(e)
        return

    def scroll_to_bottom(driver):
        last_height = driver.execute_script(
            "return document.body.scrollHeight")

        while True:
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Allow time for the page to load

            new_height = driver.execute_script(
                "return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    options = Options()
    options.add_argument("--lang=en")  # Set browser language to English
    options.add_argument("--window-size=1920,1080")  # Set browser window size
    options.add_argument("--headless")  # Run browser in headless mode (no GUI)
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )  # Set user agent to mimic a real browser
    driver = webdriver.Chrome(options=options)

    try:
        t = int(t) * 86400  # Convert 't' to seconds for the LinkedIn filter
        driver.get(
            f"https://www.linkedin.com/jobs/search/?keywords={job_title}&location={location}&f_TPR=r{t}"
        )  # Open the LinkedIn job search page
    except WebDriverException as e:
        print(f"Error loading LinkedIn page: {e}")
        driver.quit()
        return

    try:
        wb = load_workbook(e_name)  # Load the Excel workbook
        sheet = wb.active  # Select the active sheet
    except Exception as e:
        print(f"Error loading Excel workbook: {e}")
        driver.quit()
        return

    try:
        # Scroll to the bottom to load all job postings
        scroll_to_bottom(driver)
    except WebDriverException as e:
        print(f"Error scrolling the page: {e}")
        driver.quit()
        return

    c = 0
    try:
        results_list = driver.find_element(
            By.CLASS_NAME, "jobs-search__results-list")
        job_elements = results_list.find_elements(
            By.CSS_SELECTOR, "li")  # Get all job postings
    except NoSuchElementException as e:
        print(f"Error finding job results: {e}")
        driver.quit()
        return

    for job_elem in job_elements:  # Iterate through each job posting
        info = []
        if c == count // 3:  # Stop if the count limit is reached
            driver.quit()
            return
        try:
            job = job_elem.find_element(
                By.CSS_SELECTOR, "a")  # Get the job element
            info.append(job.text)  # Get the job title
            info.append(job_elem.find_element(
                By.CLASS_NAME, "base-search-card__subtitle").text)  # Get the company name
            info.append(job_elem.find_element(
                By.CSS_SELECTOR, "span.job-search-card__location").text)  # Get the job location
            # Placeholder for job description
            info.append("LinkedIn doesn't provide quick job descriptions")
            info.append(job.get_attribute("href"))  # Get the job link
        except NoSuchElementException as e:
            print(f"Error extracting job details: {e}")
            continue

        try:
            sheet.append(info)  # Append job info to the Excel sheet
            wb.save(e_name)  # Save the workbook
            c += 1
        except Exception as e:
            print(f"Error saving Excel workbook: {e}")
            continue

    driver.quit()  # Quit the browser
