from selenium import webdriver
from openpyxl import load_workbook
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time


def stepstone_info(job_title, location, e_name, t, count):
    try:
        count = int(count)  # Ensure 'count' is an integer
    except Exception as e:
        print(e)
        return

    options = Options()
    options.add_argument("--lang=en")  # Set browser language to English
    options.add_argument("--window-size=1920,1080")  # Set browser window size
    options.add_argument("--headless")  # Run browser in headless mode (no GUI)
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )  # Set user agent to mimic a real browser
    driver = webdriver.Chrome(options=options)

    try:
        wb = load_workbook(e_name)  # Load the Excel workbook
        sheet = wb.active  # Select the active sheet
    except Exception as e:
        print(f"Error loading workbook: {e}")
        return

    try:
        driver.get(
            f"https://www.stepstone.de/jobs/{job_title}/in-{location}?radius=30&page=1&ag=age_{t}"
        )  # Open the StepStone job search page
        page_info_element = driver.find_element(By.CLASS_NAME, 'res-tqs0ve')
        page_info_text = page_info_element.text
        # Get the total number of pages
        count_of_page = int(page_info_text.split()[-1])
    except (NoSuchElementException, TimeoutException, WebDriverException) as e:
        print(f"Error while loading page or finding elements: {e}")
        return

    c = 0

    # Iterate through each page of search results
    for page in range(1, count_of_page + 1):
        try:
            driver.get(
                f"https://www.stepstone.de/jobs/{job_title}/in-{location}?radius=30&page={page}&ag=age_{t}"
            )  # Open the job search results for the current page
            # Get all job postings on the page
            vac1 = driver.find_elements(By.CSS_SELECTOR, 'article.res-1p8f8en')
        except (NoSuchElementException, TimeoutException, WebDriverException) as e:
            print(f"Error while loading page or finding job articles: {e}")
            continue

        for job in vac1:  # Iterate through each job posting
            info = []
            if c == count // 3:  # Stop if the count limit is reached
                driver.quit()
                return

            try:
                i2 = job.find_element(By.CLASS_NAME, 'res-urswt')
                # Get the job title
                info.append(i2.find_element(By.CLASS_NAME, 'res-nehv70').text)
                # Get the company name
                info.append(i2.find_element(By.CLASS_NAME, 'res-btchsq').text)
                info.append(i2.find_element(By.CLASS_NAME, 'res-qchjmw').find_element(
                    By.CSS_SELECTOR, 'span.res-btchsq').text)  # Get the job location
            except NoSuchElementException as e:
                print(f"Error while extracting job details: {e}")
                continue

            try:
                desc = job.find_element(By.CLASS_NAME, "res-t9x10w")
                info.append(desc.text[:-5])  # Get the job description
            except NoSuchElementException:
                info.append("-----")  # Placeholder if description is not found

            try:
                link = i2.find_element(
                    By.CSS_SELECTOR, 'a.res-1foik6i').get_attribute('href')  # Get the job link
                info.append(link)
            except NoSuchElementException as e:
                print(f"Error while extracting job link: {e}")
                continue

            try:
                sheet.append(info)  # Append job info to the Excel sheet
                wb.save(e_name)  # Save the workbook
                c += 1
            except Exception as e:
                print(f"Error saving workbook: {e}")
                continue

    driver.quit()  # Quit the browser
