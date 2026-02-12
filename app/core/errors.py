from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions.base import (
    AppDetailedError,
    BadRequestError,
    ConflictError,
    NotFoundError,
)


def setup_exception_handlers(app: FastAPI):
    @app.exception_handler(AppDetailedError)
    async def app_exception_handler(request: Request, exc: AppDetailedError):
        return JSONResponse(
            status_code=get_status_code(exc),
            content={'error': {'code': exc.code, 'detail': exc.detail}},
        )


def get_status_code(exc: AppDetailedError) -> int:
    if isinstance(exc, NotFoundError):
        return 404
    if isinstance(exc, ConflictError):
        return 409
    if isinstance(exc, BadRequestError):
        return 400
    return 500
