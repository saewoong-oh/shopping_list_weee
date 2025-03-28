from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set up Chrome driver
options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # Optional: hide browser
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Open Google Maps
driver.get("https://www.google.com/maps")
time.sleep(3)

# Ask user what to search for
search_term = input("🔍 Enter what you want to search for (e.g. 'potatoes near me'): ")
search_box = driver.find_element(By.ID, "searchboxinput")
search_box.send_keys(search_term)
search_box.send_keys(Keys.RETURN)

# Wait for results to load
time.sleep(8)

# Wait for scrollable results panel
try:
    scroll_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "m6QErb"))
    )

    # Scroll to load more cards
    for _ in range(4):
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollTop + 1000;", scroll_box)
        time.sleep(2)

except Exception as e:
    print("❌ Could not find scrollable results panel:", e)

# Get store cards
store_cards = driver.find_elements(By.CLASS_NAME, "Nv2PK")
print(f"\n🛒 Filtered Results for '{search_term}' with 'in stock' or 'updated today':")
print(f"🔍 Found {len(store_cards)} raw cards. Filtering...\n")

output = ""
for card in store_cards:
    try:
        name = card.find_element(By.CLASS_NAME, "qBF1Pd").text
        raw_info = card.text.replace(name, "").strip()

        # ✅ Filter to only include cards that mention stock status
        if "in stock" in raw_info.lower() or "updated today" in raw_info.lower():
            output += f"✅ 🏬 {name}\n📄 {raw_info}\n\n"
        else:
            continue  # Skip cards without keywords

    except Exception as e:
        print("⚠️ Skipped a card due to error:", e)
        continue

if output.strip() == "":
    print("⚠️ No 'in stock' listings found for your search.")
else:
    print(output)

driver.quit()
