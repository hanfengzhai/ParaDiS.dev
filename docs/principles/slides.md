# ParaDiS — Slide Principles (Agent Guide)

Use when **writing or refining** presentation decks about ParaDiS simulations, especially:

- Marp Markdown under `docs/slides/` (if present)
- Beamer sources under `Writings.git` or project-specific `doc/slides/`
- Figures from `examples/<name>/output/`

Goal: **clear scientific storytelling** — not a README, runbook, or code walkthrough.

> **Invariant (edits):** math notation, figure filenames, and slide order must stay consistent with the underlying simulation. Do not invent metrics, paths, or results the user has not supplied or approved.

**Read first (do not contradict):**

- [`coding.md`](coding.md) — repo layout; use for *facts*, not slide tone
- [`../instructions/`](../instructions/) — cluster details belong off slides unless the audience is ops-only

**Writings rule of thumb:** less text, more figures, be expressive.

---

## What belongs on slides

| Put on slides | Keep off slides |
|---------------|-----------------|
| Physics model, stress state, mobility choice | Full `mpirun` command lines unless teaching setup |
| Hero figures (`first_vs_final.png`, property plots) | Raw gnuplot file trees, restart filenames |
| One comparison table per recipe change | Complete `.ctrl` parameter dumps |
| 3–4 numbered takeaways | Slurm partition names, module versions |

---

## Agent workflow

1. **Read context** — existing deck, example `output/` figures, relevant `.ctrl` physics.
2. **Confirm assets** — use figures the user specified; ask if a named plot is missing.
3. **Apply rules below** — one idea per slide; math + visuals first.
4. **Export smoke check** — Marp HTML or `pdflatex` if Beamer; fix broken `![](…)` paths.
5. **Stop when clear** — no appendix command cheatsheets unless requested.

---

## Core philosophy: show, don't shell

| Do | Don't |
|----|-------|
| State physics in LaTeX ($\sigma_{zx}$, $\mathbf{b}$, glide plane) | Paste `module load` / `sbatch` blocks |
| Lead with figures and short captions | Walls of bullets or README prose |
| Write as you would **say it aloud** — simple words, short sentences | Dense jargon or nested clauses |
| One hero figure per result slide | Three small plots with no headline message |

**Concise is better.** If a slide needs more than ~6 lines of body text, split it or replace text with a figure.

---

## Title slide

Include only:

1. Talk title (optional one-line subtitle)
2. Presenter name
3. Institution
4. Email
5. Date

No abstract, acknowledgments, or parameter dump on slide 1.

---

## Mathematics

- Display math (`$$ … $$`) for main equations; inline `$…$` for symbols in prose.
- Stress: use Voigt order consistent with ParaDiS `.ctrl` when showing applied loads.
- Define each symbol once; reuse on later slides.
- Map code names to math on slides: `appliedStress[4]` → $\sigma_{zx}$, not raw index notation.

---

## Figures (ParaDiS examples)

| Kind | Typical source | Slide use |
|------|----------------|-----------|
| Initial vs final | `output/first_vs_final.png` | Loop expansion, Frank-Read bowing |
| Animation frame | `output/frames/0t*.png` | Intermediate morphology |
| Density vs time | `output/density_vs_time.png` | Network growth rate |
| Density vs strain | `output/density_vs_strain.png` | Constitutive context |

```markdown
![Glissile loop expansion](../../examples/1_glissile_loops/output/first_vs_final.png)
```

Rules:

- One **hero figure** per slide when explaining a result.
- Short caption under the image (one sentence).
- For (001) glissile loops, note the viewing angle if oblique 3D could mislead — prefer top-down or state “loop remains at $z=0$”.
- If the figure is missing, **stop and ask** — do not fabricate plots.

---

## Slide structure (simulation talks)

Recommended flow:

1. **Setup** — crystal, box size, mobility law
2. **Loading** — stress tensor or strain-rate direction
3. **Initial state** — schematic or first frame
4. **Result** — hero figure (expansion, bowing, density)
5. **Diagnostics** — property plot or segment count
6. **Comparison** — vs reference test or OpenDiS analogue (if applicable)
7. **Summary** — 3–4 numbered takeaways

Avoid: “Directory layout”, “How to submit on MC3” slides unless the audience is internal ops-only.

---

## Text and bullets

- Simple oral words — “the loop expands in the glide plane” not “the dislocation manifold undergoes area growth.”
- Short sentences — one idea each.
- Maximum ~5 bullets per slide; prefer 2–3.
- Bullets are phrases or one short sentence — except the summary slide.
- No nested bullets deeper than one level.

---

## Format: Marp (if used)

```yaml
---
marp: true
theme: default
paginate: true
math: mathjax
size: 16:9
style: |
  section { font-size: 28px; }
  h2 { color: #1a365d; }
---
```

- Slide breaks: `---` on its own line.
- `#` for title slide only; `##` for content slides.

---

## Checklist

- [ ] Title slide: title, name, institution, email, date only
- [ ] No `mpirun` / module dumps on science slides
- [ ] Notation matches `.ctrl` and figure axis labels
- [ ] Every referenced figure path exists
- [ ] One main idea per slide; text stays short
- [ ] Prose readable aloud
- [ ] Summary slide matches evidence shown earlier
