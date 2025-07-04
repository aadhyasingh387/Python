import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import warnings

# Suppress warnings (related to SSL/TLS verification)
warnings.filterwarnings("ignore", message="Unverified HTTPS request")

# Set up the WebDriver (this will download the driver automatically if needed)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# URL for the attendance page
url = "https://sgi.servergi.com:8077/ISIMSGI/Home"

# Date range
date_from = "01/04/2025"
date_to = datetime.now().strftime("%d/%m/%Y")

# Load the page
driver.get(url)

# Wait for the page to load fully
try:
    # Wait for the required elements (ViewState fields) to load (adjust the time limit if necessary)
    viewstate = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "__VIEWSTATE"))
    ).get_attribute("value")
    
    eventvalidation = driver.find_element(By.ID, "__EVENTVALIDATION").get_attribute("value")
    viewstategenerator = driver.find_element(By.ID, "__VIEWSTATEGENERATOR").get_attribute("value")
    
    print("✅ Viewstate fields found.")
except Exception as e:
    print(f"⚠️ Error fetching Viewstate fields: {e}")
    driver.quit()
    exit()

# Simulate "Date Wise" button click with date input
driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_ddlAttendanceType").send_keys("DateWise")
driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_txtFromDate").send_keys(date_from)
driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_txtToDate").send_keys(date_to)
driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_btnSubmit").click()

# Wait for the results page to load
time.sleep(5)

# Now, extract the attendance percentage from the result page
try:
    rows = driver.find_elements(By.XPATH, "//tr")
    total_attendance = None
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        if any("Total" in cell.text for cell in cells):
            for cell in cells:
                try:
                    value = float(cell.text.strip())
                    if 0 <= value <= 100:
                        total_attendance = value
                        break
                except ValueError:
                    continue

    if total_attendance:
        print(f"✅ Total Attendance: {total_attendance}%")
    else:
        print("⚠️ Couldn't find total attendance.")
except Exception as e:
    print(f"⚠️ Error extracting attendance data: {e}")

# Close the driver
driver.quit()
