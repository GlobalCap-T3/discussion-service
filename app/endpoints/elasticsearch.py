from typing import Optional
from logging import getLogger
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, validator
from elasticsearch import AsyncElasticsearch

logger = getLogger(f'uvicorn.{__name__}')
__idxprefix__ = "data-"

class ElasticSearchMapping(BaseModel):
    properties: dict

class ElasticSearchConfig(BaseModel):
    host: str
    port: int
    protocol: str = "http"
    index: str
    mapping: ElasticSearchMapping

    @validator('index')
    def validate_index(cls, index):
        return __idxprefix__ + index

class ElasticSearch():

    config_key = "elasticsearch"

    def __init__(self, config: Optional[dict] = None):
        if config:
            self.init_config(config)

    def init_config(self, config):
        if self.config_key in config:
            self.config = ElasticSearchConfig(**config[self.config_key])
            self.uri = f"{self.config.protocol}://{self.config.host}:{self.config.port}"
            self.client = AsyncElasticsearch(self.uri)
            self.index = self.config.index
            self.mapping = self.config.mapping
            logger.debug("[db] ES client connected at %s", self.uri)
        else:
            raise ValueError(
                f"Expected {self.config_key} in configuration dict but found None."
            )

    async def init_db(self):
        template = {
            "mappings": {
                "properties": {
                    "@timestamp": { "type": "date" },
                    "create_at": { "type": "date" },
                    "update_at": { "type": "date" },
                }
            }
        }
        response = await self.client.cluster.put_component_template(
            name=f"{__idxprefix__}default-mapping",
            template=template,
        )
        logger.debug(
            "[db] ES create default mapping component template response %s.", response
        )
        response = await self.client.indices.put_index_template(
            name=f"{__idxprefix__}default-template",
            composed_of=[f"{__idxprefix__}default-mapping"],
            index_patterns=f"{__idxprefix__}*"
        )
        logger.debug("[db] ES create default data template response %s.", response)

        pipeline = {
            "description": "Set create time and update time.",
            "processors": [
                {
                    "script": {
                        "source": """
                            def now = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(new Date());
                            ctx["update_at"] = now;
                            if (!ctx.containsKey('created_at')) {
                                ctx['created_at'] = now;
                            }
                        """,
                        "if": f"ctx['_index'].contains('{__idxprefix__}')",
                    }
                }
            ],
        }
        self.client.ingest.put_pipeline(**pipeline)

    async def init_index(self):
        # Check if index already exists
        if await self.client.indices.exists(index=self.index):
            response = await self.client.indices.put_mapping(
                index=self.index,
                properties=self.mapping.properties
            )
            logger.debug("[db] ES update index %s mapping return %s.", self.index, response)
        else:
            response = await self.client.indices.create(
                index=self.index,
                mappings=jsonable_encoder(self.mapping)
            )
            logger.debug("[db] ES create index %s returns %s.", self.index, response)