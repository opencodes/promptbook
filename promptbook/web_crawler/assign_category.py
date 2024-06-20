import re

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

# Function to match prompt to categories
def assign_category(prompt):
    prompt = prompt.lower()
    matched_categories = {
        "Art Types": [],
        "Modifiers": [],
        "Composition": [],
        "Famous Artists": [],
        "Gender": [],
        "Object Types": []
    }

    for main_category, keywords in categories.items():
        for keyword in keywords:
            keyword_lower = keyword.lower()
            if re.search(r'\b' + re.escape(keyword_lower) + r'\b', prompt):
                matched_categories[main_category].append(keyword)
    
    return matched_categories

# Prompt
prompt = "Create a ultra realistic oil painting image showing Buddha in meditation posture focussing on his lotus like eyes, sharp nose, broad gentle smily lips with thick deep brush strokes. Use Vivid colours. Strictly no face smudging. Clear face."

# Get matched categories
matched_categories = assign_category(prompt)

# Output the result
import json
print(json.dumps(matched_categories, indent=4))
