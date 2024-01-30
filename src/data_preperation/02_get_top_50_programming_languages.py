import requests
from bs4 import BeautifulSoup
import json

def scrape_tiobe_index():
    url = "https://www.tiobe.com/tiobe-index/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract languages from the "top20" table
    top_20_table = soup.find('table', {'id': 'top20'})
    top_20_rows = top_20_table.find_all('tr')[1:]  # Skip header row
    top_20_languages = [row.find_all('td')[4].text.strip() for row in top_20_rows]

    # Extract languages from the next table for positions 21-50
    next_30_table = soup.find('table', {'id': 'otherPL'})
    next_30_rows = next_30_table.find_all('tr')[1:]  # Skip header row
    next_30_languages = [row.find_all('td')[1].text.strip() for row in next_30_rows]

    # Combine both lists
    top_50_languages = top_20_languages + next_30_languages

    return top_50_languages[:50]  # Ensure only top 50 are included

top_50 = scrape_tiobe_index()
print(top_50)

# Optionally, save to a JSON file
with open('data/datasets/top_50_languages.json', 'w') as f:
    json.dump(top_50, f, indent=4)
