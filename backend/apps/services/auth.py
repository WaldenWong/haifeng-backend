#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
from datetime import datetime, timedelta

from fastapi import Request
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import Field

from backend.apps.auth import create_access_token, judge_user_activated
from backend.apps.core.cache import RedisCache
from backend.apps.core.errors import (
    ReachLoginAttemptsLimit,
    UserAuthFailed,
    UserWasAlreadyDisabled,
)
from backend.apps.models import db
from backend.apps.models.user import User as UserORM
from backend.apps.schemas import RWModel
from backend.apps.schemas.request import LoginRequest
from backend.apps.schemas.response import DataResponse
from backend.apps.services.captcha import CaptchaService
from backend.apps.services.login_log import LoginLogService
from backend.apps.settings import settings

PasswordContext = CryptContext(schemes=[settings.CRYPT_SCHEMA], deprecated="auto")


class TokenResponse(RWModel):
    token_type: str = Field(description="token_type")
    access_token: str = Field(description="token")


class AuthService:
    logger = logging.getLogger("AuthService")

    @classmethod
    async def login_json(cls, request: Request, data: LoginRequest) -> DataResponse:
        ip = request.client.host  # type: ignore[union-attr]

        attempts_limit = 6

        attempts = int(await RedisCache.get(f"backend:login:{ip}:{data.username}") or 0)
        attempts += 1

        if attempts > attempts_limit:
            if not settings.DEBUG:  # pragma: no cover
                raise ReachLoginAttemptsLimit

        if attempts == attempts_limit:
            expire = 60 * 2
        else:
            expire = 60

        await RedisCache.set(f"backend:login:{ip}:{data.username}", attempts, ex=expire)

        await CaptchaService.verify_image_captcha(data)

        async with db.transaction():
            user = await UserORM.get_by(username=data.username)

            if not user:
                raise UserAuthFailed

            if await judge_user_activated(user):
                if PasswordContext.verify(data.password, user.password):
                    code = 200
                    message = "获取认证成功"
                    now = datetime.now()
                    expired_at = now + timedelta(minutes=settings.TOKEN_EXPIRE_MINUTES)
                    access_token = create_access_token(data={"sub": user.username}, expire=expired_at)
                    await user.update(expired_at=expired_at)

                    if request.session.get("info"):
                        info = request.session["info"]
                        res = {k: v for k, v in info.items() if v}
                        unionid = res.pop("unionid")
                        if not user.unionid:
                            if not await UserORM.get_by(unionid=unionid) and not user.unionid:
                                # FIXME 钉钉扫码登录绑定时，暂时不更新手机号，防止冲突
                                userinfo = {
                                    "nickname": info["nickname"],
                                    "avatar": info.get("avatar"),
                                }
                                if info.get("realname"):
                                    userinfo["realname"] = info["realname"]
                                await user.update(
                                    unionid=unionid,
                                    **userinfo,
                                )
                        elif user.unionid and unionid != user.unionid:
                            code = 201
                            message = "当前登录用户已绑定钉钉，请在登录后解绑重试"
                        request.session.clear()

                    await RedisCache.delete(f"backend:login:{ip}:{data.username}")
                    # 解析ip信息、headers并存入数据库
                    await LoginLogService.new(request, user.id)

                    return DataResponse(
                        code=code, message=message, data=TokenResponse(access_token=access_token, token_type="bearer")
                    )
                else:
                    raise UserAuthFailed
        raise UserWasAlreadyDisabled

    @classmethod
    async def login_from(cls, data: OAuth2PasswordRequestForm) -> TokenResponse:
        async with db.transaction():
            user = await UserORM.get_by(username=data.username)

            if not user:
                raise UserAuthFailed
            result = await judge_user_activated(user)
            if result:
                now = datetime.now()
                expire = now + timedelta(minutes=settings.TOKEN_EXPIRE_MINUTES)
                if PasswordContext.verify(data.password, user.password):
                    access_token = create_access_token(data={"sub": user.username}, expire=expire)
                    await user.update(expired_at=expire)
                    return TokenResponse(access_token=access_token, token_type="bearer")
                else:
                    raise UserAuthFailed
        raise UserWasAlreadyDisabled
