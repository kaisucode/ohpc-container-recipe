"""OpenHPC container

Sample workflow:
$ hpccm.py --recipe recipes/ohpc.py --format docker > Dockerfile
$ docker build -t ohpc-recipe -f Dockerfile .
$ docker run -v $PWD/python_scripts/:/mnt/python_scripts/ -it --rm ohpc-recipe python3 /mnt/python_scripts/benchmark.py
"""
# pylint: disable=invalid-name, undefined-variable, used-before-assignment
import os

Stage0 += comment(__doc__, reformat=False)

Stage0 += baseimage(image='quay.io/ohpc/ohpc-gnu9', _distro='centos8')


Stage0 += shell(commands=["sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-*",
                          "sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-*"])

Stage0 += shell(commands=['yum update -y',
                          'rm -rf /var/cache/yum/*'])

#  Stage0 += packages(epel=True,
#                     yum=['wget', 'python38'])

Stage0 += environment(variables={
    'CONDA_CUDA_OVERRIDE': "11.2",
    'PATH': '/usr/local/anaconda/bin:$PATH', 
    'LD_LIBRARY_PATH': '$LD_LIBRARY_PATH:/usr/local/anaconda/lib'
    })

Stage0 += conda(eula=True, channels=['conda-forge'], 
        #  packages=['tensorflow-gpu==2.6.0', 'cudatoolkit==11.2', 'cudnn'])
        packages=['tensorflow-gpu==2.6.0'])
        #  packages=['keras==2.6.0', 'tensorflow-gpu==2.6.0'])
## needs to be `tensorflow-gpu` instead of `tensorflow`, so that conda will also install cudatoolkit and cudnn



# for vagrant testing without bind point
Stage0 += copy(src='python_scripts/benchmark.py', dest='benchmark_cpy.py')
#  Stage0 += shell(commands=[
#      'mpicc -o /usr/local/bin/mpi_bandwidth /var/tmp/mpi_bandwidth.c'])




#  def sourceEnvRunscript(): 
    #  Stage1 += runscript(commands=['/usr/local/anaconda/bin/activate'])
    #      'echo "#!/bin/bash\\nsource /usr/local/anaconda/bin/activate {}\\n > /usr/local/bin/entrypoint.sh'.format('base'),
    #  Stage1 += hpccm.primitives.shell(commands=[
    #      'echo "#!/bin/bash \n source /usr/local/anaconda/bin/activate" > /usr/local/bin/entrypoint.sh',
    #      'chmod a+x /usr/local/bin/entrypoint.sh'])
    #  Stage1 += hpccm.primitives.runscript(
    #          commands=['/usr/local/bin/entrypoint.sh'])

# Install Python 3.7
#  Stage1 += shell(commands=['cd /tmp/', 
#      'wget https://developer.download.nvidia.com/compute/cuda/11.3.0/local_installers/cuda-repo-rhel8-11-3-local-11.3.0_465.19.01-1.x86_64.rpm', 
#      'sudo rpm -i cuda-repo-rhel8-11-3-local-11.3.0_465.19.01-1.x86_64.rpm'])


# Install Python 3.7
#  Stage1 += packages(epel=True,
#                     yum=['nvidia-driver:latest-dkms', 'cuda'])

#  Stage1 += pip(packages=['keras==2.6.0', 'tensorflow==2.6.0', 'protobuf==3.20.*'], pip='pip3.8')


