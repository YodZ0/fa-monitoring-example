from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from fastapi import Request, Response

from src.metrics import (
    HTTP_REQUESTS_CURRENT,
    HTTP_REQUESTS_MAX,
)

# Set max inflight requests count
HTTP_REQUESTS_MAX.set(50)


class InflightRequestsMiddleware(BaseHTTPMiddleware):
    """
    Count current inflight requests.
    Note: Only example implementation. Do not use in production.
    """

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        HTTP_REQUESTS_CURRENT.inc()
        response = await call_next(request)
        HTTP_REQUESTS_CURRENT.dec()
        return response
