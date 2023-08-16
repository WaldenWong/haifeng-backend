#!/usr/bin/env python3
# -*- coding: utf-8 -*-
class ApplicationError(Exception):
    code = 400
    message = "你的请求发生了错误，请稍后重试"


class UserLoginFailed(ApplicationError):
    headers = {"WWW-Authenticate": "Bearer"}
    code = 401
    message = "用户未登录"


class UserTokenWasExpired(ApplicationError):
    headers = {"WWW-Authenticate": "Bearer"}
    code = 401
    message = "用户验证信息有误或已过期，请重新登录"


class UserTokenWasUpdated(ApplicationError):
    headers = {"WWW-Authenticate": "Bearer"}
    code = 401
    message = "检测到账号已在其他地方登录，请重新登录"


class ReachLoginAttemptsLimit(ApplicationError):
    code = 425
    message = "该用户尝试登录次数到达上限，请两分钟后重试"


class UserWasAlreadyDisabled(ApplicationError):
    code = 401
    message = "该账户已禁用，请联系管理员"


class UserAuthFailed(ApplicationError):
    code = 403
    message = "用户名或密码错误"


# CaptchaService
class CaptchaVerifyFailed(ApplicationError):
    code = 422
    message = "验证码输入有误，请重试"


class CaptchaWasExpired(ApplicationError):
    code = 425
    message = "验证码已过期，请重新获取"


class UserPhoneHasSentTooManyTimes(ApplicationError):
    code = 410
    message = "用户手机号已达当日发送上限，请明日重试"


class NotFilterApi(ApplicationError):
    code = 424
    message = "目标路由不存在或暂不支持条件筛选器，请检查后重试"


class GoodsAlreadyExists(ApplicationError):
    code = 424
    message = "商品已存在"


class GoodsNotExists(ApplicationError):
    code = 424
    message = "商品不存在"
