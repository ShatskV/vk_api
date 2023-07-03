import requests
from requests.exceptions import HTTPError
import os
from dotenv import load_dotenv
from utils import get_and_save_image_to_disk
from random import randint


API_VERSION = 5.131
MAX_NUM_COMICS = 2796


def check_response(answer):
    error = answer.get('error', {}).get('error_msg')
    if error:
        raise HTTPError(error)


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
    check_response(answer)
    return answer


def upload_photo_to_server(imagepath, url):
    with open(imagepath, 'rb') as file:
        response = requests.post(url, files={'photo': file})
    response.raise_for_status()
    answer = response.json()
    check_response(answer)
    return answer


def save_to_group(vk_token, user_id, group_id, server, photo, hash_, caption):
    vk_token = os.getenv('VK_TOKEN_2')

    params = {'photo': photo, 'server': server, 'hash': hash_, 'user_id': user_id, 'v': API_VERSION,
              'caption': caption, 'group_id': group_id, 'access_token': vk_token}
    response = requests.post('https://api.vk.com/method/photos.saveWallPhoto', params=params)
    response.raise_for_status()
    answer = response.json().get('response', [])[0]
    return answer


def post_photo_in_group(vk_token, group_id, attachments):

    params = {'attachments': attachments, 'owner_id': -group_id, 'v': API_VERSION,
              'access_token': vk_token}
    
    response = requests.post('https://api.vk.com/method/wall.post', params=params)
    response.raise_for_status()

    return response.json()


def main():
    load_dotenv()
    user_id = os.getenv('USER_ID')
    group_id = os.getenv('GROUP_ID')
    vk_token = os.getenv('VK_TOKEN')
    # comic_url = 'https://xkcd.com/614/info.0.json'
    num_comic = randint(1, MAX_NUM_COMICS)
    comic_url = f'https://xkcd.com/{num_comic}/info.0.json'
    data = get_upload_url()
    print(data)
    upload_url = data.get('response', {}).get('upload_url')
    images_directory = os.getenv('IMAGES_DIRECTORY', 'images/')
    imagepath, caption = download_comic(comic_url, images_directory)
    answer = upload_photo_to_server(imagepath, upload_url)
    server = answer.get('server')
    photo = answer.get('photo')
    hash_ = answer.get('hash')
    # print(photo, server, hash_)
    answer = save_to_group(server, photo, hash_, caption)
    photo_id = answer.get('id')
    owner_id = answer.get('owner_id')
    attachments = f'photo{owner_id}_{photo_id}'

    # print(attachments)
    answer = post_photo_in_group(attachments)
    os.remove(imagepath)


if __name__ == '__main__':
    main()
    # get_upload_url()

