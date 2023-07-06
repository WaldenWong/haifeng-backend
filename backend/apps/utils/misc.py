#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64
import random
import string
from typing import Tuple

from captcha.image import ImageCaptcha

from backend.apps.settings import settings


def generate_password(length: int = 10) -> str:
    chars = string.ascii_letters + string.digits
    return "".join([random.choice(chars) for _ in range(length)])


def get_captcha() -> Tuple[str, bytes]:
    strings = string.ascii_uppercase + string.digits
    captcha_content = "".join([random.choice(strings) for _ in range(5)])

    if settings.CAPTCHA_FONT_PATHS:  # pragma: no cover
        image = ImageCaptcha(fonts=list(settings.CAPTCHA_FONT_PATHS))
    else:
        image = ImageCaptcha()
    io_data = image.generate(captcha_content)
    bytes_like = io_data.read()
    return captcha_content, base64.b64encode(bytes_like)


def escape_sql_symbols(search_content: str) -> str:
    # 对通配符进行转义
    return search_content.replace("%", "\\%").replace("_", "\\_")
