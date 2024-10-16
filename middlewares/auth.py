import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from config import settings

public_routes = ["/","/docs","/openapi.json","/auth/login", "/auth/register"]

class CheckPermission(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if request.url.path in public_routes:
            return await call_next(request)

        token = request.headers.get("Authorization")
        if not token:
            return JSONResponse(status_code=401, content={"message": "Token not found"})
        
        if token.startswith("Bearer "):
            try:
                token = token.split(" ")[1]
            except IndexError:
                return JSONResponse(status_code=401, content={"message": "Invalid auth token format"})
        else:
            return JSONResponse(status_code=401, content={"message": "Unauthorized"})
        
        try:
            _id = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])["_id"]
        except ExpiredSignatureError:
            return JSONResponse(status_code=401, content={"message": "Token expired"})
        except InvalidTokenError:
            return JSONResponse(status_code=401, content={"message": "Invalid auth token"})
        
        request.state._id = _id # Use request.state to store additional state
        return await call_next(request)
