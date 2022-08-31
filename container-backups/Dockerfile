# OpenHPC container
# 
# Sample workflow:
# $ hpccm.py --recipe recipes/ohpc.py --format docker > Dockerfile
# $ docker build -t ohpc-recipe -f Dockerfile .
# $ docker run -v $PWD/python_scripts/:/mnt/python_scripts/ -it --rm ohpc-recipe python3.7 /mnt/python_scripts/benchmark.py
# 

FROM quay.io/ohpc/ohpc-gnu9

RUN sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-* && \
    sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-* && \
    yum update -y

RUN cd /etc/yum.repos.d/ && \
    sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-* && \
    sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-* && \
    yum update -y

RUN yum update -y && \
    rm -rf /var/cache/yum/*

RUN yum install -y \
        appstream-data \
        wget && \
    rm -rf /var/cache/yum/*

# Anaconda
RUN yum install -y \
        ca-certificates \
        wget && \
    rm -rf /var/cache/yum/*
RUN mkdir -p /var/tmp && wget -q -nc --no-check-certificate -P /var/tmp http://repo.anaconda.com/miniconda/Miniconda3-py38_4.8.3-Linux-x86_64.sh && \
    bash /var/tmp/Miniconda3-py38_4.8.3-Linux-x86_64.sh -b -p /usr/local/anaconda && \
    /usr/local/anaconda/bin/conda init && \
    ln -s /usr/local/anaconda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    . /usr/local/anaconda/etc/profile.d/conda.sh && \
    conda activate base && \
    conda install -y tensorflow-gpu && \
    /usr/local/anaconda/bin/conda clean -afy && \
    rm -rf /var/tmp/Miniconda3-py38_4.8.3-Linux-x86_64.sh


