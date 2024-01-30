from github import Github
import json
import os
import time

def load_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def save_json_file(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def fetch_repositories_for_language(github, language, max_repos=100):
    repos = []
    for repo in github.search_repositories(query=f'language:{language}', sort='stars'):
        repos.append(repo.clone_url)
        if len(repos) >= max_repos:
            break
        time.sleep(1)
    return repos

def main():
    current_directory = os.getcwd()
    supported_languages_path = os.path.join(current_directory, 'data', 'datasets', 'top_38_supported_languages.json')
    output_path = os.path.join(current_directory, 'data', 'datasets', 'git_clone_urls_by_language_100.json')
    supported_languages = load_json_file(supported_languages_path)

    # Fetch GitHub API token from environment variable
    github_token = os.environ.get('GITHUB_TOKEN')
    if not github_token:
        raise Exception("GitHub token not found in environment variables.")

    github = Github(github_token)

    git_clone_urls_by_language = {}
    for language in supported_languages.keys():
        print(f"Fetching repos for {language}")
        git_clone_urls_by_language[language] = fetch_repositories_for_language(github, language)

    save_json_file(git_clone_urls_by_language, output_path)
    print(f"Git clone URLs saved to {output_path}")

if __name__ == "__main__":
    main()
