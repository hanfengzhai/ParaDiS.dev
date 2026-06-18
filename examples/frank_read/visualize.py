#!/usr/bin/env python3
"""Visualize ParaDiS Frank-Read results with matplotlib.

Reads gnuplot segment dumps and properties files, writes PNG frames,
summary plots, and an animation to output/.

Usage (from examples/frank_read/):
    python visualize.py
    python visualize.py --results frank_read_results --fps 2
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 — registers 3d projection
from matplotlib.animation import FFMpegWriter, PillowWriter


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_RESULTS = SCRIPT_DIR / "frank_read_results"
DEFAULT_OUTPUT = SCRIPT_DIR / "output"


def parse_box(path: Path) -> np.ndarray:
    """Return Nx2x3 array of box edge endpoints."""
    pts = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) >= 3:
            pts.append([float(parts[0]), float(parts[1]), float(parts[2])])
    arr = np.asarray(pts, dtype=float)
    if len(arr) < 2:
        return np.zeros((0, 2, 3))
    return arr.reshape(-1, 2, 3)


def parse_gnuplot_frame(path: Path) -> list[tuple[np.ndarray, np.ndarray]]:
    """Return list of (p1, p2) segment endpoint pairs."""
    segments = []
    pending = None
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) < 3:
            continue
        pt = np.array([float(parts[0]), float(parts[1]), float(parts[2])])
        if pending is None:
            pending = pt
        else:
            segments.append((pending, pt))
            pending = None
    return segments


def list_gnuplot_frames(gnu_dir: Path) -> list[Path]:
    frames = sorted(gnu_dir.glob("0t*"))
    return [f for f in frames if f.is_file() and not f.name.endswith(".final")]


def _set_equal_3d(ax, pts: np.ndarray, pad: float = 0.05) -> None:
    if pts.size == 0:
        return
    mins = pts.min(axis=0)
    maxs = pts.max(axis=0)
    centers = 0.5 * (mins + maxs)
    radius = 0.5 * np.max(maxs - mins)
    radius = max(radius, 1.0)
    radius *= 1.0 + pad
    for center, setter in zip(
        centers,
        [ax.set_xlim, ax.set_ylim, ax.set_zlim],
    ):
        setter(center - radius, center + radius)


def render_frame(
    segments: list[tuple[np.ndarray, np.ndarray]],
    box_edges: np.ndarray,
    title: str,
    out_path: Path,
    dpi: int = 150,
) -> None:
    fig = plt.figure(figsize=(8, 7))
    ax = fig.add_subplot(111, projection="3d")

    seg_pts = []
    for p1, p2 in segments:
        ax.plot(
            [p1[0], p2[0]],
            [p1[1], p2[1]],
            [p1[2], p2[2]],
            color="#1f77b4",
            linewidth=1.2,
            alpha=0.9,
        )
        seg_pts.extend([p1, p2])

    for edge in box_edges:
        ax.plot(
            edge[:, 0],
            edge[:, 1],
            edge[:, 2],
            color="0.55",
            linewidth=0.6,
            alpha=0.35,
        )

    if seg_pts:
        _set_equal_3d(ax, np.asarray(seg_pts))

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.set_title(title)
    ax.view_init(elev=22, azim=-58)
    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=dpi, bbox_inches="tight")
    plt.close(fig)


def load_properties(props_dir: Path) -> dict[str, np.ndarray]:
    data = {}
    for name in ("time_Plastic_strain", "density", "alleps"):
        path = props_dir / name
        if path.is_file():
            data[name] = np.loadtxt(path)
    return data


def plot_properties(props: dict[str, np.ndarray], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)

    if "time_Plastic_strain" in props:
        t_eps = props["time_Plastic_strain"]
        fig, ax = plt.subplots(figsize=(7, 4.5))
        ax.plot(t_eps[:, 0], t_eps[:, 1], "o-", markersize=3, linewidth=1.2)
        ax.set_xlabel("simulation time (s)")
        ax.set_ylabel("plastic strain")
        ax.set_title("Plastic strain vs time")
        ax.grid(True, alpha=0.3)
        fig.tight_layout()
        fig.savefig(out_dir / "plastic_strain_vs_time.png", dpi=150)
        plt.close(fig)

    if "density" in props:
        dens = props["density"]
        fig, ax = plt.subplots(figsize=(7, 4.5))
        ax.plot(dens[:, 1], dens[:, 2], "o-", markersize=3, linewidth=1.2, color="C1")
        ax.set_xlabel("strain")
        ax.set_ylabel("dislocation density (m$^{-2}$)")
        ax.set_title("Dislocation density vs strain")
        ax.grid(True, alpha=0.3)
        fig.tight_layout()
        fig.savefig(out_dir / "density_vs_strain.png", dpi=150)
        plt.close(fig)

        if "time_Plastic_strain" in props:
            t_eps = props["time_Plastic_strain"]
            fig, ax = plt.subplots(figsize=(7, 4.5))
            ax.plot(t_eps[:, 0], dens[:, 2], "o-", markersize=3, linewidth=1.2, color="C2")
            ax.set_xlabel("simulation time (s)")
            ax.set_ylabel("dislocation density (m$^{-2}$)")
            ax.set_title("Dislocation density vs time")
            ax.grid(True, alpha=0.3)
            fig.tight_layout()
            fig.savefig(out_dir / "density_vs_time.png", dpi=150)
            plt.close(fig)


def write_video(frame_paths: list[Path], out_path: Path, fps: int) -> bool:
    if not frame_paths:
        return False

    if out_path.suffix.lower() == ".gif":
        writer = PillowWriter(fps=fps)
    else:
        if shutil.which("ffmpeg") is None:
            return False
        writer = FFMpegWriter(fps=fps, bitrate=2400)

    fig, ax = plt.subplots(figsize=(8, 7))
    ax.axis("off")
    img = plt.imread(frame_paths[0])
    im = ax.imshow(img)

    def update(i):
        im.set_array(plt.imread(frame_paths[i]))
        return [im]

    from matplotlib.animation import FuncAnimation

    anim = FuncAnimation(fig, update, frames=len(frame_paths), blit=True)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        anim.save(str(out_path), writer=writer)
        plt.close(fig)
        return True
    except Exception:
        plt.close(fig)
        return False


def frame_label(path: Path) -> str:
    m = re.search(r"0t(\d+)", path.name)
    step = int(m.group(1)) if m else 0
    return f"Frank-Read source — step {step}"


def main() -> None:
    parser = argparse.ArgumentParser(description="Visualize Frank-Read ParaDiS results")
    parser.add_argument(
        "--results",
        type=Path,
        default=DEFAULT_RESULTS,
        help="Simulation results directory (default: frank_read_results)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Output directory for PNGs and videos (default: output)",
    )
    parser.add_argument("--fps", type=int, default=2, help="Animation frames per second")
    parser.add_argument("--dpi", type=int, default=150, help="PNG resolution")
    args = parser.parse_args()

    results = args.results.resolve()
    gnu_dir = results / "gnuplot"
    props_dir = results / "properties"
    out_dir = args.output.resolve()
    frames_dir = out_dir / "frames"

    if not gnu_dir.is_dir():
        raise SystemExit(f"gnuplot directory not found: {gnu_dir}")

    box_path = gnu_dir / "box.in"
    box_edges = parse_box(box_path) if box_path.is_file() else np.zeros((0, 2, 3))

    frame_files = list_gnuplot_frames(gnu_dir)
    if not frame_files:
        raise SystemExit(f"No gnuplot frames found in {gnu_dir}")

    print(f"Rendering {len(frame_files)} dislocation frames...")
    png_paths: list[Path] = []
    for frame_path in frame_files:
        segments = parse_gnuplot_frame(frame_path)
        out_png = frames_dir / f"{frame_path.name}.png"
        render_frame(
            segments,
            box_edges,
            frame_label(frame_path),
            out_png,
            dpi=args.dpi,
        )
        png_paths.append(out_png)
        print(f"  {out_png.name}")

    if props_dir.is_dir():
        print("Plotting properties...")
        plot_properties(load_properties(props_dir), out_dir)

    print("Writing animation...")
    mp4_path = out_dir / "dislocation_network.mp4"
    gif_path = out_dir / "dislocation_network.gif"

    if write_video(png_paths, mp4_path, args.fps):
        print(f"  {mp4_path}")
    else:
        print("  mp4 skipped (ffmpeg not available or write failed)")

    if write_video(png_paths, gif_path, args.fps):
        print(f"  {gif_path}")

    # Also copy a contact sheet of first/last frame
    if len(png_paths) >= 2:
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        for ax, png, label in zip(
            axes,
            [png_paths[0], png_paths[-1]],
            ["initial", "final"],
        ):
            ax.imshow(plt.imread(png))
            ax.set_title(label)
            ax.axis("off")
        fig.suptitle("Frank-Read dislocation network")
        fig.tight_layout()
        summary = out_dir / "first_vs_final.png"
        fig.savefig(summary, dpi=args.dpi, bbox_inches="tight")
        plt.close(fig)
        print(f"  {summary}")

    print(f"Done. Outputs in {out_dir}")


if __name__ == "__main__":
    main()
