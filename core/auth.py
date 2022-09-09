from fastapi.security.api_key import APIKeyHeader
from fastapi import Security, HTTPException, Depends, Request
from starlette.status import HTTP_403_FORBIDDEN
from core.config import settings


api_key_header = APIKeyHeader(name="Authorization", auto_error=False)


async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header in settings.API_KEYS:
        return api_key_header   
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate API KEY"
        )



    
def verify_token(req: Request):
    token = req.headers["Authorization"]
    # Here your code for verifying the token or whatever you use
    if token not in settings.API_KEYS:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )
    return True