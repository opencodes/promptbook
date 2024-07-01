import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def read_prompts_from_file(file_path):
    """
    Reads prompts from a specified file and returns a list of non-empty, trimmed prompts.
    """
    try:
        with open(file_path, 'r') as file:
            prompts = file.readlines()
        prompts = [prompt.strip() for prompt in prompts if prompt.strip()]
        logging.info(f"Successfully read {len(prompts)} prompts from {file_path}")
        return prompts
    except FileNotFoundError:
        logging.error(f"The file '{file_path}' was not found.")
        return []
    except Exception as e:
        logging.error(f"An error occurred while reading the file '{file_path}': {e}")
        return []

def truncate_title(prompt, max_length=50):
    """
    Truncates the prompt to a specified maximum length, appending '...' if truncated.
    """
    return prompt if len(prompt) <= max_length else prompt[:max_length] + "..."

def write_json_to_file(file_path, data):
    """
    Writes the provided data to a JSON file with the specified file path.
    """
    try:
        with open(file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)
        logging.info(f"Successfully wrote JSON data to {file_path}")
    except IOError as e:
        logging.error(f"Error writing to file '{file_path}': {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred while writing to file '{file_path}': {e}")

def process_prompt(prompt):
    """
    Processes a single prompt into a structured dictionary.
    """
    try:
        return {
            "title": truncate_title(prompt),
            "content": prompt,
            "image_path": "",
            "categories": [1]
        }
    except Exception as e:
        logging.error(f"Failed to process prompt '{prompt}': {e}")
        return None

def main():
    input_file_path = "prompt.txt"
    output_file_path = "posts.json"

    try:
        prompts = read_prompts_from_file(input_file_path)
        if not prompts:
            logging.warning("No prompts to process.")
            return

        prompt_json_arr = [process_prompt(prompt) for prompt in prompts if prompt]

        # Filter out any None values that may have resulted from processing errors
        prompt_json_arr = [prompt for prompt in prompt_json_arr if prompt]

        write_json_to_file(output_file_path, prompt_json_arr)
    except Exception as e:
        logging.error(f"An error occurred in the main function: {e}")

if __name__ == "__main__":
    main()
