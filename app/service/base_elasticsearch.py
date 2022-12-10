from logging import getLogger
from elasticsearch import AsyncElasticsearch

logger = getLogger(f'uvicorn.{__name__}')

class BaseElasticSearch():

    index: str

    @classmethod
    async def create(cls, client: AsyncElasticsearch, doc_obj: dict):
        response = await client.index(
            index=cls.index,
            op_type='create',
            document=doc_obj
        )
        logger.debug("[srv] %s create response %s.", cls.__name__, response)
        return response.body.get("_id")

    @classmethod
    async def get(cls, client: AsyncElasticsearch, _id: str):
        response = await client.get(index=cls.index, id=_id)
        logger.debug("[srv] %s get response %s.", cls.__name__, response)
        return response.body.get("_source", {})