import re
import requests

# Output the result
import json

# Configuration - Replace with your WordPress site details
WORDPRESS_URL = "https://promptbook.in/wp-json/wp/v2/"
USERNAME = "promptbook.in"
PASSWORD = "u7uR 0PaF gY0h cHQJ F4jV ek6l"

# JSON structure with categories
categories = {
    "Art Types": [
        "Realism", "Surrealism", "Modernism", "Impressionism", "Romanticism", 
        "Expressionism", "Psychedelic Art", "Postmodernism", "Hyperrealism", 
        "Fantasy", "Cyberpunk", "Minimalism", "Pop Art", "Folk Art", "Retro", 
        "Abstract", "Fauvism", "Art Nouveau", "Arabesque", "Vintage boho", 
        "Anime", "Cartography", "Vector Art", "Tile art", "Floral", "Prehistoric", 
        "Wonderland", "Creepy", "Mosaic"
    ],
    "Modifiers": [
        "Pixel Art", "Sticker", "App icon", "Geometric", "Manga", "Ukiyo-e", 
        "Paper Collage", "Pastel Drawing", "Pan-African", "Graffiti Art", "Art Deco", 
        "Cubism", "Purism", "Pointilism", "Conceptual Art", "Photography", 
        "Miniature diorama", "Pencil Sketch", "Watercolor", "Oil Painting", 
        "3D Animation", "Anthropomorphic", "Comic", "Cartoon", "Child Art", 
        "Coloring Book", "Mythical", "Neon", "Avatar", "Blog illustration", 
        "Flat design", "Vector vignette", "Line sticker", "Papercraft", "Futuristic", 
        "8K", "2D", "3D", "8-bit", "Splatter paint", "Cybernetic", "Glow in the dark", 
        "Studio lightning", "Sharp focus", "Macabre", "Ultra-sharp", "Film noir", 
        "Disney", "Chibi", "Portrait", "Soft illumination", "Monochrome", "Emoji", 
        "Stained glass", "Fluffy", "Logo", "Isometric", "Metallic", "Landscape", 
        "Illustration", "Poster"
    ],
    "Composition": [
        "Close up", "Fish-eye view", "Long angle", "Minimal line art", "Vintage postcard", 
        "Studio shot", "Framed", "Canvas", "Sculpture", "Cave painting", "Drone shot", 
        "Map", "Vector line art", "Single line drawing"
    ],
    "Famous Artists": [
        "Van Gogh", "Salvador Dali", "Claude Monet", "Max Ernst", "Picasso", 
        "Frida Kahlo", "Rene Magritte", "Leibovitz", "Roy Liechtenstein", 
        "Yoshitaka Amano", "Leonardo da Vinci", "Andy Warhol"
    ],
    "Gender": [
        "Male", "Female", "Gender-neutral"
    ],
    "Object Types": [
        "Human", "Animal", "Non-living", "Nature"
    ]
}
json_file_path = 'category.json'



def extract_term_ids(input_dict):
    term_ids = [1]
    for values in input_dict.values():
        term_ids.extend(values)
    return term_ids
def read_terms_from_json(file_path):
    with open(file_path, 'r') as file:
        terms = json.load(file)
    return terms
# Function to match prompt to categories
def assign_category(prompt):
    prompt = prompt.lower()
    matched_categories = {
        "Art Types": [],
        "Modifiers": [],
        "Composition": [],
        "Famous Artists": [],
        "Gender": [],
        "Object Types": [],
    }

    for main_category, keywords in categories.items():
        for keyword in keywords:
            keyword_lower = keyword.lower()
            if re.search(r'\b' + re.escape(keyword_lower) + r'\b', prompt):
                matched_categories[main_category].append(keyword)
    result = replace_values_by_term_id(matched_categories, terms)
    return extract_term_ids(result)

def replace_values_by_term_id(input_dict, terms):
    # Create a mapping from name to term_id
    term_mapping = {term['name']: term['term_id'] for term in terms}

    # Function to replace the values in the input_dict
    def replace_in_dict(d):
        for key, values in d.items():
            # Replace each value with its corresponding term_id if it exists in the term_mapping
            d[key] = [term_mapping[value] for value in values if value in term_mapping]

    replace_in_dict(input_dict)

    return input_dict
# Function to retrieve categories associated with a post
def get_post_categories(post_id):
    url = f"{WORDPRESS_URL}posts/{post_id}"
    response = requests.get(url)
    if response.status_code == 200:
        post_data = response.json()
        categories = post_data['categories']
        return categories
    else:
        print(f"Failed to retrieve categories for post {post_id}")
        return None

# Function to update categories associated with a post
def update_post_categories(post_id, new_category_ids):
    url = f"{WORDPRESS_URL}posts/{post_id}"
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        'categories': new_category_ids
    }
    response = requests.post(url, headers=headers, json=data, auth=(USERNAME, PASSWORD))
    if response.status_code == 200:
        print(f"Successfully updated categories for post {post_id}")
    else:
        print(f"Failed to update categories for post {post_id}")


# Prompt
prompt = "Create a ultra realistic oil painting image showing Buddha in meditation posture focussing on his lotus like eyes, sharp nose, broad gentle smily lips with thick deep brush strokes. Use Vivid colours. Strictly no face smudging. Clear face."

# Function to retrieve posts with pagination
def get_posts(page=1, per_page=10):
    url = f"{WORDPRESS_URL}posts"
    params = {
        'page': page,
        'per_page': per_page
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        posts = response.json()
        return posts
    else:
        print(f"Failed to fetch posts (page {page})")
        return None

# Function to update categories associated with a post
def update_post_categories(post_id, new_category_ids):
    url = f"{WORDPRESS_URL}posts/{post_id}"
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        'categories': new_category_ids
    }
    response = requests.post(url, headers=headers, json=data, auth=(USERNAME, PASSWORD))
    print(data)
    if response.status_code == 200:
        print(f"Successfully updated categories for post {post_id}")
    else:
        print(f"Failed to update categories for post {post_id}")
terms = read_terms_from_json(json_file_path)
# Main execution
def main():
    # Fetch and update posts in batches
    total_posts_to_update = 135
    posts_per_batch = 10

    for page in range(1, (total_posts_to_update // posts_per_batch) + 2):
        posts = get_posts(page=page, per_page=posts_per_batch)
        if posts is None:
            break

        for post in posts:
            post_id = post['id']
            new_category_ids = assign_category(post['content']['rendered'])
            update_post_categories(post_id, new_category_ids)

            # Check if we've updated enough posts
            total_posts_to_update -= 1
            if total_posts_to_update <= 0:
                break

        if total_posts_to_update <= 0:
            break

if __name__ == '__main__':
    main()

