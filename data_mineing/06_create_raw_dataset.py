import git
import glob
import json
import os
import shutil
import logging
import random
from hashlib import md5

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Modify clone_repository to return a success status
def clone_repository(repo_url, dest):
    try:
        git.Repo.clone_from(repo_url, dest, depth=1)
        logging.info(f"Cloned {repo_url} successfully.")
        return True
    except Exception as e:
        logging.error(f"Error cloning {repo_url}: {str(e)}")
        return False

def process_repository(repo_path, allowed_extensions, language_mapping):
    repo_data = {}
    for file_path in glob.glob(f'{repo_path}/**', recursive=True):
        if os.path.isfile(file_path) and any(file_path.endswith(ext) for ext in allowed_extensions):
            ext = os.path.splitext(file_path)[1]
            language = language_mapping.get(ext)
            if language:
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        file_content = file.read()
                        repo_data.setdefault(language, []).append(file_content)
                except UnicodeDecodeError:
                    logging.warning(f"Skipped non UTF-8 file: {file_path}")
    return repo_data

def update_final_json(final_json_path, new_data):
    if os.path.exists(final_json_path):
        with open(final_json_path, 'r') as file:
            existing_data = json.load(file)
    else:
        existing_data = {}

    for lang, contents in new_data.items():
        existing_data.setdefault(lang, []).extend(contents)

    with open(final_json_path, 'w') as file:
        json.dump(existing_data, file, indent=4)

def randomize_json_data(json_path):
    with open(json_path, 'r') as file:
        data = json.load(file)

    for key in data:
        random.shuffle(data[key])

    with open(json_path, 'w') as file:
        json.dump(data, file, indent=4)

def main():
    allowed_extensions = load_json_file('data/datasets/allowed_extensions.json')
    language_mapping = {ext: lang for lang, exts in load_json_file('data/datasets/top_38_supported_languages.json').items() for ext in exts}
    git_clone_urls = load_json_file('data/datasets/git_clone_urls_by_language_100.json')

    final_json_path = 'data/datasets/github_t100_repos_for_t38_langs.json'

    for language, repos in git_clone_urls.items():
        for repo in repos:
            unique_dir_name = md5(repo.encode('utf-8')).hexdigest()
            temp_repo_path = os.path.join("/tmp", unique_dir_name)

            if not clone_repository(repo, temp_repo_path):
                continue  # Skip this repo if cloning failed

            repo_data = process_repository(temp_repo_path, allowed_extensions, language_mapping)
            update_final_json(final_json_path, repo_data)

            if os.path.exists(temp_repo_path):
                shutil.rmtree(temp_repo_path)
                logging.info(f"Removed repository directory {temp_repo_path}")

    randomize_json_data(final_json_path)
    logging.info("Repository processing completed.")

if __name__ == "__main__":
    main()
