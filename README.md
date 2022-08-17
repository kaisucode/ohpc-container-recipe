
## OpenHPC Container Recipe

This is a container recipe for [NVIDIA's HPC container maker](https://github.com/NVIDIA/hpc-container-maker). The base image is [OpenHPC's development environment](https://quay.io/repository/ohpc/ohpc-gnu9), with added Python, TensorFlow, and Keras support


## Usage examples


#### Docker

```bash
hpccm --recipe recipes/ohpc-recipe.py --format docker > Dockerfile
docker build -t ohpc-recipe -f Dockerfile .
docker run -v $PWD/python_scripts/:/mnt/python_scripts/ -it --rm ohpc-recipe python3.7 /mnt/python_scripts/test.py
```

#### Singularity

```bash
hpccm --recipe recipes/ohpc-recipe.py --format singularity > Singularity.def
singularity build ohpc-recipe.simg Singularity.def
singularity exec --nv ohpc-recipe.simg python3.7 $PWD/python_scripts/benchmark.py
```

