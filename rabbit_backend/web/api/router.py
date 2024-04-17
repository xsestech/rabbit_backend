from fastapi.routing import APIRouter

from rabbit_backend.web.api import monitoring, topics, users

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(users.router)
api_router.include_router(topics.router, prefix="/topics")
