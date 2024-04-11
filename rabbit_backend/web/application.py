from importlib import metadata

from fastapi import FastAPI
from fastapi.responses import UJSONResponse

from rabbit_backend.logging import configure_logging
from rabbit_backend.web.api.router import api_router
from rabbit_backend.web.lifetime import register_shutdown_event, register_startup_event
from rabbit_backend.web.util import get_api_prefix


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    configure_logging()
    api_prefix = get_api_prefix()
    app = FastAPI(
        title="rabbit_backend",
        version=metadata.version("rabbit_backend"),
        docs_url=f"{api_prefix}/docs",
        redoc_url=f"{api_prefix}/redoc",
        openapi_url=f"{api_prefix}/openapi.json",
        default_response_class=UJSONResponse,
    )

    # Adds startup and shutdown events.
    register_startup_event(app)
    register_shutdown_event(app)

    # Main router for the API.
    app.include_router(router=api_router, prefix=api_prefix)

    return app
