#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from backend.apps.schemas.response import DataListResponse


class SupplierService:
    @classmethod
    async def supplier_items(cls) -> DataListResponse:
        # 查询
        data = [{"id": 1, "name": "xxx"}, {"id": 2, "name": "yyy"}, {"id": 3, "name": "mmm"}, {"id": 4, "name": "nnn"}]
        return DataListResponse(data=data)
