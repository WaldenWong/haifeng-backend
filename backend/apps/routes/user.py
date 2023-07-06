#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends

from backend.apps.auth import Authenticated, Permission, get_current_user
from backend.apps.auth.acl import BaseOperationACL
from backend.apps.auth.permission import Allow
from backend.apps.schemas.response import DataResponse
from backend.apps.schemas.user import AddRequest

router = APIRouter()


class OperationACL(BaseOperationACL):
    __acl__ = [(Allow, Authenticated, "view")]


@router.post(
    "/add",
    name="添加用户",
    dependencies=[Permission.all(["view"], OperationACL)],
    response_model=DataResponse,
)
async def add(request: AddRequest, user=Depends(get_current_user)):
    return {"data": {"user_id": user.id, "request": request}}
