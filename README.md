
# ParaDiS.dev

**Personal research fork.** This repository is my working copy of ParaDiS, adjusted for dislocation-dynamics studies in the **Micro and Nano Mechanics Group** at Stanford University. It adds example workflows, cluster build notes, and visualization tooling on top of the public release. Upstream ParaDiS is not actively developed; see OpenDiS below.

**IMPORTANT: ParaDiS development is no longer supported as the code is being replaced by our new open-source project [OpenDiS](https://github.com/OpenDiS/OpenDiS), which includes the high-performance [ExaDiS](https://github.com/LLNL/exadis) core library that runs on GPU. More information about OpenDiS is available at the [OpenDiS documentation](https://opendis.github.io/OpenDiS).**

> ParaDiS Public Release Version 4.0
> 
> ParaDiS (Parallel Dislocation Simulator) performs direct numerical simulation of dislocation ensembles—the carriers of plasticity—to predict strength in crystalline materials from defect motion, evolution, and interaction.
> 
> The code has been deployed on large HPC systems and used to study strength and strain hardening in cubic crystals, micro-pillars, and irradiated materials at LLNL (including runs with over ten million active degrees of freedom).

## This fork

- `examples/` — glissile loops, Frank-Read, strain hardening (Cu, Al); SLURM submit scripts
- `examples/utils/visualize.py` — plots and movies from restart files
- `docs/instructions/` — build notes for MC3, LC Linux, macOS

Run `paradis` from the repo root. MC3: `docs/instructions/mc3.md`.

## Installation

### Quick start

The public distribution is built with conventional makefiles.

1. Select a target system (e.g. `SYS=gcc` at line 52) and compilation mode (`MODE=SERIAL` or `MODE=PARALLEL` at lines 66-67) in `makefile.setup`
2. Compile from the repository root: `make`
3. Binaries appear in `./bin`
4. Test the installation:

```
./bin/paradis tests/frank_read_src.ctrl
```

### Detailed instructions

Build system makefiles:

* `makefile`           : build ParaDiS and supporting utilities
* `makefile.setup`     : enable/disable application features
* `makefile.sys`       : system-specific build settings
* `makefile.srcs`      : complete source file list
* `src/makefile`       : builds ParaDiS
* `src/makefile.dep`   : dependencies (auto-generated via `make depend`)
* `tests/makefile`     : test directory management
* `utils/makefile`     : utility applications
* `ext/makefile`       : external dependencies

Customize `makefile.sys` and `makefile.setup` before `make` if needed. Running `make` from the root builds all tools; run `make` from `src/` for the main executable only.

#### makefile.sys

Identify the target system before building. Preset systems include:

```
linux.intel     Linux systems using native Intel compilers.
linux           Generic linux system
gcc             Generic system build using gnu compilers
aix             IBM aix systems using native compilers (LLNL's ice, berg, purple, um, up, uv...)
mac             MacBook Pro 
bgp             LC BlueGene/P systems (dawn, dawndev)
bgq             LC BlueGene/Q systems (sequoia, rzuseq)
mc-cc           Stanford ME Linux system using intel compilers
wcr             Stanford ME Linux system using intel compilers
cygwin          Stanford Linux emulator for Windows PC
xt4             Cray XT4 systems (NERSC's franklin)
```

For unlisted systems, copy/adjust an entry in `makefile.sys` and set `SYS=` in `makefile.setup`.

#### makefile.setup

User-specific features are toggled in `makefile.setup` (serial vs MPI, optimization, X-Windows display, etc.). Main parameters:

```
# required parameter, must identify the target host machine
SYS=[linux.intel | linux | gcc | aix| mac | bgp| bgq | mc-cc| wcr| cygwin | xt4 ]

MODE=SERIAL     # sets the execution mode to serial
MODE=PARALLEL   # sets the execution mode to parallel (default, requires an MPI installation) 

XLIB_MODE=ON    # enables  the X-Window visualization (do not use for production runs)
XLIB_MODE=OFF   # disables the X-Window visualization (default)
```

All other switches are documented in `makefile.setup`.

## Directory Structure

* `./bin`      : executables (created during build)
* `./src`      : C/C++ source (*.cc)
* `./include`  : C/C++ headers (*.h)
* `./obj`      : object files (parallel and serial builds)
* `./docs`     : documentation (instructions, principles)
* `./inputs`   : Rijm tables, FMM tables, gnuplot defaults
* `./tests`    : upstream example tests (`*.ctrl`, `*.data`, `*.sh`)
* `./examples` : research examples with submit scripts and visualization
* `./utils`    : support utilities
* `./tools`    : support tools

## Applications and Tools

Built from the repository root:

* `./bin/paradis`           : main ParaDiS simulator
* `./bin/paradisconvert`    : conversion utility for older control and data files
* `./bin/calcdensity`       : dislocation density calculator
* `./bin/ctablegen`         : PBC image correction tables
* `./bin/ctablegenp`        : PBC image correction tables (MPI)
* `./bin/paradisgen`        : initial random dislocation networks
* `./bin/paradisrepart`     : repartition domain decompositions
* `./bin/stresstablegen`    : far-field stress tables

## Simulation Examples

Upstream examples live in `tests/`. ParaDiS is controlled by a `.data` file (domain and initial network) and a `.ctrl` file (material parameters, loading, numerics).

Most `tests/` control files use 8 MPI ranks (`numXdoms = numYdoms = numZdoms = 2`). Total processes = `numXdoms * numYdoms * numZdoms` and must match the launch count:

```
mpirun -n 8 ./bin/paradis ./tests/mg-cAxis.ctrl
```

Several tests use precomputed FMM tables in `./inputs`. Paths in `.ctrl` files assume ParaDiS is started from the repository root. If not, use paths relative to the launch directory.

Generate an isotropic FMM table with:

```
  ./bin/ctablegen -nu 3.327533e-01 -mu 6.488424e+10 -mporder 2 -torder 5 -outfile inputs/fmm-ctab.data
```

See the ParaDiS users guide for more on FMM tables. Initial networks can be created with `paradisgen`.

## Citation

```
@article{arsenlis2007enabling,
  title={Enabling strain hardening simulations with dislocation dynamics},
  author={Arsenlis, Athanasios and Cai, Wei and Tang, Meijie and Rhee, Moono and Oppelstrup, Tomas and Hommes, Gregg and Pierce, Tom G and Bulatov, Vasily V},
  journal={Modelling and Simulation in Materials Science and Engineering},
  volume={15},
  number={6},
  pages={553},
  year={2007},
  publisher={IOP Publishing}
}
```

## License

ParaDiS is released under the BSD-3 license. See [LICENSE](LICENSE) for details.

LLNL-CODE-853453
