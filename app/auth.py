from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader

from config import CONFIG

api_key_header = APIKeyHeader(name="token")


def get_api_key(api_key: str = Depends(api_key_header)):
    if api_key != CONFIG['API_TOKEN_SERVICE']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    return api_key
