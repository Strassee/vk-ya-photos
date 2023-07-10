import requests
import datetime, time
from tqdm import tqdm
from pprint import pprint
import json

def get_vk_photos_profile(token_vk, owner_id, count = 5):
    URL = 'https://api.vk.com/method/photos.get'
    params = {
        'access_token': token_vk,
        'owner_id': owner_id,
        'album_id' : 'profile',
        'photo_sizes' : 1,
        'extended' : 1,
        'count' : count,
        'v':'5.131'
    }
    return(requests.get(URL, params=params))

def upload_photo(token_ya, res):
    file_info = []
    url_ya = "https://cloud-api.yandex.net/v1/disk/resources/"
    params = {
        "path": res['response']['items'][0]['owner_id']
    }
    headers = {
        "Authorization": token_ya
    }
    response = requests.get(url_ya, headers=headers, params=params)
    if response.status_code == 404:
        response = requests.put(url_ya, headers=headers, params=params)
    
    for photo in tqdm(res['response']['items'], colour="green", desc='Обработка фото'):
        time.sleep(0.5)
        photo_info = {}
        filename = str(photo['likes']['count']) + '.jpg'
        index_p = None
        height = 0
        width = 0
        for index, size in enumerate(photo['sizes']):
            if size['height'] >= height and size['width'] >= width:
                index_p = index
                height = size['height']
                width = size['width']

        params = {
            "path": f'{res["response"]["items"][0]["owner_id"]}/{filename}',
        }
        response = requests.get(url_ya, headers=headers, params=params)
        # tqdm.write(str(response.status_code))
        if response.status_code == 200:
            filename = str(photo['likes']['count']) + '_' + str(photo['date']) + '.jpg'
        
        url_upload = "https://cloud-api.yandex.net/v1/disk/resources/upload"

        params = {
            "path": f'{res["response"]["items"][0]["owner_id"]}/{filename}',
            "url" : photo['sizes'][index_p]['url'],
        }
        requests.post(url_upload, headers=headers, params=params)
        photo_info['file_name'] = filename
        photo_info['size'] = photo['sizes'][index_p]['type']
        file_info.append(photo_info)
    
    return file_info

token_vk = input('Введите токен Vk: ')
token_ya = input('Введите токен Ya.Диск: ')
vk_id = input('Введите ID Vk пользователя: ')
res = get_vk_photos_profile(token_vk, vk_id, 30).json()
if res['response']['count'] != 0:
    file_info = upload_photo(token_ya, res)
    with open(f'file_info_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.json', 'w') as f:
        json.dump(file_info, f)
else:
    print('Нет файлов для загрузки')