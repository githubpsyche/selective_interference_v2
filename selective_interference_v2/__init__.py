"""Selective interference simulation and analysis utilities."""

from .cmr import PhasedSourceOnlyECMR, make_factory
from .fitting import load_fit_params
from .paradigm import (
    Paradigm,
    compute_n_presented,
    make_extended_break,
    make_extended_filler,
    make_extended_interference,
    make_is_emotional,
)
from .pipeline import (
    PreparedSweep,
    batch_trial,
    configure_rates,
    film_recalled_stats,
    prepare_sweep,
    run_count_sweep,
    run_sweep,
    split_scales_for_cache,
    sweep_rngs,
)
from .remapping import (
    break_extended_remap,
    filler_extended_remap,
    interference_extended_remap,
    remap_recalls,
    standard_remap,
)
from .plotting import (
    add_filler_boundary,
    light_to_dark_colors,
    plot_interference_spc,
    plot_summary_dv,
    save_figure,
)

__all__ = [
    "Paradigm",
    "PreparedSweep",
    "prepare_sweep",
    "run_count_sweep",
    "run_sweep",
    "split_scales_for_cache",
    "batch_trial",
    "configure_rates",
    "sweep_rngs",
    "remap_recalls",
    "standard_remap",
    "interference_extended_remap",
    "filler_extended_remap",
    "break_extended_remap",
    "film_recalled_stats",
    "load_fit_params",
    "PhasedSourceOnlyECMR",
    "make_factory",
    "compute_n_presented",
    "make_extended_interference",
    "make_extended_break",
    "make_extended_filler",
    "make_is_emotional",
    "plot_interference_spc",
    "plot_summary_dv",
    "add_filler_boundary",
    "light_to_dark_colors",
    "save_figure",
]
