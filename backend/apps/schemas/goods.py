#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
from enum import Enum

from pydantic import Field

from backend.apps.schemas import RWModel
from backend.apps.schemas.request import PageListRequest


class GoodsType(str, Enum):
    meat = "肉"
    vegetable = "蔬菜"
    dry_goods = "干货"


class Goods(RWModel):
    name: str = Field(None, description="商品名")
    identifier: str = Field(None, description="编号")
    type: GoodsType = Field(None, description="种类")
    purchase_price: float = Field(None, description="进价")
    selling_price: float = Field(None, description="售价")
    inventory: int = Field(None, description="库存")
    sales_volume: int = Field(None, description="销量")
    purchase_at: datetime = Field(None, description="入库时间")
    supplier: int = Field(None, description="供应商id")


class GoodsAddRequest(Goods):
    ...


class GoodsUpdateRequest(Goods):
    ...


class GoodsListRequest(PageListRequest):
    name: str = Field(None, description="商品名")
    identifier: str = Field(None, description="编号")
    type: GoodsType = Field(None, description="种类")
    supplier: str = Field(None, description="供应商")
