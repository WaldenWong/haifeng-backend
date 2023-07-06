#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import functools
from typing import Any, Optional, Tuple, Type, Union

from fastapi import Depends, HTTPException, params
from typing_extensions import Literal

from backend.apps.auth.system_privileges import Role

__all__ = [
    "Allow",
    "Deny",
    "Everyone",
    "Authenticated",
    "has_permission",
    "AuthPermissionDenied",
    "configure_permissions",
    "permission_dependency_factory",
]
# constants

Allow = "Allow"  # acl "allow" action
Deny = "Deny"  # acl "deny" action

Everyone = "system:everyone"  # user principal for everyone
Authenticated = "system:authenticated"  # authenticated user principal


# the exception that will be raised, if no sufficient permissions are found
# can be configured in the configure_permissions() function


class AuthPermissionDenied(Exception):
    code = 403
    message = "当前用户操作权限不足"


DEFAULT_PERMISSION_EXCEPTION = AuthPermissionDenied


def configure_permissions(
    active_principals_func: Any,
    permission_exception: Type[AuthPermissionDenied] = DEFAULT_PERMISSION_EXCEPTION,
    method: Union[Literal["all"], Literal["any"]] = "all",
) -> functools.partial:
    """sets the basic configuration for the permissions system
    active_principals_func:
        a dependency that returns the principals of the current active user
    permission_exception:
        the exception used if a permission is denied
    returns: permission_dependency_factory function,
             with some parameters already provisioned
    """
    active_principals_func = Depends(active_principals_func)

    return functools.partial(
        permission_dependency_factory,
        active_principals_func=active_principals_func,
        permission_exception=permission_exception,
        method=method,
    )


def permission_dependency_factory(
    permission: Any,
    resource: Any,
    active_principals_func: Any,
    permission_exception: HTTPException,
    method: str,
) -> params.Depends:
    """returns a function that acts as a dependable for checking permissions
    This is the actual function used for creating the permission dependency,
    with the help of fucntools.partial in the "configure_permissions()"
    function.
    permission:
        the permission to check
    resource:
        the resource that will be accessed
    active_principals_func (provisioned  by configure_permissions):
        a dependency that returns the principals of the current active user
    permission_exception (provisioned  by configure_permissions):
        exception if permission is denied
    returns: dependency function for "Depends()"
    """

    dependable_resource = Depends(resource)

    # to get the caller signature right, we need to add only the resource and
    # user dependable in the definition
    # the permission itself is available through the outer function scope
    def permission_dependency(
        resource: params.Depends = dependable_resource, principals: Any = active_principals_func
    ) -> Optional[params.Depends]:
        if isinstance(permission, list):
            if method == "all":
                for p in permission:
                    if not has_permission(principals, p, resource):
                        raise permission_exception
            elif method == "any":
                for p in permission:
                    if has_permission(principals, p, resource):
                        return resource
                raise permission_exception
        else:
            if has_permission(principals, permission, resource):
                return resource
            raise permission_exception
        return None

    return Depends(permission_dependency)


def has_permission(user_principals: list, requested_permission: str, resource: Any) -> bool:
    """checks if a user has the permission for a resource
    The order of the function parameters can be remembered like "Joe eat apple"
    user_principals: the principals of a user
    requested_permission: the permission that should be checked
    resource: the object the user wants to access, must provide an ACL
    returns bool: permission granted or denied
    """
    if Role.SYSTEM_ADMIN in user_principals:
        return True
    acl = normalize_acl(resource)
    if requested_permission in user_principals:
        return True

    for action, principal, permissions in acl:
        if isinstance(permissions, str):
            permissions = {permissions}
        if requested_permission in permissions:
            if principal in user_principals:
                return action == Allow
    return False


# utility functions


def normalize_acl(resource: Any) -> Union[Tuple, Any]:
    """returns the access control list for a resource
    If the resource is not an acl list itself it needs to have an "__acl__"
    attribute. If the "__acl__" attribute is a callable, it will be called and
    the result of the call returned.
    An existing __acl__ attribute takes precedence before checking if it is an
    iterable.
    """
    acl = getattr(resource, "acl", None)
    if isinstance(acl, property):
        acl = getattr(resource(), "acl", None)
    return acl if acl is not None else []
