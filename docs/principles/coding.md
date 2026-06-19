# ParaDiS — Coding Principles (Agent Guide)

Use when **refactoring or extending** Python and shell tooling in this repository, especially:

- `examples/utils/` — shared visualization (`visualize.py`)
- `examples/<name>/` — per-example `.ctrl`, `.data`, generators, submit scripts
- `examples/<name>/output/` — PNG frames, MP4/MOV, property plots

The C++ core under `src/` follows existing ParaDiS conventions; apply these rules to **new Python/bash** around simulations.

> **Invariant (refactors):** behavior must stay equivalent — figure paths, plot layout, CLI flags and defaults, `.ctrl`/`.data` semantics, and Slurm wiring.

**Read first (do not contradict):**

- [`../../README.md`](../../README.md) — build and launch from repo root
- [`../instructions/README.md`](../instructions/README.md) — cluster-specific `make` and `mpirun` rules

---

## Repository layout

```
ParaDiS.llnl.git/
  src/                          # C++ core (paradis)
  bin/                          # paradis executable (after make)
  inputs/                       # FMM tables, Rijm, mobility inputs
  examples/
    utils/
      visualize.py              # shared ParadiSVisualizer
    <name>/                     # e.g. 1_glissile_loops, 2_frank_read
      <name>.ctrl
      <name>.data
      make_loop_data.py         # optional generators
      submit_cpu.sh / submit_gpu.sh
      <name>_results/           # ParaDiS run output (gnuplot, properties, restart)
      output/                   # visualization PNG/MP4 (from visualize.py)
  docs/
    instructions/
    principles/                 # this file
```

| Location | Contents |
|----------|----------|
| `examples/<name>/` | Simulation case: control, data, submit, run logs |
| `examples/<name>/<name>_results/` | Raw ParaDiS output — do not hand-edit |
| `examples/<name>/output/` | Rendered figures and animation |
| `examples/utils/` | Shared Python only — no per-example forks of plotting logic |

Launch **`paradis` from the repository root** so `inputs/` paths in `.ctrl` resolve.

---

## Core philosophy: less is more

| Do | Don't |
|----|-------|
| Remove dead code, duplicate helpers, decorative prints | Add abstractions that do not reduce line count |
| Extend `ParadiSVisualizer` in `examples/utils/` | Copy `visualize.py` into each example |
| Keep submit scripts thin (env, `mpirun`, paths) | Embed plotting or data generation in bash |
| Prefer one clear class when it removes duplication | Split a readable file into many tiny modules |

**Shorter is better**, but never at the cost of the invariant above.

---

## Python structure

### Entry points

```python
if __name__ == "__main__":
    ParadiSVisualizer(example_dir=os.getcwd()).run()
```

- Do not introduce `main()` wrappers unless there is a clear need.
- Utility modules (`examples/utils/`) omit `if __name__ == "__main__":`.

### Classes

- Use class-based organization for multi-step workflows (`ParadiSVisualizer`).
- Use `@staticmethod` when instance state is not required.
- One blank line between top-level `def` blocks.
- General names: `ParadiSVisualizer`, not `GlissileLoopPlot0618`.

### Imports and paths

- Use `os.path.join(...)` / `os.path.abspath` — no hard-coded absolute paths.
- Minimize imports to what is used.

### Progress

- Use `tqdm` for frame rendering loops.
- Use `tqdm.write(...)` inside tqdm loops, not bare `print()`.

---

## Plotting standards

Enforce project style:

```python
plotting_params = {
    "font.family": "serif",
    "font.serif": ["Libertinus Serif"],
    "mathtext.fontset": "cm",
    "xtick.labelsize": 15,
    "ytick.labelsize": 15,
    "axes.labelsize": 15,
    "legend.fontsize": 15,
    "axes.unicode_minus": False,
}
```

| Rule | Value / convention |
|------|-------------------|
| Dislocation segments | `#1f4fd8`, linewidth ~1.5 |
| Simulation box | `#1a1a1a`, low alpha |
| Property curves | `darkblue`, markers with black edges |
| Spatial axes | `r"$X$ [$\mu$m]"`, same for Y, Z |
| 3D ticks | min / mid / max only per axis |
| Tick labels | Clean integers or half-integers — avoid `1.423` |
| Scientific notation | mantissa + `$\times 10^{n}$` on property plots |
| Strain axis | `[%]` where applicable |
| DPI | 200 for saved PNGs |
| Animation | MP4 or MOV only — no GIF |
| Aspect | 1:1:1 for 3D box (`set_box_aspect`) |

### Example-specific views

- **Glissile loop on (001):** top-down view (`elev=90`) — oblique 3D makes in-plane ellipses look tilted.
- **Frank-Read / general 3D:** oblique view is fine (`elev=22`, `azim=-58`).

### Panel labels

- Place summary panel titles at **bottom center** with a light bbox — avoid overlap with Z-axis labels in top-down views.

---

## Submit scripts (`examples/<name>/submit_*.sh`)

- Resolve repo root from `SLURM_SUBMIT_DIR` or script location.
- `module load` lines match [`../instructions/`](../instructions/).
- Call `mpirun` on `./bin/paradis` from repo root with `-d` paths to example `.data` and `.ctrl`.
- Optional post-run: `python examples/utils/visualize.py --example-dir ...`
- Logs under `examples/<name>/bash_logs/` or example-local `.log` — not beside `src/`.

---

## Comments and formatting

- Minimize inline comments — only non-obvious physics, units (µm, Pa, b), or ParaDiS Voigt stress order.
- No trailing whitespace; no space-only lines.
- Align continued lines with the opening delimiter (shift left, not right).
- Tunable parameters in argparse or submit bash — not buried magic numbers in library code.

---

## Refactoring checklist

- [ ] Output-equivalence confirmed (PNGs, MP4, property plots)
- [ ] No unnecessary argparse or `.ctrl` default changes
- [ ] Plot style rules satisfied
- [ ] `tqdm.write()` inside progress loops
- [ ] Paths use `os.path.join(...)`
- [ ] Figures under `output/` — not beside `.py` sources
- [ ] Shared logic in `examples/utils/`, not duplicated per example

---

## Quick reference

**Prefer**

```python
from examples.utils.visualize import ParadiSVisualizer
ParadiSVisualizer(example_dir=example_dir).run()
```

```text
examples/1_glissile_loops/
  glissile_loop.ctrl
  glissile_loop_results/gnuplot/
  output/first_vs_final.png
```

**Avoid**

```python
plt.savefig("frame.png")  # next to make_loop_data.py
```

```text
examples/utils/glissile_only_viz.py   # duplicate of visualize.py
src/plot_loop.py                      # Python beside C++ core
```
