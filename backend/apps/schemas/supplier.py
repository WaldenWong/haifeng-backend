#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pydantic import Field

from backend.apps.schemas import RWModel


class Supplier(RWModel):
    name: str = Field(None, description="供应商名")
    boss_name: str = Field(None, description="老板名")
