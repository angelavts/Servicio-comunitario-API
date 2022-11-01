from fastapi.security.api_key import APIKeyHeader
from fastapi import Security, HTTPException, Depends, Request
from starlette.status import HTTP_403_FORBIDDEN
from core.config import settings


api_key_header = APIKeyHeader(name="access_token", auto_error=False)


async def get_api_key(api_key_header: str = Security(api_key_header)):
    return api_key_header   
