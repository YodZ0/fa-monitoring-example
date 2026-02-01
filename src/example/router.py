import asyncio
import random
from functools import partial

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

__all__ = ("router",)

router = APIRouter(
    prefix="/example",
    tags=["Example"],
)


def random_status(statuses: list[int]) -> int:
    index = random.randint(0, len(statuses) - 1)
    return statuses[index]


random_2xx = partial(
    random_status,
    [
        status.HTTP_200_OK,
        status.HTTP_201_CREATED,
    ],
)
random_4xx = partial(
    random_status,
    [
        status.HTTP_400_BAD_REQUEST,
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_404_NOT_FOUND,
        status.HTTP_429_TOO_MANY_REQUESTS,
    ],
)
random_5xx = partial(
    random_status,
    [
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        status.HTTP_501_NOT_IMPLEMENTED,
        status.HTTP_503_SERVICE_UNAVAILABLE,
        status.HTTP_504_GATEWAY_TIMEOUT,
    ],
)


@router.get("/code-2xx")
async def code_2xx() -> JSONResponse:
    """
    Return random 2xx status response.
    """
    return JSONResponse(
        content={"message": "OK"},
        status_code=random_2xx(),
    )


@router.get("/code-4xx")
async def code_4xx():
    """
    Return random 4xx status response.
    """
    return JSONResponse(
        content={"message": "Error"},
        status_code=random_4xx(),
    )


@router.get("/code-5xx")
async def code_5xx():
    """
    Return random 5xx status response.
    """
    return JSONResponse(
        content={"message": "Server Error"},
        status_code=random_5xx(),
    )


@router.get("/ms-200", status_code=status.HTTP_200_OK)
async def ms_200():
    await asyncio.sleep(0.2)
    return {"message": "OK"}


@router.get("/ms-500", status_code=status.HTTP_200_OK)
async def ms_500():
    await asyncio.sleep(0.5)
    return {"message": "OK"}


@router.get("/ms-1000", status_code=status.HTTP_200_OK)
async def ms_1000():
    await asyncio.sleep(1)
    return {"message": "OK"}
