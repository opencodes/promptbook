import os
import time
import base64
import json
import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

POSTS_FILE = "posts.json"
SITE_URL = "https://promptbook.in"
USERNAME = "promptbook.in"
PASSWORD = "jtlG puvW m2oL caMP 2WpN BUHg"

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

def write_unprocessed_post_to_json(unprocessed_posts, json_file_path):
    # Write the list to a JSON file
    with open(json_file_path, "w") as json_file:
        json.dump(unprocessed_posts, json_file, indent=4)
    
def setup_webdriver():
    # Connect to the existing Chrome session
    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(options=options)
    return driver

def open_webpage(driver, url):
    driver.get(url)
    time.sleep(5)  # Wait for the page to load completely

def find_element(driver, by, value, timeout=10):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))

def find_elements(driver, by, value, timeout=10):
    return WebDriverWait(driver, timeout).until(EC.presence_of_all_elements_located((by, value)))

def click_prompt_button(driver):
    try:
        print("- Clicking prompt button...")
        prompt_button = find_element(driver, By.CSS_SELECTOR, 'button[data-testid="input-option-button-prompt"]')
        prompt_button.send_keys(Keys.RETURN)
        time.sleep(2)
    except Exception as e:
        print(f"Failed to find or click prompt button: {e}")
        raise RuntimeError(f"Failed to find or click prompt button: {e}")

def enter_prompt_text(driver, prompt):
    try:
        print(f"- Entering prompt '{prompt}'...")
        textareas = find_elements(driver, By.CSS_SELECTOR, 'textarea[data-testid="test-text-area"]')
        print(f"Found {len(textareas)} textareas.")
        prompt_input = textareas[0]  # Select the second one
        prompt_input.send_keys('')  # Clear any existing text
        prompt_input.send_keys(prompt)
        prompt_input.click()  # Ensure the textarea has focus
        driver.execute_script("arguments[0].value = '';", prompt_input)
        time.sleep(5)
        prompt_input.send_keys(prompt)
        time.sleep(5)
    except Exception as e:
        print(f"- Failed to find or enter text in prompt input: {e}")
        raise RuntimeError(f"Failed to find or enter text in prompt input: {e}")

def click_generate_button(driver):
    try:
        print("- Generating image...")
        generate_button = find_element(driver, By.CSS_SELECTOR, 'button[data-testid="omni-prompt-generate-button"]')
        generate_button.send_keys(Keys.RETURN)
        time.sleep(30)  # Adjust the sleep time if necessary
    except Exception as e:
        print(f"- Failed to find or click generate button: {e}")
        raise RuntimeError(f"Failed to find or click generate button: {e}")

def download_image(driver, directory):
    try:
        print("- Downloading image...")
        image_element = find_element(driver, By.CSS_SELECTOR, 'button[data-testid^="media-asset-button-0"] img')
        image_data_base64 = image_element.get_attribute('src').split(',')[1]  # Extract base64 data from src attribute
        image_data = base64.b64decode(image_data_base64)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_path = os.path.join(directory, f'generated_image_{timestamp}.png')
        with open(image_path, 'wb') as file:
            file.write(image_data)
        return image_path
    except Exception as e:
        print(f"- Failed to download image: {e}")
        raise RuntimeError(f"Failed to locate, extract or save generated image: {e}")

def generate_image(driver, prompt, directory):
    try:
        print(f"----- Processing prompt '{prompt}' -----")
        click_prompt_button(driver)
        enter_prompt_text(driver, prompt)
        click_generate_button(driver)
        error_message = "Images couldn't be generated"
        if driver.page_source.find(error_message) != -1:
            print(f"- Failed to generate image for prompt '{prompt}'")
            return None
        image_path = download_image(driver, directory)
        print(f"Image for prompt downloaded successfully!")
        return image_path
    except Exception as e:
        print(f"Failed to process prompt '{prompt}': {e}")
        return None
def upload_image(file_path):
    api_url = SITE_URL + "/wp-json/wp/v2/media"

    # Open the file in binary mode and read its contents
    with open(file_path, "rb") as file:
        # Prepare the request headers with authentication
        headers = {
            "Authorization": "Basic " + base64.b64encode(f"{USERNAME}:{PASSWORD}".encode()).decode(),
            "Content-Disposition": f"attachment; filename={file_path}",
            "Content-Type": "image/png"  # Adjust content type according to your file type
        }

        # Send the POST request to upload the media
        response = requests.post(api_url, headers=headers, data=file)
        # Check the response
        if response.status_code == 201:
            print("Media uploaded successfully.")
            # If successful, you can get the media URL from the response
            media_url = response.json()["source_url"]
            media_id =  response.json()["id"]
            print("Media URL:", media_url)
            print("Media ID:", media_id)
            return media_id
        else:
            print("Failed to upload media. Status code:", response.status_code)
            print("Response:", response.text)
            return None


def create_post(title, content, image_id):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Basic " + base64.b64encode(f"{USERNAME}:{PASSWORD}".encode()).decode()
    }
    post_data = {
        "title": title,
        "content": content,
        "status": "publish",
        "featured_media": image_id
    }
    
    response = requests.post(f"{SITE_URL}/wp-json/wp/v2/posts", headers=headers, json=post_data)
    
    if response.status_code == 201:
        print("----- Post creation complete -----")
        return response.json()
    else:
        print(f"Failed to create post {title}: {response.content}")
        return None


def main():
    driver = setup_webdriver()
    try:
        print("----- Starting image generation -----")
        print("Opening webpage...")
        open_webpage(driver, "https://designer.microsoft.com/image-creator")
        print("Webpage opened successfully!")
        
        unprocessed_post = []
        error_messages = []
        directory = "generated_images"


        with open(POSTS_FILE, 'r') as file:
            posts = json.load(file)

        if not os.path.exists(directory):
            os.makedirs(directory)
        
        for post in posts:
            prompt = post.get('content')
            image_path = generate_image(driver, prompt, directory)

            if image_path:
                print("----- Image generation complete -----")
                create_post(post.get('title'), post.get('content'), upload_image(image_path))
                os.remove(image_path)
            else:
                unprocessed_post.append(post)
                print(f"- Failed to generate image for prompt '{prompt}'")
                error_messages.append(post.get('title'))
        
        write_unprocessed_post_to_json(unprocessed_post, "posts.json")
        print("JSON file generated and unprocessed prompts updated successfully!")
        
        if error_messages:
            print("\nErrors encountered during processing:")
            for error in error_messages:
                print(error)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
