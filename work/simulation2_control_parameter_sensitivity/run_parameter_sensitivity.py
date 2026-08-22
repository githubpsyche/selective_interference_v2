#!/usr/bin/env python3
"""Run the frozen Simulation 2 retrieval-control sensitivity analysis.

The primary analysis crosses realized start-of-film drift and retrieval
monitoring over their full admissible domains while category-cue support is
zero. It retains paired Monte Carlo-batch summaries, computes declared
three-way contrasts, and renders figures only from those saved summaries.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import math
import os
import platform
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

os.environ.setdefault(
    "MPLCONFIGDIR",
    str(Path(tempfile.gettempdir()) / "selective-interference-matplotlib"),
)

import jax
import jax.numpy as jnp
from jax import random
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import numpy as np
import pandas as pd
from scipy.stats import t as student_t

from selective_interference_v2 import (
    Paradigm,
    apply_supplied_item_context_cue,
    batch_trial,
    configure_rates,
    load_fit_params,
    make_factory,
    make_is_emotional,
    make_is_target,
    prepare_sweep,
    simulate_periodic_cued_free_recall,
    split_scales_for_cache,
    standard_remap,
)


PACKAGE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = PACKAGE_DIR.parents[1]
DEFAULT_SPEC = PACKAGE_DIR / "analysis_spec.json"
DEFAULT_OUTPUT_DIR = PACKAGE_DIR / "results"
METRIC_COLUMNS = [
    "reminder_task_cost",
    "no_reminder_task_cost",
    "reminder_specific_sensitivity",
    "primary_selective_protection",
    "reminder_condition_protection",
    "no_reminder_condition_protection",
    "generic_recall_gain",
    "high_interference_gain",
    "endpoint_loss",
    "endpoint_protection",
]
PARAMETER_COLUMNS = [
    "parameter_id",
    "mechanism_family",
    "beta_start_effective",
    "beta_start_multiplier",
    "beta_source",
    "regular_grid_beta",
    "kappa",
    "monitoring_strength",
    "film_item_support_boost",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", type=Path, default=DEFAULT_SPEC)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--experiment-count", type=int)
    parser.add_argument("--batch-count", type=int)
    parser.add_argument(
        "--beta-values",
        help="Comma-separated effective beta values; token 'fitted' is allowed.",
    )
    parser.add_argument("--kappa-values", help="Comma-separated values in [0,1].")
    parser.add_argument("--cue-boost-values", help="Comma-separated values in [0,1].")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def read_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as handle:
        json.dump(value, handle, indent=2, sort_keys=True, allow_nan=False)
        handle.write("\n")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def command_output(args: list[str]) -> str | None:
    try:
        result = subprocess.run(
            args,
            cwd=PROJECT_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return result.stdout.rstrip("\n")


def package_version(name: str) -> str | None:
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return None


def parse_override(value: str | None) -> list[float | str] | None:
    if value is None:
        return None
    parsed: list[float | str] = []
    for token in value.split(","):
        token = token.strip()
        if not token:
            continue
        parsed.append("fitted" if token.lower() == "fitted" else float(token))
    if not parsed:
        raise ValueError("A parameter override cannot be empty")
    return parsed


def resolve_values(values: Iterable[float | str], fitted_beta: float) -> list[dict[str, Any]]:
    resolved: list[dict[str, Any]] = []
    for raw in values:
        source = "fitted" if raw == "fitted" else "grid"
        number = fitted_beta if source == "fitted" else float(raw)
        if not 0.0 <= number <= 1.0:
            raise ValueError(f"Parameter value outside [0, 1]: {number}")
        if any(np.isclose(number, item["value"], atol=1e-12) for item in resolved):
            continue
        resolved.append({"value": float(number), "source": source})
    return sorted(resolved, key=lambda item: item["value"])


def slug_float(value: float) -> str:
    return f"{value:.6f}".replace("-", "m").replace(".", "p")


def build_parameter_configs(
    spec: dict[str, Any],
    fitted_beta: float,
    beta_override: list[float | str] | None,
    kappa_override: list[float | str] | None,
    boost_override: list[float | str] | None,
) -> list[dict[str, Any]]:
    beta_raw = beta_override or spec["no_category_grid"]["beta_start_effective_values"]
    kappa_raw = kappa_override or spec["no_category_grid"]["kappa_values"]
    boost_raw = boost_override or spec["category_cue_comparators"][
        "film_item_support_boost_values"
    ]
    beta_values = resolve_values(beta_raw, fitted_beta)
    kappa_values = resolve_values(kappa_raw, fitted_beta)
    boost_values = resolve_values(boost_raw, fitted_beta)
    configs: list[dict[str, Any]] = []

    for beta in beta_values:
        for kappa in kappa_values:
            beta_value = beta["value"]
            kappa_value = kappa["value"]
            configs.append(
                {
                    "parameter_id": (
                        f"grid_beta_{slug_float(beta_value)}_kappa_{slug_float(kappa_value)}"
                    ),
                    "mechanism_family": spec["no_category_grid"]["mechanism_family"],
                    "beta_start_effective": beta_value,
                    "beta_start_multiplier": beta_value / fitted_beta,
                    "beta_source": beta["source"],
                    "regular_grid_beta": beta["source"] == "grid",
                    "kappa": kappa_value,
                    "monitoring_strength": 1.0 - kappa_value,
                    "film_item_support_boost": 0.0,
                }
            )

    for family in spec["category_cue_comparators"]["families"]:
        beta_raw_value = family["beta_start_effective"]
        beta_value = fitted_beta if beta_raw_value == "fitted" else float(beta_raw_value)
        beta_source = "fitted" if beta_raw_value == "fitted" else "fixed"
        kappa_value = float(family["kappa"])
        for boost in boost_values:
            boost_value = boost["value"]
            configs.append(
                {
                    "parameter_id": (
                        f"{family['mechanism_family']}_boost_{slug_float(boost_value)}"
                    ),
                    "mechanism_family": family["mechanism_family"],
                    "beta_start_effective": beta_value,
                    "beta_start_multiplier": beta_value / fitted_beta,
                    "beta_source": beta_source,
                    "regular_grid_beta": False,
                    "kappa": kappa_value,
                    "monitoring_strength": 1.0 - kappa_value,
                    "film_item_support_boost": boost_value,
                }
            )

    parameter_ids = [item["parameter_id"] for item in configs]
    if len(parameter_ids) != len(set(parameter_ids)):
        raise ValueError("Parameter IDs are not unique")
    return configs


def position_phase_labels(paradigm: Paradigm) -> list[str]:
    return (
        ["film"] * paradigm.n_film
        + ["break"] * paradigm.n_break
        + ["task"] * paradigm.n_interference
        + ["filler"] * paradigm.n_filler
    )


def cued_recall_trial(
    model,
    rng,
    film_items,
    cue_scale,
    max_recall,
    cue_interval,
    first_cue_after,
):
    recall_rng, initial_cue_rng = random.split(rng)
    model = model.start_retrieving()
    if first_cue_after == 0:
        cue_item = random.choice(initial_cue_rng, film_items)
        model = apply_supplied_item_context_cue(model, cue_item, cue_scale)
        scheduled_first_cue_after = cue_interval
    else:
        scheduled_first_cue_after = first_cue_after
    _, recalls, cue_attempts, cue_items = simulate_periodic_cued_free_recall(
        model,
        max_recall,
        recall_rng,
        film_items,
        cue_scale,
        cue_interval=cue_interval,
        first_cue_after=scheduled_first_cue_after,
    )
    return recalls, cue_attempts, cue_items


batched_cued_recall = batch_trial(cued_recall_trial, n_args=7, n_static=3)


def make_common_rngs(
    master_seed: int,
    n_subjects: int,
    experiment_count: int,
    batch_count: int,
) -> tuple[jax.Array, np.ndarray, list[dict[str, Any]]]:
    if experiment_count % batch_count:
        raise ValueError("experiment_count must be divisible by batch_count")
    per_batch = experiment_count // batch_count
    keys = []
    seed_rows = []
    for batch_id in range(batch_count):
        root_key = random.fold_in(random.PRNGKey(master_seed), batch_id)
        batch_keys = random.split(root_key, n_subjects * per_batch).reshape(
            n_subjects, per_batch, -1
        )
        keys.append(batch_keys)
        seed_rows.append(
            {
                "batch_id": batch_id,
                "fold_in_index": batch_id,
                "root_key_uint32": [int(value) for value in np.asarray(root_key)],
                "replications_per_subject": per_batch,
            }
        )
    rngs = jnp.concatenate(keys, axis=1)
    replication_index = np.tile(np.arange(experiment_count), n_subjects)
    batch_ids = replication_index // per_batch
    return rngs, batch_ids, seed_rows


def spc_from_recalls(recalls: np.ndarray, n_presented: int) -> np.ndarray:
    return (
        np.bincount(recalls.reshape(-1), minlength=n_presented + 1)[1 : n_presented + 1]
        / recalls.shape[0]
    )


def transition_counts(recalls: np.ndarray, n_film: int) -> tuple[int, int]:
    current = recalls[:, :-1]
    following = recalls[:, 1:]
    valid = (current > 0) & (following > 0)
    current_is_film = (current >= 1) & (current <= n_film)
    following_is_film = (following >= 1) & (following <= n_film)
    film_seen_before_following = np.cumsum(current_is_film, axis=1)
    eligible = valid & ~current_is_film & (film_seen_before_following < n_film)
    denominator = int(np.sum(eligible))
    numerator = int(np.sum(eligible & following_is_film))
    return numerator, denominator


def batch_metrics(
    recalls: np.ndarray,
    batch_ids: np.ndarray,
    paradigm: Paradigm,
    parameter: dict[str, Any],
    condition: dict[str, Any],
    batch_count: int,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    phase_bounds = {
        "film": (1, paradigm.n_film),
        "break": (paradigm.n_film + 1, paradigm.n_film + paradigm.n_break),
        "task": (
            paradigm.n_film + paradigm.n_break + 1,
            paradigm.n_film + paradigm.n_break + paradigm.n_interference,
        ),
        "filler": (
            paradigm.n_film + paradigm.n_break + paradigm.n_interference + 1,
            paradigm.list_length,
        ),
    }
    for batch_id in range(batch_count):
        subset = recalls[batch_ids == batch_id]
        spc = spc_from_recalls(subset, paradigm.list_length)
        numerator, denominator = transition_counts(subset, paradigm.n_film)
        first_output = subset[:, 0]
        row: dict[str, Any] = {
            **{name: parameter[name] for name in PARAMETER_COLUMNS},
            "condition_id": condition["condition_id"],
            "reminder_condition": condition["reminder_condition"],
            "task_condition": condition["task_condition"],
            "batch_id": batch_id,
            "n_trials": int(subset.shape[0]),
            "film_early_probability": float(np.mean(spc[0:5])),
            "film_middle_probability": float(np.mean(spc[5:11])),
            "film_late_probability": float(np.mean(spc[11:16])),
            "first_output_film_probability": float(
                np.mean((first_output >= 1) & (first_output <= paradigm.n_film))
            ),
            "offtarget_to_film_numerator": numerator,
            "offtarget_to_film_denominator": denominator,
            "offtarget_to_film_probability": (
                float(numerator / denominator) if denominator else np.nan
            ),
            "mean_output_count": float(np.mean(np.sum(subset > 0, axis=1))),
        }
        for phase, (lower, upper) in phase_bounds.items():
            per_trial = np.sum((subset >= lower) & (subset <= upper), axis=1)
            row[f"{phase}_items_recalled"] = float(np.mean(per_trial))
        rows.append(row)
    return rows


def prepare_conditions(
    params: dict[str, jax.Array],
    paradigm: Paradigm,
    factory,
    spec: dict[str, Any],
) -> dict[str, Any]:
    prepared: dict[str, Any] = {}
    for condition in spec["conditions"]:
        fixed = {
            **spec["fixed_scales"],
            "reminder_start_drift_scale": condition["reminder_start_drift_scale"],
            "reminder_drift_scale": condition["reminder_drift_scale"],
            "interference_mcf_scale": condition["task_mcf_scale"],
        }
        pre_cache, _ = split_scales_for_cache(fixed, spec["simulation"]["cache_after"])
        prepared[condition["condition_id"]] = prepare_sweep(
            params,
            paradigm,
            factory,
            cache_after=spec["simulation"]["cache_after"],
            **pre_cache,
        )
    return prepared


def run_simulations(
    spec: dict[str, Any],
    params: dict[str, jax.Array],
    paradigm: Paradigm,
    parameter_configs: list[dict[str, Any]],
    common_rngs: jax.Array,
    batch_ids: np.ndarray,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    factory = make_factory(
        is_emotional=make_is_emotional(
            paradigm,
            film_emotional=spec["simulation"]["film_emotional"],
            interference_emotional=spec["simulation"]["interference_emotional"],
        ),
        is_target=make_is_target(paradigm),
    )
    prepared = prepare_conditions(params, paradigm, factory, spec)
    position_phase = position_phase_labels(paradigm)
    cell_rows: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []
    spc_rows: list[dict[str, Any]] = []
    total = len(parameter_configs)
    started = time.monotonic()

    for parameter_index, parameter in enumerate(parameter_configs, start=1):
        if parameter_index == 1 or parameter_index % 10 == 0 or parameter_index == total:
            elapsed = time.monotonic() - started
            print(
                f"Parameter configuration {parameter_index}/{total} "
                f"({parameter['parameter_id']}); elapsed {elapsed / 60:.1f} min",
                flush=True,
            )
        for condition in spec["conditions"]:
            fixed = {
                **spec["fixed_scales"],
                "reminder_start_drift_scale": condition[
                    "reminder_start_drift_scale"
                ],
                "reminder_drift_scale": condition["reminder_drift_scale"],
                "interference_mcf_scale": condition["task_mcf_scale"],
            }
            _, post_cache = split_scales_for_cache(
                fixed, spec["simulation"]["cache_after"]
            )
            ready_models = configure_rates(
                prepared[condition["condition_id"]].models,
                **post_cache,
                start_drift_scale=parameter["beta_start_multiplier"],
                rejected_recall_drift_scale=parameter["kappa"],
                film_item_support_boost=parameter["film_item_support_boost"],
            )
            recalls, _, _ = batched_cued_recall(
                ready_models,
                common_rngs,
                paradigm.film_items,
                spec["external_recall_cues"]["film_cue_reinstatement"],
                paradigm.max_recall,
                spec["external_recall_cues"]["cue_interval"],
                spec["external_recall_cues"]["first_cue_after"],
            )
            raw_recalls = np.asarray(recalls).reshape(-1, recalls.shape[-1])
            remapped = np.asarray(
                standard_remap(raw_recalls, paradigm, show_break=True)
            )
            realized_beta = float(np.asarray(ready_models.start_drift_rate)[0])
            realized_kappa = float(
                np.asarray(ready_models.rejected_recall_drift_scale)[0]
            )
            realized_boost = float(np.asarray(ready_models.film_item_support_boost)[0])
            cell_id = f"{parameter['parameter_id']}__{condition['condition_id']}"
            cell_rows.append(
                {
                    "cell_id": cell_id,
                    **{name: parameter[name] for name in PARAMETER_COLUMNS},
                    "condition_id": condition["condition_id"],
                    "reminder_condition": condition["reminder_condition"],
                    "task_condition": condition["task_condition"],
                    "reminder_start_drift_scale": condition[
                        "reminder_start_drift_scale"
                    ],
                    "reminder_drift_scale": condition["reminder_drift_scale"],
                    "task_mcf_scale": condition["task_mcf_scale"],
                    "realized_beta_start_effective": realized_beta,
                    "realized_kappa": realized_kappa,
                    "realized_film_item_support_boost": realized_boost,
                    "n_subject_parameter_sets": int(recalls.shape[0]),
                    "experiment_count_per_parameter_set": paradigm.experiment_count,
                    "n_trials": int(remapped.shape[0]),
                }
            )
            summary_rows.extend(
                batch_metrics(
                    remapped,
                    batch_ids,
                    paradigm,
                    parameter,
                    condition,
                    spec["simulation"]["batch_count"],
                )
            )
            spc = spc_from_recalls(remapped, paradigm.list_length)
            for position, probability in enumerate(spc, start=1):
                spc_rows.append(
                    {
                        **{name: parameter[name] for name in PARAMETER_COLUMNS},
                        "condition_id": condition["condition_id"],
                        "reminder_condition": condition["reminder_condition"],
                        "task_condition": condition["task_condition"],
                        "position": position,
                        "phase": position_phase[position - 1],
                        "recall_probability": float(probability),
                    }
                )
    return pd.DataFrame(cell_rows), pd.DataFrame(summary_rows), pd.DataFrame(spc_rows)


def condition_values(rows: pd.DataFrame, value_column: str) -> dict[str, float]:
    if rows["condition_id"].nunique() != 4:
        raise ValueError("Every estimand requires all four experimental cells")
    return {
        str(row.condition_id): float(getattr(row, value_column))
        for row in rows.itertuples(index=False)
    }


def compute_estimand_batches(batch_df: pd.DataFrame) -> pd.DataFrame:
    baseline = batch_df[
        (batch_df["mechanism_family"] == "no_category_grid")
        & np.isclose(batch_df["beta_start_effective"], 0.0)
        & np.isclose(batch_df["kappa"], 1.0)
        & np.isclose(batch_df["film_item_support_boost"], 0.0)
    ]
    if baseline.empty:
        raise ValueError("The no-control baseline is missing")
    baseline_by_batch = {
        int(batch_id): condition_values(group, "film_items_recalled")
        for batch_id, group in baseline.groupby("batch_id", sort=True)
    }
    rows: list[dict[str, Any]] = []
    for (parameter_id, batch_id), group in batch_df.groupby(
        ["parameter_id", "batch_id"], sort=False
    ):
        candidate = condition_values(group, "film_items_recalled")
        unguided = baseline_by_batch[int(batch_id)]
        c_no = candidate["no_reminder_weak"] - candidate["no_reminder_strong"]
        c_rem = candidate["reminder_weak"] - candidate["reminder_strong"]
        u_no = unguided["no_reminder_weak"] - unguided["no_reminder_strong"]
        u_rem = unguided["reminder_weak"] - unguided["reminder_strong"]
        sensitivity = c_rem - c_no
        baseline_sensitivity = u_rem - u_no
        candidate_endpoint_loss = (
            candidate["no_reminder_weak"] - candidate["reminder_strong"]
        )
        baseline_endpoint_loss = (
            unguided["no_reminder_weak"] - unguided["reminder_strong"]
        )
        first = group.iloc[0]
        rows.append(
            {
                **{name: first[name] for name in PARAMETER_COLUMNS},
                "batch_id": int(batch_id),
                "n_trials_per_condition": int(first["n_trials"]),
                "film_no_reminder_weak": candidate["no_reminder_weak"],
                "film_no_reminder_strong": candidate["no_reminder_strong"],
                "film_reminder_weak": candidate["reminder_weak"],
                "film_reminder_strong": candidate["reminder_strong"],
                "baseline_reminder_specific_sensitivity": baseline_sensitivity,
                "baseline_endpoint_loss": baseline_endpoint_loss,
                "reminder_task_cost": c_rem,
                "no_reminder_task_cost": c_no,
                "reminder_specific_sensitivity": sensitivity,
                "primary_selective_protection": baseline_sensitivity - sensitivity,
                "reminder_condition_protection": u_rem - c_rem,
                "no_reminder_condition_protection": u_no - c_no,
                "generic_recall_gain": (
                    candidate["no_reminder_weak"] - unguided["no_reminder_weak"]
                ),
                "high_interference_gain": (
                    candidate["reminder_strong"] - unguided["reminder_strong"]
                ),
                "endpoint_loss": candidate_endpoint_loss,
                "endpoint_protection": baseline_endpoint_loss - candidate_endpoint_loss,
            }
        )
    return pd.DataFrame(rows)


def summarize_estimands(estimand_batches: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for parameter_id, group in estimand_batches.groupby("parameter_id", sort=False):
        first = group.iloc[0]
        n_batches = len(group)
        t_critical = float(student_t.ppf(0.975, n_batches - 1))
        row: dict[str, Any] = {
            **{name: first[name] for name in PARAMETER_COLUMNS},
            "n_batches": n_batches,
            "n_trials_per_condition": int(group["n_trials_per_condition"].sum()),
            "primary_positive_batch_fraction": float(
                np.mean(group["primary_selective_protection"] > 0)
            ),
        }
        for metric in METRIC_COLUMNS + ["baseline_reminder_specific_sensitivity"]:
            values = group[metric].to_numpy(dtype=float)
            mean = float(np.mean(values))
            sd = float(np.std(values, ddof=1)) if n_batches > 1 else np.nan
            se = sd / math.sqrt(n_batches) if n_batches > 1 else np.nan
            half_width = t_critical * se if n_batches > 1 else np.nan
            row[f"{metric}_mean"] = mean
            row[f"{metric}_sd"] = sd
            row[f"{metric}_se"] = se
            row[f"{metric}_ci_low"] = mean - half_width
            row[f"{metric}_ci_high"] = mean + half_width
        rows.append(row)
    return pd.DataFrame(rows)


def select_parameter(
    frame: pd.DataFrame,
    family: str,
    beta: float,
    kappa: float,
    boost: float,
) -> str:
    matches = frame[
        (frame["mechanism_family"] == family)
        & np.isclose(frame["beta_start_effective"], beta, atol=1e-8)
        & np.isclose(frame["kappa"], kappa, atol=1e-8)
        & np.isclose(frame["film_item_support_boost"], boost, atol=1e-8)
    ]
    if len(matches) != 1:
        raise ValueError(
            f"Expected one representative match for {family}, beta={beta}, "
            f"kappa={kappa}, boost={boost}; found {len(matches)}"
        )
    return str(matches.iloc[0]["parameter_id"])


def representative_settings(
    summary: pd.DataFrame, fitted_beta: float
) -> list[dict[str, str]]:
    declarations = [
        ("No control", "no_category_grid", 0.0, 1.0, 0.0),
        ("Start reinstatement", "no_category_grid", fitted_beta, 1.0, 0.0),
        ("Monitoring", "no_category_grid", 0.0, 0.0, 0.0),
        ("Start + monitoring", "no_category_grid", fitted_beta, 0.0, 0.0),
        ("Category cue", "category_cue_only", 0.0, 1.0, 1.0),
        (
            "All three controls",
            "category_cue_plus_current_other_controls",
            fitted_beta,
            0.0,
            1.0,
        ),
    ]
    return [
        {
            "representative_setting": label,
            "parameter_id": select_parameter(summary, family, beta, kappa, boost),
        }
        for label, family, beta, kappa, boost in declarations
    ]


def summarize_representatives(
    batch_df: pd.DataFrame,
    estimand_summary: pd.DataFrame,
    settings: list[dict[str, str]],
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    diagnostic_metrics = [
        "film_items_recalled",
        "film_early_probability",
        "film_middle_probability",
        "film_late_probability",
        "first_output_film_probability",
        "offtarget_to_film_probability",
        "mean_output_count",
    ]
    for setting in settings:
        parameter_id = setting["parameter_id"]
        group = batch_df[
            (batch_df["parameter_id"] == parameter_id)
            & (batch_df["condition_id"] == "reminder_strong")
        ]
        estimate = estimand_summary[estimand_summary["parameter_id"] == parameter_id].iloc[0]
        first = group.iloc[0]
        n_batches = len(group)
        t_critical = float(student_t.ppf(0.975, n_batches - 1))
        row: dict[str, Any] = {
            **setting,
            **{name: first[name] for name in PARAMETER_COLUMNS if name != "parameter_id"},
            "n_batches": n_batches,
            "primary_selective_protection_mean": estimate[
                "primary_selective_protection_mean"
            ],
            "primary_selective_protection_ci_low": estimate[
                "primary_selective_protection_ci_low"
            ],
            "primary_selective_protection_ci_high": estimate[
                "primary_selective_protection_ci_high"
            ],
        }
        for metric in diagnostic_metrics:
            values = group[metric].to_numpy(dtype=float)
            mean = float(np.nanmean(values))
            sd = float(np.nanstd(values, ddof=1))
            se = sd / math.sqrt(n_batches)
            half_width = t_critical * se
            row[f"{metric}_mean"] = mean
            row[f"{metric}_ci_low"] = mean - half_width
            row[f"{metric}_ci_high"] = mean + half_width
        rows.append(row)
    return pd.DataFrame(rows)


def render_figure(
    summary: pd.DataFrame,
    batch_df: pd.DataFrame,
    spc_df: pd.DataFrame,
    representatives: list[dict[str, str]],
    fitted_beta: float,
    output_dir: Path,
) -> list[Path]:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 9,
            "axes.titlesize": 10,
            "axes.labelsize": 9,
            "legend.fontsize": 8,
        }
    )
    fig, axes = plt.subplots(2, 2, figsize=(10.2, 8.0), constrained_layout=True)
    axis_a, axis_b, axis_c, axis_d = axes.flat

    regular = summary[
        (summary["mechanism_family"] == "no_category_grid")
        & summary["regular_grid_beta"].astype(bool)
    ].copy()
    beta_values = sorted(regular["beta_start_effective"].unique())
    monitoring_values = sorted(regular["monitoring_strength"].unique())
    surface = regular.pivot(
        index="monitoring_strength",
        columns="beta_start_effective",
        values="primary_selective_protection_mean",
    ).reindex(index=monitoring_values, columns=beta_values)
    abs_bound = max(abs(float(np.nanmin(surface))), abs(float(np.nanmax(surface))), 1e-6)
    heatmap = axis_a.pcolormesh(
        beta_values,
        monitoring_values,
        surface.to_numpy(),
        shading="nearest",
        cmap="RdBu_r",
        vmin=-abs_bound,
        vmax=abs_bound,
    )
    axis_a.scatter(
        [fitted_beta],
        [1.0],
        marker="*",
        s=90,
        color="black",
        edgecolor="white",
        linewidth=0.6,
        label="Current no-cue setting",
        zorder=4,
    )
    axis_a.set(
        xlabel=r"Effective start drift, $\beta_{start}$",
        ylabel=r"Monitoring strength, $1-\kappa$",
        title="A  Selective-protection surface (category cue absent)",
        xlim=(-0.03, 1.03),
        ylim=(-0.03, 1.03),
    )
    axis_a.legend(frameon=False, loc="upper left")
    fig.colorbar(heatmap, ax=axis_a, shrink=0.86)

    no_category = summary[summary["mechanism_family"] == "no_category_grid"]
    scatter = axis_b.scatter(
        no_category["generic_recall_gain_mean"],
        no_category["primary_selective_protection_mean"],
        c=no_category["beta_start_effective"],
        s=18 + 32 * no_category["monitoring_strength"],
        cmap="viridis",
        norm=Normalize(0, 1),
        alpha=0.72,
        linewidth=0,
        label="No-category grid",
    )
    comparator_styles = {
        "category_cue_only": ("#D55E00", "Category cue alone"),
        "category_cue_plus_current_other_controls": (
            "#7A3E9D",
            "Cue + current other controls",
        ),
    }
    for family, (color, label) in comparator_styles.items():
        curve = summary[summary["mechanism_family"] == family].sort_values(
            "film_item_support_boost"
        )
        axis_b.plot(
            curve["generic_recall_gain_mean"],
            curve["primary_selective_protection_mean"],
            color=color,
            marker="o",
            markersize=3.5,
            linewidth=1.6,
            label=label,
        )
    axis_b.axhline(0, color="#777777", linewidth=0.8, linestyle="--")
    axis_b.axvline(0, color="#BBBBBB", linewidth=0.7, linestyle=":")
    axis_b.set(
        xlabel="Generic film-recall gain, G",
        ylabel="Three-way selective protection, P",
        title="B  Protection is reported separately from generic lift",
    )
    axis_b.legend(frameon=False, loc="best")
    cbar = fig.colorbar(scatter, ax=axis_b, shrink=0.86)
    cbar.set_label(r"Effective $\beta_{start}$ (point size = monitoring)")

    representative_lookup = {
        item["representative_setting"]: item["parameter_id"] for item in representatives
    }
    line_styles = {
        "No control": ("#666666", "--"),
        "Start reinstatement": ("#0072B2", "-"),
        "Monitoring": ("#009E73", "-"),
        "Category cue": ("#D55E00", "-"),
    }
    for label, (color, linestyle) in line_styles.items():
        curve = spc_df[
            (spc_df["parameter_id"] == representative_lookup[label])
            & (spc_df["condition_id"] == "reminder_strong")
            & (spc_df["phase"] == "film")
        ].sort_values("position")
        axis_c.plot(
            curve["position"],
            curve["recall_probability"],
            label=label,
            color=color,
            linestyle=linestyle,
            linewidth=1.6,
        )
    axis_c.set(
        xlabel="Film input position",
        ylabel="Recall probability",
        title="C  Input-position signatures in the high-interference cell",
        xlim=(1, 16),
    )
    axis_c.set_xticks([1, 4, 8, 12, 16])
    axis_c.legend(frameon=False, ncol=2)

    high = batch_df[
        (batch_df["mechanism_family"] == "no_category_grid")
        & (batch_df["condition_id"] == "reminder_strong")
    ]
    for beta, color, label in [
        (0.0, "#666666", r"$\beta_{start}=0$"),
        (fitted_beta, "#0072B2", r"$\beta_{start}=$ fitted"),
    ]:
        curve = high[np.isclose(high["beta_start_effective"], beta)].groupby(
            "monitoring_strength", as_index=False
        )["offtarget_to_film_probability"].agg(["mean", "std", "count"]).reset_index()
        curve["se"] = curve["std"] / np.sqrt(curve["count"])
        axis_d.plot(
            curve["monitoring_strength"],
            curve["mean"],
            color=color,
            marker="o",
            markersize=3.5,
            linewidth=1.6,
            label=label,
        )
        axis_d.fill_between(
            curve["monitoring_strength"],
            curve["mean"] - 1.96 * curve["se"],
            curve["mean"] + 1.96 * curve["se"],
            color=color,
            alpha=0.14,
            linewidth=0,
        )
    axis_d.set(
        xlabel=r"Monitoring strength, $1-\kappa$",
        ylabel="P(next output is film | current output is non-film)",
        title="D  Output-transition signature of monitoring",
        xlim=(-0.03, 1.03),
        ylim=(0, None),
    )
    axis_d.legend(frameon=False)

    for axis in axes.flat:
        axis.spines["top"].set_visible(False)
        axis.spines["right"].set_visible(False)
        axis.grid(axis="y", color="#E5E5E5", linewidth=0.5, zorder=0)

    output_paths = [
        output_dir / "parameter_sensitivity.png",
        output_dir / "parameter_sensitivity.svg",
        output_dir / "parameter_sensitivity.pdf",
    ]
    fig.savefig(output_paths[0], dpi=300, bbox_inches="tight")
    fig.savefig(output_paths[1], bbox_inches="tight")
    fig.savefig(output_paths[2], bbox_inches="tight")
    plt.close(fig)
    return output_paths


def render_contrast_figure(
    summary: pd.DataFrame,
    fitted_beta: float,
    output_dir: Path,
) -> list[Path]:
    regular = summary[
        (summary["mechanism_family"] == "no_category_grid")
        & summary["regular_grid_beta"].astype(bool)
    ].copy()
    beta_values = sorted(regular["beta_start_effective"].unique())
    monitoring_values = sorted(regular["monitoring_strength"].unique())
    panels = [
        (
            "primary_selective_protection_mean",
            "A  Reminder-specific three-way protection",
        ),
        (
            "reminder_condition_protection_mean",
            "B  Protection within the reminder condition",
        ),
        (
            "endpoint_protection_mean",
            "C  Low-to-high endpoint protection",
        ),
    ]
    fig, axes = plt.subplots(1, 3, figsize=(12.4, 3.8), constrained_layout=True)
    for axis, (metric, title) in zip(axes, panels, strict=True):
        surface = regular.pivot(
            index="monitoring_strength",
            columns="beta_start_effective",
            values=metric,
        ).reindex(index=monitoring_values, columns=beta_values)
        bound = max(
            abs(float(np.nanmin(surface))),
            abs(float(np.nanmax(surface))),
            1e-6,
        )
        image = axis.pcolormesh(
            beta_values,
            monitoring_values,
            surface.to_numpy(),
            shading="nearest",
            cmap="RdBu_r",
            vmin=-bound,
            vmax=bound,
        )
        axis.scatter(
            [fitted_beta],
            [1.0],
            marker="*",
            s=75,
            color="black",
            edgecolor="white",
            linewidth=0.5,
            zorder=4,
        )
        axis.set(
            xlabel=r"Effective start drift, $\beta_{start}$",
            title=title,
            xlim=(-0.03, 1.03),
            ylim=(-0.03, 1.03),
        )
        axis.spines["top"].set_visible(False)
        axis.spines["right"].set_visible(False)
        fig.colorbar(image, ax=axis, shrink=0.82, label="Protection (film items)")
    axes[0].set_ylabel(r"Monitoring strength, $1-\kappa$")
    fig.suptitle(
        "Same parameter grid, three non-equivalent definitions of protection",
        fontsize=11,
        fontweight="bold",
    )
    output_paths = [
        output_dir / "contrast_sensitivity.png",
        output_dir / "contrast_sensitivity.svg",
        output_dir / "contrast_sensitivity.pdf",
    ]
    fig.savefig(output_paths[0], dpi=300, bbox_inches="tight")
    fig.savefig(output_paths[1], bbox_inches="tight")
    fig.savefig(output_paths[2], bbox_inches="tight")
    plt.close(fig)
    return output_paths


def row_as_dict(row: pd.Series, fields: list[str]) -> dict[str, float]:
    return {field: float(row[field]) for field in fields}


def build_robustness_summary(
    summary: pd.DataFrame, fitted_beta: float, regular_grid_size: int
) -> dict[str, Any]:
    grid = summary[
        (summary["mechanism_family"] == "no_category_grid")
        & summary["regular_grid_beta"].astype(bool)
    ].copy()
    maximum = grid.loc[grid["primary_selective_protection_mean"].idxmax()]
    minimum = grid.loc[grid["primary_selective_protection_mean"].idxmin()]
    maximum_reminder = grid.loc[grid["reminder_condition_protection_mean"].idxmax()]
    maximum_endpoint = grid.loc[grid["endpoint_protection_mean"].idxmax()]
    current = summary[
        (summary["mechanism_family"] == "no_category_grid")
        & np.isclose(summary["beta_start_effective"], fitted_beta)
        & np.isclose(summary["kappa"], 0.0)
    ].iloc[0]
    category_only = summary[
        (summary["mechanism_family"] == "category_cue_only")
        & np.isclose(summary["film_item_support_boost"], 1.0)
    ].iloc[0]
    full = summary[
        (summary["mechanism_family"] == "category_cue_plus_current_other_controls")
        & np.isclose(summary["film_item_support_boost"], 1.0)
    ].iloc[0]
    fields = [
        "beta_start_effective",
        "kappa",
        "monitoring_strength",
        "film_item_support_boost",
        "primary_selective_protection_mean",
        "primary_selective_protection_ci_low",
        "primary_selective_protection_ci_high",
        "generic_recall_gain_mean",
        "high_interference_gain_mean",
        "reminder_condition_protection_mean",
        "reminder_condition_protection_ci_low",
        "reminder_condition_protection_ci_high",
        "endpoint_protection_mean",
        "endpoint_protection_ci_low",
        "endpoint_protection_ci_high",
    ]
    return {
        "regular_grid_point_count": int(len(grid)),
        "declared_regular_grid_point_count": int(regular_grid_size),
        "points_with_positive_mean_protection": int(
            np.sum(grid["primary_selective_protection_mean"] > 0)
        ),
        "fraction_with_positive_mean_protection": float(
            np.mean(grid["primary_selective_protection_mean"] > 0)
        ),
        "points_with_95pct_mc_interval_above_zero": int(
            np.sum(grid["primary_selective_protection_ci_low"] > 0)
        ),
        "fraction_with_95pct_mc_interval_above_zero": float(
            np.mean(grid["primary_selective_protection_ci_low"] > 0)
        ),
        "points_with_positive_reminder_condition_protection": int(
            np.sum(grid["reminder_condition_protection_mean"] > 0)
        ),
        "points_with_reminder_condition_95pct_mc_interval_above_zero": int(
            np.sum(grid["reminder_condition_protection_ci_low"] > 0)
        ),
        "points_with_positive_endpoint_protection": int(
            np.sum(grid["endpoint_protection_mean"] > 0)
        ),
        "points_with_endpoint_95pct_mc_interval_above_zero": int(
            np.sum(grid["endpoint_protection_ci_low"] > 0)
        ),
        "maximum_no_category_grid": row_as_dict(maximum, fields),
        "minimum_no_category_grid": row_as_dict(minimum, fields),
        "maximum_reminder_condition_protection": row_as_dict(
            maximum_reminder, fields
        ),
        "maximum_endpoint_protection": row_as_dict(maximum_endpoint, fields),
        "current_no_category_setting": row_as_dict(current, fields),
        "category_cue_only_at_boost_1": row_as_dict(category_only, fields),
        "all_three_controls_at_boost_1": row_as_dict(full, fields),
        "interpretation": (
            "The surface describes existence, magnitude, and Monte Carlo stability. "
            "It does not impose a post-hoc threshold for psychological sufficiency."
        ),
    }


def write_results_markdown(path: Path, robust: dict[str, Any]) -> None:
    max_row = robust["maximum_no_category_grid"]
    current = robust["current_no_category_setting"]
    cue = robust["category_cue_only_at_boost_1"]
    full = robust["all_three_controls_at_boost_1"]
    reminder = robust["maximum_reminder_condition_protection"]
    endpoint = robust["maximum_endpoint_protection"]
    text = f"""# Sensitivity-analysis results

The declared regular no-category grid contained
{robust['regular_grid_point_count']} start-reinstatement × monitoring settings.
Positive mean selective protection occurred at
{robust['points_with_positive_mean_protection']} settings
({100 * robust['fraction_with_positive_mean_protection']:.1f}%). The paired 95%
Monte Carlo interval was entirely above zero at
{robust['points_with_95pct_mc_interval_above_zero']} settings
({100 * robust['fraction_with_95pct_mc_interval_above_zero']:.1f}%).

The largest no-category value was P =
{max_row['primary_selective_protection_mean']:.3f}
[{max_row['primary_selective_protection_ci_low']:.3f},
{max_row['primary_selective_protection_ci_high']:.3f}] at effective
beta_start = {max_row['beta_start_effective']:.3f} and kappa =
{max_row['kappa']:.3f}. Its generic recall gain was
G = {max_row['generic_recall_gain_mean']:.3f} items.

The simpler contrasts do reveal technical protection. Within the reminder
condition, {robust['points_with_positive_reminder_condition_protection']} of
121 settings had a positive mean value and
{robust['points_with_reminder_condition_95pct_mc_interval_above_zero']} had a
95% Monte Carlo interval entirely above zero. The maximum was
P_rem = {reminder['reminder_condition_protection_mean']:.3f}
[{reminder['reminder_condition_protection_ci_low']:.3f},
{reminder['reminder_condition_protection_ci_high']:.3f}] at effective
beta_start = {reminder['beta_start_effective']:.3f}, kappa =
{reminder['kappa']:.3f}.

For the low-to-high endpoint contrast displayed in the current decomposition
figure, {robust['points_with_positive_endpoint_protection']} of 121 settings
had positive mean endpoint protection and
{robust['points_with_endpoint_95pct_mc_interval_above_zero']} had an interval
entirely above zero. The maximum was
P_endpoint = {endpoint['endpoint_protection_mean']:.3f}
[{endpoint['endpoint_protection_ci_low']:.3f},
{endpoint['endpoint_protection_ci_high']:.3f}] at effective beta_start =
{endpoint['beta_start_effective']:.3f}, kappa = {endpoint['kappa']:.3f}; its
generic recall gain was G = {endpoint['generic_recall_gain_mean']:.3f}.

Thus, a setting can look modestly protective under the reminder-only or
endpoint contrast while failing the reminder-specific three-way criterion.
Those secondary contrasts must not be relabeled as the selective-interference
interaction.

At the manuscript's current no-category combination (fitted effective
beta_start plus maximal monitoring), P =
{current['primary_selective_protection_mean']:.3f}
[{current['primary_selective_protection_ci_low']:.3f},
{current['primary_selective_protection_ci_high']:.3f}] and G =
{current['generic_recall_gain_mean']:.3f}.

For the declared outcome-space comparators, the category cue alone at support
1 produced P = {cue['primary_selective_protection_mean']:.3f} and G =
{cue['generic_recall_gain_mean']:.3f}; all three controls produced P =
{full['primary_selective_protection_mean']:.3f} and G =
{full['generic_recall_gain_mean']:.3f}.

These are simulation outcomes under the fixed fitted base regime. The correct
claim is bounded to the evaluated grid. Positive P establishes that a setting
can produce the target contrast; the joint P-versus-G display is needed to
judge whether that protection is selective or accompanies a broad recall
increase. Monte Carlo intervals do not represent empirical or fitted-parameter
uncertainty.
"""
    path.write_text(text)


def internal_verification(
    cell_df: pd.DataFrame,
    batch_df: pd.DataFrame,
    spc_df: pd.DataFrame,
    estimand_batches: pd.DataFrame,
    parameter_configs: list[dict[str, Any]],
    spec: dict[str, Any],
    fitted_beta: float,
) -> dict[str, Any]:
    expected_cells = len(parameter_configs) * len(spec["conditions"])
    expected_batch_rows = expected_cells * spec["simulation"]["batch_count"]
    expected_spc_rows = expected_cells * (
        spec["simulation"]["n_film"]
        + spec["simulation"]["n_break"]
        + spec["simulation"]["n_interference"]
        + spec["simulation"]["n_filler"]
    )
    baseline_id = select_parameter(
        pd.DataFrame(parameter_configs), "no_category_grid", 0.0, 1.0, 0.0
    )
    category_zero_id = select_parameter(
        pd.DataFrame(parameter_configs), "category_cue_only", 0.0, 1.0, 0.0
    )
    current_grid_id = select_parameter(
        pd.DataFrame(parameter_configs),
        "no_category_grid",
        fitted_beta,
        0.0,
        0.0,
    )
    current_comparator_zero_id = select_parameter(
        pd.DataFrame(parameter_configs),
        "category_cue_plus_current_other_controls",
        fitted_beta,
        0.0,
        0.0,
    )

    def duplicate_difference(first_id: str, second_id: str) -> float:
        columns = ["condition_id", "batch_id", "film_items_recalled"]
        first = batch_df[batch_df["parameter_id"] == first_id][columns].sort_values(
            ["condition_id", "batch_id"]
        )
        second = batch_df[batch_df["parameter_id"] == second_id][columns].sort_values(
            ["condition_id", "batch_id"]
        )
        return float(
            np.max(
                np.abs(
                    first["film_items_recalled"].to_numpy()
                    - second["film_items_recalled"].to_numpy()
                )
            )
        )

    identity_error = float(
        np.max(
            np.abs(
                estimand_batches["primary_selective_protection"]
                - (
                    estimand_batches["baseline_reminder_specific_sensitivity"]
                    - estimand_batches["reminder_specific_sensitivity"]
                )
            )
        )
    )
    endpoint_identity_error = float(
        np.max(
            np.abs(
                estimand_batches["endpoint_protection"]
                - (
                    estimand_batches["baseline_endpoint_loss"]
                    - estimand_batches["endpoint_loss"]
                )
            )
        )
    )
    checks = {
        "cell_count": {
            "observed": int(len(cell_df)),
            "expected": expected_cells,
            "pass": len(cell_df) == expected_cells,
        },
        "batch_row_count": {
            "observed": int(len(batch_df)),
            "expected": expected_batch_rows,
            "pass": len(batch_df) == expected_batch_rows,
        },
        "spc_row_count": {
            "observed": int(len(spc_df)),
            "expected": expected_spc_rows,
            "pass": len(spc_df) == expected_spc_rows,
        },
        "condition_completeness": {
            "minimum_conditions_per_parameter_batch": int(
                batch_df.groupby(["parameter_id", "batch_id"])[
                    "condition_id"
                ].nunique().min()
            ),
            "pass": bool(
                (
                    batch_df.groupby(["parameter_id", "batch_id"])[
                        "condition_id"
                    ].nunique()
                    == 4
                ).all()
            ),
        },
        "realized_beta_matches_request": {
            "maximum_absolute_error": float(
                np.max(
                    np.abs(
                        cell_df["realized_beta_start_effective"]
                        - cell_df["beta_start_effective"]
                    )
                )
            ),
            "pass": bool(
                np.allclose(
                    cell_df["realized_beta_start_effective"],
                    cell_df["beta_start_effective"],
                    atol=1e-6,
                )
            ),
        },
        "spc_probability_range": {
            "minimum": float(spc_df["recall_probability"].min()),
            "maximum": float(spc_df["recall_probability"].max()),
            "pass": bool(spc_df["recall_probability"].between(0, 1).all()),
        },
        "film_total_range": {
            "minimum": float(batch_df["film_items_recalled"].min()),
            "maximum": float(batch_df["film_items_recalled"].max()),
            "pass": bool(
                batch_df["film_items_recalled"].between(
                    0, spec["simulation"]["n_film"]
                ).all()
            ),
        },
        "primary_estimand_identity": {
            "maximum_absolute_error": identity_error,
            "pass": identity_error < 1e-12,
        },
        "endpoint_estimand_identity": {
            "maximum_absolute_error": endpoint_identity_error,
            "pass": endpoint_identity_error < 1e-12,
        },
        "category_zero_duplicates_baseline": {
            "maximum_absolute_error": duplicate_difference(
                baseline_id, category_zero_id
            ),
            "pass": duplicate_difference(baseline_id, category_zero_id) < 1e-12,
        },
        "full_comparator_zero_duplicates_grid_anchor": {
            "maximum_absolute_error": duplicate_difference(
                current_grid_id, current_comparator_zero_id
            ),
            "pass": duplicate_difference(
                current_grid_id, current_comparator_zero_id
            )
            < 1e-12,
        },
    }
    return {"pass": all(value["pass"] for value in checks.values()), "checks": checks}


def dataframe_to_csv(frame: pd.DataFrame, path: Path) -> None:
    frame.to_csv(path, index=False, lineterminator="\n", float_format="%.10g")


def active_spec(
    original: dict[str, Any], args: argparse.Namespace
) -> tuple[dict[str, Any], dict[str, Any]]:
    spec = json.loads(json.dumps(original))
    overrides: dict[str, Any] = {}
    if args.experiment_count is not None:
        spec["simulation"]["experiment_count"] = args.experiment_count
        overrides["experiment_count"] = args.experiment_count
    if args.batch_count is not None:
        spec["simulation"]["batch_count"] = args.batch_count
        overrides["batch_count"] = args.batch_count
    for name, argument, spec_path in [
        (
            "beta_values",
            args.beta_values,
            ("no_category_grid", "beta_start_effective_values"),
        ),
        ("kappa_values", args.kappa_values, ("no_category_grid", "kappa_values")),
        (
            "cue_boost_values",
            args.cue_boost_values,
            ("category_cue_comparators", "film_item_support_boost_values"),
        ),
    ]:
        parsed = parse_override(argument)
        if parsed is not None:
            spec[spec_path[0]][spec_path[1]] = parsed
            overrides[name] = parsed
    return spec, overrides


def main() -> None:
    args = parse_args()
    spec_path = args.spec.resolve()
    output_dir = args.output_dir.resolve()
    original_spec = read_json(spec_path)
    spec, overrides = active_spec(original_spec, args)
    if spec["simulation"]["experiment_count"] % spec["simulation"]["batch_count"]:
        raise ValueError("experiment_count must be divisible by batch_count")

    fit_path = PROJECT_ROOT / spec["fit_path"]
    params, n_subjects = load_fit_params(fit_path)
    fitted_beta = float(np.asarray(params["start_drift_rate"])[0])
    parameter_configs = build_parameter_configs(
        spec,
        fitted_beta,
        parse_override(args.beta_values),
        parse_override(args.kappa_values),
        parse_override(args.cue_boost_values),
    )
    expected_cells = len(parameter_configs) * len(spec["conditions"])
    expected_trials = (
        expected_cells * spec["simulation"]["experiment_count"] * n_subjects
    )
    print(
        json.dumps(
            {
                "parameter_configurations": len(parameter_configs),
                "experimental_cells": expected_cells,
                "simulated_trials": expected_trials,
                "fitted_beta_start": fitted_beta,
                "output_dir": str(output_dir),
                "overrides": overrides,
            },
            indent=2,
        ),
        flush=True,
    )
    if args.dry_run:
        return
    if output_dir.exists() and any(output_dir.iterdir()) and not args.overwrite:
        raise FileExistsError(
            f"Output directory is not empty: {output_dir}. Use --overwrite explicitly."
        )
    output_dir.mkdir(parents=True, exist_ok=True)

    paradigm = Paradigm(
        n_film=spec["simulation"]["n_film"],
        n_break=spec["simulation"]["n_break"],
        n_interference=spec["simulation"]["n_interference"],
        n_filler=spec["simulation"]["n_filler"],
        experiment_count=spec["simulation"]["experiment_count"],
        max_recall=spec["simulation"]["max_recall"],
    )
    common_rngs, batch_ids, batch_seed_manifest = make_common_rngs(
        spec["simulation"]["master_seed"],
        n_subjects,
        paradigm.experiment_count,
        spec["simulation"]["batch_count"],
    )
    started = time.monotonic()
    cell_df, batch_df, spc_df = run_simulations(
        spec,
        params,
        paradigm,
        parameter_configs,
        common_rngs,
        batch_ids,
    )
    estimand_batches = compute_estimand_batches(batch_df)
    estimand_summary = summarize_estimands(estimand_batches)
    settings = representative_settings(estimand_summary, fitted_beta)
    representative_df = summarize_representatives(
        batch_df, estimand_summary, settings
    )

    paths = {
        "cell_manifest": output_dir / "cell_manifest.csv",
        "batch_summaries": output_dir / "batch_summaries.csv",
        "spc": output_dir / "spc.csv",
        "estimand_batches": output_dir / "estimand_batches.csv",
        "estimand_summary": output_dir / "estimand_summary.csv",
        "representative_diagnostics": output_dir / "representative_diagnostics.csv",
        "robustness_summary": output_dir / "robustness_summary.json",
        "results_markdown": output_dir / "RESULTS.md",
        "verification": output_dir / "verification.json",
    }
    dataframe_to_csv(cell_df, paths["cell_manifest"])
    dataframe_to_csv(batch_df, paths["batch_summaries"])
    dataframe_to_csv(spc_df, paths["spc"])
    dataframe_to_csv(estimand_batches, paths["estimand_batches"])
    dataframe_to_csv(estimand_summary, paths["estimand_summary"])
    dataframe_to_csv(representative_df, paths["representative_diagnostics"])

    regular_beta_count = sum(
        value != "fitted"
        for value in spec["no_category_grid"]["beta_start_effective_values"]
    )
    regular_grid_size = regular_beta_count * len(spec["no_category_grid"]["kappa_values"])
    robust = build_robustness_summary(
        estimand_summary, fitted_beta, regular_grid_size
    )
    write_json(paths["robustness_summary"], robust)
    write_results_markdown(paths["results_markdown"], robust)
    figure_paths = render_figure(
        estimand_summary,
        batch_df,
        spc_df,
        settings,
        fitted_beta,
        output_dir,
    )
    contrast_figure_paths = render_contrast_figure(
        estimand_summary,
        fitted_beta,
        output_dir,
    )

    verification = internal_verification(
        cell_df,
        batch_df,
        spc_df,
        estimand_batches,
        parameter_configs,
        spec,
        fitted_beta,
    )
    write_json(paths["verification"], verification)
    if not verification["pass"]:
        raise RuntimeError(f"Verification failed; inspect {paths['verification']}")

    source_paths = [
        Path(__file__).resolve(),
        spec_path,
        PACKAGE_DIR / "METHODS.md",
        PACKAGE_DIR / "FEEDBACK_TRACE.md",
        PACKAGE_DIR / "README.md",
        PACKAGE_DIR / "verify_results.py",
        fit_path.resolve(),
        PROJECT_ROOT / "selective_interference_v2/cmr.py",
        PROJECT_ROOT / "selective_interference_v2/pipeline.py",
        PROJECT_ROOT / "selective_interference_v2/paradigm.py",
        PROJECT_ROOT / "selective_interference_v2/remapping.py",
    ]
    output_paths = [*paths.values(), *figure_paths, *contrast_figure_paths]
    manifest = {
        "analysis_id": spec["analysis_id"],
        "schema_version": spec["schema_version"],
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "elapsed_seconds": time.monotonic() - started,
        "command": [sys.executable, *sys.argv],
        "project_root": str(PROJECT_ROOT),
        "output_dir": str(output_dir),
        "overrides": overrides,
        "active_spec": spec,
        "fitted_parameters": {
            "n_parameter_sets": n_subjects,
            "start_drift_rate": fitted_beta,
            "choice_sensitivity": float(np.asarray(params["choice_sensitivity"])[0]),
        },
        "rng": {
            "implementation": "jax.random.PRNGKey + fold_in(batch_id) + split",
            "common_random_numbers_across_all_cells": True,
            "batches": batch_seed_manifest,
        },
        "git": {
            "commit": command_output(["git", "rev-parse", "HEAD"]),
            "status_porcelain": command_output(["git", "status", "--porcelain"]),
        },
        "environment": {
            "python": sys.version,
            "platform": platform.platform(),
            "jax": jax.__version__,
            "jaxlib": package_version("jaxlib"),
            "numpy": np.__version__,
            "pandas": pd.__version__,
            "scipy": package_version("scipy"),
            "matplotlib": matplotlib.__version__,
            "jaxcmr": package_version("jaxcmr"),
            "jax_devices": [str(device) for device in jax.devices()],
        },
        "source_sha256": {
            str(path.relative_to(PROJECT_ROOT)): sha256_file(path) for path in source_paths
        },
        "output_sha256": {
            path.name: sha256_file(path) for path in output_paths
        },
        "verification_passed": verification["pass"],
    }
    manifest_path = output_dir / "run_manifest.json"
    write_json(manifest_path, manifest)
    print(f"Completed in {(time.monotonic() - started) / 60:.1f} min", flush=True)
    print(manifest_path, flush=True)


if __name__ == "__main__":
    main()
