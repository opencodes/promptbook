import facebook
import requests

# pip install facebook-sdk requests

# Facebook access token
access_token = 'YOUR_ACCESS_TOKEN'

# Facebook Group ID
group_id = 'YOUR_GROUP_ID'

# Image URL
image_url = 'URL_OF_YOUR_IMAGE'

# Initialize Facebook graph API object
graph = facebook.GraphAPI(access_token)

# Upload image to Facebook
image = requests.get(image_url)
data = {
    'source': image.content,
    'message': 'Check out this cool image!',
}

# Post image to group
graph.put_photo(image=open('temp_image.jpg', 'rb'), album_path=f'{group_id}/photos', message='Check out this cool image!')
