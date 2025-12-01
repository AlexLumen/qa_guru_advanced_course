import json
import os
from http import HTTPStatus

import dotenv
import pytest
import requests
from mimesis import Person, Internet

from tests.clients import create_user, delete_user, get_users


@pytest.fixture(autouse=True)
def envs():
    dotenv.load_dotenv()


@pytest.fixture
def app_url():
    return os.getenv("APP_URL")


@pytest.fixture(scope="module")
def fill_test_data(app_url):
    with open("users.json") as f:
        test_data_users = json.load(f)
    api_users = []
    for user in test_data_users:
        response = requests.post(f"{app_url}/api/users", json=user)
        api_users.append(response.json())
    user_ids = [user["id"] for user in api_users]

    yield user_ids

    for user_id in user_ids:
        requests.delete(f"{app_url}/api/users/{user_id}")

@pytest.fixture()
def person_generator():
    """
    Генератор человека
    """
    return Person('ru')


@pytest.fixture()
def internet_data_generator():
    """
    Генератор человека
    """
    return Internet()

@pytest.fixture()
def user_data(person_generator, internet_data_generator):
    """
    :return: возвращает тестовые данные для создания пользователя
    """
    data = {
        "email": person_generator.email(domains=['test.ru'],
                                      unique=True),
        "first_name": person_generator.first_name(),
        "last_name": person_generator.last_name(),
        "avatar": internet_data_generator.stock_image_url()
        }
    return data

@pytest.fixture()
def user_data_for_edit(person_generator, internet_data_generator):
    """
    :return: возвращает тестовые данные для создания пользователя
    """
    data = {
        "email": person_generator.email(domains=['test.ru'],
                                      unique=True),
        "first_name": person_generator.first_name(),
        "last_name": person_generator.last_name(),
        "avatar": internet_data_generator.stock_image_url(width=1840, height=980)
        }
    return data

@pytest.fixture()
def create_new_user(app_url,user_data, request):
    """
    Фикстура создания пользователя
    """
    response = create_user(app_url, user_data)
    def teardown():
       delete_user(app_url, response.json()['id'])

    request.addfinalizer(teardown)
    return response



@pytest.fixture
def users(app_url):
    response = get_users(app_url)
    assert response.status_code == HTTPStatus.OK
    return response.json()
