#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from backend.apps.routes.auth import AuthRouter
from backend.apps.routes.goods import router as goods_router
from backend.apps.routes.supplier import router as supplier_router
from backend.apps.routes.user import router as user_router

router = APIRouter()
router.include_router(AuthRouter, tags=["权限模块"])
router.include_router(user_router, tags=["用户管理"], prefix="/user")
router.include_router(goods_router, tags=["商品信息"], prefix="/goods")
router.include_router(supplier_router, tags=["供应商信息"], prefix="/supplier")
