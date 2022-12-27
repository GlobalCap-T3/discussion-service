from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.endpoints import endpoints

oauth2_scheme = OAuth2PasswordBearer(endpoints.authentication_ep.uri+"/login")

def get_client():
    return endpoints.elasticsearch.client

def get_current_user(token: str = Depends(oauth2_scheme)):
    user = endpoints.authentication_ep.get_current_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Cannot verify user.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user