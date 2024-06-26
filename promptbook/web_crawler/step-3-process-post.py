import json
import base64
import requests
import os

POSTS_FILE = "posts.json"
# Set your WordPress site URL and authentication details
SITE_URL = "https://promptbook.in"
USERNAME = "promptbook.in"
PASSWORD = "jtlG puvW m2oL caMP 2WpN BUHg"

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

def main():
    with open(POSTS_FILE, 'r') as file:
        posts = json.load(file)
    
    for post in posts:
        title = post.get('title')
        content = post.get('content')
        image_path = post.get('image_path')
        
        image_id = upload_image(image_path)
        print(f"Uploaded post {post} to WordPress")
        
        if image_id:
            os.remove(image_path)
            create_post(title, content, image_id)

if __name__ == "__main__":
    main()