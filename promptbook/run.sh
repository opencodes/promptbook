#!/bin/bash

cd web_crawler

# Run the first Python script
# python3 create_post.py
python3 image_creator.py

# Check if the first script executed successfully
if [ $? -eq 0 ]; then
    # Run the second Python script
    echo "Succesfully Completed the first script. Running the second script..."
    python3 create_post.py
else
    echo "The first script failed. The second script will not run."
fi
