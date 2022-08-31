import requests
import json

user = 'zmb3'

def user_exist(user):  # Проверяет существование пользователя с именем user в БД github.com
    url=f"https://api.github.com/users/{user}"

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'User-agent': '	Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:104.0) Gecko/20100101 Firefox/104.0',

    }
    try:
        response = requests.get(url, headers)
    except requests.ConnectionError:
        print('Ошибка подключения.')
        exit()
    if response.status_code == 200:
        return True
    else:
        return False

def get_user_repositories(user): # Запрашивает информацию о пользователе у github.com
    url = f'https://api.github.com/users/{user}/repos'

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'User-agent': '	Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:104.0) Gecko/20100101 Firefox/104.0',

    }
    try:
        response = requests.get(url, headers)
    except requests.ConnectionError:
        print('Ошибка подключения.')
        exit()
    return response


def write_user_json(user, response): #Записывает json-файл
    f_path = f'./log/{user}_repositories.json'
    try:
        with open(f_path, "w") as write_f:
            json.dump(response.json(), write_f)
            return f_path
    except IOError:
        print(f"Произошла ошибка записи файла {f_path}")
        exit()


def print_short_info(repositories): #Выводит на экран краткую информацию по всем репозиториям пользователя
    i = 1
    print(f' \n Количество публичных репозиториев пользователя {user}: {len(repositories.json())} \n')
    for rep in repositories.json():
        print(f" Репозиторий: {rep['name']} ({i})")
        print(f" URL:         {rep['url']}")
        print(f" Дата последнего обновления:         {rep['updated_at']} \n")
        i += 1

if user_exist(user):
    repositories = get_user_repositories(user)
    if repositories.status_code == 200:
        print_short_info(repositories)
        print(f'Данные о репозиториях пользователя {user} записаны в файл {write_user_json(user, repositories)}')
    else:
        print(f'Ошибка запроса к серверу {repositories.url}')
else:
    print(f'Пользователя с именем {user} не существует')