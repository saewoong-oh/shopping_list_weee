from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
import time

driver.get("https://www.google.com")

try:
    consent_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Accept all')]")
    consent_button.click()
except:
    pass

search_box = driver.find_element(By.NAME, "q")
query = input("🔍 Enter your search: ")
search_box.send_keys(query)
search_box.send_keys(Keys.RETURN)
time.sleep(5)

results = driver.find_elements(By.CSS_SELECTOR, 'div.tF2Cxc')  

print("\n🔎 Search Results:\n")

for result in results:
    try:
        title = result.find_element(By.TAG_NAME, "h3").text
        link = result.find_element(By.TAG_NAME, "a").get_attribute("href")
        print(f"🟢 {title}\n🔗 {link}\n")
    except:
        continue

driver.quit()
