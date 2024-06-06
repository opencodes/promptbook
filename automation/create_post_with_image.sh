#!/bin/bash

# Set your WordPress site URL and authentication details
SITE_URL="https://promptbook.in"
USERNAME="promptbook.in"
PASSWORD="WnZ7 RLg2 D7sU 5CBT L5zd iiAR"
IMAGE_PATH="/path/to/your/image.jpg"
POST_TITLE="My New Post"
POST_CONTENT="This is the content of the new post."

# Upload the image
IMAGE_RESPONSE=$(curl -s -X POST "$SITE_URL/wp-json/wp/v2/media" \
    -H "Content-Disposition: attachment; filename=$(basename $IMAGE_PATH)" \
    -H "Authorization: Basic $(echo -n "$USERNAME:$PASSWORD" | base64)" \
    --data-binary @$IMAGE_PATH)

# Extract the image ID from the response
IMAGE_ID=$(echo $IMAGE_RESPONSE | jq .id)

# Create a new post and set the uploaded image as the featured image
POST_RESPONSE=$(curl -s -X POST "$SITE_URL/wp-json/wp/v2/posts" \
    -H "Content-Type: application/json" \
    -H "Authorization: Basic $(echo -n "$USERNAME:$PASSWORD" | base64)" \
    -d '{
          "title": "'"$POST_TITLE"'",
          "content": "'"$POST_CONTENT"'",
          "status": "publish",
          "featured_media": '"$IMAGE_ID"'
        }')

# Output the response from creating the post
echo $POST_RESPONSE
