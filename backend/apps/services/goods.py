#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
        return PageListResponse(data=[], page=1, page_size=10)

    @classmethod
    async def goods_delete(cls, goods_id: int) -> PageListResponse:
        return PageListResponse(data=[], page=1, page_size=10)
