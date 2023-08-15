#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""celery 创建与注册任务"""
# TODO 测试后台任务中使用异步方法
# import asyncio
import inspect
from datetime import timedelta
from typing import Tuple, Union

from celery import Celery
from celery.schedules import crontab

# 生成celery应用
celery_app = Celery(
    "taotie",
    broker="amqp://rabbit:rabbit@localhost:5672//",  # 使用rabbitmq作为消息代理
    backend="redis://:redis@localhost:56379",  # 把任务结果存在了Redis
)
# # 加载配置文件
celery_app.conf.update(
    dict(
        celery_timezone="Asia/Shanghai",  # celery使用的时区
        celery_enable_utc=False,  # celery是否使用UTC
        celery_accept_content=["json", "msgpack"],  # 指定接受的内定类型
        celery_task_serailizer="json",  # 指定序列化方式
        celery_result_serailizer="json",  # 指定结果序列化方式, 读取任务结果一般性能要求不高，所以使用了可读性更好的JSON
        celery_task_result_expires=60 * 60 * 24,  # celery任务结果有效期
        celery_log_file="logs/celery.log",  # celery日志存储位置
        broker_connection_retry_on_startup=True,
        # celery_imports=["celery_tasks"],  # 添加任务
    )
)


def background_job(
    job_name: str, job_schedule: Union[crontab, timedelta] = None, job_args: Tuple = tuple, actor: str = None, **kwargs
):
    async def wrapper(func):
        nonlocal actor
        actor = actor or func.__name__

        if not inspect.iscoroutinefunction(func):
            raise ValueError("actor must be a coroutine function")
        # celery_app.task(name=actor)(asyncio.run(func))
        if job_schedule:
            celery_app.conf.beat_schedule = {
                job_name: {
                    "task": actor,
                    "schedule": job_schedule,
                    "args": job_args,
                    "kwargs": kwargs,
                }
            }

        return func

    return wrapper
