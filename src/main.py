from fastapi import FastAPI

from src.metrics.router import router as metrics_router
from src.middlewares import HTTPMetricsMiddleware, InflightRequestsMiddleware

app = FastAPI()

# The last one added is called first
app.add_middleware(HTTPMetricsMiddleware)
app.add_middleware(InflightRequestsMiddleware)

app.include_router(metrics_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app="src.main:app",
        host="127.0.0.1",
        port=8000,
    )
