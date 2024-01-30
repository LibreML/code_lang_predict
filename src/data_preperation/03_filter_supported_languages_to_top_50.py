import json
import os

def load_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def save_json_file(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def find_language_in_supported(lang, supported_languages):
    lang_lower = lang.lower()
    for key in supported_languages.keys():
        if key.lower() == lang_lower:
            return key
    return None

# File paths
current_directory = os.getcwd()
supported_languages_path = os.path.join(current_directory,'data', 'datasets', 'supported_languages.json')
top_50_languages_path = os.path.join(current_directory,'data', 'datasets', 'top_50_languages.json')

# Load the datasets
supported_languages = load_json_file(supported_languages_path)
top_50_languages = load_json_file(top_50_languages_path)

# Match languages and handle missing ones
top_50_supported_languages = {}
missing_languages = []

for lang in top_50_languages:
    original_name = find_language_in_supported(lang, supported_languages)
    if original_name:
        top_50_supported_languages[original_name] = supported_languages[original_name]
    else:
        missing_languages.append(lang)

# Report missing languages
print("Missing languages (manual intervention needed):")
for lang in missing_languages:
    print(lang)

# Save the results
output_path = os.path.join(current_directory, 'datasets', 'top_50_supported_languages.json')
save_json_file(top_50_supported_languages, output_path)

print(f"Output saved to {output_path}")
