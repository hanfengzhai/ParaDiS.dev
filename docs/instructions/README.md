# ParaDiS Build Instructions

Machine-specific guides for installing and compiling ParaDiS. Each document
covers prerequisites, environment setup, build commands, verification, and a
minimal test run.

| Machine | Document | Typical use |
|---------|----------|-------------|
| MC3 (OHPC, Ampere GPU) | [mc3.md](mc3.md) | GPU-enabled builds and batch jobs |
| LLNL LC Linux clusters (Quartz, Pascal, …) | [lc-linux.md](lc-linux.md) | CPU MPI production and development |
| macOS (MacBook / local) | [macos.md](macos.md) | Local development and debugging |

## Common build overview

All platforms share the same makefile-based build:

1. Clone or copy the ParaDiS source tree.
2. Load the compiler and MPI modules for your machine (see per-machine docs).
3. Set build options in `makefile.setup` or pass them on the `make` command line.
4. Run `make` from the repository root.
5. Confirm that `./bin/paradis` was created.

The two makefile parameters that matter on every machine are:

- **`SYS`** — selects compiler and library paths in `makefile.sys`. On Linux
  clusters this must be passed explicitly, e.g. `make SYS=linux`.
- **`MODE`** — `PARALLEL` (default, MPI) or `SERIAL`. Parallel builds require
  a working `mpicxx`.

Optional flags in `makefile.setup`:

- **`GPU_ENABLED=ON`** — compile CUDA device code (requires `nvcc` on the build node).
- **`XLIB_MODE=OFF`** — disable X-Window visualization (recommended for HPC).

See the root [README.md](../../README.md) for a full list of build switches and
directory layout.
