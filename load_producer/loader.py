import asyncio
import logging
import sys

from producer import HTTPLoadProducer, EndpointConfig, LoadConfig, LoadPattern


async def main() -> None:
    endpoints = [
        EndpointConfig(url="http://localhost:8000/example/code-2xx", weight=50),
        EndpointConfig(url="http://localhost:8000/example/code-4xx", weight=3),
        EndpointConfig(url="http://localhost:8000/example/code-5xx", weight=2),
        EndpointConfig(url="http://localhost:8000/example/ms-200", weight=30),
        EndpointConfig(url="http://localhost:8000/example/ms-500", weight=10),
        EndpointConfig(url="http://localhost:8000/example/ms-1000", weight=5),
    ]
    config = LoadConfig(pattern=LoadPattern.CONSTANT)
    producer = HTTPLoadProducer(
        endpoints=endpoints,
        config=config,
    )
    try:
        await producer.start(num_workers=5)
    finally:
        await producer.stop()


if __name__ == "__main__":
    try:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s | %(levelname)-8s | %(message)s",
            datefmt="%H:%M:%S",
        )
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(0)
