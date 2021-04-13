## 📝 Google Docs Batch Converter

This script uses the Google API to access a Sheet with url's of Google Docs. once collected, it uses Selenium to automate the conversion process.

---

### Usage:
1. Create an .env file with your Google Sheets info and destination website url.
2. If using Docker, run `docker-compose up`, then run `docker-compose run batchconverter python script.py first_row last_row sheet_index`. Otherwise, run `pip install -r requirements.txt` prior to the script to get all the required dependencies, and make sure you have the chromedriver saved somewhere in your Path. You can either pass the first row, last row and sheet index as arguments like with Docker, or you can input them when prompted.
3. After script is complete, you can copy all the files generated using a command like `docker cp batchconverter:/app output`. If you opted for using your system's version of Python, all files should be downloaded to Chrome's default download folder.

---

### This script utilizes:

* [Google Sheets API v4](https://developers.google.com/sheets/api/quickstart/python)
* [Selenium WebDriver for Python](https://www.selenium.dev/selenium/docs/api/py/api.html)