#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum
from typing import Dict

from pydantic import Field, root_validator

from backend.apps.schemas import RWModel


class OrderBy(str, Enum):
    DESC = "desc"
    ASC = "asc"


class DateTypes(str, Enum):
    minute = "minute"
    hour = "hour"
    day = "day"
    week = "week"
    month = "month"
    year = "year"


class CaptchaRequest(RWModel):
    answer: str = Field(..., description="验证码答案")
    challenge: str = Field(..., description="验证码id")


class LoginRequest(CaptchaRequest):
    username: str
    password: str


class LocationRequest(RWModel):
    # 需要调用acl.location检查权限的Request继承于此类
    province: str = Field(None, description="省")
    city: str = Field(None, description="市")
    district: str = Field(None, description="区县")

    @root_validator
    def verify(cls, values: Dict[str, str]) -> Dict[str, str]:
        # 防止只传入区县，不传入省市等情况
        if values.get("district"):
            if not values.get("province") or not values.get("city"):
                raise ValueError("参数错误，必须传入完整所在地信息")
        elif values.get("city"):
            if not values.get("province"):
                raise ValueError("参数错误，必须传入完整所在地信息")
        return values


class FilterRequest(RWModel):
    # 条件筛选器Request
    pass


class OffsetLimitRequest(FilterRequest):
    offset: int = Field(default=1, title="页码", gte=0)
    limit: int = Field(default=15, title="每页条数", gt=0, le=50)


class PageListRequest(FilterRequest):
    page: int = Field(default=1, title="页码", gt=0)
    page_size: int = Field(default=15, title="每页条数", gt=0, le=50)
