#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Optional

from pydantic import Field

from backend.apps.schemas import RWModel


class IPLocation(RWModel):
    country: Optional[str] = Field(None, title="国家")
    province: Optional[str] = Field(None, title="省")
    city: Optional[str] = Field(None, title="市")
    district: Optional[str] = Field(None, title="区县")
    wgs_lat: Optional[float] = Field(None, title="纬度")
    wgs_lon: Optional[float] = Field(None, title="经度")
    scene: Optional[str] = Field(None, title="IP使用场景")
    areas: Optional[dict] = Field(None, title="多地区，街道信息")
    owner: Optional[str] = Field(None, title="所属机构")
    isp: Optional[str] = Field(None, title="运营商")
