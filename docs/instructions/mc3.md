# Building ParaDiS on MC3

Instructions for compiling and running ParaDiS on the MC3 OHPC cluster
(`mc3-login-*` login nodes, `gpu-ampere` / `gpu-tesla` / `cpu` partitions).

## Prerequisites

- ParaDiS source checked out on MC3 filesystem storage.
- Slurm account with access to the desired partition.
- For GPU builds: CUDA is only available on GPU compute nodes, not login nodes.
  Either build inside a GPU batch/interactive allocation, or let a submit script
  build on first run (see [Run an example](#run-an-example) below).

## Environment setup

Load the GNU toolchain, OpenMPI, and (for GPU builds) CUDA:

```bash
module purge
module load gnu12/12.3.0
module load openmpi4/4.1.6
module load cuda/12.5    # GPU builds only; skip for CPU-only
```

Verify compilers:

```bash
which gcc mpicxx
# GPU builds also require:
which nvcc    # only available on GPU compute nodes
```

## makefile.setup settings

Edit `makefile.setup` or pass flags on the command line. Recommended MC3
settings:

| Setting | Value | Notes |
|---------|-------|-------|
| `SYS` | `linux` | Pass on every `make` invocation |
| `MODE` | `PARALLEL` | Default |
| `GPU_ENABLED` | `ON` or `OFF` | `ON` for GPU force kernels |
| `XLIB_MODE` | `OFF` | No display on cluster nodes |

**Important:** use `SYS=linux`, not `SYS=gcc`. The `gcc` target links against
`-lmpich`, which is not provided by the OpenMPI module on MC3.

For GPU builds, export CUDA paths before `make` (Ampere nodes use `sm_80`):

```bash
export CUDA_PATH=/usr/local/cuda-12.5
export CUDA_LIBS=/usr/local/cuda-12.5/lib64
export NVCC="${CUDA_PATH}/bin/nvcc"
export NVCC_FLAGS="-O3 -g -rdc=true -Wno-deprecated-gpu-targets -gencode arch=compute_80,code=sm_80"
```

Adjust `-gencode` for other GPU partitions if needed (`gpu-tesla`, `gpu-A100`, etc.).

## Build (CPU only)

From the repository root on a login node:

```bash
cd /path/to/ParaDiS.llnl.git
module load gnu12/12.3.0 openmpi4/4.1.6

make SYS=linux
```

Executables appear in `./bin/`, including `./bin/paradis`.

## Build (with GPU support)

Request a short interactive GPU session, then build there:

```bash
salloc -p gpu-ampere --gres=gpu:1 -N 1 -t 00:30:00

module purge
module load gnu12/12.3.0 openmpi4/4.1.6 cuda/12.5

cd /path/to/ParaDiS.llnl.git
export CUDA_PATH=/usr/local/cuda-12.5
export CUDA_LIBS=/usr/local/cuda-12.5/lib64
export NVCC="${CUDA_PATH}/bin/nvcc"
export NVCC_FLAGS="-O3 -g -rdc=true -Wno-deprecated-gpu-targets -gencode arch=compute_80,code=sm_80"

make SYS=linux GPU_ENABLED=ON
```

## Verify the build

```bash
ls -l bin/paradis
mpirun -n 1 bin/paradis -help 2>&1 | head
```

## Run an example

ParaDiS must be launched from the repository root so that `inputs/` paths in
control files resolve correctly.

### Interactive (CPU partition)

```bash
cd /path/to/ParaDiS.llnl.git
srun -N 1 -n 8 -p cpu bin/paradis -d tests/frank_read_src.data tests/frank_read_src.ctrl
```

### Batch (Frank-Read on gpu-ampere)

A ready-made script is provided under `examples/frank_read/`:

```bash
cd examples/frank_read
sbatch submit.sh
```

The script loads modules, builds with `GPU_ENABLED=ON` if needed, and runs the
Frank-Read source example with elastic FMM forces and `BCC_glide` mobility.

## Clean rebuild

```bash
make SYS=linux clean
make SYS=linux GPU_ENABLED=ON   # add GPU_ENABLED=ON if needed
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `target system has not been identified` | Pass `SYS=linux` on every `make` and `make clean` command |
| `cannot find -lmpich` | You used `SYS=gcc`; switch to `SYS=linux` |
| `NVCC compiler not found` | Load `cuda/12.5` on a GPU compute node, not a login node |
| `openmpi4` module won't load | Load `gnu12/12.3.0` first: `module load gnu12/12.3.0 openmpi4/4.1.6` |
| FMM table not found at runtime | Run `paradis` from the repository root, not from a subdirectory |
