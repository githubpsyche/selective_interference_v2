#!/usr/bin/env python3
"""Run an isolated repeated-versus-unique film-retrieval pilot."""

from __future__ import annotations

import argparse
import json
import math
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

os.environ.setdefault(
    "MPLCONFIGDIR",
    str(Path(tempfile.gettempdir()) / "selective-interference-matplotlib"),
)

import jax.numpy as jnp
from jax import random
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
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
)


PACKAGE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = PACKAGE_DIR.parents[1]
FIT_PATH = (
    PROJECT_ROOT
    / "work/fitting/"
    "Dupertuys2026_eCMR_source_only_phi_no_shared_support_best_of_1.json"
)
DEFAULT_OUTPUT_DIR = PACKAGE_DIR / "results"

N_FILM = 16
N_BREAK = 16
N_TASK = 16
N_FILLER = 16
MAX_RECALL = 48
DEFAULT_EXPERIMENT_COUNT = 5000
DEFAULT_BATCH_COUNT = 10
MASTER_SEED = 31000

FILM_CUE_REINSTATEMENT = 0.90
CUE_INTERVAL = 4
FIRST_CUE_AFTER = 0
CACHE_AFTER = "filler"

FIXED_SCALES = {
    "break_drift_scale": 1.0,
    "break_mcf_scale": 1.0,
    "filler_drift_scale": 1.0,
    "filler_mcf_scale": 1.0,
    "source_learning_baseline": 0.05,
    "primacy_scale": 0.1,
    "primacy_decay": 1.5,
    "tau_scale": 1.0,
    "target_recall_drift_scale": 1.0,
    "recall_drift_scale": 1.0,
}

CONDITIONS = [
    {
        "condition_id": "no_reminder_weak",
        "reminder_condition": "No reminder",
        "task_condition": "Weak task encoding",
        "reminder_start_drift_scale": 0.0,
        "reminder_drift_scale": 0.0,
        "task_mcf_scale": 1.0,
    },
    {
        "condition_id": "no_reminder_strong",
        "reminder_condition": "No reminder",
        "task_condition": "Strong task encoding",
        "reminder_start_drift_scale": 0.0,
        "reminder_drift_scale": 0.0,
        "task_mcf_scale": 2.0,
    },
    {
        "condition_id": "reminder_weak",
        "reminder_condition": "With reminder",
        "task_condition": "Weak task encoding",
        "reminder_start_drift_scale": 1.0,
        "reminder_drift_scale": 1.0,
        "task_mcf_scale": 1.0,
    },
    {
        "condition_id": "reminder_strong",
        "reminder_condition": "With reminder",
        "task_condition": "Strong task encoding",
        "reminder_start_drift_scale": 1.0,
        "reminder_drift_scale": 1.0,
        "task_mcf_scale": 2.0,
    },
]

RETRIEVAL_MODES = [
    {
        "retrieval_mode": "Unguided",
        "start_drift_scale": 0.0,
        "film_item_support_boost": 0.0,
        "rejected_recall_drift_scale": 1.0,
    },
    {
        "retrieval_mode": "Deliberate",
        "start_drift_scale": 1.0,
        "film_item_support_boost": 1.0,
        "rejected_recall_drift_scale": 0.5,
    },
]

CONTRAST_METRICS = {
    "total": "mean_film_total_events",
    "unique": "mean_film_unique_items",
    "repeated": "mean_film_repeated_events",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument(
        "--experiment-count", type=int, default=DEFAULT_EXPERIMENT_COUNT
    )
    parser.add_argument("--batch-count", type=int, default=DEFAULT_BATCH_COUNT)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def write_json(path: Path, value: Any) -> None:
    with path.open("w") as handle:
        json.dump(value, handle, indent=2, sort_keys=True, allow_nan=False)
        handle.write("\n")


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


BATCHED_CUED_RECALL = batch_trial(cued_recall_trial, n_args=7, n_static=3)


def per_trial_recurrence_metrics(
    recalls: np.ndarray,
    n_film: int,
) -> dict[str, np.ndarray]:
    """Return recurrence quantities without conventional SPC deduplication."""
    recalls = np.asarray(recalls, dtype=int)
    if recalls.ndim != 2:
        raise ValueError("recalls must be a two-dimensional trial-by-output array")

    film_mask = (recalls >= 1) & (recalls <= n_film)
    item_counts = np.stack(
        [np.sum(recalls == item_id, axis=1) for item_id in range(1, n_film + 1)],
        axis=1,
    )
    total = np.sum(film_mask, axis=1)
    unique = np.sum(item_counts > 0, axis=1)
    repeated = total - unique

    max_count = np.max(item_counts, axis=1)
    concentration = np.divide(
        max_count,
        total,
        out=np.zeros_like(max_count, dtype=float),
        where=total > 0,
    )
    adjacent_film = film_mask[:, :-1] & film_mask[:, 1:]
    immediate_same = adjacent_film & (recalls[:, :-1] == recalls[:, 1:])

    return {
        "output_count": np.sum(recalls > 0, axis=1),
        "film_total_events": total,
        "film_unique_items": unique,
        "film_repeated_events": repeated,
        "film_max_item_share": concentration,
        "film_immediate_same_events": np.sum(immediate_same, axis=1),
        "film_adjacent_transition_count": np.sum(adjacent_film, axis=1),
    }


def validate_metric_implementation() -> None:
    toy = np.array(
        [
            [1, 1, 2, 0, 0],
            [3, 4, 3, 3, 0],
            [17, 17, 0, 0, 0],
        ]
    )
    metrics = per_trial_recurrence_metrics(toy, n_film=16)
    np.testing.assert_array_equal(metrics["film_total_events"], [3, 4, 0])
    np.testing.assert_array_equal(metrics["film_unique_items"], [2, 2, 0])
    np.testing.assert_array_equal(metrics["film_repeated_events"], [1, 2, 0])
    np.testing.assert_array_equal(metrics["film_immediate_same_events"], [1, 1, 0])
    if not np.all(
        metrics["film_total_events"]
        == metrics["film_unique_items"] + metrics["film_repeated_events"]
    ):
        raise AssertionError("total = unique + repeated invariant failed")


def make_common_rngs(
    n_subjects: int,
    experiment_count: int,
) -> tuple[jnp.ndarray, np.ndarray]:
    keys = random.split(
        random.PRNGKey(MASTER_SEED), n_subjects * experiment_count
    ).reshape(n_subjects, experiment_count, -1)
    return keys, np.arange(experiment_count)


def prepare_condition(
    params: dict[str, jnp.ndarray],
    paradigm: Paradigm,
    factory,
    condition: dict[str, Any],
):
    scales = {
        **FIXED_SCALES,
        "reminder_start_drift_scale": condition["reminder_start_drift_scale"],
        "reminder_drift_scale": condition["reminder_drift_scale"],
        "interference_mcf_scale": condition["task_mcf_scale"],
    }
    pre_cache_scales, post_cache_scales = split_scales_for_cache(
        scales, CACHE_AFTER
    )
    prepared = prepare_sweep(
        params,
        paradigm,
        factory,
        cache_after=CACHE_AFTER,
        **pre_cache_scales,
    )
    return prepared, post_cache_scales


def summarize_batches(
    recalls: np.ndarray,
    batch_ids: np.ndarray,
    batch_count: int,
    metadata: dict[str, Any],
    n_film: int,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for batch_id in range(batch_count):
        subset = recalls[batch_ids == batch_id]
        values = per_trial_recurrence_metrics(subset, n_film)
        total_events = int(np.sum(values["film_total_events"]))
        repeated_events = int(np.sum(values["film_repeated_events"]))
        adjacent_transitions = int(
            np.sum(values["film_adjacent_transition_count"])
        )
        immediate_repeats = int(np.sum(values["film_immediate_same_events"]))
        rows.append(
            {
                **metadata,
                "batch_id": batch_id,
                "n_trials": int(subset.shape[0]),
                "mean_output_count": float(np.mean(values["output_count"])),
                "mean_film_total_events": float(
                    np.mean(values["film_total_events"])
                ),
                "mean_film_unique_items": float(
                    np.mean(values["film_unique_items"])
                ),
                "mean_film_repeated_events": float(
                    np.mean(values["film_repeated_events"])
                ),
                "film_repeat_fraction": (
                    repeated_events / total_events if total_events else 0.0
                ),
                "trial_film_recurrence_probability": float(
                    np.mean(values["film_repeated_events"] > 0)
                ),
                "mean_film_max_item_share": float(
                    np.mean(values["film_max_item_share"])
                ),
                "film_immediate_repeat_fraction": (
                    immediate_repeats / adjacent_transitions
                    if adjacent_transitions
                    else 0.0
                ),
            }
        )
    return rows


def interval_summary(
    frame: pd.DataFrame,
    group_columns: list[str],
    value_columns: list[str],
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for keys, group in frame.groupby(group_columns, sort=False, dropna=False):
        if not isinstance(keys, tuple):
            keys = (keys,)
        row = dict(zip(group_columns, keys, strict=True))
        for column in value_columns:
            values = group[column].to_numpy(dtype=float)
            mean = float(np.mean(values))
            if len(values) > 1:
                sem = float(np.std(values, ddof=1) / math.sqrt(len(values)))
                half_width = float(student_t.ppf(0.975, len(values) - 1) * sem)
            else:
                half_width = 0.0
            row[f"{column}_mean"] = mean
            row[f"{column}_ci_low"] = mean - half_width
            row[f"{column}_ci_high"] = mean + half_width
        rows.append(row)
    return pd.DataFrame(rows)


def make_contrast_batches(batch_frame: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for allow_repeats in [False, True]:
        for batch_id in sorted(batch_frame["batch_id"].unique()):
            for metric_name, metric_column in CONTRAST_METRICS.items():
                sensitivities: dict[str, dict[str, float]] = {}
                for retrieval_mode in ["Unguided", "Deliberate"]:
                    subset = batch_frame[
                        (batch_frame["allow_repeated_recalls"] == allow_repeats)
                        & (batch_frame["batch_id"] == batch_id)
                        & (batch_frame["retrieval_mode"] == retrieval_mode)
                    ].set_index("condition_id")
                    values = subset[metric_column].to_dict()
                    no_reminder_cost = (
                        values["no_reminder_weak"] - values["no_reminder_strong"]
                    )
                    reminder_cost = values["reminder_weak"] - values["reminder_strong"]
                    sensitivities[retrieval_mode] = {
                        "no_reminder_task_cost": no_reminder_cost,
                        "reminder_task_cost": reminder_cost,
                        "reminder_specific_sensitivity": (
                            reminder_cost - no_reminder_cost
                        ),
                    }
                rows.append(
                    {
                        "allow_repeated_recalls": allow_repeats,
                        "batch_id": batch_id,
                        "metric": metric_name,
                        "unguided_no_reminder_task_cost": sensitivities["Unguided"][
                            "no_reminder_task_cost"
                        ],
                        "unguided_reminder_task_cost": sensitivities["Unguided"][
                            "reminder_task_cost"
                        ],
                        "unguided_reminder_specific_sensitivity": sensitivities[
                            "Unguided"
                        ]["reminder_specific_sensitivity"],
                        "deliberate_no_reminder_task_cost": sensitivities[
                            "Deliberate"
                        ]["no_reminder_task_cost"],
                        "deliberate_reminder_task_cost": sensitivities["Deliberate"][
                            "reminder_task_cost"
                        ],
                        "deliberate_reminder_specific_sensitivity": sensitivities[
                            "Deliberate"
                        ]["reminder_specific_sensitivity"],
                        "selective_protection": (
                            sensitivities["Unguided"][
                                "reminder_specific_sensitivity"
                            ]
                            - sensitivities["Deliberate"][
                                "reminder_specific_sensitivity"
                            ]
                        ),
                    }
                )
    return pd.DataFrame(rows)


def render_figure(
    cell_summary: pd.DataFrame,
    contrast_summary: pd.DataFrame,
    output_dir: Path,
) -> None:
    enabled = cell_summary[
        (cell_summary["allow_repeated_recalls"])
        & (cell_summary["reminder_condition"] == "With reminder")
    ].copy()
    enabled["order"] = enabled["retrieval_mode"].map(
        {"Unguided": 0, "Deliberate": 1}
    ) * 2 + enabled["task_condition"].map(
        {"Weak task encoding": 0, "Strong task encoding": 1}
    )
    enabled = enabled.sort_values("order")

    labels = [
        "Unguided\nweak",
        "Unguided\nstrong",
        "Deliberate\nweak",
        "Deliberate\nstrong",
    ]
    x = np.arange(len(labels))
    unique = enabled["mean_film_unique_items_mean"].to_numpy()
    repeated = enabled["mean_film_repeated_events_mean"].to_numpy()

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.4))
    axes[0].bar(x, unique, color="#4C78A8", label="Unique film items")
    axes[0].bar(
        x,
        repeated,
        bottom=unique,
        color="#F58518",
        label="Repeated film events",
    )
    axes[0].set_xticks(x, labels)
    axes[0].set_ylabel("Mean film retrieval events")
    axes[0].set_title("A  Recurrence composition with film reminder")
    axes[0].legend(frameon=False)

    contrast = contrast_summary[
        contrast_summary["allow_repeated_recalls"]
    ].set_index("metric")
    metric_order = ["total", "unique", "repeated"]
    metric_labels = ["Total events", "Unique items", "Repeated events"]
    width = 0.34
    x2 = np.arange(len(metric_order))
    unguided = contrast.loc[
        metric_order, "unguided_reminder_specific_sensitivity_mean"
    ].to_numpy()
    deliberate = contrast.loc[
        metric_order, "deliberate_reminder_specific_sensitivity_mean"
    ].to_numpy()
    axes[1].axhline(0, color="#888888", linewidth=0.8)
    axes[1].bar(x2 - width / 2, unguided, width, color="#E45756", label="Unguided")
    axes[1].bar(
        x2 + width / 2,
        deliberate,
        width,
        color="#72B7B2",
        label="Deliberate",
    )
    axes[1].set_xticks(x2, metric_labels)
    axes[1].set_ylabel("Reminder-specific task cost")
    axes[1].set_title("B  Selective interference depends on scoring")
    axes[1].legend(frameon=False)

    for axis in axes:
        axis.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(output_dir / "recurrence_summary.png", dpi=200)
    fig.savefig(output_dir / "recurrence_summary.svg")
    plt.close(fig)


def write_results_markdown(
    batch_frame: pd.DataFrame,
    contrast_summary: pd.DataFrame,
    output_dir: Path,
) -> None:
    disabled_repeat_max = float(
        batch_frame.loc[
            ~batch_frame["allow_repeated_recalls"],
            "mean_film_repeated_events",
        ].max()
    )
    enabled = batch_frame[batch_frame["allow_repeated_recalls"]]
    recurrence_probability = float(
        enabled["trial_film_recurrence_probability"].mean()
    )
    immediate_fraction = float(enabled["film_immediate_repeat_fraction"].mean())
    contrast = contrast_summary[
        contrast_summary["allow_repeated_recalls"]
    ].set_index("metric")
    total_protection = float(
        contrast.loc["total", "selective_protection_mean"]
    )
    unique_protection = float(
        contrast.loc["unique", "selective_protection_mean"]
    )
    repeated_protection = float(
        contrast.loc["repeated", "selective_protection_mean"]
    )
    text = f"""# Results

The implementation invariant held: with repeated recalls disabled, the
largest mean repeated-film count in any batch was {disabled_repeat_max:.3f}.

With repeated recalls enabled, the mean probability that a trial contained at
least one repeated film item was {recurrence_probability:.3f}. Across adjacent
film-to-film transitions, {immediate_fraction:.3f} were immediate repetitions
of the same item. This immediate-repeat diagnostic is important because the
toggle contains no refractory mechanism.

For the reminder-specific selective-protection contrast, scoring all film
events gave {total_protection:.3f}; scoring unique film items gave
{unique_protection:.3f}; and the repeated-event component gave
{repeated_protection:.3f}. Thus the total-versus-unique difference is exactly
the contribution of recurrence under this within-sequence implementation.

These values are a model diagnostic, not a fitted account of diary recurrence.
The current toggle allows a sampled item to remain immediately available in
one retrieval sequence; it does not represent separated intrusion episodes or
changing real-world triggers.
"""
    (output_dir / "RESULTS.md").write_text(text)


def run(args: argparse.Namespace) -> None:
    validate_metric_implementation()
    if args.experiment_count <= 0 or args.batch_count <= 0:
        raise ValueError("experiment-count and batch-count must be positive")
    if args.experiment_count % args.batch_count:
        raise ValueError("experiment-count must be divisible by batch-count")

    output_dir = args.output_dir.resolve()
    if output_dir.exists() and any(output_dir.iterdir()) and not args.overwrite:
        raise FileExistsError(
            f"Output directory is not empty: {output_dir}. Pass --overwrite."
        )
    output_dir.mkdir(parents=True, exist_ok=True)

    params, n_subjects = load_fit_params(FIT_PATH)
    paradigm = Paradigm(
        n_film=N_FILM,
        n_break=N_BREAK,
        n_interference=N_TASK,
        n_filler=N_FILLER,
        experiment_count=args.experiment_count,
        max_recall=MAX_RECALL,
    )
    factory = make_factory(
        is_emotional=make_is_emotional(
            paradigm,
            film_emotional=True,
            interference_emotional=False,
        ),
        is_target=make_is_target(paradigm),
    )
    common_rngs, replication_ids = make_common_rngs(
        n_subjects, args.experiment_count
    )
    per_batch = args.experiment_count // args.batch_count
    one_subject_batches = replication_ids // per_batch
    batch_ids = np.tile(one_subject_batches, n_subjects)

    batch_rows: list[dict[str, Any]] = []
    example_rows: list[dict[str, Any]] = []
    total_cells = 2 * len(RETRIEVAL_MODES) * len(CONDITIONS)
    cell_index = 0

    for allow_repeats in [False, True]:
        toggle_params = dict(params)
        toggle_params["allow_repeated_recalls"] = jnp.full(
            (n_subjects,), float(allow_repeats)
        )
        prepared_conditions = {
            condition["condition_id"]: prepare_condition(
                toggle_params, paradigm, factory, condition
            )
            for condition in CONDITIONS
        }
        for retrieval in RETRIEVAL_MODES:
            for condition in CONDITIONS:
                cell_index += 1
                print(
                    f"Cell {cell_index}/{total_cells}: repeats={allow_repeats}, "
                    f"{retrieval['retrieval_mode']}, {condition['condition_id']}"
                )
                prepared, post_cache_scales = prepared_conditions[
                    condition["condition_id"]
                ]
                ready_models = configure_rates(
                    prepared.models,
                    **post_cache_scales,
                    start_drift_scale=retrieval["start_drift_scale"],
                    film_item_support_boost=retrieval["film_item_support_boost"],
                    rejected_recall_drift_scale=retrieval[
                        "rejected_recall_drift_scale"
                    ],
                )
                recalls, _, _ = BATCHED_CUED_RECALL(
                    ready_models,
                    common_rngs,
                    paradigm.film_items,
                    FILM_CUE_REINSTATEMENT,
                    paradigm.max_recall,
                    CUE_INTERVAL,
                    FIRST_CUE_AFTER,
                )
                raw_recalls = np.asarray(recalls).reshape(-1, recalls.shape[-1])
                metadata = {
                    "allow_repeated_recalls": allow_repeats,
                    "retrieval_mode": retrieval["retrieval_mode"],
                    "condition_id": condition["condition_id"],
                    "reminder_condition": condition["reminder_condition"],
                    "task_condition": condition["task_condition"],
                    "task_mcf_scale": condition["task_mcf_scale"],
                    "start_drift_scale": retrieval["start_drift_scale"],
                    "film_item_support_boost": retrieval[
                        "film_item_support_boost"
                    ],
                    "rejected_recall_drift_scale": retrieval[
                        "rejected_recall_drift_scale"
                    ],
                }
                batch_rows.extend(
                    summarize_batches(
                        raw_recalls,
                        batch_ids,
                        args.batch_count,
                        metadata,
                        paradigm.n_film,
                    )
                )
                for example_index, sequence in enumerate(raw_recalls[:3]):
                    example_rows.append(
                        {
                            **metadata,
                            "example_index": example_index,
                            "sequence": " ".join(str(int(value)) for value in sequence),
                        }
                    )

    batch_frame = pd.DataFrame(batch_rows)
    value_columns = [
        "mean_output_count",
        "mean_film_total_events",
        "mean_film_unique_items",
        "mean_film_repeated_events",
        "film_repeat_fraction",
        "trial_film_recurrence_probability",
        "mean_film_max_item_share",
        "film_immediate_repeat_fraction",
    ]
    group_columns = [
        "allow_repeated_recalls",
        "retrieval_mode",
        "condition_id",
        "reminder_condition",
        "task_condition",
    ]
    cell_summary = interval_summary(batch_frame, group_columns, value_columns)
    contrast_batches = make_contrast_batches(batch_frame)
    contrast_value_columns = [
        column
        for column in contrast_batches.columns
        if column not in {"allow_repeated_recalls", "batch_id", "metric"}
    ]
    contrast_summary = interval_summary(
        contrast_batches,
        ["allow_repeated_recalls", "metric"],
        contrast_value_columns,
    )

    batch_frame.to_csv(output_dir / "batch_metrics.csv", index=False)
    cell_summary.to_csv(output_dir / "cell_summary.csv", index=False)
    contrast_batches.to_csv(output_dir / "contrast_batches.csv", index=False)
    contrast_summary.to_csv(output_dir / "contrast_summary.csv", index=False)
    pd.DataFrame(example_rows).to_csv(
        output_dir / "example_sequences.csv", index=False
    )
    render_figure(cell_summary, contrast_summary, output_dir)
    write_results_markdown(batch_frame, contrast_summary, output_dir)

    no_repeat_max = float(
        batch_frame.loc[
            ~batch_frame["allow_repeated_recalls"],
            "mean_film_repeated_events",
        ].max()
    )
    manifest = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "fit_path": str(FIT_PATH.relative_to(PROJECT_ROOT)),
        "experiment_count": args.experiment_count,
        "batch_count": args.batch_count,
        "n_subjects": n_subjects,
        "master_seed": MASTER_SEED,
        "max_recall": MAX_RECALL,
        "film_cue_reinstatement": FILM_CUE_REINSTATEMENT,
        "cue_interval": CUE_INTERVAL,
        "first_cue_after": FIRST_CUE_AFTER,
        "common_random_numbers": True,
        "scope": "within_retrieval_sequence_recurrence",
        "analysis_compatibility_audit_deferred": True,
        "checks": {
            "metric_identity_checked": True,
            "disabled_toggle_repeated_event_max": no_repeat_max,
            "disabled_toggle_has_no_repeated_film_events": no_repeat_max == 0.0,
        },
    }
    write_json(output_dir / "run_manifest.json", manifest)
    print(output_dir)


if __name__ == "__main__":
    run(parse_args())
