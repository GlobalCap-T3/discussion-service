from .base_elasticsearch import BaseElasticSearch

class DiscussionService(BaseElasticSearch):
    index = "data-discussion"