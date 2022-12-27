import os
from pyaml_env import parse_config

from .authentication_ep import AuthenticationService
from .elasticsearch import ElasticSearch

class Singleton:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance

class EndpointsManager(Singleton):
    def init_config(self, config):
        self.elasticsearch = ElasticSearch(config)
        self.authentication_ep = AuthenticationService(config)

    async def init_db(self):
        await self.elasticsearch.init_db()
        await self.elasticsearch.init_index()

def load_config():
    env = os.getenv("SERVICE_ENV", "dev")
    config = parse_config("config/config.yml").get(env)
    return config

endpoints = EndpointsManager()
endpoints.init_config(load_config())