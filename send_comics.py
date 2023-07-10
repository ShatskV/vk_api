import os
import shutil
from random import randint

import requests
import requests.exceptions as req_exc
from dotenv import load_dotenv

from utils import get_and_save_image_to_disk

API_VERSION = 5.131
MAX_NUM_COMICS = 2796


def check_vk_response(answer):
    error = answer.get('error', {}).get('error_msg')
    if error:
        raise req_exc.HTTPError(error)


def download_comic(comic_json_url, images_directory):
    filename = 'comic'
    response = requests.get(comic_json_url)
    comic_data = response.json()
    filepath_template = os.path.join(images_directory, filename)
    img_url = comic_data.get('img')
    comic_comment = comic_data.get('alt')
    return get_and_save_image_to_disk(img_url, filepath_template), comic_comment


def get_upload_url(vk_token, group_id):
    params = {'group_id': group_id, 'access_token': vk_token, 'v': 5.131}
    response = requests.get('https://api.vk.com/method/photos.getWallUploadServer', params=params)
    answer = response.json()
    check_vk_response(answer)
    upload_url = answer.get('response', {}).get('upload_url')
    return upload_url


def upload_photo_to_server(imagepath, url):
    with open(imagepath, 'rb') as file:
        response = requests.post(url, files={'photo': file})
    response.raise_for_status()
    answer = response.json()
    check_vk_response(answer)
    return answer


def save_to_group(vk_token, user_id, group_id, server, photo, hash_, caption):
    params = {'photo': photo, 'server': server, 'hash': hash_, 'user_id': user_id, 'v': API_VERSION,
              'caption': caption, 'group_id': group_id, 'access_token': vk_token}
    response = requests.post('https://api.vk.com/method/photos.saveWallPhoto', params=params)
    response.raise_for_status()
    answer = response.json()
    check_vk_response(answer)
    answer = answer.get('response', [])[0]
    return answer


def post_photo_in_group(vk_token, group_id, attachments):
    owner_id = '-' + group_id
    params = {'attachments': attachments, 'owner_id': owner_id, 'v': API_VERSION,
              'access_token': vk_token}
    response = requests.post('https://api.vk.com/method/wall.post', params=params)
    response.raise_for_status()
    answer = response.json()
    check_vk_response(answer)
    return answer


def main():
    load_dotenv()
    vk_token = os.getenv('VK_TOKEN')
    group_id = os.getenv('GROUP_ID')
    user_id = os.getenv('USER_ID')

    num_comic = randint(1, MAX_NUM_COMICS)
    comic_url = f'https://xkcd.com/{num_comic}/info.0.json'
    
    images_directory = os.getenv('IMAGES_DIRECTORY', 'images/')

    try:
        imagepath, caption = download_comic(comic_url, images_directory)
    except req_exc.ConnectionError as e:
        print('Connection error при загрузке комикса c xkcd.com:', e)
        return
    except req_exc.Timeout as e:
        print('Timeout error при загрузке комикса с xkcd.com:', e)
        return
    except req_exc.HTTPError as e:
        print('Http error при загрузке комикса с xkcd.com:', e)
        return

    try:
        vk_upload_url = get_upload_url(vk_token, group_id)
    except req_exc.ConnectionError as e:
        print('Connection error при получении ссылки загрузки ВК:', e)
        return
    except req_exc.Timeout as e:
        print('Timeout error при получении ссылки загрузки ВК:', e)
        return
    except req_exc.HTTPError as e:
        print('Http error при получении ссылки загрузки ВК:', e)
        return

    try:
        answer = upload_photo_to_server(imagepath, vk_upload_url)
    except req_exc.ConnectionError as e:
        print('Connection error при загрузке комикса в ВК:', e)
        return
    except req_exc.Timeout as e:
        print('Timeout error при загрузке комикса в ВК:', e)
        return
    except req_exc.HTTPError as e:
        print('Http error при загрузке комикса в ВК:', e)
        return

    server = answer.get('server')
    photo = answer.get('photo')
    hash_ = answer.get('hash')
    if not photo:
        print('Комикс не был загружен в ВК! Ошибка загрузки!')
        return
    try:
        answer = save_to_group(vk_token, user_id, group_id, server, photo, hash_, caption)  
    except req_exc.ConnectionError as e:
        print('Connection error при сохранении комикса в группе ВК:', e)
        return
    except req_exc.Timeout as e:
        print('Timeout error при сохранении комикса в группе ВК:', e)
        return
    except req_exc.HTTPError as e:
        print('Http error при сохранении комикса в группе ВК:', e)
        return
    except IndexError:
        print('Не удалось сохранить комикс в группе ВК! Ошибка сохранения!')
        return
    
    photo_id = answer.get('id')
    owner_id = answer.get('owner_id')
    attachments = f'photo{owner_id}_{photo_id}'

    try:
        answer = post_photo_in_group(vk_token, group_id, attachments)
    except req_exc.ConnectionError as e:
        print('Connection error при публикации комикса в группе ВК:', e)
        return
    except req_exc.Timeout as e:
        print('Timeout error при публикации комикса в группе ВК:', e)
        return
    except req_exc.HTTPError as e:
        print('Http error при публикации комикса в группе ВК:', e)
        return
    shutil.rmtree(images_directory)
    print('Комикс был успешно загружен в группу ВК!')

if __name__ == '__main__':
    main()
