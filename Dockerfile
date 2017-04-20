FROM centos:7
MAINTAINER Eric Zhang <eric.pucker@gmail.com>
ENV REFRESHED_AT 2017-04-20 11AM

# 安装python环境
# 下载源码并解压
RUN wget https://www.python.org/ftp/python/2.7.13/Python-2.7.13.tgz && tar -xvf Python-2.7.13.tgz
# 新建python2.7.13文件夹（作为python的安装路径，以免覆盖老的版本，新旧版本可以共存的)
RUN cd Python-2.7.13 && \
    mkdir /usr/local/python2.7.13
# 安装依赖
RUN yum -y update && \
    yum -y install openssl openssl-devel zlib-devel gcc && \
    ./configure --prefix=/usr/local/python2.7.13 && \
    make && make install
# 修改老版本路径
RUN mv /usr/bin/python /usr/bin/python2.7.5
# 建立新版本python的软链接
RUN ln -s /usr/local/python2.7.13/bin/python2.7 /usr/bin/python
# 安装pip
RUN yum -y install epel-release; yum clean all
RUN yum -y install python-pip; yum clean all

# 创建代码目录
RUN mkdir -p /data/ota.creole && \
    adduser deploy
RUN mkdir -p /data/.virtualenv && \
    chown -R deploy:deploy /data/.virtualenv

# 复制代码
ADD . /data/ota.creole
RUN chown -R deploy:deploy /data/ota.creole

# 切换用户, 创建虚拟环境
USER deploy
RUN cd /data/.virtualenv && \
    virtualenv ota.creole

# 安装依赖包
WORKDIR /data/ota.creole
RUN /data/.virtualenv/ota.creole/bin/pip install -r requirements_dev.txt -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com
RUN /data/.virtualenv/ota.creole/bin/pip install -e .

# 运行app
CMD /data/.virtualenv/ota.creole/bin/creole serve
