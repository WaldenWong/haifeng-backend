#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
from enum import Enum
from typing import List

from pydantic import Field

from backend.apps.schemas import RWModel
from backend.apps.schemas.request import PageListRequest
from backend.apps.schemas.supplier import Supplier


class GoodsType(str, Enum):
    meat = "肉"
    vegetable = "蔬菜"
    dry_goods = "干货"


class Goods(RWModel):
    name: str = Field(None, title="商品名")
    identifier: str = Field(None, title="编号")
    type: GoodsType = Field(None, title="种类")
    purchase_price: float = Field(None, title="进价")
    selling_price: float = Field(None, title="售价")
    inventory: int = Field(None, title="库存")
    sales_volume: int = Field(None, title="销量")
    purchase_at: datetime = Field(None, title="入库时间")


class GoodsAddRequest(Goods):
    supplier: int = Field(None, title="供应商id")


class GoodsUpdateRequest(GoodsAddRequest):
    ...


class GoodsList(Goods):
    id: int = Field(title="ID")
    supplier: Supplier = Field(None, title="供应商id")


class GoodsListRequest(PageListRequest):
    name: str = Field(None, description="商品名")
    identifier: str = Field(None, description="编号")
    type: GoodsType = Field(None, description="种类")
    supplier: str = Field(None, description="供应商")
