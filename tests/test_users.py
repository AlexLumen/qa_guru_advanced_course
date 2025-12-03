import math
from http import HTTPStatus

import allure
import pytest

from app.models.User import User
from tests.clients import get_users


@allure.title("Тест списка пользователей")
def test_users(app_url):
    response = get_users(app_url)
    assert response.status_code == HTTPStatus.OK

    users = response.json()['items']
    for user in users:
        User.model_validate(user)


@allure.title("Проверить что пользователи не дублируются")
def test_users_no_duplicates(users):
    users_ids = [user["id"] for user in users['items']]
    assert len(users_ids) == len(set(users_ids))


@allure.title("Тест пагинации списка пользователей")
@pytest.mark.parametrize("page, size", [
    (1, 6),
    (2, 6),
    (3, 6),
    (1, 1),
    (5, 2),
    (1, 12),
    (2, 12),
    (1, 13),
    (25, 5)
])
def test_users_list_pagination(app_url, page, size):
    response = get_users(app_url, params={"page": page, "size": size})
    print(response.json())
    all_users_list = get_users(app_url)
    response_page_1 = get_users(app_url, params={"page": 1, "size": 6})
    response_page_2 = get_users(app_url, params={"page": 2, "size": 6})

    total_users = len(all_users_list.json()['items'])
    start = (page - 1) * size
    if start >= total_users:
        expected_count = 0
    else:
        expected_count = min(size, total_users - start)


    with allure.step("Проверить что вернулся указанный page"):
        assert response.json()['page'] == page
    with allure.step("Проверить что вернулся указанный size"):
        assert response.json()['size'] == size
    with allure.step("Проверить количество пользователей"):
        assert len(response.json()['items']) == expected_count
    with allure.step("Проверить количество страниц"):
        assert response.json()['pages'] == math.ceil(len(all_users_list.json()['items']) / size)
    with allure.step("Проверить что возвращаются разные данные при разных page"):
        assert response_page_1.json()['items'] != response_page_2.json()['items']
