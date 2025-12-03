import math
from http import HTTPStatus

import allure
import pytest
import requests

from models.User import User

@allure.title("Тест списка пользователей")
def test_users(app_url):
    response = requests.get(f"{app_url}/api/users/")
    assert response.status_code == HTTPStatus.OK

    users = response.json()
    for user in users:
        User.model_validate(user)

@allure.title("Тест получения пользователя по id")
@pytest.mark.parametrize("user_id", [1, 2, 6, 11, 12])
def test_user(app_url, user_id):
    response = requests.get(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.OK
    user = response.json()
    User.model_validate(user)

@allure.title("Проверить возврат ошибки при указании невалидного id")
@pytest.mark.parametrize("user_id", [-1, 0, "fafaf"])
def test_user_invalid_values(app_url, user_id):
    response = requests.get(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

@allure.title("Проверить что пользователи не дублируются")
def test_users_no_duplicates(users):
    users_ids = [user["id"] for user in users]
    assert len(users_ids) == len(set(users_ids))


@allure.step("Проверить что возвращается 404 при указании несуществующего id")
@pytest.mark.parametrize("user_id", [13])
def test_user_nonexistent_values(app_url, user_id):
    response = requests.get(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.NOT_FOUND


@allure.title("Тест пагинации списка пользователей")
@pytest.mark.parametrize("page, size, expected_count", [
    (1, 6, 6),
    (2, 6, 6),
    (3, 6, 0),
    (1, 1, 1),
    (1, 2, 2),
    (1, 12, 12),
    (2, 12, 0),
    (1, 13, 12)
])
def test_users_list_pagination(app_url, page, size, expected_count):
    response = requests.get(f"{app_url}/api/users/?page={page}&size={size}")
    all_users_list = requests.get(f"{app_url}/api/users/")
    response_page_1 = requests.get(f"{app_url}/api/users/?page={1}&size={6}")
    response_page_2 = requests.get(f"{app_url}/api/users/?page={2}&size={6}")
    with allure.step("Проверить что вернулся указанный page"):
        assert response.json()['page'] == page
    with allure.step("Проверить что вернулся указанный size"):
        assert response.json()['size']  == size
    with allure.step("Проверить количество пользователей"):
        assert len(response.json()['items']) == expected_count
    with allure.step("Проверить количество страниц"):
        assert response.json()['pages'] == math.ceil(len(all_users_list.json()['items'])/size)
    with allure.step("Проверить что возвращаются разные данные при разных page"):
        assert response_page_1.json()['items'] != response_page_2.json()['items']
