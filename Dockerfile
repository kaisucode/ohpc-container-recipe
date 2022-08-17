# OpenHPC container
# 
# Sample workflow:
# $ hpccm.py --recipe recipes/ohpc.py > Dockerfile
# $ docker build -t ohpc-recipe -f Dockerfile .
# $ nvidia-docker run --rm -ti gromacs.eb bash -l
# 

FROM quay.io/ohpc/ohpc-gnu9

RUN sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-* && \
    sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-*

RUN yum update -y && \
    rm -rf /var/cache/yum/*

RUN yum install -y epel-release && \
    yum install -y dnf-utils && \
    yum-config-manager --set-enabled powertools && \
    yum install -y \
        make gcc wget openssl-devel bzip2-devel libffi-devel && \
    rm -rf /var/cache/yum/*

RUN cd /tmp/ && \
    wget https://www.python.org/ftp/python/3.7.9/Python-3.7.9.tgz && \
    tar xzf Python-3.7.9.tgz && \
    cd Python-3.7.9 && \
    ./configure --enable-optimizations && \
    make altinstall && \
    ln -sfn /usr/local/bin/python3.7 /usr/bin/python3.7 && \
    ln -sfn /usr/local/bin/pip3.7 /usr/bin/pip3.7

# pip
RUN yum install -y \
        python3-pip && \
    rm -rf /var/cache/yum/*
RUN pip3.7 --no-cache-dir install keras==2.6.0 tensorflow==2.6.0 protobuf==3.20.*


