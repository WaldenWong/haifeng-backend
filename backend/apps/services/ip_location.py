#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import ipaddress
import logging
from typing import Optional

import aiohttp

from backend.apps.schemas.login_log import IPLocation


class IpLocationApi:
    """IP综合查询接口，查询IP地址的归属信息"""

    logger = logging.getLogger("IpLocationApi")

    @classmethod
    def ip_is_private(cls, ip: str) -> bool:
        try:
            if "local" in ip:
                return True
            return ipaddress.IPv4Address(ip).is_private
        except Exception as e:
            cls.logger.error(repr(e), exc_info=True)
        return False

    @classmethod
    async def get_location(cls, ip: str) -> Optional[IPLocation]:
        # TODO aiohttp
        async with aiohttp.ClientSession() as session:
            resp = await session.get(url="")
        return IPLocation(**resp.__dict__)
