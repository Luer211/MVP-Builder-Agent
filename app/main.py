from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.routes import router
from app.core.config import get_settings
from app.core.errors import AppError
from app.core.logging import setup_logging
from app.schemas.responses import ApiError


def create_app() -> FastAPI:
    settings = get_settings()
    setup_logging(settings.env)

    app = FastAPI(title=settings.app_name)
    app.include_router(router)

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "app": settings.app_name}

    @app.exception_handler(AppError)
    async def app_error_handler(_: Request, exc: AppError) -> JSONResponse:
        error = ApiError(code=exc.code, message=exc.message, detail=exc.detail)
        return JSONResponse(status_code=exc.status_code, content={"error": error.model_dump()})

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
        error = ApiError(
            code="INVALID_INPUT",
            message="Request validation failed.",
            detail={"errors": exc.errors()},
        )
        return JSONResponse(status_code=400, content={"error": error.model_dump()})

    return app


app = create_app()
