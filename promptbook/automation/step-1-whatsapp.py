import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

# Initialize the Chrome driver
options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(options=options)

# Open WhatsApp Web
driver.get("https://web.whatsapp.com")

# Wait for the user to scan the QR code
print("Please scan the QR code with your phone to log in.")
time.sleep(10)  # Adjust the sleep time as necessary for scanning QR code

# Select the chat you want to scrape (you can improve this part to select dynamically)
input("Press Enter after selecting the chat you want to scrape messages from...")

def scroll_to_top(driver):
    chat_box = driver.find_element(By.CSS_SELECTOR, 'div.copyable-area')
    actions = ActionChains(driver)
    actions.move_to_element(chat_box).click().perform()
    for _ in range(10):  # Adjust the range to scroll further if needed
        actions.send_keys(Keys.PAGE_UP).perform()
        time.sleep(1)

# Scroll to the top of the chat to load all messages
scroll_to_top(driver)

# Read messages from the chat
messages = driver.find_elements(By.CSS_SELECTOR, "span.selectable-text.copyable-text")

# Open a file to write the messages
with open("prompt.txt", "w", encoding="utf-8") as file:
    for message in messages:
        file.write(message.text + "\n\n")

# Close the browser
driver.quit()
