from fastapi import FastAPI
from routes.auth.auth import router as auth_router
from routes.paper.paper import router as paper_router
from routes.extract.extract import router as extract_router
from middlewares.auth import CheckPermission
from middlewares.rate_limiter import RateLimiterMiddleware
from config.cache import redis_client
from config.db import paper_collection

app = FastAPI()

@app.get("/")
async def root():
    return {"Hello": "World"}

@app.on_event("startup")
async def startup():
    await paper_collection.create_index(
        [("sections.questions.question", "text"), ("sections.questions.answer", "text")]
    )

app.add_middleware(RateLimiterMiddleware, redis_client=redis_client, rate_limit=10, time_window=60)
app.add_middleware(CheckPermission)
app.include_router(auth_router)
app.include_router(paper_router)
app.include_router(extract_router)