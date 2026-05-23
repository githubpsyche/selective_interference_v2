"""Plotting helpers for selective interference simulations.

Provides convenience functions for visualizing context trajectories,
recall curves, and interference effects from selective interference
simulation results.

"""

import os
from typing import Optional, Sequence, Union

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
from matplotlib.axes import Axes
from matplotlib.transforms import blended_transform_factory

from jaxcmr.plotting import init_plot, set_plot_labels
from jaxcmr.typing import Array, Float


__all__ = [
    "PHASE_COLORS",
    "PHASE_FILLS",
    "add_phase_bands",
    "plot_interference_spc",
    "plot_summary_dv",
    "add_filler_boundary",
    "light_to_dark_colors",
    "save_figure",
]


PHASE_COLORS = {
    "film": "#1764D8",
    "break": "#3D4B5C",
    "task": "#D96B2B",
    "filler": "#3D4B5C",
    "reminder": "#178A4C",
}

PHASE_FILLS = {
    "film": "#EAF2FF",
    "break": "#F2F4F6",
    "task": "#FFF0E6",
    "filler": "#F2F4F6",
}


def light_to_dark_colors(n: int) -> list[str]:
    """Return *n* grey-scale hex codes from light to dark."""
    fracs = np.linspace(0.75, 0.10, n)
    return [f"#{int(f*255):02x}{int(f*255):02x}{int(f*255):02x}" for f in fracs]


def save_figure(figure_dir: str, figure_str: str, suffix: Optional[str] = None) -> None:
    """Save the current matplotlib figure as PNG and SVG, or just show it."""
    plt.tight_layout()
    if not figure_str:
        plt.show()
        return
    os.makedirs(figure_dir, exist_ok=True)
    suffix_str = f"_{suffix}" if suffix else ""
    base = os.path.join(figure_dir, f"{figure_str}{suffix_str}")
    plt.savefig(f"{base}.png", bbox_inches="tight", dpi=600)
    plt.savefig(f"{base}.svg", bbox_inches="tight")
    plt.show()


def add_phase_bands(
    axis: Axes,
    phase_labels: Sequence[str],
    *,
    label_y: float = 1.02,
) -> Axes:
    """Add Figure-1-style phase bands to an encoded-position plot."""
    if len(phase_labels) == 0:
        return axis

    trans = blended_transform_factory(axis.transData, axis.transAxes)
    start = 1
    current = phase_labels[0]
    for idx, phase in enumerate([*phase_labels[1:], None], start=2):
        if phase == current:
            continue
        end = idx - 1
        fill = PHASE_FILLS.get(current, "#F2F4F6")
        color = PHASE_COLORS.get(current, "#3D4B5C")
        axis.axvspan(start - 0.5, end + 0.5, color=fill, alpha=0.65, zorder=0)
        axis.text(
            (start + end) / 2,
            label_y,
            current.title(),
            ha="center",
            va="bottom",
            fontsize=10,
            fontweight="bold",
            color=color,
            transform=trans,
            clip_on=False,
        )
        start = idx
        current = phase
    return axis


def plot_interference_spc(
    spc_curves: Sequence[Float[Array, " list_length"]],
    labels: Optional[Sequence[str]] = None,
    n_film: int = 16,
    n_break: int = 0,
    n_presented: Optional[Union[int, Sequence[int]]] = None,
    color_cycle: Optional[list[str]] = None,
    contrast_name: Optional[str] = None,
    axis: Optional[Axes] = None,
    ylabel: str = "Recall Probability",
    reminder_label: Optional[str] = None,
) -> Axes:
    """Plot multi-line SPC with film / break / interference boundaries.

    Parameters
    ----------
    spc_curves : Sequence[Float[Array, " list_length"]]
        One recall-probability curve per condition.
    labels : Sequence[str], optional
        Legend label for each curve.
    n_film : int
        Number of film items (boundary position).
    n_break : int
        Number of break items shown (0 = no break zone).
    n_presented : int or Sequence[int], optional
        Number of valid study positions per curve. Positions beyond
        this are masked so the line terminates at the last real item.
        A single int applies to all curves.
    color_cycle : list[str], optional
        Colours for each curve; defaults to matplotlib colour cycle.
    contrast_name : str, optional
        Legend title passed to ``set_plot_labels``.
    axis : Axes, optional
        Matplotlib axes to plot on.
    ylabel : str
        Y-axis label.
    reminder_label : str, optional
        Label to place along the pre-/post-reminder boundary.

    Returns
    -------
    Axes

    """
    axis = init_plot(axis)
    if labels is None:
        labels = [""] * len(spc_curves)
    if color_cycle is None:
        color_cycle = [each["color"] for each in rcParams["axes.prop_cycle"]]

    list_length = len(spc_curves[0])
    positions = np.arange(1, list_length + 1)

    for i, (curve, label, color) in enumerate(
        zip(spc_curves, labels, color_cycle)
    ):
        arr = np.asarray(curve, dtype=float)
        if n_presented is not None:
            n = n_presented[i] if not isinstance(n_presented, (int, np.integer)) else n_presented
            arr[n:] = np.nan
        arr[arr == 0.0] = np.nan
        axis.plot(positions, arr, color=color, label=label, linewidth=1.5)

    # Boundary lines
    film_end = n_film + 0.5
    break_end = n_film + n_break + 0.5
    axis.axvline(x=film_end, color="red", linewidth=1.5, linestyle="--", alpha=0.7)
    if n_break > 0:
        axis.axvline(x=break_end, color="red", linewidth=1.5, linestyle="--", alpha=0.7)

    # Zone labels (data x, axes y via blended transform)
    trans = blended_transform_factory(axis.transData, axis.transAxes)
    film_mid = (1 + n_film) / 2
    axis.text(film_mid, 1.02, "Film", ha="center", va="bottom",
            fontsize=10, fontweight="bold", transform=trans, clip_on=False)
    if n_break > 0:
        break_mid = n_film + (1 + n_break) / 2
        axis.text(break_mid, 1.02, "Break", ha="center", va="bottom",
                fontsize=10, fontweight="bold", color="gray",
                transform=trans, clip_on=False)
        interf_mid = n_film + n_break + (1 + (list_length - n_film - n_break)) / 2
    else:
        interf_mid = n_film + (1 + (list_length - n_film)) / 2
    axis.text(interf_mid, 1.02, "Interference", ha="center", va="bottom",
            fontsize=10, fontweight="bold", color="red",
            transform=trans, clip_on=False)

    if reminder_label:
        reminder_x = n_film + n_break + 0.5
        axis.text(reminder_x, 0.97, reminder_label, rotation=90, ha="right", va="top",
                  fontsize=10, fontstyle="italic", color="black",
                  transform=trans, clip_on=True)

    set_plot_labels(axis, "Study Position", ylabel, contrast_name)
    return axis


def plot_summary_dv(
    x_values: Sequence[float],
    means: Sequence[float],
    ci_lower: Sequence[float],
    ci_upper: Sequence[float],
    xlabel: str = "Parameter Value",
    ylabel: str = "Film Items Recalled",
    axis: Optional[Axes] = None,
) -> Axes:
    """Plot swept parameter vs dependent variable with 95 % CI.

    Parameters
    ----------
    x_values : Sequence[float]
        Swept parameter values.
    means : Sequence[float]
        Mean DV at each value.
    ci_lower, ci_upper : Sequence[float]
        Lower and upper bounds of 95 % CI.
    xlabel, ylabel : str
        Axis labels.
    axis : Axes, optional
        Matplotlib axes.

    Returns
    -------
    Axes

    """
    axis = init_plot(axis)

    x = np.asarray(x_values)
    m = np.asarray(means)
    lo = np.asarray(ci_lower)
    hi = np.asarray(ci_upper)

    axis.fill_between(x, lo, hi, alpha=0.25, color="black")
    axis.plot(x, m, "o-", color="black", linewidth=1.5, markersize=5)

    set_plot_labels(axis, xlabel, ylabel)
    return axis


def add_filler_boundary(
    axis: Axes,
    n_film: int,
    n_interference: int,
    n_filler: int,
    n_break: int = 0,
    show_fillers: bool = True,
    reminder_label: Optional[str] = None,
) -> Axes:
    """Add filler zone boundary and relabel zones on an SPC axes.

    Parameters
    ----------
    axis : Axes
        Matplotlib axes with an existing SPC plot.
    n_film : int
        Number of film items.
    n_interference : int
        Number of interference items.
    n_filler : int
        Number of filler items.
    n_break : int
        Number of break items shown (0 = no break zone).
    show_fillers : bool
        Whether to draw the filler boundary.
    reminder_label : str, optional
        Label to place along the pre-/post-reminder boundary.

    Returns
    -------
    Axes

    """
    if not show_fillers or n_filler <= 0:
        return axis
    filler_start = n_film + n_break + n_interference + 0.5
    axis.axvline(
        x=filler_start, color="blue", linewidth=1.5, linestyle=":", alpha=0.7
    )
    for txt in list(axis.texts):
        txt.remove()
    trans = blended_transform_factory(axis.transData, axis.transAxes)
    film_mid = (1 + n_film) / 2
    interf_mid = n_film + n_break + (1 + n_interference) / 2
    filler_mid = n_film + n_break + n_interference + (1 + n_filler) / 2
    axis.text(film_mid, 1.02, "Film", ha="center", va="bottom",
            fontsize=10, fontweight="bold", transform=trans, clip_on=False)
    if n_break > 0:
        break_mid = n_film + (1 + n_break) / 2
        axis.text(break_mid, 1.02, "Break", ha="center", va="bottom",
                fontsize=10, fontweight="bold", color="gray",
                transform=trans, clip_on=False)
    axis.text(interf_mid, 1.02, "Interference", ha="center", va="bottom",
            fontsize=10, fontweight="bold", color="red",
            transform=trans, clip_on=False)
    axis.text(filler_mid, 1.02, "Filler", ha="center", va="bottom",
            fontsize=10, fontweight="bold", color="blue",
            transform=trans, clip_on=False)

    if reminder_label:
        reminder_x = n_film + n_break + 0.5
        axis.text(reminder_x, 0.97, reminder_label, rotation=90, ha="right", va="top",
                  fontsize=10, fontstyle="italic", color="black",
                  transform=trans, clip_on=True)
    return axis
