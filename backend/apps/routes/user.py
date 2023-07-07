#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, Query

from backend.apps.auth import Authenticated, Permission, get_current_user
from backend.apps.auth.acl import BaseOperationACL
from backend.apps.auth.permission import Allow
from backend.apps.schemas.response import DataResponse
from backend.apps.schemas.user import AddRequest

router = APIRouter()


class OperationACL(BaseOperationACL):
    __acl__ = [(Allow, Authenticated, "view")]


@router.get(
    "/info",
    name="用户信息",
    # dependencies=[Permission.all(["view"], OperationACL)],
    response_model=DataResponse,
)
async def info(token: str = Query(..., title="token")):
    return DataResponse(
        code=200,
        message="success",
        data=dict(roles=["user", "admin"], name="admin", avatar="123", introduction="11222"),
    )


@router.post(
    "/add",
    name="添加用户",
    dependencies=[Permission.all(["view"], OperationACL)],
    response_model=DataResponse,
)
async def add(request: AddRequest, user=Depends(get_current_user)):
    return {"data": {"user_id": user.id, "request": request}}
