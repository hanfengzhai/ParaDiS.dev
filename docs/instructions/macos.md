# Building ParaDiS on macOS

Instructions for compiling and running ParaDiS locally on a Mac (MacBook Pro or
similar). The build system auto-selects `SYS=mac` when `uname -s` returns
`Darwin`.

## Prerequisites

Install the following before building:

- **Xcode Command Line Tools** — provides `clang` / `g++`
  ```bash
  xcode-select --install
  ```
- **OpenMPI** — for parallel builds (`MODE=PARALLEL`)
  ```bash
  brew install open-mpi
  ```
  or via MacPorts:
  ```bash
  sudo port install openmpi
  ```
- **XQuartz** (optional) — only needed if `XLIB_MODE=ON` for live X-Window plotting

## Environment setup

Ensure `mpicxx` is on your `PATH`:

```bash
which mpicxx g++
mpicxx --version
```

If using Homebrew OpenMPI:

```bash
export PATH="/opt/homebrew/bin:$PATH"          # Apple Silicon
# or
export PATH="/usr/local/bin:$PATH"             # Intel Mac
```

## makefile.setup settings

On macOS, `makefile.setup` sets `SYS=mac` automatically. Key defaults:

| Setting | Default on macOS | Notes |
|---------|------------------|-------|
| `SYS` | `mac` | Auto-detected |
| `MODE` | `PARALLEL` | Requires OpenMPI |
| `XLIB_MODE` | `ON` | Turn `OFF` if XQuartz is not installed |
| `GPU_ENABLED` | `OFF` | Enable only if CUDA toolkit is installed |

To disable X-Window support, edit `makefile.setup`:

```
XLIB_MODE=OFF
```

## Build

From the repository root:

```bash
cd /path/to/ParaDiS.llnl.git
mkdir -p obj/p obj/s bin
make
```

Because `SYS=mac` is auto-detected, you do not need to pass `SYS=` on the
command line.

For a clean rebuild:

```bash
make clean
mkdir -p obj/p obj/s bin
make
```

Executables are created in `./bin/paradis` and supporting tools in `./bin/`.

### Optional GPU build

If the NVIDIA CUDA toolkit is installed at `/usr/local/cuda`:

```bash
make GPU_ENABLED=ON
```

The macOS `makefile.sys` entry expects CUDA at `/usr/local/cuda` and sets
`-gencode arch=compute_30,code=sm_30` by default in `makefile.setup` comments.
Update `NVCC_FLAGS` for your GPU architecture if needed.

## Verify the build

```bash
ls -l bin/paradis
mpirun -n 1 bin/paradis -help 2>&1 | head
```

## Run an example

Start ParaDiS from the repository root. The test scripts under `tests/` detect
macOS hosts as `osx` and use `mpirun`.

### Serial (1 MPI task)

```bash
./bin/paradis tests/frank_read_src.ctrl
```

### Parallel (8 MPI tasks)

Match the domain count in the control file (`numXdoms = numYdoms = numZdoms = 2`):

```bash
mpirun -n 8 ./bin/paradis -d tests/frank_read_src.data tests/frank_read_src.ctrl
```

This mirrors `tests/frs_strain_kinsol_aa.sh` and other `tests/*.sh` scripts on
the `osx` code path.

### Example with separate data file

```bash
mpirun -n 8 ./bin/paradis -d tests/frank_read_src.data tests/frank_read_src.ctrl
```

## Clean up test output

```bash
make -C tests clean
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `mpicxx: command not found` | Install OpenMPI and add it to `PATH` |
| X11 / Xlib link errors | Set `XLIB_MODE=OFF` in `makefile.setup`, or install XQuartz |
| `target system has not been identified` on Linux VM | You are not on macOS; use [lc-linux.md](lc-linux.md) instead |
| MPI task count mismatch | Set `mpirun -n` to `numXdoms * numYdoms * numZdoms` |
| Missing `inputs/` files at runtime | Run `paradis` from the repository root |
| `can't create ../obj/p/*.o` | Run `mkdir -p obj/p obj/s bin` before `make` |
