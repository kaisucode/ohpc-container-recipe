"""OpenHPC container

Sample workflow:
$ hpccm.py --recipe recipes/ohpc.py --format docker > Dockerfile
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
# Install Python 3.7
Stage0 += packages(epel=True,
                   yum=['python38'])

Stage0 += pip(packages=['keras==2.6.0', 'tensorflow==2.6.0', 'protobuf==3.20.*'], pip='pip3.8')


