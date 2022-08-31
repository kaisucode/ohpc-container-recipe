
## OpenHPC Container Recipe

This is a container recipe for [NVIDIA's HPC container maker](https://github.com/NVIDIA/hpc-container-maker). The base image is [OpenHPC's development environment](https://quay.io/repository/ohpc/ohpc-gnu9), with added Python, TensorFlow, and Keras support



---
[share]$ nvcc --version
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2015 NVIDIA Corporation
Built on Tue_Aug_11_14:27:32_CDT_2015
Cuda compilation tools, release 7.5, V7.5.17

module: loading 'cuda/7.5.18'

---


tensorflow-2.6.0
cuDNN 8.1	
cuda 11.2


in sbatch script, 
module load cuda/11.3.1
module load cudnn/8.1.0


https://www.tensorflow.org/install/source


## Usage examples


#### Docker

```bash
hpccm --recipe ohpc-recipe.py --format docker > Dockerfile
docker build -t ohpc-recipe -f Dockerfile .
docker run -v $PWD/python_scripts/:/mnt/python_scripts/ -it --rm ohpc-recipe python3.7 /mnt/python_scripts/test.py
```

#### Singularity

Note: For singularity builds, root access is required. If you are on MacOS or Windows, please check out the instructions [here](https://docs.sylabs.io/guides/3.0/user-guide/installation.html#mac) on how to use Vagrant to build a Singularity virtual machine

```bash
hpccm --recipe ohpc-recipe.py --format singularity > Singularity.def
sudo singularity build ohpc-recipe.simg Singularity.def
singularity exec --nv ohpc-recipe.simg python3.7 $PWD/python_scripts/benchmark.py
```

