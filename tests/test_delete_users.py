from http import HTTPStatus

import allure

from tests.clients import delete_user
from tests.messages import USER_DELETED

@allure.title("Удаление пользователя")
def test_delete_user(app_url, create_new_user):
    user_id = create_new_user.json()['id']
    response = delete_user(app_url, user_id)
    assert response.status_code == HTTPStatus.OK
    assert response.json()['message'] == USER_DELETED
