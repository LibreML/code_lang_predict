import json

def count_supported_languages(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return len(data)
    except FileNotFoundError:
        print(f"The file {file_path} was not found.")
    except json.JSONDecodeError:
        print(f"The file {file_path} does not contain valid JSON.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Replace 'datasets/supported_languages.json' with your actual file path
number_of_languages = count_supported_languages('data/datasets/supported_languages.json')
print(f"Number of supported programming languages: {number_of_languages}")
