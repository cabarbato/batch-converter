import os
import csv
import time
import pickle
import os.path
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

URL = os.environ["URL"]
SCOPES = os.environ["SCOPES"]
SPREADSHEET_ID = os.environ["SPREADSHEET_ID"]
SHEETS = os.environ["SHEETS"]

class GoogleDocGenerator:
    def __init__(self, page_type):
        self.page_type = page_type
        self.urls = []

    def authenticate(self, RANGE_NAME):
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range=RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('No urls found in that range')
        else:
            for row in values:
                self.urls.append(row)
            self.getGeneratorUrl()

    def fillInputField(self, id, text):
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
            (By.XPATH, "//input[@id='" + id + "']"))).clear()
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
            (By.XPATH, "//input[@id='" + id + "']"))).send_keys(text)

    def getGeneratorUrl(self):
        try:
            driver.set_page_load_timeout(30)
            driver.get(URL)
            for url in self.urls:
                self.generateDoc(url)
        except selenium.common.exceptions.TimeoutException as ex:
            print(ex)

    def generateDoc(self, row):
        self.fillInputField('document_url', row[0])
        if self.page_type == 1:
            self.fillInputField('document_url', row[1])
            self.fillInputField('document_url', row[2].split("; ")[0])
            self.fillInputField('document_url', row[2].split("; ")[1])
        driver.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(10)


driver = webdriver.Chrome()

start_row = input("Enter the first row # you'd like to generate files from: ")
end_row = input("Now enter the last row # to generate: ")

while True:
    page_type = input(
        "Select a page type by entering the corresponding number.\n" +
        "1. " + SHEETS[0] + "\n" +
        "2. " + SHEETS[1] + "\n"
    )

    page_type = int(page_type)
    GD = GoogleDocGenerator(page_type)

    if page_type not in (1, 2):
        print("Please enter a valid selection.")
    else:
        if page_type == 1:
            columns = ('D', 'F')
        else:
            columns = ('C', 'C')
        google_sheet_range = SHEETS[page_type - 1] + '!' + columns[0] + \
            str(start_row) + ':' + columns[1] + str(end_row) + ''
        GD.authenticate(google_sheet_range)
        break

driver.quit()
