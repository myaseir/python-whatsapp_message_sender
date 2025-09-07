import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import urllib.parse
import random

# ----------------------
# Step 1: Read CSV
# ----------------------
df = pd.read_csv("contacts_updated.csv")

# ----------------------
# Step 2: Prepare phone numbers
# ----------------------
phone_numbers = []
skipped_numbers = []

for num in df["Phone"].dropna().astype(str):
    num = num.strip()
    if num.startswith("0"):
        num = num[1:]  # Remove leading 0

    # Only accept 10-digit numbers after removing leading 0
    if num.isdigit() and len(num) == 10:
        phone_numbers.append("+92" + num)
    else:
        print(f"⚠️ Skipping invalid number: {num}")
        skipped_numbers.append(num)

# Remove duplicates
phone_numbers = list(set(phone_numbers))

# ----------------------
# Step 3: Message template
# ----------------------
message = "Hello, this is a testing message"

# ----------------------
# Step 4: Launch WhatsApp Web
# ----------------------
chrome_options = Options()
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])  # suppress warnings

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://web.whatsapp.com")
print("Scan the QR code to log in to WhatsApp Web")

# Wait for login (pane-side shows when login is complete)
WebDriverWait(driver, 60).until(
    EC.presence_of_element_located((By.ID, "pane-side"))
)
print("✅ Login successful!")

# ----------------------
# Step 5: Send messages
# ----------------------
failed_numbers = []

for number in phone_numbers:
    try:
        # Open chat with the number
        url = f"https://web.whatsapp.com/send?phone={number}&text={urllib.parse.quote(message)}"
        driver.get(url)

        # Wait for the send button
        send_btn = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Send"]'))
        )

        # Click the send button
        send_btn.click()
        print(f"✅ Message sent to {number}")

        # Random short delay
        time.sleep(random.uniform(5, 10))

    except Exception as e:
        print(f"❌ Failed to send to {number}: {e}")
        failed_numbers.append(number)
        time.sleep(3)


print("🎉 All messages processed!")
driver.quit()

# ----------------------
# Step 6: Save skipped & failed numbers
# ----------------------
if skipped_numbers:
    pd.DataFrame({"Skipped": skipped_numbers}).to_csv("skipped_numbers.csv", index=False)
    print(f"⚠️ Skipped numbers saved to skipped_numbers.csv")

if failed_numbers:
    pd.DataFrame({"Failed": failed_numbers}).to_csv("failed_numbers.csv", index=False)
    print(f"❌ Failed numbers saved to failed_numbers.csv")
