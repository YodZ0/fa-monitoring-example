import time

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from fastapi import Request, Response

from src.metrics import (
    HTTP_REQUESTS_TOTAL,
    HTTP_REQUESTS_DURATION_HISTOGRAM,
)


class HTTPMetricsMiddleware(BaseHTTPMiddleware):
    """
    Calculates request process time, count total requests.
    """

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        method = request.method
        endpoint = request.url.path

        # Calculate request process time
        start_time = time.perf_counter()
        response = await call_next(request)
        process_time = time.perf_counter() - start_time

        # Request process time metric
        HTTP_REQUESTS_DURATION_HISTOGRAM.labels(
            method=method,
            endpoint=endpoint,
        ).observe(process_time)

        # Total requests count metric
        HTTP_REQUESTS_TOTAL.labels(
            method=method,
            endpoint=endpoint,
            http_status=str(response.status_code),
        ).inc()

        return response
