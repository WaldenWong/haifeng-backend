#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import logging
from copy import deepcopy
from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, Optional, Type, Union

import jwt
from fastapi import Depends, Request, params
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from pydantic import ValidationError

from backend.apps.auth.permission import Authenticated, configure_permissions
from backend.apps.auth.system_privileges import ROLE_RELATIONS, SHOW, Role
from backend.apps.core.errors import (
    UserLoginFailed,
    UserTokenWasExpired,
    UserTokenWasUpdated,
    UserWasAlreadyDisabled,
)
from backend.apps.models import Base
from backend.apps.models.user import User as UserORM
from backend.apps.models.user_role import UserRole as UserRoleORM
from backend.apps.settings import settings

if TYPE_CHECKING:
    from backend.apps.auth.acl import BaseOperationACL

logger = logging.getLogger("Auth")


async def judge_user_activated(user: Union[UserORM, Base]) -> bool:
    if user.activated is False:
        return False
    else:
        if user.stopped_on and user.stopped_on.date() < datetime.now().date():
            await user.update(activated=False).apply()
            return False
    return True


async def verify_login_user(authorization: str) -> UserORM:
    scheme, param = get_authorization_scheme_param(authorization)
    if scheme.lower() != "bearer":
        user = await UserORM.get_by(api_key=authorization)
        token_expire = None
    else:
        try:
            payload = jwt.decode(param, str(settings.SECRET_KEY), algorithms=[settings.TOKEN_ALGORITHM])
            username = payload["sub"]
            if not username:
                raise UserTokenWasExpired
            user = await UserORM.get_by(username=username)
            token_expire = datetime.fromtimestamp(payload["exp"])
        except (jwt.PyJWTError, ValidationError):
            raise UserTokenWasExpired

    if not user:
        raise UserTokenWasExpired
    if not await judge_user_activated(user):
        raise UserWasAlreadyDisabled
    if token_expire:
        if user.expired_at != token_expire:
            raise UserTokenWasUpdated

    return user


class BackendServerOAuth(OAuth2):
    def __init__(
        self,
        token_url: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[dict] = None,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": token_url, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=True)

    async def __call__(self, request: Request) -> Optional[UserORM]:
        authorization: str = request.headers.get("Authorization")
        if not authorization:
            raise UserLoginFailed
        return await verify_login_user(authorization)


def create_access_token(*, data: Dict[str, Any], expire: datetime) -> str:
    to_encode = data.copy()
    to_encode.update({"exp": expire.timestamp()})
    encoded_jwt = jwt.encode(to_encode, str(settings.SECRET_KEY), algorithm=settings.TOKEN_ALGORITHM)
    return encoded_jwt


async def get_current_user(
    user: UserORM = Depends(BackendServerOAuth(token_url=f"/api{settings.TOKEN_URL}")),
) -> UserORM:
    return user


async def get_active_roles(user: UserORM = Depends(get_current_user)) -> list:
    roles = {
        Authenticated,
        f"user:{user.username}",
        Role.USER.value.format(user_id=user.id),
    }
    user_roles = await UserRoleORM.get_all(user_id=user.id)
    roles = roles.union([r.role for r in user_roles])
    logger.debug(f"user:<{user.username}>  roles:<{roles}>")
    return list(roles)


class Permission(params.Depends):
    all = configure_permissions(get_active_roles, method="all")
    any = configure_permissions(get_active_roles, method="any")

    def __new__(cls, resource: str, operation_acl: Type["BaseOperationACL"]) -> "Permission":
        return configure_permissions(get_active_roles, method="all")(resource, operation_acl)


def more_roles(shows: Dict[Role, dict]) -> list:
    """
    递归将字典内权限展开拆分为列表
    例：
    a = {'a':{},'b':{},'c':{'d':{'w':{'e':{},'q':{}}},"t":{'p':{}}}}
    返回 ['a', 'b', 'c', 'd', 't', 'w', 'e', 'q', 'p']
    :param shows:
    :return:
    """
    shows = deepcopy(shows)
    roles = list(shows.keys())
    for v in shows.values():
        if v:
            roles += more_roles(v)
    return roles


def matched_roles(roles: list, relations: Optional[Dict[Role, dict]] = None) -> Dict[Role, dict]:
    relations = deepcopy(ROLE_RELATIONS) if relations is None else relations

    for role in list(relations.keys()):
        value = role.value
        if value in roles:
            roles.remove(value)
        elif set(more_roles(relations[role])) & set(roles):
            pass
        else:
            relations.pop(role)
            continue

        matched_roles(roles, relations[role])
    return relations


def get_relation_roles(roles: list, sub_roles: Dict[Role, dict], parent_role: Optional[str] = None) -> Dict[Role, dict]:
    """
    递归寻找目标权限涉及到的父权限
    sub_roles = {'a':{},'b':{},'c':{'d':{'w':{'e':{},'q':{}}},"t":{'p':{}}}}
    targets = ['p', 'q', 'e']
    返回 {'c': {'d': {'w': {'q': {}, 'e': {}}}, 't': {'p': {}}}}
    :param sub_roles: ROLE_RELATIONS
    :param roles:
    :param parent_role:
    :return:
    """
    results: dict = dict()
    matched: list = list()
    for t in roles:
        if t in sub_roles:
            if not parent_role:
                results[t] = {}
            else:
                if parent_role not in results:
                    results[parent_role] = {t: {}}
                else:
                    results[parent_role][t] = {}
            matched.append(t)
    roles = [t for t in roles if t not in matched]
    if roles:
        for k, v in sub_roles.items():
            if v:
                sub_result = get_relation_roles(roles, v, k)
                if sub_result:
                    if parent_role:
                        if parent_role in results:
                            results[parent_role].update(sub_result)
                        else:
                            results[parent_role] = sub_result
                    else:
                        results.update(sub_result)
    return results


def roles_to_shows(roles: list) -> Dict[str, Any]:
    """
    通过传入的roles，返回一个可以用于创建 role_group/user权限 的shows
    :param roles:
    :return:
    """
    sub_roles = deepcopy(ROLE_RELATIONS)
    relations_roles = more_roles(ROLE_RELATIONS)
    for r in roles:
        if r not in relations_roles:
            sub_roles[r] = {}
    relations = get_relation_roles(roles=roles, sub_roles=sub_roles)
    shows: Dict[str, Any] = dict()
    for show, show_info in SHOW.items():
        for parent_role in relations.keys():
            if isinstance(show_info["optional_roles"], list) and parent_role in (
                show_info["optional_roles"] + show_info["required_roles"]
            ):
                if show in shows:
                    shows[show][parent_role] = relations[parent_role]
                else:
                    shows[show] = {parent_role: relations[parent_role]}
    return shows


def remove_roles(shows: Dict[str, Any], roles: list) -> None:
    for r in roles:
        if r in shows.keys():
            shows.pop(r)
    for k, v in shows.items():
        if v:
            remove_roles(v, roles)
