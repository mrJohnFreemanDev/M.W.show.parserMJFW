import requests
from bs4 import BeautifulSoup
import re

url = 'https://www.1tv.ru/sitemap-160.xml'

def get_title(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        title_tag = soup.find('title')
        if title_tag:
            title = title_tag.get_text().strip().replace('\xa0', ' ')
            return title
        else:
            return "Title not found"
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении заголовка для {url}: {e}")
        return None

def get_description(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        description_tag = soup.find('div', class_=['editor text-block', 'editor text-block active'])
        if description_tag:
            description = description_tag.get_text().strip().replace('\xa0', ' ')
            return description
        else:
            return "Description not found"
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении описания для {url}: {e}")
        return None

try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    print("XML загружен успешно.")

    soup = BeautifulSoup(response.content, 'xml')
    loc_tags = soup.find_all('loc')

    if loc_tags:
        valid_urls = [loc.get_text() for loc in loc_tags if not re.search(r'momenty', loc.get_text(), re.IGNORECASE) 
                      and not re.search(r'fragment-vypuska', loc.get_text(), re.IGNORECASE)
                      and not re.search(r'vse-video', loc.get_text(), re.IGNORECASE)
                      and not re.search(r'premera-na-pervom', loc.get_text(), re.IGNORECASE)
                      and not re.search(r'byvshaya-zhena-aleksandra-kerzhakova-ne-nado-igrat-na-chuvstvah-materi', loc.get_text(), re.IGNORECASE)
                      and not re.search(r'uchastvuyte-v-proekte', loc.get_text(), re.IGNORECASE)
                      and not re.search(r'search', loc.get_text(), re.IGNORECASE)
                      and not re.search(r'programmy-o-zvezdah', loc.get_text(), re.IGNORECASE)
                      and not re.search(r'top-5-video-nedeli', loc.get_text(), re.IGNORECASE)
                      and not re.search(r'o-proekte', loc.get_text(), re.IGNORECASE)]

        with open('man_woman_episodes.txt', 'w', encoding='utf-8') as file:
            for index, url in enumerate(valid_urls[2:], start=0):
                title = get_title(url)
                description = get_description(url)
                if title:
                    file.write(f"{index} '{title}' '{description}' '{url}'\n")
                    print(f"{index}. DONE!\n")
                else:
                    file.write(f"{index}. {url} - Заголовок или описание не получены\n")
                    print(f"Ошибка - {e}\n")
        print("Создан файл man_woman_episodes!")
    else:
        print("Теги <loc> не найдены.")
except requests.exceptions.RequestException as e:
    print(f"Ошибка при загрузке XML: {e}")
