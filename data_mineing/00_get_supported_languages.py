import requests
import yaml
import json
import os

def fetch_supported_languages():
    url = "https://raw.githubusercontent.com/github-linguist/linguist/master/lib/linguist/languages.yml"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to fetch languages data")

    languages_data = yaml.safe_load(response.text)
    programming_languages = {
        lang: details.get("extensions", [])
        for lang, details in languages_data.items()
        if details.get("type") == "programming" and "extensions" in details
    }

    return programming_languages


def save_to_json(data, filename):
    os.makedirs("datasets", exist_ok=True)
    with open(os.path.join("datasets", filename), "w") as file:
        json.dump(data, file, indent=4)

def main():
    languages = fetch_supported_languages()
    save_to_json(languages, "supported_languages.json")

if __name__ == "__main__":
    main()
