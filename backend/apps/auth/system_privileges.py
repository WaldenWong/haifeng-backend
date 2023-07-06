from enum import Enum
from typing import Dict

from typing_extensions import TypedDict


class Show(TypedDict):
    name: str  # 英文简称
    alias: str  # 中文名称
    optional_roles: list  # 可选权限
    required_roles: list  # 必选权限
    description: str  # 详细介绍
    required: bool  # 是否为必选界面


class Role(str, Enum):
    # 系统管理员
    SYSTEM_ADMIN = "system:admin"
    # 分组管理员
    GROUP_ADMIN = "group:admin"
    # 系统权限管理员
    ROLE_OPERATE = "role:operate"

    # 用户管理
    USER = "user:{user_id}"
    USER_GROUP_MEMBER = "user:group:{group_id}"

    TEST_MODEL = "test:model"

    # 后台任务
    JOB_VIEW = "job:view"
    JOB_OPERATE = "job:operate"


ROLE_RELATIONS: Dict[Role, dict] = {
    Role.GROUP_ADMIN: {Role.ROLE_OPERATE: {}},
    Role.JOB_VIEW: {Role.JOB_OPERATE: {}},
    Role.TEST_MODEL: {},
}

ROLE_DESCRIPTIONS: Dict[Role, dict] = {
    Role.SYSTEM_ADMIN: {"alias": "系统管理员", "description": "拥有系统所有权限"},
    Role.GROUP_ADMIN: {"alias": "分组管理员", "description": "拥有指定用户组所有权限，可以创建组员并指派组内权限"},
    Role.ROLE_OPERATE: {"alias": "系统权限管理员", "description": "允许操作所有与用户权限相关的功能"},
    Role.JOB_VIEW: {"alias": "后台任务", "description": "查看系统所有后台任务"},
    Role.JOB_OPERATE: {"alias": "后台任务管理", "description": "允许用户操作自己创建的后台任务"},
}

SHOW: Dict[str, Show] = {
    "model": {
        "name": "trend",
        "alias": "模块",
        "optional_roles": [],
        "required_roles": [Role.TEST_MODEL],
        "description": "xxx模块页面",
        "required": True,
    },
    "settings": {
        "name": "settings",
        "alias": "系统设置",
        "optional_roles": [Role.GROUP_ADMIN, Role.JOB_VIEW, Role.TEST_MODEL],
        "required_roles": [],
        "description": "向用户展示系统设置界面",
        "required": False,
    },
}
