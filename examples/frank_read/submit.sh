#!/bin/bash
#SBATCH -J paradis-frank-read
#SBATCH -o frank_read.%j.out
#SBATCH -e frank_read.%j.err
#SBATCH -p gpu-ampere
#SBATCH -N 1
#SBATCH --ntasks=8
#SBATCH --cpus-per-task=1
#SBATCH --gres=gpu:1
#SBATCH -t 01:00:00

set -euo pipefail

module purge
module load gnu12/12.3.0
module load openmpi4/4.1.6
module load cuda/12.5

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$REPO_ROOT"

EXE="${REPO_ROOT}/bin/paradis"
DAT="examples/frank_read/frank_read.data"
CTL="examples/frank_read/frank_read.ctrl"
LOG="examples/frank_read/frank_read.log"
RESULTS="examples/frank_read/frank_read_results"

NDOMS=8

export CUDA_PATH=/usr/local/cuda-12.5
export CUDA_LIBS=/usr/local/cuda-12.5/lib64
export NVCC="${CUDA_PATH}/bin/nvcc"
export NVCC_FLAGS="-O3 -g -rdc=true -Wno-deprecated-gpu-targets -gencode arch=compute_80,code=sm_80"

echo "Job started: $(date)"
echo "Host: $(hostname)"
echo "Repo: ${REPO_ROOT}"

if [ ! -x "${EXE}" ]; then
    echo "Building ParaDiS with GPU support on ${HOSTNAME}..."
    mkdir -p "${REPO_ROOT}/obj/p" "${REPO_ROOT}/obj/s" "${REPO_ROOT}/bin"
    make SYS=linux GPU_ENABLED=ON
fi

if [ ! -x "${EXE}" ]; then
    echo "ERROR: ${EXE} not found after build"
    exit 1
fi

if command -v nvidia-smi >/dev/null 2>&1; then
    nvidia-smi -L
else
    echo "WARNING: nvidia-smi not available on this node"
fi

rm -rf "${RESULTS}" "${LOG}" slurm*.out

echo "Launching ${NDOMS} MPI tasks..."
srun -n "${NDOMS}" "${EXE}" -d "${DAT}" "${CTL}" | tee -a "${LOG}"

echo "Job finished: $(date)"
