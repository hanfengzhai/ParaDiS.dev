# ParaDiS — Scientific Writing Principles (Agent Guide)

Use when **revising or drafting** prose for papers, proposals, README sections, or LaTeX about ParaDiS simulations and results.

Goal: **clear, concise academic prose** — preserve the author's voice and citations.

> **Invariant (edits):** do not delete citations (e.g. `\cite{Wang2023}`); do not change notation that matches `.ctrl` stress order, mobility law names, or figure labels without explicit approval.

---

## Core revision rules

- Improve clarity and concision; keep the author's original style.
- Avoid extremely fancy or rare words.
- Use short sentences with clear messages — no `"this — however … — provides"` constructions.
- Delete repeated information within the same paragraph.
- When revising a paragraph, provide suggested text as **separate sentences** so each can be edited independently.

---

## LaTeX and equations

- Always return **copyable LaTeX** for equations: use `$a_5$` or `$$ … $$` — not rendered-only math the user cannot paste into Overleaf.
- Prefer `$a_5$` over `\(a_5\)`.
- No need for full `\begin{equation}` blocks unless the user asks — inline/display math in normal text is fine.
- In `.tex` source, put **one sentence per line** with `%` line breaks when the user works that way.

---

## Figure and text layout

### Default rhythm: one float, then interpretation

1. One `figure` per main idea.
2. Follow immediately with 2–3 sentences interpreting that figure.
3. Avoid **three or more full-width figures in a row** without intervening prose.

### Subfigures

- Merge panels that share the **same case, same instant, different field components** (e.g. $u_x$ and $u_y$).
- Do **not** merge unrelated diagnostics (loss plot + parity plot stay separate).
- Empty subcaptions with labels on each panel; narrative in the **parent** caption.
- Refer in prose as `(a) and~(b) of Fig.~\ref{fig:...}` — not `Panel~(a) shows …`.

### Linked figures

When two floats show the **same simulation** at different abstraction levels, state the one-to-one correspondence in main text after the second figure appears.

### Place each figure in the subsection it supports

- Field snapshots at a given resolution → the subsection that produced that resolution.
- Global scalar trajectories → the subsection for that rollout metric.
- Do not attach a coarse-grid metric figure to fine-grid scaling prose.

### Captions vs main text

| Location | Content |
|----------|---------|
| **Caption** | What is plotted, panel letters, resolution/units, one-line takeaway |
| **Main text** | Physics, agreement/error location, link to equations, relation to other figures |

For dislocation examples: cite stress components with ParaDiS Voigt order `(xx, yy, zz, yz, zx, xy)` when discussing `appliedStress` in `.ctrl` files.

---

## ParaDiS-specific prose

- Name mobility laws exactly as in ParaDiS (`BCC_Linear`, `BCC_0`, …).
- Distinguish **simulation coordinates** from display-only camera angles in figures.
- When claiming a loop stays on a glide plane, support with quantitative z-span or plane-normal data — not visual impression alone.
- Units: Burgers vector magnitude `b`, stress in Pa, length in µm in figures, time in µs/ms/s as appropriate.

---

## Checklist before calling a section done

1. No run of ≥3 consecutive figure floats without prose between them.
2. Related component panels merged; unrelated plots stay separate.
3. Cross-linked figure pairs explained in the body.
4. Every `\ref{fig:...}` points to the subsection that produced that result.
5. Symbols in figures match Methods notation.
6. Citations preserved; no invented metrics or paths.
