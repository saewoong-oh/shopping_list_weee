from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set up the Chrome driver
options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # Uncomment to hide the browser
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Open Google Maps
driver.get("https://www.google.com/maps")
time.sleep(3)

# Search input
search_term = input("🔍 Enter what you want to search for (e.g. 'grocery stores near me'): ")
search_box = driver.find_element(By.ID, "searchboxinput")
search_box.send_keys(search_term)
search_box.send_keys(Keys.RETURN)

# Wait for results to load
time.sleep(8)

# Wait for the scrollable results panel
try:
    scroll_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "m6QErb"))
    )

    # Scroll to load more results
    for _ in range(4):
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollTop + 1000;", scroll_box)
        time.sleep(2)

except Exception as e:
    print("❌ Could not find scrollable results panel:", e)

# Scrape results
store_cards = driver.find_elements(By.CLASS_NAME, "Nv2PK")
print(f"\n🛒 Nearby Stores:")
print(f"🔍 Found {len(store_cards)} result cards.\n")

output = ""
for card in store_cards:
    try:
        # Name is usually under this class
        name = card.find_element(By.CLASS_NAME, "qBF1Pd").text

        # This will grab all text (like address, category, hours, etc.)
        raw_info = card.text.replace(name, "").strip()

        output += f"🏬 {name}\n📄 {raw_info}\n\n"
    except Exception as e:
        print("⚠️ Skipped a card due to error:", e)
        continue

if output.strip() == "":
    print("⚠️ No readable store data found.")
else:
    print(output)

driver.quit()
