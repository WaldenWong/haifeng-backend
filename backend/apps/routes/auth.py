#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm

from backend.apps.schemas.request import LoginRequest
from backend.apps.schemas.response import DataResponse
from backend.apps.services.auth import AuthService
from backend.apps.services.captcha import CaptchaService
from backend.apps.settings import settings

AuthRouter = APIRouter()


@AuthRouter.get("/captcha", name="获取验证码", response_model=DataResponse)
async def captcha_image():
    image_data, challenge = await CaptchaService.generate_image_captcha()
    return {
        "message": "获取验证码成功",
        "data": {"image": image_data, "challenge": challenge},
    }


@AuthRouter.post("/login", name="用户登录(json)")
async def login_json(request: Request, login_data: LoginRequest):
    return DataResponse(code=200, message="success", data=dict(token="1215123"))
    # return await AuthService.login_json(request, login_data)


if settings.DEBUG or settings.TESTING:

    @AuthRouter.post(settings.TOKEN_URL, name="用户登录(Form)")
    async def login_form(form_data: OAuth2PasswordRequestForm = Depends()):
        return await AuthService.login_from(form_data)
