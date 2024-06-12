#!/bin/bash

# Set your WordPress site URL and authentication details
SITE_URL="https://promptbook.in"
USERNAME="promptbook.in"
PASSWORD="u7uR 0PaF gY0h cHQJ F4jV ek6l"

# Path to the categories JSON file
CATEGORIES_FILE="categories.json"

# Read the JSON file and iterate over each category
jq -c '.[]' $CATEGORIES_FILE | while read -r category; do
    # Send a POST request to create the category
    response=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$SITE_URL/wp-json/wp/v2/categories" \
        -H "Content-Type: application/json" \
        -u "$USERNAME:$PASSWORD" \
        -d "$category")
    
    # Check the response status code
    if [ "$response" -eq 201 ]; then
        echo "Category created successfully: $(echo $category | jq -r '.name')"
    else
        echo "Failed to create category: $(echo $category | jq -r '.name') - HTTP status code: $response"
    fi
done
