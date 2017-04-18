FROM python:2.7
MAINTAINER Eric Zhang <eric.pucker@gmail.com>
# 更新yum
# RUN yum -y upgrade
# RUN yum -y install epel-release

# 创建代码目录
RUN mkdir -p /data/ota.creole && \
    adduser deploy
RUN mkdir -p /data/.virtualenv && \
    chown -R deploy:deploy /data/.virtualenv

# 复制代码
ADD . /data/ota.creole
RUN chown -R deploy:deploy /data/ota.creole

# 切换用户, 创创建虚拟环境
USER deploy
RUN cd /data/.virtualenv && \
    virtualenv ota.creole

# 安装依赖包
WORKDIR /data/ota.creole
RUN /data/.virtualenv/ota.creole/bin/pip install -r requirements_dev.txt -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com
RUN /data/.virtualenv/ota.creole/bin/pip install -e .

# 运行app
CMD /data/.virtualenv/ota.creole/bin/creole serve
