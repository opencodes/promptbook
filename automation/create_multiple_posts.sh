#!/bin/bash

# Set your WordPress site URL and authentication details
SITE_URL="https://promptbook.in"
USERNAME="promptbook.in"
PASSWORD="WnZ7 RLg2 D7sU 5CBT L5zd iiAR"

# Path to the posts JSON file
POSTS_FILE="posts.json"

# Function to upload an image and return its ID
upload_image() {
    local image_path=$1
    local image_response=$(curl -s -X POST "$SITE_URL/wp-json/wp/v2/media" \
        -H "Content-Disposition: attachment; filename=$(basename $image_path)" \
        -H "Authorization: Basic $(echo -n "$USERNAME:$PASSWORD" | base64)" \
        --data-binary @$image_path)
    echo $image_response | jq .id
}

# Read the JSON file and iterate over each post
jq -c '.[]' $POSTS_FILE | while read -r post; do
    # Extract post details
    title=$(echo $post | jq -r '.title')
    content=$(echo $post | jq -r '.content')
    image_path=$(echo $post | jq -r '.image_path')

    # Upload the image and get the image ID
    image_id=$(upload_image $image_path)

    # Create the post with the uploaded image as the featured image
    post_response=$(curl -s -X POST "$SITE_URL/wp-json/wp/v2/posts" \
        -H "Content-Type: application/json" \
        -H "Authorization: Basic $(echo -n "$USERNAME:$PASSWORD" | base64)" \
        -d '{
              "title": "'"$title"'",
              "content": "'"$content"'",
              "status": "publish",
              "featured_media": '"$image_id"'
            }')

    # Output the response from creating the post
    echo "Created post: $title"
    echo $post_response
done
