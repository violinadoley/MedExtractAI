import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
from topHospital import hospital_list
MAX_DEPTH = 0

def scrape_website(url, depth=0, visited_urls=None):
    if visited_urls is None:
        visited_urls = set()
    if depth > MAX_DEPTH or url in visited_urls:
        return {}
    visited_urls.add(url)

    try:
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            tags_to_scrape = ['p']
            scraped_data = {
                "url": url,
                "content": {}
            }
            for tag_name in tags_to_scrape:
                tag_elements = soup.find_all(tag_name)
                tag_texts = [element.get_text(strip=True)
                             for element in tag_elements]
                if tag_texts:
                    scraped_data["content"][tag_name] = tag_texts
            link_elements = soup.find_all('a', href=True)
            links_to_visit = [urljoin(url, element['href'])
                              for element in link_elements]

            for link in links_to_visit:
                link_data = scrape_website(link, depth + 1, visited_urls)
                if link_data:
                    for tag_name, tag_texts in link_data["content"].items():
                        scraped_data["content"].setdefault(
                            tag_name, []).extend(tag_texts)

            return scraped_data

        else:
            pass
    except requests.exceptions.InvalidSchema:
        pass


website_urls = hospital_list()
hospitalData = []

for i, website_url in enumerate(website_urls):
    try:
        # Scrape the website
        print(f'scraping {i}. {website_url}')
        data = scrape_website(website_url)
        hospitalData.append(data)
    except:
        print(f'Error occurred at {i} {website_url}')

# Save the formatted data to a JSON file
with open("scraped_data.json", "w") as file:
    json.dump(hospitalData, file, indent=4)
    print('Saved Json File!!!!!!')
