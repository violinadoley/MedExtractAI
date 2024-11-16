import requests
from bs4 import BeautifulSoup

url = "https://www.newsweek.com/rankings/worlds-best-hospitals-2024/india"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
}

def hospital_list():
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table')
        hospital_links = []
        rows = table.find_all('tr')[1:]
        for row in rows:
            link = row.find('a')['href']
            hospital_links.append(link)
        hospital_links = hospital_links[:50] 
    else:
        print(f"Error {response.status_code} occurred.")
    return hospital_links