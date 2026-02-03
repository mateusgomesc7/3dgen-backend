from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.exceptions.base import AppDetailedException, NotFoundException, ConflictException, BadRequestException

def setup_exception_handlers(app: FastAPI):
    @app.exception_handler(AppDetailedException)
    async def app_exception_handler(request: Request, exc: AppDetailedException):
        return JSONResponse(
            status_code=get_status_code(exc),
            content={
                "error": {
                    "code": exc.code,
                    "detail": exc.detail
                }
            },
        )

def get_status_code(exc: AppDetailedException) -> int:
    if isinstance(exc, NotFoundException):
        return 404
    if isinstance(exc, ConflictException):
        return 409
    if isinstance(exc, BadRequestException):
        return 400
    return 500
