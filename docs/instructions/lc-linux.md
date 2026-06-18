# Building ParaDiS on LLNL LC Linux Clusters

Instructions for compiling and running ParaDiS on Livermore Computing
commodity Linux clusters (Quartz, Pascal, Borax, Syrah, Surface, Rztopaz, etc.).
The test scripts under `tests/` detect these hosts as `lc-linux` and launch jobs
with `salloc` / `srun`.

## Prerequisites

- ParaDiS source on LC filesystem (`/g/g*`, `/p/lustre*`, or similar).
- Valid LC bank / account for Slurm allocations.
- Intel compilers and MVAPICH2 (or the cluster-default MPI module).

## Environment setup

Load the standard LC compiler and MPI stack. Exact module names vary slightly
by cluster; use `module avail` to confirm:

```bash
module purge
module load intel/2023.2.1       # or cluster-default intel module
module load mvapich2/2.3.7       # or openmpi, depending on cluster
```

Verify:

```bash
which icpc mpicxx
mpicxx --version
```

For GPU clusters (Surface, Pascal GPU nodes), also load CUDA before a GPU build:

```bash
module load cudatoolkit/12.5     # module name varies; check module avail cuda
```

## makefile.setup settings

| Setting | Value | Notes |
|---------|-------|-------|
| `SYS` | `linux.intel` or `linux` | `linux.intel` when using Intel `mpicxx` |
| `MODE` | `PARALLEL` | Default |
| `GPU_ENABLED` | `OFF` | Set `ON` only for GPU-enabled builds |
| `XLIB_MODE` | `OFF` | Recommended on compute nodes |

On LC Linux, `SYS` is not auto-detected. Pass it on the command line:

```bash
make SYS=linux.intel
```

Use `SYS=linux` instead if building with GCC/`mpicxx` from a generic OpenMPI
module and no Intel compilers.

## Build

From the repository root:

```bash
cd /path/to/ParaDiS.llnl.git

make SYS=linux.intel
```

For a clean rebuild:

```bash
make SYS=linux.intel clean
make SYS=linux.intel
```

Executables are written to `./bin/paradis` and supporting utilities.

### Optional GPU build (Surface / Pascal)

Build on a GPU compute node after loading CUDA:

```bash
export CUDA_PATH=${CUDA_HOME:-/usr/local/cuda}
export CUDA_LIBS="${CUDA_PATH}/lib64"
export NVCC="${CUDA_PATH}/bin/nvcc"
export NVCC_FLAGS="-O3 -g -rdc=true -Wno-deprecated-gpu-targets -gencode arch=compute_60,code=sm_60"

make SYS=linux.intel GPU_ENABLED=ON
```

Adjust `-gencode` to match the GPU architecture on your partition.

## Verify the build

```bash
ls -l bin/paradis
```

## Run an example

Always start ParaDiS from the repository root. Control files reference tables
under `inputs/` with paths relative to that directory.

### Quick test (serial domain count)

```bash
./bin/paradis tests/frank_read_src.ctrl
```

The bundled `tests/frank_read_src.ctrl` uses `numXdoms = numYdoms = numZdoms = 1`.

### Parallel test via interactive allocation

This matches the pattern used in `tests/frs_strain_kinsol_aa.sh` and other
`tests/*.sh` scripts:

```bash
NDOMS=8
EXE=./bin/paradis
DAT=tests/frs_strain.data
CTL=tests/frs_strain_kinsol_aa.ctrl

salloc -n ${NDOMS} -c 1 -t 30 -p pdebug \
  srun -n ${NDOMS} ${EXE} -d ${DAT} ${CTL}
```

The number of MPI tasks (`-n`) must equal `numXdoms * numYdoms * numZdoms` in
the control file.

### Batch job

```bash
#!/bin/bash
#SBATCH -J paradis-test
#SBATCH -N 1
#SBATCH -n 8
#SBATCH -t 00:30:00
#SBATCH -p pbatch

cd /path/to/ParaDiS.llnl.git
srun -n 8 ./bin/paradis -d tests/frank_read_src.data tests/frank_read_src.ctrl
```

Submit with `sbatch job.sh`.

## Clean up test output

```bash
make -C tests clean
```

Or remove individual result directories listed in each test's `.ctrl` file.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `target system has not been identified` | Add `SYS=linux.intel` (or `SYS=linux`) to `make` |
| MPI launch hangs or wrong task count | Match `srun -n` to `numXdoms * numYdoms * numZdoms` |
| Missing FMM table | Run from repo root; confirm `inputs/fm-ctab.*.dat` exists |
| `cannot find -lmpich` with `SYS=linux.intel` | Ensure the Intel/MVAPICH module is loaded before building |
| HDF5 link errors | Leave `HDF_MODE` off in `makefile.setup` unless HDF restart is needed |
