#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    格式化接口输入输出的数据结构
    Format API request/response data
"""
from pydantic import BaseConfig, BaseModel


class RWModel(BaseModel):
    class Config(BaseConfig):
        allow_population_by_field_name = True
        # json_encoders = {datetime.datetime: convert_datetime_to_real_world}
