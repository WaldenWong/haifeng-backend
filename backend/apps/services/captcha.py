import random
import uuid
from typing import Tuple

from backend.apps.core.cache import RedisCache
from backend.apps.core.errors import (
    CaptchaVerifyFailed,
    CaptchaWasExpired,
    UserPhoneHasSentTooManyTimes,
)
from backend.apps.core.sms import SMSService
from backend.apps.schemas.request import CaptchaRequest
from backend.apps.settings import settings
from backend.apps.utils.misc import get_captcha


class CaptchaService:
    @classmethod
    async def generate_image_captcha(cls, expire: int = 30) -> Tuple[bytes, str]:
        captcha, base64_data = get_captcha()
        challenge = str(uuid.uuid4())
        await RedisCache.set(f"backend:captcha:{challenge}", captcha.lower(), ex=expire)
        return base64_data, challenge

    @classmethod
    async def verify_image_captcha(cls, request: CaptchaRequest) -> bool:
        # 图形验证码验证一次就失败
        answer = ""
        res = await RedisCache.get(f"backend:captcha:{request.challenge}")
        if not res:
            if not settings.DEBUG:
                raise CaptchaWasExpired
        else:
            answer = res.decode()

        await RedisCache.delete(f"backend:captcha:{request.challenge}")

        if request.answer.lower() != answer.lower():
            if not settings.DEBUG:
                raise CaptchaVerifyFailed

        return True

    @classmethod
    async def generate_phone_captcha(cls, phone: str, expire: int = 300) -> str:
        await RedisCache.set(f"backend:captcha:lock:phone:{phone}", 1, ex=3600 * 24, nx=True)
        if await RedisCache.incr(f"backend:captcha:lock:phone:{phone}") >= 10:
            raise UserPhoneHasSentTooManyTimes  # pragma: no cover

        captcha = random.randint(100000, 999999)
        challenge = str(uuid.uuid4())
        await RedisCache.set(f"backend:captcha:phone:{phone}:{challenge}", str(captcha), ex=expire)
        await SMSService.send(phone, str(captcha))
        return challenge

    @classmethod
    async def verify_phone_captcha(cls, request: CaptchaRequest, phone: str) -> bool:
        # 短信验证码验证成功后失败
        challenge = await RedisCache.get(f"backend:captcha:phone:{phone}:{request.challenge}")
        if not challenge:
            raise CaptchaWasExpired  # pragma: no cover
        else:
            answer = challenge.decode()

        if request.answer != answer:
            raise CaptchaVerifyFailed
        await RedisCache.delete(f"backend:captcha:phone:{phone}:{request.challenge}")
        return True
