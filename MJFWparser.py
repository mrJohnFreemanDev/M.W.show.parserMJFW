import requests  # Импорт библиотеки для выполнения HTTP-запросов.
from bs4 import BeautifulSoup  # Импорт модуля для парсинга HTML и XML.
import re  # Импорт модуля для работы с регулярными выражениями.

url = 'https://www.1tv.ru/sitemap-160.xml'  # URL карты сайта для обработки.

# Функция для получения заголовка страницы.
def get_title(url):
    try:
        response = requests.get(url, timeout=10)  # Отправляем GET-запрос к указанному URL с таймаутом 10 секунд.
        response.raise_for_status()  # Проверяем успешность запроса.
        soup = BeautifulSoup(response.content, 'html.parser')  # Парсим содержимое ответа как HTML.

        title_tag = soup.find('title')  # Ищем тег <title> на странице.

        if title_tag:  # Если тег найден,
            title = title_tag.get_text().strip().replace('\xa0', ' ')  # Получаем текст, убираем пробелы и заменяем символы.
            return title  # Возвращаем заголовок.
        else:
            return "Title not found"  # Если тег <title> не найден, возвращаем сообщение.
    except requests.exceptions.RequestException as e:  # Обрабатываем ошибки запросов.
        print(f"Ошибка при получении заголовка для {url}: {e}")  # Выводим сообщение об ошибке.
        return None  # Возвращаем None, если произошла ошибка.

# Функция для получения описания страницы.
def get_description(url):
    try:
        response = requests.get(url, timeout=10)  # Отправляем GET-запрос к указанному URL с таймаутом 10 секунд.
        response.raise_for_status()  # Проверяем успешность запроса.
        soup = BeautifulSoup(response.content, 'html.parser')  # Парсим содержимое ответа как HTML.

        # Ищем элемент <div> с определёнными классами.
        description_tag = soup.find('div', class_=['editor text-block', 'editor text-block active'])

        if description_tag:  # Если элемент найден,
            description = description_tag.get_text().strip().replace('\xa0', ' ')  # Получаем текст, убираем пробелы и заменяем символы.
            return description  # Возвращаем описание.
        else:
            return "Description not found"  # Если элемент <div> не найден, возвращаем сообщение.
    except requests.exceptions.RequestException as e:  # Обрабатываем ошибки запросов.
        print(f"Ошибка при получении описания для {url}: {e}")  # Выводим сообщение об ошибке.
        return None  # Возвращаем None, если произошла ошибка.

try:
    response = requests.get(url, timeout=10)  # Отправляем GET-запрос для загрузки XML карты сайта.
    response.raise_for_status()  # Проверяем успешность запроса.
    print("XML загружен успешно.")  # Сообщаем об успешной загрузке.

    soup = BeautifulSoup(response.content, 'xml')  # Парсим содержимое ответа как XML.

    loc_tags = soup.find_all('loc')  # Ищем все элементы <loc> в XML.

    if loc_tags:  # Если элементы <loc> найдены,
        # Фильтруем ссылки, исключая те, что соответствуют определённым условиям.
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

        with open('man_woman_episodes.txt', 'w', encoding='utf-8') as file:  # Открываем файл для записи в режиме 'w'.
            for index, url in enumerate(valid_urls[2:], start=0):  # Перебираем ссылки, начиная с третьей.
                title = get_title(url)  # Получаем заголовок страницы.
                description = get_description(url)  # Получаем описание страницы.
                if title:  # Если заголовок получен,
                    # Записываем индекс, заголовок, описание и URL в файл.
                    file.write(f"{index} '{title}' '{description}' '{url}'\n")
                    print(f"{index}. DONE!\n")  # Сообщаем об успешной обработке.
                else:  # Если заголовок не получен,
                    file.write(f"{index}. {url} - Заголовок или описание не получены\n")  # Записываем сообщение об ошибке.
                    print(f"Ошибка - {e}\n")  # Выводим сообщение об ошибке.
        print("Создан файл man_woman_episodes!")  # Сообщаем об успешном создании файла.
    else:
        print("Теги <loc> не найдены.")  # Если теги <loc> не найдены, сообщаем об этом.
except requests.exceptions.RequestException as e:  # Обрабатываем ошибки при загрузке XML.
    print(f"Ошибка при загрузке XML: {e}")  # Выводим сообщение об ошибке.
