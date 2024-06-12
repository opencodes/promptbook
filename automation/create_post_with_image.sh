#!/bin/bash

# Set your WordPress site URL and authentication details
SITE_URL="https://promptbook.in"
USERNAME="promptbook.in"
PASSWORD="u7uR 0PaF gY0h cHQJ F4jV ek6l" # Use an application password for security
IMAGE_PATH="generated_image_20240610_102746.png"
POST_TITLE="My New Post"
POST_CONTENT="This is the content of the new post."

# Encode credentials
ENCODED_CREDS=$(echo -n "$USERNAME:$PASSWORD" | base64)


# Check if the user has the necessary permissions
USER_CAPABILITIES=$(echo $TEST_RESPONSE | jq .capabilities)

if [[ $USER_CAPABILITIES == *"upload_files"* && $USER_CAPABILITIES == *"publish_posts"* ]]; then
    echo "User has necessary permissions"
else
    echo "User does not have necessary permissions"
    exit 1
fi

# Upload the image
echo "Uploading image"
IMAGE_RESPONSE=$(curl -s -X POST "$SITE_URL/wp-json/wp/v2/media" \
    -H "Content-Disposition: attachment; filename=$(basename $IMAGE_PATH)" \
    -u "$USERNAME:$PASSWORD" \
    --data-binary @$IMAGE_PATH)

# Extract the image ID from the response
IMAGE_ID=$(echo $IMAGE_RESPONSE | jq .id)

# Check if image upload was successful
if [ -z "$IMAGE_ID" ] || [ "$IMAGE_ID" == "null" ]; then
    echo "Image upload failed. Response: $IMAGE_RESPONSE"
    exit 1
fi

# Create a new post and set the uploaded image as the featured image
echo "Creating post"
POST_RESPONSE=$(curl -s -X POST "$SITE_URL/wp-json/wp/v2/posts" \
    -H "Content-Type: application/json" \
    -u "$USERNAME:$PASSWORD" \
    -d '{
          "title": "'"$POST_TITLE"'",
          "content": "'"$POST_CONTENT"'",
          "status": "publish",
          "featured_media": '"$IMAGE_ID"'
        }')

# Output the response from creating the post
echo $POST_RESPONSE
