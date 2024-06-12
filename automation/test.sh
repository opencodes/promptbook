# Set your WordPress site URL and authentication details
SITE_URL="https://promptbook.in"
USERNAME="promptbook.in"
ENCODED_CREDS="u7uR 0PaF gY0h cHQJ F4jV ek6l"  # Use the generated application password if possible

# Path to the posts JSON file
POSTS_FILE="posts.json"
# Print credentials and site URL for debugging
echo "Site URL: $SITE_URL"
echo "Encoded Credentials: $ENCODED_CREDS"

# Test API endpoint access
TEST_RESPONSE=$(curl -s -X GET "$SITE_URL/wp-json/wp/v2/posts" \
    -H "Authorization: Basic $ENCODED_CREDS")

echo "Test API Response: $TEST_RESPONSE"
