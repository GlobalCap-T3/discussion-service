from app.endpoints import endpoints

def get_client():
    return endpoints.elasticsearch.client
