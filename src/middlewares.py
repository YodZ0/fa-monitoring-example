import time

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from fastapi import Request, Response

from src.metrics import HTTP_REQUESTS_TOTAL, HTTP_REQUESTS_DURATION_HISTOGRAM


class PrometheusMetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        start_time = time.perf_counter()
        response = await call_next(request)
        process_time = time.perf_counter() - start_time

        method = request.method
        endpoint = request.url.path

        HTTP_REQUESTS_DURATION_HISTOGRAM.labels(
            method=method,
            endpoint=endpoint,
        ).observe(process_time)

        HTTP_REQUESTS_TOTAL.labels(
            method=method,
            endpoint=endpoint,
            http_status=str(response.status_code),
        ).inc()

        return response
