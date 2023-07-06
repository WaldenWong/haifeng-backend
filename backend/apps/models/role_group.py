#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from backend.apps.models import Base, BaseMeta, orm, orm_ext, sa


class RoleGroup(Base):
    class Meta(BaseMeta):
        tablename = "role_group"

    name = orm.String(max_length=32, unique=True, index=True)
    shows = orm_ext.ARRAY(item_type=sa.String(32))
    roles = orm_ext.ARRAY(item_type=sa.String(32))
    user_id = orm.BigInteger(index=True)
    config = orm.JSON()
