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

    # 用户管理
    USER = "user:{user_id}"

    # 销售记录
    SALE_VIEW = "sale:view"
    SALE_OPERATE = "sale:operate"

    # 商品信息
    GOODS_VIEW = "goods:view"
    GOODS_OPERATE = "goods:operate"

    # 销售商家
    BUSINESS_VIEW = "business:view"
    BUSINESS_OPERATE = "business:operate"

    # 供应商
    SUPPLIER_VIEW = "supplier:view"
    SUPPLIER_OPERATE = "supplier:operate"

    # 后台任务
    JOB_VIEW = "job:view"
    JOB_OPERATE = "job:operate"


ROLE_RELATIONS: Dict[Role, dict] = {
    Role.GOODS_VIEW: {Role.GOODS_OPERATE: {}},
    Role.SALE_VIEW: {Role.SALE_OPERATE: {}},
    Role.BUSINESS_VIEW: {Role.BUSINESS_OPERATE: {}},
    Role.SUPPLIER_VIEW: {Role.SUPPLIER_OPERATE: {}},
}

ROLE_DESCRIPTIONS: Dict[Role, dict] = {
    Role.SYSTEM_ADMIN: {"alias": "系统管理员", "description": "拥有系统所有权限"},
    Role.GOODS_VIEW: {"alias": "商品查询", "description": "查看商品信息"},
    Role.GOODS_OPERATE: {"alias": "商品管理", "description": "允许操作商品信息"},
    Role.SALE_VIEW: {"alias": "销售信息查询", "description": "查看销售信息"},
    Role.SALE_OPERATE: {"alias": "销售信息管理", "description": "允许操作销售信息"},
    Role.BUSINESS_VIEW: {"alias": "销售商家查询", "description": "查看销售商家信息"},
    Role.BUSINESS_OPERATE: {"alias": "销售商家管理", "description": "允许操作销售商家信息"},
    Role.SUPPLIER_VIEW: {"alias": "供应商信息查询", "description": "查看供应商信息"},
    Role.SUPPLIER_OPERATE: {"alias": "供应商信息管理", "description": "允许操作供应商信息"},
    Role.JOB_VIEW: {"alias": "后台任务", "description": "查看系统所有后台任务"},
    Role.JOB_OPERATE: {"alias": "后台任务管理", "description": "允许用户操作自己创建的后台任务"},
}

SHOW = {
    "sale": Show(
        name="sale",
        alias="销售记录",
        optional_roles=[Role.SALE_OPERATE],  # 可选
        required_roles=[],  # 必选（默认选择）
        description="销售记录",
        required=True,
    ),
    "goods": Show(
        name="goods",
        alias="商品信息",
        optional_roles=[Role.SALE_VIEW],
        required_roles=[],
        description="商品信息",
        required=False,
    ),
    "business": Show(
        name="business",
        alias="销售商家",
        optional_roles=[Role.BUSINESS_VIEW],
        required_roles=[],
        description="销售商家",
        required=False,
    ),
    "supplier": Show(
        name="supplier",
        alias="供应商",
        optional_roles=[Role.SUPPLIER_VIEW],
        required_roles=[],
        description="供应商",
        required=False,
    ),
    "settings": Show(
        name="settings",
        alias="系统设置",
        optional_roles=[Role.JOB_VIEW],
        required_roles=[],
        description="向用户展示系统设置界面",
        required=False,
    ),
}
