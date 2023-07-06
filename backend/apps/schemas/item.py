#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List

from pydantic import Field

from backend.apps.core.filter import OperatorType, Option
from backend.apps.schemas import RWModel


class Filter(RWModel):
    name: str = Field(..., title="参数名称")
    op_type: OperatorType = Field(..., title="操作符类型")
    category: str = Field(..., title="中文名称")
    ops: List[str] = Field(..., title="运算符")
    options: List[Option] = Field(None, title="选择型可选项")
