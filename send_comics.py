import requests
import os
from dotenv import load_dotenv
from utils import get_and_save_image_to_disk


def get_comics(comic_json_url, images_directory):
    filename_template = 'comic'
    response = requests.get(comic_json_url)
    comic_data = response.json()
    filepath_template = os.path.join(images_directory, filename_template)
    img_url = comic_data.get('img')
    comic_comment = comic_data.get('alt')
    print(comic_comment)
    # print(img_url)
    get_and_save_image_to_disk(img_url, filepath_template)

    


def main():
    load_dotenv()
    # comic_url = 'https://xkcd.com/614/info.0.json'
    
    comic_url = 'https://xkcd.com/353/info.0.json'
    images_directory = os.getenv('IMAGES_DIRECTORY', 'images/')
    get_comics(comic_url, images_directory)


if __name__ == '__main__':
    main()

