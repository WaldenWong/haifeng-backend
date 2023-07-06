#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum
from typing import Dict, List, Union
from uuid import UUID

from pydantic import Field

from backend.apps.schemas import RWModel


class ResponseCode(int, Enum):
    SUCCESS = 200
    ERROR = 500
    UNKNOWN_REQUEST = 400  # 未知请求
    PERMISSION_DENIED = 403  # 无权限
    NOT_FOUND = 404  # 未找到


class BoolResponse(RWModel):
    code: ResponseCode = ResponseCode.SUCCESS
    message: str


class DataResponse(RWModel):
    code: Union[int, ResponseCode] = ResponseCode.SUCCESS
    message: str = "操作成功"
    data: Union[str, Dict, RWModel, UUID] = Field(None)


class DataListResponse(RWModel):
    code: ResponseCode = ResponseCode.SUCCESS
    message: str = "操作成功"
    data: List[Dict] = Field(None)


class OffsetLimitResponse(DataListResponse):
    offset: int
    limit: int
    amount: int = 0


class PageListResponse(DataListResponse):
    page: int
    page_size: int
    total_pages: int = 1
    amount: int = 0
