#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

from fastapi import Request
from user_agents import parse

from backend.apps.models.login_log import LoginLog as LoginLogORM
from backend.apps.services.ip_location import IpLocationApi


class LoginLogService:
    logger = logging.getLogger("LoginLogService")

    @classmethod
    async def new(cls, request: Request, user_id: int) -> None:
        try:
            source_ip = request.client.host if request.client else None
            source_port = request.client.port if request.client else None
            headers = dict(request.headers)
            ua = parse(headers.get("user-agent"))
            browser, version, os, device = ua.browser.family, ua.browser.version_string, ua.os.family, ua.device.family

            is_pc = False
            country, province, city = None, None, None

            if device != "Other":
                pc_devices = ["Mac", "PC"]
                for p in pc_devices:
                    if p in device:
                        is_pc = True
                        break
            else:
                if os == "Windows":  # 当 os == Linux时 is_ps = False
                    is_pc = True
            if source_ip and not IpLocationApi.ip_is_private(source_ip):
                ip_location = await IpLocationApi.get_location(source_ip)
                if ip_location:
                    country = ip_location.country
                    province = ip_location.province
                    city = ip_location.city
            await LoginLogORM.create(
                user_id=user_id,
                ip=source_ip,
                port=source_port,
                country=country,
                province=province,
                city=city,
                device=device if device and device != "Other" else None,
                os=os,
                browser=f"{browser} {version}",
                is_pc=is_pc,
                ua=headers.get("user-agent"),
                headers=headers,
            )
        except Exception as exc:
            cls.logger.debug(f"登陆日志记录失败: {repr(exc)}", exc_info=True)
