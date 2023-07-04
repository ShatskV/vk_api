# Публикация комиксов

Данный скрипт публикует рандомные комиксы с сайта [xkcd.com](https://xkcd.com) в ваше сообщество в VK

### Как установить

- Для запуска сайта вам понадобится Python третьей версии.

- Скачайте код с GitHub. Затем установите зависимости

    ```
    pip install -r requirements.txt
    ```

- Рекомендуется использовать [virtualenv/venv](https://docs.python.org/3/library/venv.html) для изоляции проекта.

## Как пользоваться

- Создайте приложение в разделе Мои приложения. [Страница для разработчиков](https://vk.com/dev) тип приложения укажите standalone. Получите **CLIENT_ID**

- Получите **access_token** [Процедура Implicit Flow](https://vk.com/dev/implicit_flow_user)
    ```
    https://oauth.vk.com/authorize?client_id={{ CLIENT_ID }}
    &display=page&redirect_uri=http://vk.com/callback&scope=photos,groups,wall&response_type=token&v=5.131&state=123456
    ```
- Создайте группу в ВК

- Создайте файл **.env** в корне проекта:
    ```
    USER_ID=ID_Пользователя
    GROUP_ID=ID_Группы
    VK_TOKEN=Полученный_access_token
    ```

- Запустите скрипт для загрузки рандомного комикса в группу:
    ```
    python3 send_comics.py
    ```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).