from config.config import Server
from session.BaseSession import BaseSession


class UsersApi:
    def __init__(self, env):
        self.session = BaseSession(base_url=Server(env).app)

    def create_user(self, data: dict):
        """
        Запрос создания пользователя
        """
        response = self.session.post("/api/users/", json=data)
        return response

    def update_user(self, user_id: int, data: dict):
        """
         Запрос обновления пользователя
        """
        response = self.session.patch(f"/api/users/{user_id}/", json=data)
        return response

    def delete_user(self, user_id: int):
        """
         Запрос удаления пользователя
        """
        response = self.session.delete(f"/api/users/{user_id}/")
        return response

    def get_users(self, **kwargs):
        """
        Запрос на получение пользователей
        """
        response = self.session.get("/api/users/", params=kwargs)
        return response

    def get_user(self, user_id: int):
        """
        Запрос на получение пользователя
        """
        response = self.session.get(f"/api/users/{user_id}/")
        return response
