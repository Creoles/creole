FROM python:2.7
MAINTAINER Eric Zhang <eric.pucker@gmail.com>
# 更新yum
# RUN yum -y upgrade
# RUN yum -y install epel-release
# 创建代码目录
RUN mkdir -p /data/ota.creole && \
    adduser deploy && \
    chown -R deploy:deploy /data/ota.creole
USER deploy
ADD . /data/ota.creole
WORKDIR /data/ota.creole
RUN pip install -r requirements_dev.txt
RUN pip install -e .
CMD creole serve
