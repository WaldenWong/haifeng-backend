#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Any, Dict, List, Optional, Union

import ormar as orm
import ormar_postgres_extensions as orm_ext
import sqlalchemy as sa
from databases import Database
from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.asyncio import AsyncEngine

from backend.apps.settings import settings

__all__ = ["orm_ext", "orm", "sa", "Base", "BaseMeta", "db"]

if settings.DATABASE_CONFIG.url:
    db_url = settings.DATABASE_CONFIG.url.render_as_string(hide_password=False)
else:
    raise ConnectionError
db = Database(db_url)
metadata = MetaData()
engine = AsyncEngine(create_engine(db_url))

"""
ormar参考：https://github.com/collerek/ormar
如果使用JSONB参考：https://github.com/tophat/ormar-postgres-extensions
原生sqlalchemy执行查看Database()源码
"""


class BaseMeta(orm.ModelMeta):
    metadata = metadata
    database = db


class Base(orm.Model):
    class Meta(BaseMeta):
        abstract = True

    id = orm.Integer(primary_key=True)
    created_on = orm.DateTime(default=datetime.now, server_default=sa.func.now(), index=True)
    updated_on = orm.DateTime(default=datetime.now, onupdate=sa.func.now(), server_default=sa.func.now(), index=True)

    def to_dict(self) -> Dict[str, Union[str, None]]:
        return {c.name: getattr(self, c.name, None) for c in self.Meta.columns}

    @classmethod
    async def create(cls, **kwargs: Any) -> Any:
        return await cls.objects.create(**kwargs)

    @classmethod
    async def first(cls) -> Any:
        try:
            return await cls.objects.first()
        except orm.NoMatch:
            return None

    @classmethod
    async def get(cls, *args: Any, **kwargs: Any) -> Optional["Base"]:
        if args:
            kwargs.update(id=args[0])
        res = await cls.objects.filter(**kwargs).limit(limit_count=1).all()
        return res[0] if res else None

    @classmethod
    async def get_by(cls, **kwargs: Any) -> Optional["Base"]:
        return await cls.get(**kwargs)

    @classmethod
    async def get_all(cls, **kwargs: Any) -> List["Base"]:
        res = await cls.objects.filter(**kwargs).all()
        return res

    @classmethod
    async def exists(cls, **kwargs: Any) -> bool:
        return await cls.objects.filter(kwargs).exists()


async def create_table() -> None:
    async with engine.begin() as tx:
        await tx.run_sync(metadata.create_all)


async def drop_table() -> None:
    async with engine.begin() as tx:
        await tx.run_sync(metadata.drop_all)
