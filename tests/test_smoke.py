from http import HTTPStatus
import allure
import requests

@allure.title("Проверить, что приложение запущено")
def test_status_app(app_url):
    response = requests.get(f"{app_url}/status")
    assert response.status_code == HTTPStatus.OK
    assert response.json()['users'] == True
