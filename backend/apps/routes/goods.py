#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fastapi import APIRouter, Query

from backend.apps.auth import Authenticated, Permission, Role
from backend.apps.auth.acl import BaseOperationACL
from backend.apps.auth.permission import Allow
from backend.apps.schemas.goods import (
    GoodsAddRequest,
    GoodsListRequest,
    GoodsUpdateRequest,
)
from backend.apps.services.goods import GoodsService

router = APIRouter()


class OperationACL(BaseOperationACL):
    __acl__ = [(Allow, Authenticated, "view")]


@router.post(
    "/add",
    name="添加商品",
    dependencies=[Permission.all(Role.SYSTEM_ADMIN, OperationACL)],
)
async def goods_add(request: GoodsAddRequest):
    return GoodsService.goods_add(request)


@router.put(
    "/update",
    name="更新商品",
    dependencies=[Permission.all(Role.SYSTEM_ADMIN, OperationACL)],
)
async def goods_update(request: GoodsUpdateRequest):
    return GoodsService.goods_update(request)


@router.get(
    "/menu",
    name="商品菜单",
    dependencies=[Permission.all(Role.SYSTEM_ADMIN, OperationACL)],
)
async def goods_menu():
    return GoodsService.goods_menu()


@router.post(
    "/list",
    name="商品信息列表",
    dependencies=[Permission.all(Role.SYSTEM_ADMIN, OperationACL)],
)
async def goods_list(request: GoodsListRequest):
    return GoodsService.goods_list(request)


@router.delete(
    "/delete",
    name="商品信息列表",
    dependencies=[Permission.all(Role.SYSTEM_ADMIN, OperationACL)],
)
async def goods_delete(goods_id: int = Query(..., title="商品id")):
    return GoodsService.goods_delete(goods_id)
