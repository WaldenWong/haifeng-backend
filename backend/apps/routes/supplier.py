#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from backend.apps.services.supplier import SupplierService

router = APIRouter()


@router.get("/items", name="供应商选项")
async def supplier_items():
    return await SupplierService.supplier_items()
