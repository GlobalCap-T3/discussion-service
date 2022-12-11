from logging import getLogger
from elasticsearch import AsyncElasticsearch, NotFoundError

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
        try:
            response = await client.get(index=cls.index, id=_id)
            logger.debug("[srv] %s get response %s.", cls.__name__, response)
            return response.body.get("_source", {})
        except NotFoundError as e:
            logger.debug("[srv] ES not found error %s", e)

    @classmethod
    async def search(cls, client: AsyncElasticsearch, query_str: str, fields: list[str]):
        query = {
            "combined_fields": {
                "query": query_str,
                "fields": fields
            }
        }
        response = await client.search(index=cls.index, query=query)
        return response.body.get("hits", {}).get("hits", [])