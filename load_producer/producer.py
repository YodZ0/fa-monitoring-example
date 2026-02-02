import asyncio
import logging
import random
from dataclasses import dataclass
from enum import Enum, auto

import httpx


@dataclass(frozen=True)
class EndpointConfig:
    url: str
    method: str = "GET"
    weight: int = 50
    timeout: float = 5.0


@dataclass
class RequestResult:
    url: str
    status_code: int
    status: str = "Success"


class LoadPattern(Enum):
    CONSTANT = auto()
    RANDOM = auto()


@dataclass
class LoadConfig:
    duration_seconds: float = 0.0  # 0.0 - inf
    pattern: LoadPattern = LoadPattern.CONSTANT

    base_rps: float = 10.0

    # RANDOM pattern params
    random_min_delay_seconds: float = 0.01
    random_max_delay_seconds: float = 2.0


class HTTPLoadProducer:
    def __init__(
        self,
        endpoints: list[EndpointConfig],
        config: LoadConfig,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self.endpoints = endpoints
        self.config = config
        self.client = client or httpx.AsyncClient(
            limits=httpx.Limits(
                max_connections=100,
                max_keepalive_connections=20,
            ),
            timeout=httpx.Timeout(30.0),
        )
        self._shutdown_event = asyncio.Event()
        self._tasks: set[asyncio.Task] = set()

    def _select_endpoint(self) -> EndpointConfig:
        """
        Weighted random endpoint selection.
        """
        weights = [ep.weight for ep in self.endpoints]
        return random.choices(self.endpoints, weights=weights, k=1)[0]

    def _seconds_delay(self) -> float:
        """
        Delay before next request.
        """
        if self.config.pattern == LoadPattern.CONSTANT:
            return 1.0 / self.config.base_rps

        elif self.config.pattern == LoadPattern.RANDOM:
            return random.uniform(
                self.config.random_min_delay_seconds,
                self.config.random_max_delay_seconds,
            )

        return 1.0 / self.config.base_rps

    async def _execute_request(self, endpoint: EndpointConfig) -> RequestResult:
        """
        Execute request via httpx client.
        """
        try:
            response = await self.client.request(
                url=endpoint.url,
                method=endpoint.method,
                timeout=httpx.Timeout(endpoint.timeout),
            )
            return RequestResult(url=endpoint.url, status_code=response.status_code)
        except Exception:
            return RequestResult(url=endpoint.url, status_code=999, status="FAILED")

    async def _worker(self, worker_id: int) -> None:
        while not self._shutdown_event.is_set():
            endpoint = self._select_endpoint()
            response = await self._execute_request(endpoint)
            logging.info(
                "WorkerID: %s | Endpoint: %s | Code: %s | Status: %s",
                worker_id,
                endpoint.url,
                response.status_code,
                response.status,
            )
            delay = self._seconds_delay()
            try:
                await asyncio.wait_for(self._shutdown_event.wait(), timeout=delay)
            except asyncio.TimeoutError:
                pass

    async def start(self, num_workers: int = 5) -> None:
        logging.info(
            "HTTPLoadProducer started | Pattern: %s | Base RPS: %s | Workers: %s",
            self.config.pattern.name,
            self.config.base_rps,
            num_workers,
        )

        for i in range(num_workers):
            task = asyncio.create_task(self._worker(i), name=f"load-worker-{i}")
            self._tasks.add(task)

        await self._shutdown_event.wait()

    async def stop(self) -> None:
        """
        Graceful shutdown with pending current requests.
        """
        if self._shutdown_event.is_set():
            return

        logging.info("Stopping HTTPLoadProducer...")
        self._shutdown_event.set()

        # Wait pending requests with timeout
        if self._tasks:
            done, pending = await asyncio.wait(
                self._tasks,
                timeout=5.0,
                return_when=asyncio.ALL_COMPLETED,
            )

            for task in pending:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass

        await self.client.aclose()
        logging.info("HTTPLoadProducer has been stopped successfully!")
