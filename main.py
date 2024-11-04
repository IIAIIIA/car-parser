import requests

headers = {
    'Host': 'cars.av.by',
    'User-Agent': 'Google', #
    'Accept': '*/*', #
    'Accept-Encoding': 'gzip, deflate, br', #
    'Connection': 'keep-alive' #
}

av_request = requests.get('https://cars.av.by/volkswagen/polo', headers=headers)
print(av_request.text)

