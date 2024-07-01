import os
import time
import base64
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def read_prompts_from_file(file_path):
    with open(file_path, 'r') as file:
        prompts = file.readlines()
    # Remove any leading or trailing whitespace and empty lines
    prompts = [prompt.strip() for prompt in prompts if prompt.strip()]
    return prompts

def truncate_title(prompt):
    max_length = 50
    if len(prompt) <= max_length:
        return prompt
    else:
        return prompt[:max_length] + "..."

def write_json_and_update_prompts(image_data_list, unprocessed_prompts, json_file_path, prompt_file_path):
    # Write the list to a JSON file
    with open(json_file_path, "w") as json_file:
        json.dump(image_data_list, json_file, indent=4)
    
    # Update the prompt file with unprocessed prompts
    with open(prompt_file_path, "w") as prompt_file:
        prompt_file.write("\n".join(unprocessed_prompts))

def main():
    # Connect to the existing Chrome session
    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

    driver = webdriver.Chrome(options=options)

    try:
        # Open the web page
        driver.get("https://designer.microsoft.com/image-creator")
        
        # Wait for the page to load completely
        time.sleep(5)
        
        # Read prompts from a text file
        prompt_file_path = "prompt.txt"
        prompts = read_prompts_from_file(prompt_file_path)
        
        image_data_list = []
        unprocessed_prompts = []
        
        # Create the directory for saving images if it does not exist
        directory = "generated_images"
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        for prompt in prompts:
            try:
                prompt_buttont = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="input-option-button-prompt"]')
                print("Found prompt button with test id :", prompt_buttont.get_attribute("data-testid"))
                prompt_buttont.send_keys(Keys.RETURN)
                time.sleep(2)
                # Find the prompt input box and enter a prompt
                # prompt_input = driver.find_element(By.CSS_SELECTOR, 'textarea[data-testid="test-text-area"]')
                # Wait for all textarea elements and select the first one
                textareas = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'textarea[data-testid="test-text-area"]'))
                )
                prompt_input = textareas[1]  # Select the first one
                prompt_input.send_keys('')  #
                prompt_input.send_keys(prompt)  #
                prompt_input.click()  # Ensure the textarea has focus
                driver.execute_script("arguments[0].value = '';", prompt_input)
                time.sleep(5)
                print("prompt :", prompt)
                prompt_input.send_keys(prompt)  #
                time.sleep(5)
                
                generate_buttont = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="omni-prompt-generate-button"]')
                print("Found generate button with test id :", generate_buttont.get_attribute("data-testid"))
                generate_buttont.send_keys(Keys.RETURN)
                
                # Wait for the images to be generated
                time.sleep(5)  # Adjust the sleep time if necessary
                
                # Locate the generated image
                image_element = driver.find_element(By.CSS_SELECTOR, 'button[data-testid^="media-asset-button-"]')
                
                # Download the image
                image_data_base64 = image_element.get_attribute('src').split(',')[1]  # Extract base64 data from src attribute
                image_data = base64.b64decode(image_data_base64)

                # Save the base64 decoded data to a file with timestamp appended
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                image_path = os.path.join(directory, f'generated_image_{timestamp}.png')
                with open(image_path, 'wb') as file:
                    file.write(image_data)

                print(f"Image for prompt '{prompt}' downloaded successfully!")
                
                # Add prompt, image path, and other required fields to the list
                image_data_list.append({
                    "title": truncate_title(prompt),
                    "content": prompt,  # You can add content if needed
                    "image_path": image_path,
                    "categories": [1]  # You can add categories if needed
                })
            except Exception as e:
                print(f"Failed to process prompt: {e}")
                # unprocessed_prompts.append(prompt)
        
        # Write JSON file and update prompt file with unprocessed prompts
        # write_json_and_update_prompts(image_data_list, unprocessed_prompts, "posts.json", prompt_file_path)
        print("JSON file generated and unprocessed prompts updated successfully!")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
