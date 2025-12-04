from http import HTTPStatus

import allure

from messages.messages import USER_DELETED

@allure.title("Удаление пользователя")
def test_delete_user(users_api_class, create_new_user):
    user_id = create_new_user.json()['id']
    response = users_api_class.delete_user(user_id)
    assert response.status_code == HTTPStatus.OK
    assert response.json()['message'] == USER_DELETED
