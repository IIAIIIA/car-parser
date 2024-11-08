import requests
from bs4 import BeautifulSoup

URL = 'https://auto.kufar.by/l/cars/volkswagen-touareg'

headers = {
    'Host': 'auto.kufar.by',
    'User-Agent': 'Google',  #
    'Accept': '*/*',  #
    'Accept-Encoding': 'gzip, deflate, br',  #
    'Connection': 'keep-alive'  #
}


def get_page(url):
    page = requests.get(url, headers=headers)
    return BeautifulSoup(page.text, 'html.parser')


def clean_text(string):
    return string.text.strip().replace('\xa0', ' ').replace('\u2009', ' ')


def get_cars(html_text, cars_list):
    car_carts = html_text.find_all('a', {'class': 'styles_wrapper__qHIxa'})
    for car_cart in car_carts:
        car_params = car_cart.find('div', {'class': 'styles_description__RTkd2'}).find_all('p')
        car = {
            'title': clean_text(car_cart.find('h3', {'class': 'styles_info__title__7LPbu'})),
            'price': clean_text(car_cart.find('div', {'class': 'styles_info__price___5fsJ'}).find('span')),
            'mileage': clean_text(car_params[2]),
            'year': clean_text(car_params[0]),
            'description': clean_text(car_params[1]),
            'place': clean_text(car_cart.find('div', {'class': 'styles_info__region__BGH1o'})),
            'link': car_cart['href']
        }
        cars_list.append(car)
    return cars_list


def extract_cars(link):
    cars_list = []
    while True:
        page_soup = get_page(link)
        current_page_number = page_soup.find('span', {'class': 'styles_active__GRR1D'}).text
        print(f"kufar.by - парсинг страницы {current_page_number}")
        cars_list = get_cars(page_soup, cars_list)
        next_page_link = page_soup.find('a',
                                             {'data-testid': f'auto-pagination-page-{int(current_page_number) + 1}'})
        if not next_page_link:
            break
        link = 'https://auto.kufar.by' + next_page_link['href']
    return cars_list



def extract_cars_list():
    return extract_cars(URL)