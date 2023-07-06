#!/usr/bin/env python3
# -*- coding: utf-8 -*-
class SMSService:
    def __init__(self) -> None:
        ...

    @classmethod
    async def send(cls, phone: str, code: str) -> None:
        ...
