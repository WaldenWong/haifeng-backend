# 海峰
根据FastAPI框架，集成所有后端技术的新框架

## 使用
~~~bash
   # 指定Python版本
   poetry env use <python version>
   # 安装依赖包
   poetry install
   # mac M1、2芯片使用
   arch -x86_64 poetry install
    # 容器启动
   docker run -d \
   --env=POSTGRES_PASSWORD=postgres \
   --env=TZ=Asia/Shangha \
   --volume=/Volumes/Data/tmp/haifeng/postgresql:/bitnami/postgresql \
   -p 35432:5432 \
   --restart=always \
   --name haifeng-postgres \
   bitnami/postgresql:latest
   # 创建数据库
   docker exec -it haifeng-postgres psql -U postgres -c "create database xxx;"
   # 生成数据库迁移文件
   alembic revision --autogenerate -m 'xxx'
   # 创建数据表
   alembic upgrade head
   # uvicorn启动
   python run.py
   # gunicorn 启动
   gunicorn -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 backend.asgi:app
   # 检查、格式化代码
   pre-commit run --all-file
   ~~~
### M1/M2 启动服务的bug
Error loading: /Applications/PyCharm.app/Contents/plugins/python/helpers/pydev/pydevd_attach_to_process/attach_x86_64.dylib
> 解决办法是重新编译相应的动态库为Arm64版本
> ~~~bash
> cd /Applications/PyCharm.app/Contents/plugins/python/helpers/pydev/pydevd_attach_to_process/linux_and_mac
> g++ -fPIC -D_REENTRANT -std=c++11 -arch arm64 -c -o attach_x86_64.o attach.cpp
> g++ -dynamiclib -nostartfiles -arch arm64 -o attach_x86_64.dylib attach_x86_64.o -lc
> rm attach_x86_64.o
> mv attach_x86_64.dylib ../attach_x86_64.dylib
> ~~~
