from config.config import Server
from session.BaseSession import BaseSession


class StatusApi:

    def __init__(self, env):
        self.session = BaseSession(base_url=Server(env).app)

    def status(self):
        response = self.session.get('/status')
        return response
