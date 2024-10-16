from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, redis_client, rate_limit: int, time_window: int):
        super().__init__(app)
        self.redis_client = redis_client
        self.rate_limit = rate_limit
        self.time_window = time_window

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        redis_key = f"rate_limiter:{client_ip}"
        
        current_count = self.redis_client.get(redis_key)

        if current_count is None:
            self.redis_client.set(redis_key, 1, ex=self.time_window)
        else:
            current_count = int(current_count)
            if current_count >= self.rate_limit:
                return JSONResponse(status_code=429, content={"message": "Rate limit exceeded! Try again later"})
            
            self.redis_client.incr(redis_key)

        response = await call_next(request)
        return response