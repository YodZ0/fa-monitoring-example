from prometheus_client import Counter, REGISTRY, Histogram

__all__ = (
    "HTTP_REQUESTS_TOTAL",
    "HTTP_REQUESTS_DURATION_HISTOGRAM",
)

HTTP_REQUESTS_TOTAL = Counter(
    name="http_requests_total",
    documentation="Total number of HTTP requests",
    labelnames=["endpoint", "method", "http_status"],
    registry=REGISTRY,
)


HTTP_REQUESTS_DURATION_HISTOGRAM = Histogram(
    name="http_requests_duration_seconds_histogram",
    documentation="Total number of HTTP requests",
    buckets=[
        0.1,  # 100 ms
        0.2,  # 200 ms
        0.25,  # 250 ms
        0.5,  # 500 ms
        1,  # 1000 ms
    ],
    labelnames=["endpoint", "method"],
    registry=REGISTRY,
)
