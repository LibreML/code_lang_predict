import requests
import glob
import json
import os
import shutil
import logging
import random
import zipfile
from hashlib import md5

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def download_and_extract_zip(repo_slug, dest):
    failed_attempts = 0
    for branch in ['main', 'master']:
        zip_url = f"https://github.com/{repo_slug}/archive/refs/heads/{branch}.zip"
        try:
            response = requests.get(zip_url, stream=True)
            if response.status_code == 200:
                zip_path = f"{dest}.zip"
                with open(zip_path, 'wb') as f:
                    f.write(response.content)
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(dest)
                os.remove(zip_path)  # Clean up ZIP file
                logging.info(f"Extracted {zip_url} successfully.")
                return True
        except Exception as e:
            logging.error(f"Error downloading ZIP from {zip_url}: {str(e)}")
            return False
        failed_attempts += 1

    if failed_attempts == len(['main', 'master']):
        logging.error(f"Failed to download and extract {repo_slug} for both 'main' and 'master' branches.")
    return False

def save_repo_data(repo_data, repo_slug, dest_folder):
    filename = f"{md5(repo_slug.encode('utf-8')).hexdigest()}.json"
    filepath = os.path.join(dest_folder, filename)
    with open(filepath, 'w') as file:
        json.dump(repo_data, file, indent=4)
    logging.info(f"Saved repository data to {filepath}")

def process_repository(repo_path, allowed_extensions, language_mapping):
    repo_data = {}
    for file_path in glob.glob(f'{repo_path}/**/*', recursive=True):
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

def main():
    allowed_extensions = load_json_file('data/datasets/allowed_extensions.json')
    language_mapping = {ext: lang for lang, exts in load_json_file('data/datasets/top_38_supported_languages.json').items() for ext in exts}
    git_clone_urls = load_json_file('data/datasets/git_clone_urls_by_language_100.json')

    output_folder_path = 'data/datasets/top_supported_languages'
    os.makedirs(output_folder_path, exist_ok=True)

    total_languages = len(git_clone_urls)
    languages_processed = 0
    for i, (language, repos) in enumerate(git_clone_urls.items(), start=1):
        language_folder = os.path.join(output_folder_path, language)
        os.makedirs(language_folder, exist_ok=True)

        total_repos = len(repos)
        repos_processed = 0
        for j, repo in enumerate(repos, start=1):
            repo_slug = '/'.join(repo.split('/')[-2:]).replace('.git', '')  # Ensure full repo slug is used
            unique_dir_name = md5(repo_slug.encode('utf-8')).hexdigest()
            temp_repo_path = os.path.join("/tmp", unique_dir_name)

            if download_and_extract_zip(repo_slug, temp_repo_path):
                repo_data = process_repository(temp_repo_path, allowed_extensions, language_mapping)
                save_repo_data(repo_data, repo_slug, language_folder)
                shutil.rmtree(temp_repo_path)
                repos_processed += 1
            # Progress log for each repo
            logging.info(f"Progress: [{repos_processed}/{total_repos} Repos] [{languages_processed + 1}/{total_languages} Languages]")
        languages_processed += 1

    logging.info("Repository processing completed.")

if __name__ == "__main__":
    main()
