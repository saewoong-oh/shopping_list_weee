from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def single_results(input_string):
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import time

    # Set up Chrome driver
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Uncomment to run headless
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Open Google Maps
    driver.get("https://www.google.com/maps")
    time.sleep(3)

    # Search for the term
    search_term = input_string + " near me"
    search_box = driver.find_element(By.ID, "searchboxinput")
    search_box.send_keys(search_term)
    search_box.send_keys(Keys.RETURN)

    # Wait for results to load
    time.sleep(8)

    # Auto-scroll
    try:
        scroll_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "m6QErb"))
        )

        previous_count = 0
        same_count_times = 0
        same_count_threshold = 3

        while same_count_times < same_count_threshold:
            driver.execute_script("arguments[0].scrollTop += 1500;", scroll_box)
            time.sleep(2)
            current_cards = driver.find_elements(By.CLASS_NAME, "Nv2PK")
            current_count = len(current_cards)

            if current_count == previous_count:
                same_count_times += 1
            else:
                same_count_times = 0

            previous_count = current_count

    except Exception as e:
        print("❌ Could not find scrollable results panel:", e)

    # Filter results
    out_list = []
    keywords = ["in stock", "updated today", "seen by shoppers", "sold here:"]
    store_cards = driver.find_elements(By.CLASS_NAME, "Nv2PK")

    for card in store_cards:
        try:
            name = card.find_element(By.CLASS_NAME, "qBF1Pd").text
            raw_info = card.text.replace(name, "").strip()
            lines = card.text.split("\n")

            # Keyword filtering
            if any(keyword in raw_info.lower() for keyword in keywords):
                append_this = []
                output = f"{name}\n {raw_info}\n\n"

                out_lines = output.split("\n")
                # print(out_lines)

                if len(out_lines) >= 3 and "·" in out_lines[2]:
                    address_parts = out_lines[2].split("·")
                    address_to_add = address_parts[-1].strip()
                else:
                    address_to_add = "No address found"

                closing_time = "Unknown"
                if len(lines) >= 5:
                    line4 = lines[4]
                    if "Closes" in line4:
                        try:
                            closing_time = line4.split("Closes")[1].split("·")[0].strip().replace(" ", "")
                        except:
                            pass
                    elif "Open 24 hours" in line4:
                        closing_time = "24 hours"
                
                append_this.append(name)
                append_this.append(address_to_add)
                append_this.append(closing_time)
                out_list.append(append_this)
                # print(output)
                
            else:
                continue


        except Exception as e:
            print("⚠️ Skipped a card due to error:", e)
            continue

    driver.quit()
    return out_list


print(single_results("soy sauce"))