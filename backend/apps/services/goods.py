#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import and_, case

from backend.apps.core.errors import GoodsAlreadyExists, GoodsNotExists
from backend.apps.core.pagination import generate_orm_clauses
from backend.apps.models import db
from backend.apps.models.goods import Goods as GoodsORM
from backend.apps.schemas.goods import (
    GoodsAddRequest,
    GoodsListRequest,
    GoodsType,
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
        clauses = generate_orm_clauses(
            dict(
                name=GoodsORM.name,
                identifier=GoodsORM.identifier,
                purchase_price=GoodsORM.purchase_price,
                selling_price=GoodsORM.selling_price,
                inventory=GoodsORM.inventory,
                sales=GoodsORM.sales,
                supplier=GoodsORM.supplier,
                purchase_at=GoodsORM.purchase_at,
            ),
            request,
        )
        columns = [
            GoodsORM.id,
            GoodsORM.name,
            GoodsORM.identifier,
            GoodsORM.purchase_price,
            GoodsORM.selling_price,
            GoodsORM.inventory,
            GoodsORM.sales,
            GoodsORM.month_sales,
            GoodsORM.purchase_at,
            GoodsORM.supplier,
            GoodsORM.warranty,
            GoodsORM.notes,
        ]
        order = getattr(getattr(GoodsORM, request.sort_k), request.sort)()
        goods = (
            await db.select(
                columns
                + [
                    case(
                        [
                            (GoodsORM.type == GoodsType.meat, "肉"),
                            (GoodsORM.type == GoodsType.vegetable, "蔬菜"),
                            (GoodsORM.type == GoodsType.dry_goods, "干货"),
                        ]
                    ).label("type"),
                ]
            )
            .where(and_(*clauses))
            .order_by(order)
            .gino.all()
        )
        return PageListResponse(
            data=goods,
            page=request.page,
            page_size=request.page_size,
            total_pages=20,
        )

    @classmethod
    async def goods_delete(cls, goods_id: int) -> BoolResponse:
        goods = await GoodsORM.query.where(GoodsORM.id == goods_id).gino.first()
        if not goods:
            raise GoodsNotExists
        await goods.delete()
        return BoolResponse(message="操作成功")

    @classmethod
    def goods_types(cls) -> DataListResponse:
        result = [
            {"display_name": v.field_info.title, "key": v.field_info.default or k}
            for k, v in GoodsTypeInfo.__fields__.items()
        ]
        return DataListResponse(data=result)
