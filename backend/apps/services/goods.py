#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from backend.apps.schemas.goods import (
    GoodsAddRequest,
    GoodsListRequest,
    GoodsUpdateRequest,
)
from backend.apps.schemas.response import (
    BoolResponse,
    DataListResponse,
    PageListResponse,
)


class GoodsService:
    @classmethod
    async def goods_add(cls, request: GoodsAddRequest) -> BoolResponse:
        return BoolResponse(message="成功")

    @classmethod
    async def goods_update(cls, request: GoodsUpdateRequest) -> BoolResponse:
        return BoolResponse(message="成功")

    @classmethod
    async def goods_menu(cls) -> DataListResponse:
        return DataListResponse(data=[])

    @classmethod
    async def goods_list(cls, request: GoodsListRequest) -> PageListResponse:
        data = [
            {
                "id": i,
                "name": "xxx",
                "identifier": "GB-154-266",
                "type": "冻货",
                "purchase_price": 15.2,
                "selling_price": 50.5,
                "inventory": 3000,
                "sales_volume": 500,
                "purchase_at": datetime.now(),
            }
            for i in range(1, 51)
        ]
        return PageListResponse(
            data=data,
            page=1,
            page_size=10,
            total_pages=20,
        )

    @classmethod
    async def goods_delete(cls, goods_id: int) -> PageListResponse:
        return PageListResponse(data=[], page=1, page_size=10)
