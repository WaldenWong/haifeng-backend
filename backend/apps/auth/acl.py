#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Any, List, Union

from backend.apps.auth.system_privileges import Role
from backend.apps.models.user import User as UserORM
from backend.apps.schemas.request import LocationRequest

from . import get_active_roles
from .permission import Allow, has_permission


class BaseOperationACL:
    role_acl = [(Allow, r.value, r.value) for r in Role]  # noqa
    __acl__: List[Any] = []

    @property
    def acl(self) -> List[Any]:
        return self.role_acl + self.__acl__

    @classmethod
    async def all(cls, user: UserORM, *args: Union[Role, str]) -> bool:
        """传入当前用户，操作需要的权限，全部权限满足则返回True"""
        roles = await get_active_roles(user)
        if Role.SYSTEM_ADMIN in roles:
            return True

        for role in args:
            if not has_permission(roles, role, cls):
                return False
        return True

    @classmethod
    async def any(cls, user: UserORM, *args: Any) -> bool:
        """传入当前用户，操作需要的权限，只要满足其中一个则返回True"""
        roles = await get_active_roles(user)
        if Role.SYSTEM_ADMIN in roles:
            return True

        for role in args:
            if has_permission(roles, role, cls):
                return True
        return False

    @classmethod
    async def location(cls, request: LocationRequest, user: UserORM) -> bool:
        roles = await get_active_roles(user)
        if Role.SYSTEM_ADMIN in roles:
            return True
        if not user.province:
            return False
        if user.province == "全国":
            return True
        if user.district:
            # 防止不同省市但相同区县的情况，需要同时比对city和province
            if request.district == user.district and request.city == user.city and request.province == user.province:
                return True
        elif user.city:
            # 防止不同省但相同市的情况，需要同时比对province
            if request.city == user.city and request.province == user.province:
                return True
        else:
            if request.province == user.province:
                return True
        return False
