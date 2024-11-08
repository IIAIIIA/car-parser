import math
import requests
from bs4 import BeautifulSoup
import re

# test links
# https://cars.av.by/filter?brands[0][brand]=6&brands[0][model]=2093
# https://cars.av.by/filter?brands[0][brand]=1216&brands[0][model]=1229
URL = f'https://cars.av.by/filter?brands[0][brand]=1216&brands[0][model]=1235'

headers = {
    'Host': 'cars.av.by',
    'User-Agent': 'Google',  #
    'Accept': '*/*',  #
    'Accept-Encoding': 'gzip, deflate, br',  #
    'Connection': 'keep-alive'  #
}


def extract_max_pages(url=URL):
    av_request = requests.get(url, headers=headers)
    av_soup = BeautifulSoup(av_request.text, 'html.parser')
    paginator = av_soup.find('div', {'class': 'paging__text'}).string.split()[-1]
    return math.ceil(int(paginator) / 25)


def clean_text(string):
    return string.text.strip().replace('\xa0', ' ').replace('\u2009', ' ')


def to_int(text):
    """
    if you need to change the string output in the car object
    to a numeric output with replacement of all unnecessary characters
    """
    return int(re.sub(r'\D', '', text))


def extract_cars(last_page, url=URL):
    cars = []
    for page in range(last_page):
        print(f'av.by - парсинг страницы {page + 1}')
        car_page = requests.get(f'{url}&page={page + 1}', headers=headers)
        car_page_html = BeautifulSoup(car_page.text, 'html.parser')
        # car_list = soup.find_all('div', {'class': 'listing-top'}) + soup.find_all('div', {'class': 'listing-item'})
        car_container_list = car_page_html.find_all('div', {'class': 'listing-item'})
        for car_container in car_container_list:
            car_params = car_container.find('div', {'class': 'listing-item__params'}).find_all('div')
            car = {
                'title': clean_text(car_container.find('span', {'class': 'link-text'})),
                'price': clean_text(car_container.find('div', {'class': 'listing-item__price'})),
                'mileage': clean_text(car_params[2]),
                'year': clean_text(car_params[0]),
                'description': clean_text(car_params[1]),
                'place': clean_text(car_container.find('div', {'class': 'listing-item__location'})),
                'link': 'https://cars.av.by' + car_container.find('a', {'class': 'listing-item__link'})['href']
            }
            cars.append(car)
    return cars


def extract_cars_list():
    av_by_max_page = extract_max_pages()
    return extract_cars(av_by_max_page)
