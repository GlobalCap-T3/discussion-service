import requests
from typing import Optional
from logging import getLogger
from pydantic import BaseModel

logger = getLogger(f'uvicorn.{__name__}')

class AuthenticationConfig(BaseModel):
    host: str
    port: int
    protocol: str = "http"
    prefix: str = "/v1/auth"

class AuthenticationService():

    config_key = "authentication-service"

    def __init__(self, config: Optional[dict] = None):
        if config:
            self.init_config(config)

    def init_config(self, config: dict):
        if self.config_key in config:
            self.config = AuthenticationConfig(**config[self.config_key])
            self.uri = f"{self.config.protocol}://{self.config.host}:{self.config.port}{self.config.prefix}"
            logger.debug("[ep] Init authen client config at %s", self.uri)
        else:
            raise ValueError(
                f"Expected {self.config_key} in configuration dict but found None."
            )

    def get_current_user(self, token: str):
        response = requests.get(
            self.uri+"/user/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        if (response.status_code == 200):
            return response.json()