import json
import os
from http import HTTPStatus

import dotenv
import pytest
from mimesis import Person, Internet

from clients.StatusApi import StatusApi
from clients.UsersApi import UsersApi


@pytest.fixture(scope="session")
def users_api_class(get_env):
    return UsersApi(get_env)

@pytest.fixture(scope="session")
def status_api_class(get_env):
    return StatusApi(get_env)


@pytest.fixture(autouse=True)
def envs():
    dotenv.load_dotenv()



def pytest_addoption(parser):
    """
    Add options to pytest
    """
    parser.addoption("--env", default="dev")


@pytest.fixture(scope="session")
def get_env(request):
    return request.config.getoption("--env")


@pytest.fixture
def app_url():
    return os.getenv("APP_URL")


@pytest.fixture(scope="module")
def fill_test_data(users_api_class):
    with open("users.json") as f:
        test_data_users = json.load(f)
    api_users = []
    for user in test_data_users:
        response = users_api_class.create_user(user)
        api_users.append(response.json())
    user_ids = [user["id"] for user in api_users]

    yield user_ids

    for user_id in user_ids:
        users_api_class.delete_user(user_id)

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
def create_new_user(users_api_class,user_data, request):
    """
    Фикстура создания пользователя
    """
    response = users_api_class.create_user(user_data)
    def teardown():
        users_api_class.delete_user(response.json()['id'])

    request.addfinalizer(teardown)
    return response



@pytest.fixture
def users(users_api_class):
    response = users_api_class.get_users()
    assert response.status_code == HTTPStatus.OK
    return response.json()
