"""OpenHPC container

Sample workflow:
$ hpccm.py --recipe recipes/ohpc.py > Dockerfile
$ docker build -t ohpc-recipe -f Dockerfile .
$ docker run -v $PWD/python_scripts/:/mnt/python_scripts/ -it --rm ohpc-recipe python3.7 /mnt/python_scripts/benchmark.py
"""
# pylint: disable=invalid-name, undefined-variable, used-before-assignment
import os

Stage0 += comment(__doc__, reformat=False)

Stage0 += baseimage(image='quay.io/ohpc/ohpc-gnu9', _distro='centos8')


Stage0 += shell(commands=["sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-*",
                          "sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-*"])

Stage0 += shell(commands=['yum update -y',
                          'rm -rf /var/cache/yum/*'])

Stage0 += packages(epel=True, powertools=True,
                   yum=['make gcc wget openssl-devel bzip2-devel libffi-devel'])

# Install Python 3.7
Stage0 += shell(commands=['cd /tmp/', 'wget https://www.python.org/ftp/python/3.7.9/Python-3.7.9.tgz', 
    'tar xzf Python-3.7.9.tgz', 'cd Python-3.7.9', './configure --enable-optimizations', 
    'make altinstall', 'ln -sfn /usr/local/bin/python3.7 /usr/bin/python3.7', 'ln -sfn /usr/local/bin/pip3.7 /usr/bin/pip3.7'])

Stage0 += pip(packages=['keras==2.6.0', 'tensorflow==2.6.0', 'protobuf==3.20.*'], pip='pip3.7')


