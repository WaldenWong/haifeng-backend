#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math
from typing import Dict, List, Optional, Sequence, Tuple, Type, Union

from fastapi import FastAPI
from sqlalchemy import Column, func, nullslast, select
from sqlalchemy.sql.elements import BinaryExpression, UnaryExpression
from sqlalchemy.sql.selectable import Select

from backend.apps.core.errors import NotFilterApi
from backend.apps.core.filter import BaseFilter
from backend.apps.models import db
from backend.apps.schemas import RWModel
from backend.apps.schemas.item import Filter
from backend.apps.schemas.request import FilterRequest
from backend.apps.schemas.response import OffsetLimitResponse, PageListResponse

APP_FILTERS_REQUESTS = {}


def register_app_filters(app: FastAPI) -> None:
    for route in app.routes:
        path = route.path  # type: ignore
        requests = route.endpoint.__annotations__  # type: ignore
        for var, req in requests.items():
            try:
                if issubclass(req, FilterRequest):
                    for field in req.__fields__.values():
                        if field.sub_fields and issubclass(field.sub_fields[0].type_, BaseFilter):
                            APP_FILTERS_REQUESTS[path] = req
            except TypeError:
                pass


async def generate_filters(api: str) -> List[Filter]:
    filters: List[Filter] = []

    page_request = APP_FILTERS_REQUESTS.get(api)
    if not page_request:
        raise NotFilterApi

    for field in page_request.__fields__.values():
        if field.sub_fields and issubclass(field.sub_fields[0].type_, BaseFilter):
            filter_class = field.sub_fields[0].type_
            kwargs = dict(
                name=field.name,
                category=field.field_info.title,
                op_type=filter_class.__fields__.get("op_type").default,
                ops=[item for item in filter_class.__fields__.get("op").type_],
                options=[],
            )
            for filter_class in field.sub_fields:
                # 使用get_options()可以动态控制选择器的选项
                options = await filter_class.type_.get_options()
                if options:
                    kwargs["options"] += options
            filters.append(Filter(**kwargs))
    return filters


def generate_orm_clauses(
    orm: Union[Dict[str, Column], Column, BinaryExpression],
    request: Optional[FilterRequest] = None,
    filters: Optional[Sequence[BaseFilter]] = None,
) -> List:
    # TODO 重构
    clauses = []
    if request and isinstance(orm, dict) and not filters:
        for field in request.__fields__.values():
            if field.sub_fields and issubclass(field.sub_fields[0].type_, BaseFilter):
                filters = request.__getattribute__(field.name)
                if filters and orm.get(field.name) is not None:
                    clauses += [f.generate_orm_clause(orm[field.name]) for f in filters]
            elif issubclass(field.type_, BaseFilter):
                filters = request.__getattribute__(field.name)
                if filters and orm.get(field.name) is not None:
                    clauses += [f.generate_orm_clause(orm[field.name]) for f in filters]

    elif filters:
        clauses += [f.generate_orm_clause(orm) for f in filters]  # type: ignore[arg-type]
    return clauses


async def paginate(
    query: Union[Select, Type[db.Model]],
    schema: Type[RWModel],
    where: Optional[List[BinaryExpression]] = None,
    order_by: Optional[Tuple[UnaryExpression, ...]] = None,
    null_last: bool = False,
    count: Optional[Select] = None,
    page: int = 1,
    page_size: int = 15,
) -> PageListResponse:
    if isinstance(query, type(db.Model)):
        query = query.query

    if where is not None:
        query = query.where(where)

    if count is None:
        count = query  # type: ignore[assignment]

    rv = await select([func.count()]).select_from(count.alias("_q")).gino.one()
    amount = rv[0]

    if order_by is not None:
        if not isinstance(order_by, tuple):
            order_by = (order_by,)

        if null_last:
            order_by = tuple(nullslast(c) for c in order_by)

        query = query.order_by(*order_by)

    data = []
    total_pages = math.ceil(amount / page_size)
    if page <= total_pages:
        offset_value = (0 + (page - 1)) * page_size
        remain = amount - offset_value
        limit_value = min(remain, page_size)
        query = query.offset(offset_value).limit(limit_value)
        data = [
            schema(**(isinstance(_, db.Model) and _.to_dict() or dict(_)))
            for _ in await query.gino.all()  # type:ignore[union-attr]
        ]
    return PageListResponse(
        **{
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
            "amount": amount,
            "data": data,
        }
    )


async def offset_limit(
    query: Union[Select, Type[db.Model]],
    schema: Type[RWModel],
    count: Optional[Select] = None,
    order_by: Optional[UnaryExpression] = None,
    offset: int = 0,
    limit: int = 15,
) -> OffsetLimitResponse:
    query = query.query if isinstance(query, type(db.Model)) else query
    count = query if count is None else count  # type:ignore[assignment]

    amount = await select([func.count()]).select_from(count.alias("_q")).gino.scalar()  # type:ignore[union-attr]

    query = query.order_by(order_by) if order_by is not None else query

    data = []
    if offset <= amount:
        offset_value = offset
        limit_value = limit - (offset + limit - amount) if offset + limit > amount else limit
        query = query.offset(offset_value).limit(limit_value)
        data = [
            schema(**(isinstance(_, db.Model) and _.to_dict() or dict(_)))
            for _ in await query.gino.all()  # type:ignore[union-attr]
        ]
    return OffsetLimitResponse(
        **{
            "offset": offset,
            "limit": limit,
            "amount": amount,
            "data": data,
        }
    )
