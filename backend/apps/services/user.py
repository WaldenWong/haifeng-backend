#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

import asyncpg

from backend.apps.auth import Role
from backend.apps.models import db
from backend.apps.models.user import User as UserORM
from backend.apps.models.user_role import UserRole as UserRoleORM
from backend.apps.services.auth import PasswordContext
from backend.apps.settings import settings
from backend.apps.utils.misc import generate_password


class UserService:
    logger = logging.getLogger("UserService")

    @classmethod
    async def init_admin(cls) -> None:
        """启动服务时如果系统内没有用户则生成一个"""
        async with db.transaction():
            exists_user = await UserORM.get_by()
            if exists_user is None:
                try:
                    password = "admin1234" if settings.DEBUG else generate_password()
                    user = await UserORM.create(
                        username="admin",
                        email="backend@test.com",
                        phone="11111111111",
                        realname="系统管理员",
                        password=PasswordContext.hash(password),
                        group=0,
                    )
                    await UserRoleORM.create(role=Role.SYSTEM_ADMIN, user_id=user.id)
                    logging.info("初始化管理员账号成功")
                    logging.info(f"username:{user.username}")
                    logging.info(f"password:{password}")
                except asyncpg.exceptions.UniqueViolationError:
                    pass

    # @classmethod
    # async def list(cls, request: UserPageListRequest) -> PageListResponse:
    #     CreatorORM = UserORM.alias()  # noqa
    #     clauses = []
    #     clauses += generate_orm_clauses(
    #         {
    #             "username": UserORM.username,
    #             "realname": UserORM.realname,
    #             "phone_number": UserORM.phone_number,
    #             "user_group_name": UserGroupORM.name,
    #             "creator_name": CreatorORM.realname,
    #             "created_on": UserORM.created_on,
    #             "stopped_on": UserORM.stopped_on,
    #             "activated": UserORM.activated,
    #         },
    #         request,
    #     )
    #
    #     # 用户类型归档，如果没有添加条件筛选时
    #     user_type_filed = case(
    #         [
    #             (
    #                 # 由于是一对多进行查找，所以要筛选出结果存在group:admin或system:admin的用户
    #                 exists().where(
    #                     and_(
    #                         UserRoleORM.user_id == UserORM.id,
    #                         UserRoleORM.role == Role.SYSTEM_ADMIN,
    #                     )
    #                 ),
    #                 "system:admin",
    #             ),
    #             (
    #                 exists().where(
    #                     and_(
    #                         UserRoleORM.user_id == UserORM.id,
    #                         UserRoleORM.role == Role.ROLE_OPERATE,
    #                     )
    #                 ),
    #                 "role:operate",
    #             ),
    #             (
    #                 exists().where(
    #                     and_(
    #                         UserRoleORM.user_id == UserORM.id,
    #                         UserRoleORM.role == Role.GROUP_ADMIN,
    #                     )
    #                 ),
    #                 "group:admin",
    #             ),
    #         ],
    #         else_="user",
    #     )
    #     select_from = UserORM.join(CreatorORM, UserORM.creator == CreatorORM.id, isouter=True)
    #     select_from = select_from.join(UserGroupORM, UserORM.user_groups.any(UserGroupORM.id), isouter=True)
    #     select_from = select_from.join(UserBalanceORM, UserBalanceORM.user_id == UserORM.id, isouter=True)
    #     select_from = select_from.join(PoliceUnitORM, PoliceUnitORM.id == UserORM.unit_id, isouter=True)
    #     if request.user_type:
    #         # 使用sql的case后，将结果进行筛选
    #         clauses += generate_orm_clauses(user_type_filed, filters=request.user_type)
    #
    #     if request.user_group_id:
    #         clauses.append(UserORM.user_groups.contains([request.user_group_id]))
    #
    #     query = (
    #         db.select(
    #             [
    #                 UserORM.id,
    #                 UserORM.username,
    #                 UserORM.realname,
    #                 UserORM.phone_number,
    #                 UserORM.activated,
    #                 UserORM.avatar,
    #                 UserORM.user_groups,
    #                 UserORM.province,
    #                 UserORM.city,
    #                 UserORM.district,
    #                 UserORM.created_on,
    #                 UserORM.stopped_on,
    #                 CreatorORM.realname.label("creator"),
    #                 CreatorORM.id.label("creator_id"),
    #                 CreatorORM.username.label("creator_name"),
    #                 UserGroupORM.name.label("user_group"),
    #                 user_type_filed.label("user_type"),
    #                 UserBalanceORM.analyze_limit.label("analyze_balance"),
    #                 UserBalanceORM.analyze_used.label("analyze_used"),
    #                 UserBalanceORM.case_limit.label("case_balance"),
    #                 UserBalanceORM.case_used.label("case_used"),
    #                 PoliceUnitORM.id.label("unit_id"),
    #                 PoliceUnitORM.name.label("unit_name"),
    #             ]
    #         )
    #         .select_from(select_from)
    #         .where(and_(*clauses))
    #     )
    #     order_by = (
    #         getattr(UserORM, request.sort_k).desc()
    #         if request.sort == OrderBy.DESC
    #         else getattr(UserORM, request.sort_k).asc()
    #     )
    #     # 更新列表中试用过期用户的启用状态
    #     await UserORM.update.where(UserORM.stopped_on.cast(db.Date) < datetime.now().date()).values(
    #         activated=False
    #     ).gino.status()
    #
    #     return await paginate(
    #         page=request.page,
    #         page_size=request.page_size,
    #         schema=UserListResponse,
    #         query=query,
    #         order_by=order_by,
    #     )
    #
    # @classmethod
    # async def add(cls, user_create_in: UserCreateInput, creator_id: int) -> int:
    #     exists_user = await UserORM.get_by(username=user_create_in.username)
    #     if exists_user is not None:
    #         raise UserNameExisted
    #
    #     # 组是否存在
    #     user_group = await UserGroupORM.get(user_create_in.user_group)
    #     if not user_group:
    #         raise UserGroupNotExist
    #
    #     if (user_group.analyze_balance is not None and user_create_in.analyze_balance > user_group.analyze_balance) or (
    #         user_group.case_balance is not None and user_create_in.case_balance > user_group.case_balance
    #     ):
    #         raise BalanceLimitOutGroupRange
    #
    #     if user_create_in.phone_number and await UserORM.get_by(phone_number=user_create_in.phone_number):
    #         raise UserPhoneExisted
    #
    #     user_kws = dict(
    #         creator=creator_id,
    #         realname=user_create_in.realname,
    #         email=user_create_in.email,
    #         phone_number=user_create_in.phone_number,
    #         province=user_create_in.province,
    #         city=user_create_in.city,
    #         district=user_create_in.district,
    #         user_groups=[user_create_in.user_group],
    #         unit_id=user_create_in.unit_id,
    #         username=user_create_in.username,
    #         password=PasswordContext.hash(user_create_in.password),
    #         stopped_on=user_create_in.stopped_on,
    #     )
    #
    #     # 创建用户
    #     user = await UserORM.create(**user_kws)
    #
    #     role_group = await RoleGroupORM.get(user_group.role_groups[0])
    #
    #     # 创建用户权限
    #     role_create_kws = []
    #     for show, roles in user_create_in.shows.items():
    #         if not roles:
    #             # 仅有界面，没有权限
    #             if show in role_group.config:
    #                 role_kw = dict(
    #                     role=None,
    #                     user_id=user.id,
    #                     user_group_id=user_create_in.user_group,
    #                     show=show,
    #                     creator=creator_id,
    #                 )
    #                 role_create_kws.append(role_kw)
    #             else:
    #                 await user.delete()
    #                 raise RoleNotInRoleGroup
    #         else:
    #             roles = more_roles(roles)
    #             role_group_roles = more_roles(role_group.config[show])
    #             for role in roles:
    #                 # 检验 show roles是否与权限组相符
    #                 if show in role_group.config and role in role_group_roles:
    #                     role_kw = dict(
    #                         role=role,
    #                         user_id=user.id,
    #                         user_group_id=user_create_in.user_group,
    #                         show=show,
    #                         creator=creator_id,
    #                     )
    #                     role_create_kws.append(role_kw)
    #                 else:
    #                     await user.delete()
    #                     raise RoleNotInRoleGroup
    #
    #     # 检测成功后统一创建
    #     [await UserRoleORM.create(**kw) for kw in role_create_kws]
    #     # 创建消费额度记录
    #     await AnalyzeBalanceService.new_balance(user_id=user.id, analyze_limit=user_create_in.analyze_balance)
    #     await CaseBalanceService.new_balance(user_id=user.id, case_limit=user_create_in.case_balance)
    #     return user.id
    #
    # @classmethod
    # async def update(cls, user_update_in: UserUpdateIn, target_user: UserORM, updater: UserORM) -> None:
    #     # 暂时不允许用户换组
    #     if target_user.user_groups and user_update_in.user_group != target_user.user_groups[0]:
    #         raise ChangeUserGroupDenied
    #
    #     # 组是否存在
    #     user_group = await UserGroupORM.get(user_update_in.user_group)
    #
    #     if user_group.analyze_balance and user_update_in.analyze_balance > user_group.analyze_balance:
    #         raise BalanceLimitOutGroupRange
    #
    #     update_kw: Dict[str, Any] = dict(user_groups=[user_update_in.user_group], stopped_on=user_update_in.stopped_on)
    #
    #     if user_update_in.email is not None:
    #         update_kw["email"] = user_update_in.email
    #     if user_update_in.phone_number is not None and target_user.phone_number != user_update_in.phone_number:
    #         if await UserORM.get_by(phone_number=user_update_in.phone_number):
    #             raise UserPhoneExisted
    #         update_kw["phone_number"] = user_update_in.phone_number
    #     if user_update_in.province is not None:
    #         update_kw["province"] = user_update_in.province
    #         if user_update_in.city is None:
    #             update_kw["city"] = None
    #         if user_update_in.district is None:
    #             update_kw["district"] = None
    #     if user_update_in.city is not None:
    #         update_kw["city"] = user_update_in.city
    #     if user_update_in.district is not None:
    #         update_kw["district"] = user_update_in.district
    #     if user_update_in.unit_id is not None:
    #         update_kw["unit_id"] = user_update_in.unit_id
    #     if user_update_in.password is not None:
    #         update_kw["password"] = PasswordContext.hash(user_update_in.password)
    #     if user_update_in.realname is not None:
    #         update_kw["realname"] = user_update_in.realname
    #
    #     role_create_kws = []
    #
    #     role_group = await RoleGroupORM.get(user_group.role_groups[0])
    #     for show, roles in user_update_in.shows.items():
    #         if not roles:
    #             if show in role_group.config:
    #                 role_create_kws.append(
    #                     dict(
    #                         role=None,
    #                         user_id=target_user.id,
    #                         user_group_id=user_update_in.user_group,
    #                         show=show,
    #                         creator=updater.id,
    #                     )
    #                 )
    #             else:
    #                 raise RoleNotInRoleGroup
    #         for role in more_roles(roles):
    #             # 检查权限是否在权限范围内
    #             if show in role_group.config and role in more_roles(role_group.config[show]):
    #                 role_create_kws.append(
    #                     dict(
    #                         role=role,
    #                         user_id=target_user.id,
    #                         user_group_id=user_update_in.user_group,
    #                         show=show,
    #                         creator=updater.id,
    #                     )
    #                 )
    #             else:
    #                 raise RoleNotInRoleGroup
    #     # 更新
    #     await target_user.update(**update_kw).apply()
    #     await AnalyzeBalanceService.new_balance(user_id=target_user.id, analyze_limit=user_update_in.analyze_balance)
    #     await CaseBalanceService.new_balance(user_id=target_user.id, case_limit=user_update_in.case_balance)
    #
    #     # 删除之前的权限
    #     await UserRoleORM.delete.where(
    #         and_(
    #             UserRoleORM.user_id == target_user.id,
    #             UserRoleORM.user_group_id == user_update_in.user_group,
    #         )
    #     ).gino.status()
    #     # 检测成功后统一创建新的用户权限
    #     [await UserRoleORM.create(**kw) for kw in role_create_kws]
    #
    # @classmethod
    # async def profile(cls, user: UserORM, parse: bool = False) -> UserProfile:
    #     result: Dict[str, Any] = dict(**user.to_dict())
    #     await AnalyzeBalanceService.get_user_balance(user.id)
    #     await CaseBalanceService.get_user_balance(user.id)
    #
    #     columns = [
    #         UserBalanceORM.user_id,
    #         UserBalanceORM.analyze_limit.label("analyze_balance"),
    #         UserBalanceORM.analyze_used,
    #         UserBalanceORM.case_limit.label("case_balance"),
    #         UserBalanceORM.case_used,
    #         PoliceUnitORM.id.label("unit_id"),
    #         PoliceUnitORM.name.label("unit_name"),
    #         PoliceUnitORM.province,
    #         PoliceUnitORM.city,
    #         PoliceUnitORM.district,
    #         PoliceUnitORM.longitude,
    #         PoliceUnitORM.latitude,
    #     ]
    #     group_by = [
    #         UserBalanceORM.id,
    #         UserBalanceORM.user_id,
    #         UserBalanceORM.created_on,
    #         PoliceUnitORM.id,
    #     ]
    #     clauses = [UserRoleORM.user_id == user.id]
    #     select_from = UserRoleORM.join(UserBalanceORM, UserBalanceORM.user_id == user.id, full=True)
    #     select_from = select_from.join(PoliceUnitORM, PoliceUnitORM.id == user.unit_id, isouter=True)
    #     # 查询分组
    #     user_group_id = user.user_groups[0] if user.user_groups else None
    #     if user_group_id:
    #         select_from = select_from.join(UserGroupORM, UserGroupORM.id == user_group_id, full=True)
    #         columns += [UserGroupORM.id.label("user_group_id"), UserGroupORM.name.label("user_group_name")]
    #         group_by += [UserGroupORM.id, UserGroupORM.name]
    #
    #     if not parse:
    #         columns += [
    #             db.func.array_agg(db.func.distinct(UserRoleORM.role)).label("roles_"),
    #             db.func.array_agg(
    #                 db.func.distinct(db.case([(UserRoleORM.role.is_(None), None)], else_=UserRoleORM.show))
    #             ).label("shows_"),
    #         ]
    #         user_profile = (
    #             await db.select(columns).select_from(select_from).where(and_(*clauses)).group_by(*group_by).gino.first()
    #         )
    #
    #         if not user_profile:
    #             return UserProfile(**result)
    #
    #         if Role.SYSTEM_ADMIN.value in user_profile.roles_:
    #             shows = list(SHOW.keys())
    #             roles = list(ROLE_DESCRIPTIONS.keys())
    #         else:
    #             shows = [_ for _ in user_profile.shows_ if _ is not None] + [
    #                 _ for _ in SHOW.keys() if SHOW[_]["required"]
    #             ]
    #             roles = [_ for _ in user_profile.roles_ if _ is not None]
    #         result.update(dict(shows=list(set(shows)), roles=list(set(roles)), **user_profile))  #
    #     else:
    #         columns += [UserRoleORM.role.label("roles_"), UserRoleORM.show.label("shows_")]
    #         clauses += [
    #             or_(
    #                 UserRoleORM.role.isnot(None),
    #                 and_(UserRoleORM.role.is_(None), UserRoleORM.show != "centre"),
    #             )
    #         ]
    #         group_by += [UserRoleORM.role, UserRoleORM.show]
    #         user_profile = (
    #             await db.select(columns).select_from(select_from).where(and_(*clauses)).group_by(*group_by).gino.all()
    #         )
    #         if not user_profile:
    #             return UserProfile(**result)
    #         # 返回{"clue":["task:operate", "task:view"]}这种展开型
    #         shows_parsed: Dict[str, Any] = {"others": []}
    #         if Role.SYSTEM_ADMIN.value in [_.roles_ for _ in user_profile]:
    #             shows_parsed["others"] = [Role.SYSTEM_ADMIN]
    #             shows_dict = roles_to_shows(list(ROLE_DESCRIPTIONS.keys()))
    #             for show in shows_dict.keys():
    #                 shows_parsed[show] = more_roles(shows_dict[show])
    #         else:
    #             for profile in user_profile:
    #                 if profile.shows_ not in shows_parsed:
    #                     shows_parsed[profile.shows_] = []
    #                 if profile.roles_:
    #                     shows_parsed[profile.shows_].append(profile.roles_)
    #             if shows_parsed.get("settings"):
    #                 if "role:operate" in shows_parsed["settings"]:
    #                     shows_parsed["others"] = [Role.ROLE_OPERATE]
    #                 elif "group:admin" in shows_parsed["settings"]:
    #                     shows_parsed["others"] = [Role.GROUP_ADMIN]
    #         result.update(dict(shows_parsed=shows_parsed, **user_profile[0]))
    #     return UserProfile(**result)
    #
    # @classmethod
    # async def card(cls, user_id: int) -> UserCardData:
    #     user = await UserORM.get_by(id=user_id)
    #     if not user.activated:
    #         raise UserWasAlreadyDisabled
    #     select_from = UserORM.join(UserRoleORM, UserRoleORM.user_id == UserORM.id, isouter=True)
    #     select_from = select_from.join(UserGroupORM, UserORM.user_groups.any(UserGroupORM.id), isouter=True)
    #     query = (
    #         db.select(
    #             [
    #                 UserORM.username,
    #                 UserORM.realname,
    #                 UserORM.avatar,
    #                 UserORM.created_on,
    #                 UserORM.province,
    #                 UserORM.city,
    #                 UserGroupORM.name.label("user_group_name"),
    #             ]
    #         )
    #         .select_from(select_from)
    #         .where(UserORM.id == user_id)
    #     )
    #     result = await query.gino.first()
    #     return UserCardData(**result)
    #
    # @classmethod
    # async def prepare(cls, request: UserCreatePrepareRequest) -> UserCreatePrepare:
    #     user_group: UserGroupORM = (
    #         await db.select([UserGroupORM, PoliceUnitORM.name.label("unit_name")])
    #         .where(UserGroupORM.id == request.user_group_id)
    #         .select_from(UserGroupORM.join(PoliceUnitORM, PoliceUnitORM.id == UserGroupORM.unit_id, isouter=True))
    #         .gino.first()
    #     )
    #
    #     if not user_group:
    #         raise UserGroupNotExist
    #
    #     role_group: RoleGroupORM = await RoleGroupORM.get(user_group.role_groups[0])
    #     if not role_group:
    #         raise RoleGroupNotExist
    #
    #     # 把格式从 role_group.config 转到 item/shows
    #     role_group_shows = []
    #     for show_name, roles in role_group.config.items():
    #         show: Dict[str, Any] = dict(SHOW[show_name])
    #         show["optional_roles"] = {k: v for k, v in roles.items() if k in show["optional_roles"]}
    #         show["required_roles"] = {k: v for k, v in roles.items() if k in show["required_roles"]}
    #         show["name"] = show_name
    #         role_group_shows.append(show)
    #
    #     prepare = UserCreatePrepare(
    #         role_group_shows=role_group_shows,
    #         user_group_province=user_group.province,
    #         user_group_city=user_group.city,
    #         role_group_name=role_group.name,
    #         user_group_district=user_group.district,
    #         analyze_balance=user_group.analyze_balance,
    #         case_balance=user_group.case_balance,
    #         unit_id=user_group.unit_id,
    #         unit_name=user_group.unit_name,
    #     )
    #
    #     if request.user_id is not None:
    #         if not await UserORM.get(request.user_id):
    #             raise UserNameNotFound
    #         user_role_shows: Dict[str, Any] = {}
    #         user_roles = await UserRoleORM.get_all(user_id=request.user_id, user_group_id=request.user_group_id)
    #         relations = more_roles(ROLE_RELATIONS)
    #         for user_role in user_roles:
    #             if user_role.show not in user_role_shows:
    #                 user_role_shows[user_role.show] = {"relation_roles": []}
    #             if not user_role.role:
    #                 pass
    #             elif user_role.role not in relations:
    #                 user_role_shows[user_role.show][user_role.role] = dict()  # noqa
    #             else:
    #                 user_role_shows[user_role.show]["relation_roles"].append(user_role.role)
    #         for k, v in user_role_shows.items():
    #             user_role_shows[k].update(matched_roles(v["relation_roles"]))
    #             user_role_shows[k].pop("relation_roles")
    #         prepare.user_role_shows = user_role_shows
    #     return prepare
    #
    # @classmethod
    # async def get_role_user(cls, role: Role, keyword: Optional[str], is_admin: bool) -> List[RoleUser]:
    #     """获取权限用户"""
    #     clauses_roles = [role]
    #     if is_admin:
    #         clauses_roles += [Role.SYSTEM_ADMIN]
    #     clauses = [UserRoleORM.role.in_(clauses_roles), UserORM.activated.is_(True)]
    #     if keyword:
    #         keyword = keyword.replace("%", "\\%").replace("_", "\\_")
    #         if keyword.isdigit():
    #             clauses += [UserORM.phone_number.like(f"%{keyword}%")]
    #         else:
    #             clauses += [UserORM.realname.like(f"%{keyword}%")]
    #
    #     select_from = UserORM.join(UserRoleORM, UserRoleORM.user_id == UserORM.id)
    #     result = (
    #         await db.select(
    #             [db.func.distinct(UserORM.id).label("id"), UserORM.realname.label("name"), UserORM.phone_number]
    #         )
    #         .select_from(select_from)
    #         .where(db.and_(*clauses))
    #         .order_by(UserORM.realname)
    #         .gino.all()
    #     )
    #     return [RoleUser(**_) for _ in result]
