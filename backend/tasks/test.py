#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
https://blog.csdn.net/weixin_44799217/article/details/111666885

"""
import asyncio

from backend.tasks import celery_app

# from datetime import datetime, timedelta
#
# from celery.schedules import crontab


# @background_job(job_name='定时任务', job_schedule=timedelta(seconds=1), job_args=('123', '12312'))
# async def timing_task(a, b):
#     await asyncio.sleep(0.2)
#     return "timing run success"


# @background_job(job_name='后台任务')
@celery_app.task(name="background_task")
async def background_task(a, b):
    await asyncio.sleep(0.2)
    return "background run success"


celery_app.send_task("background_task", args=("13888888888", "hello"))
# background_task.apply_async(args=('13888888888', 'hello'), countdown=5)
"""
task_id：为任务分配唯一id，默认是uuid
countdown：设置该任务等待一段时间在执行，单位为秒
eta：定义任务的开始时间，eta=time.time()+5，单位为秒，是UTC时间，设置成国内时间也没有用, 可以理解成延时启动
expires：设置任务过期时间，任务在过期时间后还没有执行则被丢弃，单位为秒
retry：如果任务失败后，是否重试，默认为True
shadow：重新指定任务的名字，覆盖其在日志中使用的任务名称
retry_policy:{}重试策略，m
"""
