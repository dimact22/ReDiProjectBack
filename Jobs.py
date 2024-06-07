from selenium import webdriver
from openpyxl import load_workbook, Workbook
from openpyxl.styles import PatternFill, Border, Side
from selenium.webdriver.chrome.options import Options
import time
import sys

# Importing job search functions from different modules
from linkedin import linkedin_info
from indeed import indeed_info
from stepstone import stepstone_info

# Define a class to manage job search information


class Jobs:
    def __init__(self, name, job_title, loc, time, count):
        self.name = name  # Name of the Excel file
        self.job_title = job_title  # Job title to search for
        self.loc = loc  # Location to search for jobs
        self.time = time  # Time range for job search
        self.count = count  # Maximum number of jobs to find

    # Method to create a new Excel file with a header row
    def create_exel(self):
        wb = Workbook()
        sheet = wb.active
        sheet.title = 'Jobs_info'  # Set the title of the sheet
        sheet.append(['Job title', 'Company name', 'Location',
                     'Description', "Link"])  # Add header row

        header_fill = PatternFill(
            start_color="FFFF00", end_color="FFFF00", fill_type="solid")  # Set header fill color
        for cell in sheet[1]:  # Apply the fill color to each cell in the header row
            cell.fill = header_fill
        wb.save(self.name)  # Save the workbook with the specified name

    # Method to search for jobs on Indeed and save to Excel
    def found_indeed(self):
        try:
            indeed_info(self.job_title, self.loc,
                        self.name, self.time, self.count)
        except Exception as e:
            print(f"Error in Indeed: {e}")

    # Method to search for jobs on Stepstone and save to Excel
    def found_stepstone(self):
        try:
            stepstone_info(self.job_title, self.loc,
                           self.name, self.time, self.count)
        except Exception as e:
            print(f"Error in Stepstone: {e}")

    # Method to search for jobs on LinkedIn and save to Excel
    def found_linkedin(self):
        try:
            linkedin_info(self.job_title, self.loc,
                          self.name, self.time, self.count)
        except Exception as e:
            print(f"Error in LinkedIn: {e}")

    # Method to search for jobs on all platforms and save to Excel
    def found_all_works(self):
        self.create_exel()  # Create a new Excel file
        self.found_indeed()  # Search for jobs on Indeed
        self.found_stepstone()  # Search for jobs on Stepstone
        self.found_linkedin()  # Search for jobs on LinkedIn
