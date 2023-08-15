#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from backend.apps.core.errors import GoodsAlreadyExists
from backend.apps.models.goods import Goods as GoodsORM
from backend.apps.schemas.goods import (
    GoodsAddRequest,
    GoodsListRequest,
    GoodsTypeInfo,
    GoodsUpdateRequest,
)
from backend.apps.schemas.response import (
    BoolResponse,
    DataListResponse,
    DataResponse,
    PageListResponse,
)


class GoodsService:
    @classmethod
    async def goods_add(cls, request: GoodsAddRequest) -> DataResponse:
        goods = await GoodsORM.get_by(name=request.name)
        if goods:
            raise GoodsAlreadyExists
        goods = await GoodsORM.create(**request.dict())
        return DataResponse(data=goods.id)

    @classmethod
    async def goods_update(cls, request: GoodsUpdateRequest) -> BoolResponse:
        return BoolResponse(message="成功")

    @classmethod
    async def goods_items(cls) -> DataListResponse:
        return DataListResponse(data=[])

    @classmethod
    async def goods_list(cls, request: GoodsListRequest) -> PageListResponse:
        kwargs = request.dict(exclude={"sort", "sort_k", "page", "page_size"}, exclude_none=True)
        order = getattr(getattr(GoodsORM, request.sort_k), request.sort)()
        goods = await GoodsORM.objects.filter(**kwargs).order_by(order).all()
        return PageListResponse(
            data=goods,
            page=request.page,
            page_size=request.page_size,
            total_pages=20,
        )

    @classmethod
    async def goods_delete(cls, goods_id: int) -> PageListResponse:
        return PageListResponse(data=[], page=1, page_size=10)

    @classmethod
    def goods_types(cls) -> DataListResponse:
        result = [
            {"display_name": v.default[0].title, "key": v.default[0].default or k}
            for k, v in GoodsTypeInfo.__fields__.items()
        ]
        return DataListResponse(data=result)
