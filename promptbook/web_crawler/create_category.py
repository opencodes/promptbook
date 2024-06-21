import json
import requests
from requests.auth import HTTPBasicAuth

# Set your WordPress site URL and authentication details
SITE_URL = "https://promptbook.in"
USERNAME = "promptbook.in"
PASSWORD = "u7uR 0PaF gY0h cHQJ F4jV ek6l"

# Path to the categories JSON file
CATEGORIES_FILE = "categories.json"

def create_category(category, parent_id=None):
    url = f"{SITE_URL}/wp-json/wp/v2/categories"
    headers = {
        "Content-Type": "application/json"
    }
    auth = HTTPBasicAuth(USERNAME, PASSWORD)
    data = {
        "name": category["name"],
        "description": category.get("description", ""),
        "slug": category.get("slug", ""),
        "parent": parent_id
    }
    response = requests.post(url, headers=headers, auth=auth, data=json.dumps(data))
    return response

def main():
    # Read the JSON file
    with open(CATEGORIES_FILE, 'r') as file:
        categories = json.load(file)

    # Iterate over each category and create it
    for category in categories:
        # Create the parent category
        response = create_category(category)
        if response.status_code == 201:
            parent_category = response.json()
            print(f"Category created successfully: {parent_category['name']}")
            parent_id = parent_category['id']

            # Create subcategories
            for subcategory in category.get("subcategories", []):
                response = create_category(subcategory, parent_id)
                if response.status_code == 201:
                    print(f"Subcategory created successfully: {subcategory['name']}")
                else:
                    print(f"Failed to create subcategory: {subcategory['name']} - HTTP status code: {response.status_code}")
        else:
            print(f"Failed to create category: {category['name']} - HTTP status code: {response.status_code}")

if __name__ == "__main__":
    main()
