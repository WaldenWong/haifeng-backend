#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
from typing import Any, Dict

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.requests import Request

from backend import __version__

# from backend.apps.auth import AuthRouter
from backend.apps.auth.permission import AuthPermissionDenied
from backend.apps.core.cache import RedisCache
from backend.apps.core.errors import ApplicationError
from backend.apps.models import db
from backend.apps.routes import router
from backend.apps.services.user import UserService
from backend.apps.settings import settings


def get_app(version: str = __version__) -> FastAPI:
    app_kwargs: Dict[str, Any] = {"title": settings.PROJECT_NAME, "debug": settings.DEBUG, "version": version}
    if settings.DEBUG:  # pragma: no cover
        logging.basicConfig(level=logging.DEBUG)
        if settings.DB_ECHO_LEVEL == "debug":
            logging.getLogger("sqlalchemy").setLevel(level=logging.DEBUG)
        else:
            logging.getLogger("sqlalchemy").setLevel(level=logging.ERROR)

    else:
        app_kwargs.update({"redoc_url": None, "docs_url": None, "openapi_url": None})

    app = FastAPI(**app_kwargs)
    app.include_router(router, prefix="/api")

    async def not_found_handler(request: Request, exc: ApplicationError) -> JSONResponse:
        json_resp = {"code": 404, "message": "Not Found"}
        return JSONResponse(status_code=200, content=json_resp)

    async def default_error_handler(request: Request, exc: ApplicationError) -> JSONResponse:
        json_resp = {"code": exc.code, "message": exc.message}
        return JSONResponse(status_code=200, content=json_resp)

    async def validation_exception_handler(request: Request, exc: ApplicationError) -> JSONResponse:
        json_resp = {"code": 422, "message": f"上传参数有误:{str(exc)}"}
        return JSONResponse(status_code=200, content=json_resp)

    @app.exception_handler(AuthPermissionDenied)
    async def auth_error_handler(request: Request, exc: AuthPermissionDenied) -> JSONResponse:
        json_resp = {"code": exc.code, "message": exc.message}
        return JSONResponse(status_code=200, content=json_resp)

    app.add_exception_handler(404, not_found_handler)
    app.add_exception_handler(ApplicationError, default_error_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)

    allowed_hosts = ["*"] if not settings.ALLOWED_HOSTS and settings.DEBUG else settings.ALLOWED_HOSTS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["content-disposition"],
    )
    # 当请求的头信息 Accept-Encoding 字段带有"gzip"时，GZipMiddleware负责完成相应的返回结果处理
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    # app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY, same_site=settings.SAME_SITE)

    if settings.IDE == "prod":
        # TrustedHostMiddleware强制发来的请求必须在Header信息中设置了Host选项，为了避免HTTP Host Header攻击
        app.add_middleware(TrustedHostMiddleware, allowed_hosts=["example.com", "*.example.com"])
        # HTTPSRedirectMiddleware强制发来的请求协议必须是https或者wss
        app.add_middleware(HTTPSRedirectMiddleware)

    @app.on_event("startup")
    async def startup_event() -> None:
        if settings.DATABASE_CONFIG.url:
            await db.connect()
        if not settings.TESTING:  # pragma: no cover
            await UserService.init_admin()

    @app.on_event("shutdown")
    async def shutdown_event() -> None:
        await RedisCache.close()
        await db.disconnect()

    return app
