#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, Query

from backend.apps.auth import Authenticated, Permission, Role, get_current_user
from backend.apps.auth.acl import BaseOperationACL
from backend.apps.auth.permission import Allow
from backend.apps.schemas.user import UserAddRequest

router = APIRouter()


class OperationACL(BaseOperationACL):
    __acl__ = [(Allow, Authenticated, "view")]


@router.post(
    "/add",
    name="添加用户",
    dependencies=[Permission.all(Role.SYSTEM_ADMIN, OperationACL)],
)
async def user_add(request: UserAddRequest, user=Depends(get_current_user)):
    return {"data": {"user_id": user.id, "request": request}}


@router.delete(
    "/delete",
    name="删除用户",
    dependencies=[Permission.all(Role.SYSTEM_ADMIN, OperationACL)],
)
async def user_delete(user_id: int = Query(..., title="用户ID", alias="id")):
    return {"data": {"user_id": user_id}}
