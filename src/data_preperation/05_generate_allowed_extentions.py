# Importing necessary libraries
import json
import os

# Function to load JSON file
def load_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Function to save data to a JSON file
def save_json_file(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# File paths
current_directory = os.getcwd()
supported_languages_path = os.path.join(current_directory, 'data', 'datasets', 'top_38_supported_languages.json')

def generate_allowed_extensions(supported_languages):
    allowed_extensions_set = set()
    for extensions in supported_languages.values():
        allowed_extensions_set.update(extensions)
    return list(allowed_extensions_set)

# Load the supported languages data
supported_languages = load_json_file(supported_languages_path)

# Generate allowed extensions list
allowed_extensions_list = generate_allowed_extensions(supported_languages)

# Save the allowed extensions to a JSON file
output_path = os.path.join('data','datasets', 'allowed_extensions.json')
save_json_file(allowed_extensions_list, output_path)
