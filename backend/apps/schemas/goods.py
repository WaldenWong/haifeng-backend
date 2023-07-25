#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
from enum import Enum
from typing import Dict

from pydantic import Field

from backend.apps.schemas import RWModel
from backend.apps.schemas.request import PageListRequest


class GoodsType(str, Enum):
    meat = "meat"
    vegetable = "vegetable"
    dry_goods = "dry_goods"


class GoodsTypeInfo(RWModel):
    meat: str = (Field(default=GoodsType.meat, title="肉"),)
    vegetable: str = (Field(default=GoodsType.vegetable, title="蔬菜"),)
    dry_goods: str = (Field(default=GoodsType.dry_goods, title="干货"),)


# class GoodsTypeOptions(MatchFilter[str]):
#     options: List[StrOption] = [
#         StrOption(value=GoodsType.meat, display="肉"),
#         StrOption(value=GoodsType.vegetable, display="蔬菜"),
#         StrOption(value=GoodsType.dry_goods, display="干货"),
#     ]
#
#     @validator("value", always=True)
#     def value_(cls, v: GoodsType) -> GoodsType:
#         if v not in set(item.value for item in GoodsType.__members__.values()):
#             raise ValueError("商品类型搜索仅支持 肉/蔬菜/干货")
#         return v


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
    supplier: Dict[str, str] = Field(None, title="供应商id")


class GoodsListRequest(PageListRequest):
    name: str = Field(None, title="商品名")
    identifier: str = Field(None, title="编号")
    type: GoodsType = Field(None, title="种类")
    purchase_price: float = Field(None, title="进价")
    selling_price: float = Field(None, title="售价")
    inventory: int = Field(None, title="库存")
    sales_volume: int = Field(None, title="销量")
    supplier: int = Field(None, description="供应商")
    purchase_at: datetime = Field(None, title="入库时间")
