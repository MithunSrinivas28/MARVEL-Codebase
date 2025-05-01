from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

# Your Chromedriver path
chrome_driver_path = "C:\Users\mithun\Downloads\chromedriver-win64\chromedriver-win64"  # Update this!

# Set up headless browser (or remove headless if you wanna see the browser)
options = Options()
options.add_argument("--headless=new")  # Remove this line if you want to see browser
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--window-size=1920,1080")

service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)

# Step 1: Go to Google Flights
driver.get("https://www.google.com/travel/flights")
wait = WebDriverWait(driver, 20)

# Step 2: Enter source and destination
def enter_location():
    wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Where from?']"))).click()
    time.sleep(1)
    from_input = driver.find_element(By.XPATH, "//input[@placeholder='Where from?']")
    from_input.clear()
    from_input.send_keys("Bengaluru")
    time.sleep(2)
    driver.find_element(By.XPATH, "//li[@data-item-index='0']").click()

    wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Where to?']"))).click()
    time.sleep(1)
    to_input = driver.find_element(By.XPATH, "//input[@placeholder='Where to?']")
    to_input.clear()
    to_input.send_keys("Hyderabad")
    time.sleep(2)
    driver.find_element(By.XPATH, "//li[@data-item-index='0']").click()

    # Click search / date or any other part to trigger search
    time.sleep(2)
    driver.find_element(By.XPATH, "//div[contains(@class, 'RMZbK')]").click()

enter_location()
time.sleep(5)

# Step 3: Wait for flight results to load
wait.until(EC.presence_of_all_elements_located((By.XPATH, "//li[@class='pIav2d']")))

# Step 4: Scrape flight data
flights = driver.find_elements(By.XPATH, "//li[@class='pIav2d']")
data = []

for flight in flights:
    try:
        airline = flight.find_element(By.XPATH, ".//div[@class='sSHqwe tPgKwe ogfYpf']/span").text
        time_range = flight.find_element(By.XPATH, ".//div[@class='gvkrdb AdWm1c tPgKwe ogfYpf']").text
        price = flight.find_element(By.XPATH, ".//div[@class='YMlIz FpEdX']").text
        data.append({
            "Airline": airline,
            "Time": time_range,
            "Price": price
        })
    except Exception as e:
        print(f"Skipped one flight block due to: {e}")

driver.quit()

# Step 5: Save to CSV or print
df = pd.DataFrame(data)
df.to_csv("flight.csv", index=False)
print(df)










