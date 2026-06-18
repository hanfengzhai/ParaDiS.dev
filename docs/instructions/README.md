# ParaDiS build instructions

Step-by-step guides for compiling and running ParaDiS on each machine.

| Machine | Guide | Start here |
|---------|-------|------------|
| **MC3** (you are likely here) | [mc3.md](mc3.md) | Steps 0–8, copy-paste in order |
| LLNL LC Linux (Quartz, Pascal, …) | [lc-linux.md](lc-linux.md) | Intel/MVAPICH workflow |
| macOS (local Mac) | [macos.md](macos.md) | Homebrew OpenMPI workflow |

## Quick start on MC3

```bash
module purge && module load gnu12/12.3.0 openmpi4/4.1.6
cd ~/codes/ParaDiS.llnl.git
mkdir -p obj/p obj/s bin
make SYS=linux
ls -l bin/paradis
```

Full details, GPU builds, and troubleshooting: **[mc3.md](mc3.md)**.

## Key rules (all machines)

1. Always run `make` from the **repository root**.
2. On Linux clusters, pass **`SYS=linux`** (or `SYS=linux.intel` on LC) on every
   `make` command — it is not auto-detected.
3. Create **`obj/p obj/s bin`** before the first build to avoid parallel-make
   directory errors.
4. Launch **`paradis` from the repository root** so `inputs/` paths in `.ctrl`
   files resolve.
5. Install git hooks once: `scripts/install-git-hooks.sh`.

See the root [README.md](../../README.md) for makefile switches and directory
layout.
