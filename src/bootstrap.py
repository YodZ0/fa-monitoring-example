from fastapi import FastAPI

from src.example.router import router as example_router
from src.metrics.router import router as metrics_router
from src.middlewares import (
    HTTPMetricsMiddleware,
    InflightRequestsMiddleware,
    ProcessTimeMiddleware,
)


def use_middlewares(app: FastAPI) -> FastAPI:
    """
    Add middlewares to FastAPI application.

    Note: The last one added is called first.
    """
    app.add_middleware(HTTPMetricsMiddleware)
    app.add_middleware(InflightRequestsMiddleware)
    app.add_middleware(ProcessTimeMiddleware)
    return app


def use_routers(app: FastAPI) -> FastAPI:
    """
    Add routers to FastAPI application.
    """
    app.include_router(example_router)
    app.include_router(metrics_router)
    return app


def create_app(*, use_instrumentator: bool = False) -> FastAPI:
    """
    Create FastAPI application.
    Applies:
    - Middlewares
    - Routers
    """
    app = FastAPI(title="FastAPI monitoring example")
    app = use_middlewares(app)
    app = use_routers(app)
    return app
