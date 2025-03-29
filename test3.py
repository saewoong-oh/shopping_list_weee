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
# options.add_argument("--headless")  # Uncomment to hide browser
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

# ✅ Auto-scroll until no new cards appear
try:
    scroll_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "m6QErb"))
    )

    previous_count = 0
    same_count_threshold = 3  # Stop after count doesn't increase for 3 scrolls
    same_count_times = 0

    print("\n🔄 Scrolling to load more results...\n")

    while same_count_times < same_count_threshold:
        driver.execute_script("arguments[0].scrollTop += 1500;", scroll_box)
        time.sleep(2)

        current_cards = driver.find_elements(By.CLASS_NAME, "Nv2PK")
        current_count = len(current_cards)

        print(f"📦 Cards loaded: {current_count}")

        if current_count == previous_count:
            same_count_times += 1
        else:
            same_count_times = 0

        previous_count = current_count

except Exception as e:
    print("❌ Could not find scrollable results panel:", e)

# Filter results based on keywords
store_cards = driver.find_elements(By.CLASS_NAME, "Nv2PK")
print(f"\n🛒 Filtered Results for '{search_term}' with stock info:")
print(f"🔍 Total cards loaded: {len(store_cards)}\n")

output = ""
keywords = [
    "in stock",
    "updated today",
    "seen by shoppers",
    "sold here:"
]

for card in store_cards:
    try:
        name = card.find_element(By.CLASS_NAME, "qBF1Pd").text
        raw_info = card.text.replace(name, "").strip()
        lines = card.text.split("\n")

        # Guess: address is usually line 2 or 3
        address = lines[1] if len(lines) > 1 else "No address found"

        # Keyword filtering
        if any(keyword in raw_info.lower() for keyword in keywords):
            output += f"✅ 🏬 {name}\n📍 {address}\n📄 {raw_info}\n\n"
        else:
            continue


    except Exception as e:
        print("⚠️ Skipped a card due to error:", e)
        continue

if output.strip() == "":
    print("⚠️ No listings matched stock-related keywords.")
else:
    print(output)

driver.quit()
