from .elasticsearch import ElasticSearch

class Singleton:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance

class EndpointsManager(Singleton):
    def init_config(self, config):
        self.elasticsearch = ElasticSearch(config)

    async def init_db(self):
        await endpoints.elasticsearch.init_db()
        await endpoints.elasticsearch.init_index()

endpoints = EndpointsManager()