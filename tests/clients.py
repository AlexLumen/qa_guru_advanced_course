import requests

def status(app_url):
    """
    Запрос статуса сервера
    """
    response = requests.get(f"{app_url}/status")
    return response




def create_user(app_url, data):
    """
    Запрос создания пользователя
    """
    response = requests.post(f"{app_url}/api/users/", json=data)
    return response



def update_user(app_url, user_id, data):
    """
     Запрос обновления пользователя
    """
    response = requests.patch(f"{app_url}/api/users/{user_id}", json=data)
    return response


def delete_user(app_url, user_id):
    """
     Запрос удаления пользователя
    """
    response = requests.delete(f"{app_url}/api/users/{user_id}/")
    return response


def get_users(app_url, params=None):
    """
    Запрос на получение пользователей
    """
    response = requests.get(f"{app_url}/api/users/", params=params)
    return response


def get_user(app_url, user_id):
    """
    Запрос на получение пользователя
    :param app_url:
    :return:
    """
    response = requests.get(f"{app_url}/api/users/{user_id}/")
    return response
