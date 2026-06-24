from __future__ import annotations

import csv
import os
import sys
from pathlib import Path

from jax import random
from jaxcmr.helpers import find_project_root
import jax.numpy as jnp
import numpy as np

SCRIPT_PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(SCRIPT_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_PROJECT_ROOT))

from selective_interference_v2 import (
    Paradigm,
    batch_trial,
    configure_rates,
    load_fit_params,
    make_factory,
    make_is_emotional,
    make_is_target,
    prepare_sweep,
    simulate_sequential_recognition_diagnostics,
    simulate_sequential_recognition,
    split_scales_for_cache,
    sweep_rngs,
)


PROJECT_ROOT = ""
FIT_PATH = "work/fitting/Dupertuys2026_eCMR_source_only_phi_no_shared_support_best_of_1.json"
DATA_DIR = "work/simulation3_recognition_test_format"
OUTPUT_PREFIX = os.environ.get(
    "SIM3_RECOGNITION_TEST_FORMAT_PREFIX",
    "simulation3_recognition_test_format",
)
RNG_SEED = 0

N_FILM = 16
N_BREAK = 16
N_INTERFERENCE = 16
N_FILLER = 16
N_FOILS = 16
EXPERIMENT_COUNT = int(os.environ.get("SIM3_RECOGNITION_EXPERIMENT_COUNT", "5000"))

TASK_MCF_VALUES = [1.0, 2.0]
TASK_MCF_LABELS = {
    1.0: "Weak task encoding",
    2.0: "Strong task encoding",
}
REMINDER_CONDITIONS = {
    "No reminder": {
        "reminder_start_drift_scale": 0.0,
        "reminder_drift_scale": 0.0,
    },
    "With reminder": {
        "reminder_start_drift_scale": 1.0,
        "reminder_drift_scale": 1.0,
    },
}

PRIMARY_SOURCE_ORIENTATION = 0.0

RECOGNITION_THRESHOLD = float(os.environ.get("RECOGNITION_THRESHOLD", "0.5"))
RECOGNITION_SENSITIVITY = float(os.environ.get("RECOGNITION_SENSITIVITY", "20.0"))
RECOGNITION_CUE_REINSTATEMENT = float(
    os.environ.get("RECOGNITION_CUE_REINSTATEMENT", "0.90")
)
RECOGNITION_TEMPORAL_WEIGHT = float(
    os.environ.get("RECOGNITION_TEMPORAL_WEIGHT", "1.0")
)
RECOGNITION_SOURCE_WEIGHT = float(os.environ.get("RECOGNITION_SOURCE_WEIGHT", "1.0"))

FILM_EMOTIONAL = True
INTERFERENCE_EMOTIONAL = False
FOIL_EMOTIONAL = True
CACHE_AFTER = "filler"

EXTRA_FIXED_SCALES = {
    "source_learning_baseline": 0.05,
    "primacy_scale": 0.1,
    "primacy_decay": 1.5,
}

BASE_FIXED_SCALES = {
    "break_drift_scale": 1.0,
    "break_mcf_scale": 1.0,
    "filler_drift_scale": 1.0,
    "filler_mcf_scale": 1.0,
}

RETRIEVAL_FIXED_SCALES = {
    "tau_scale": 1.0,
    "target_recall_drift_scale": 1.0,
    "recall_drift_scale": 1.0,
    "rejected_recall_drift_scale": 1.0,
}


def project_root() -> Path:
    return Path(PROJECT_ROOT).expanduser() if PROJECT_ROOT else Path(__file__).resolve().parents[2]


def write_rows(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def mean_ci(values: np.ndarray) -> tuple[float, float, float]:
    values = np.asarray(values, dtype=float)
    mean = float(np.mean(values))
    if values.size <= 1:
        return mean, mean, mean
    se = float(np.std(values, ddof=1) / np.sqrt(values.size))
    return mean, mean - 1.96 * se, mean + 1.96 * se


def condition_label(reminder_condition: str, task_scale: float) -> str:
    task = "weak task" if np.isclose(task_scale, 1.0) else "strong task"
    return f"{reminder_condition} + {task}"


def recognition_trial(
    model,
    rng,
    old_items,
    foil_items,
    cue_scale,
    threshold,
    sensitivity,
    temporal_weight,
    source_weight,
):
    probes = jnp.concatenate([old_items, foil_items])
    labels = jnp.concatenate([
        jnp.ones(old_items.shape[0], dtype=jnp.int32),
        jnp.zeros(foil_items.shape[0], dtype=jnp.int32),
    ])
    order = random.permutation(rng, probes.shape[0])
    probes = probes[order]
    labels = labels[order]
    model = model.start_retrieving()
    _, evidences, old_probabilities = simulate_sequential_recognition(
        model,
        probes,
        cue_scale,
        threshold,
        sensitivity,
        temporal_weight=temporal_weight,
        source_weight=source_weight,
    )
    return probes, labels, evidences, old_probabilities


batched_recognition = batch_trial(recognition_trial, n_args=9)


def recognition_diagnostic_trial(
    model,
    rng,
    old_items,
    foil_items,
    task_items,
    cue_scale,
    threshold,
    sensitivity,
    temporal_weight,
    source_weight,
):
    probes = jnp.concatenate([old_items, foil_items])
    labels = jnp.concatenate([
        jnp.ones(old_items.shape[0], dtype=jnp.int32),
        jnp.zeros(foil_items.shape[0], dtype=jnp.int32),
    ])
    serial_positions = jnp.concatenate([
        jnp.arange(1, old_items.shape[0] + 1, dtype=jnp.int32),
        jnp.zeros(foil_items.shape[0], dtype=jnp.int32),
    ])
    order = random.permutation(rng, probes.shape[0])
    probes = probes[order]
    labels = labels[order]
    serial_positions = serial_positions[order]
    recognition_positions = jnp.arange(1, probes.shape[0] + 1, dtype=jnp.int32)
    model = model.start_retrieving()
    _, diagnostics = simulate_sequential_recognition_diagnostics(
        model,
        probes,
        cue_scale,
        threshold,
        sensitivity,
        old_items,
        task_items,
        temporal_weight=temporal_weight,
        source_weight=source_weight,
    )
    return probes, labels, serial_positions, recognition_positions, diagnostics


batched_recognition_diagnostics = batch_trial(
    recognition_diagnostic_trial,
    n_args=10,
)


def recognition_summary_stats(
    labels: np.ndarray,
    evidences: np.ndarray,
    old_probabilities: np.ndarray,
) -> dict[str, tuple[float, float, float]]:
    labels = labels.astype(bool)
    old_count = np.sum(labels, axis=(1, 2))
    foil_count = np.sum(~labels, axis=(1, 2))
    old_evidence = np.sum(np.where(labels, evidences, 0.0), axis=(1, 2)) / old_count
    foil_evidence = np.sum(np.where(~labels, evidences, 0.0), axis=(1, 2)) / foil_count
    hit_probability = (
        np.sum(np.where(labels, old_probabilities, 0.0), axis=(1, 2)) / old_count
    )
    false_alarm_probability = (
        np.sum(np.where(~labels, old_probabilities, 0.0), axis=(1, 2)) / foil_count
    )
    separation = old_evidence - foil_evidence
    accuracy = hit_probability - false_alarm_probability
    auc = old_foil_auc_by_subject(labels, evidences)
    return {
        "old_mfc_current_context_evidence": mean_ci(old_evidence),
        "foil_mfc_current_context_evidence": mean_ci(foil_evidence),
        "mfc_current_context_evidence_separation": mean_ci(separation),
        "hit_probability": mean_ci(hit_probability),
        "false_alarm_probability": mean_ci(false_alarm_probability),
        "corrected_recognition": mean_ci(accuracy),
        "hit_minus_false_alarm": mean_ci(accuracy),
        "old_foil_auc": mean_ci(auc),
    }


def binary_auc(old_values: np.ndarray, foil_values: np.ndarray) -> float:
    old_values = np.asarray(old_values, dtype=float)
    foil_values = np.asarray(foil_values, dtype=float)
    n_old = old_values.size
    n_foil = foil_values.size
    if n_old == 0 or n_foil == 0:
        return float("nan")

    scores = np.concatenate([old_values, foil_values])
    labels = np.concatenate([
        np.ones(n_old, dtype=bool),
        np.zeros(n_foil, dtype=bool),
    ])
    order = np.argsort(scores, kind="mergesort")
    sorted_scores = scores[order]
    ranks = np.empty(scores.size, dtype=float)
    start = 0
    while start < scores.size:
        end = start + 1
        while end < scores.size and sorted_scores[end] == sorted_scores[start]:
            end += 1
        ranks[order[start:end]] = (start + 1 + end) / 2.0
        start = end

    rank_sum_old = float(np.sum(ranks[labels]))
    return (
        rank_sum_old - n_old * (n_old + 1) / 2.0
    ) / (n_old * n_foil)


def old_foil_auc_by_subject(
    labels: np.ndarray,
    evidences: np.ndarray,
) -> np.ndarray:
    labels = labels.astype(bool)
    subject_aucs = []
    for subject in range(labels.shape[0]):
        subject_labels = labels[subject].reshape(-1)
        subject_evidence = evidences[subject].reshape(-1)
        subject_aucs.append(
            binary_auc(
                subject_evidence[subject_labels],
                subject_evidence[~subject_labels],
            )
        )
    return np.asarray(subject_aucs, dtype=float)


def masked_subject_means(values: np.ndarray, mask: np.ndarray) -> np.ndarray:
    values = np.asarray(values, dtype=float)
    mask = np.asarray(mask, dtype=bool)
    counts = np.sum(mask, axis=(1, 2))
    totals = np.sum(np.where(mask, values, 0.0), axis=(1, 2))
    return totals / np.maximum(counts, 1)


DIAGNOSTIC_METRICS = [
    "mfc_current_context_evidence",
    "old_probability",
    "cmr_ia_temporal_similarity",
    "cmr_ia_source_similarity",
    "probe_context_to_item_support",
    "film_context_to_item_mass",
    "task_context_to_item_mass",
    "film_to_task_support_ratio",
]


def diagnostic_windows(positions: np.ndarray) -> list[tuple[str, np.ndarray]]:
    return [
        ("all", np.ones_like(positions, dtype=bool)),
        ("early_1_8", positions <= 8),
    ]


def diagnostic_probe_types(labels: np.ndarray) -> list[tuple[str, np.ndarray]]:
    old = labels.astype(bool)
    return [
        ("all", np.ones_like(old, dtype=bool)),
        ("old", old),
        ("foil", ~old),
    ]


def append_diagnostic_summary_rows(
    rows: list[dict],
    metadata: dict,
    diagnostic_setting: str,
    diagnostic_cue_scale: float,
    labels: np.ndarray,
    recognition_positions: np.ndarray,
    diagnostic_arrays: dict[str, np.ndarray],
) -> None:
    for window, window_mask in diagnostic_windows(recognition_positions):
        for probe_type, probe_mask in diagnostic_probe_types(labels):
            mask = window_mask & probe_mask
            for metric in DIAGNOSTIC_METRICS:
                values = masked_subject_means(diagnostic_arrays[metric], mask)
                mean, ci_lower, ci_upper = mean_ci(values)
                rows.append(
                    {
                        **metadata,
                        "diagnostic_setting": diagnostic_setting,
                        "diagnostic_cue_scale": diagnostic_cue_scale,
                        "probe_window": window,
                        "probe_type": probe_type,
                        "metric": metric,
                        "value": mean,
                        "ci_lower": ci_lower,
                        "ci_upper": ci_upper,
                    }
                )


def append_grouped_diagnostic_rows(
    rows: list[dict],
    metadata: dict,
    diagnostic_setting: str,
    diagnostic_cue_scale: float,
    labels: np.ndarray,
    recognition_positions: np.ndarray,
    serial_positions: np.ndarray,
    diagnostic_arrays: dict[str, np.ndarray],
) -> None:
    for position in range(1, labels.shape[-1] + 1):
        position_mask = recognition_positions == position
        for probe_type, probe_mask in diagnostic_probe_types(labels):
            mask = position_mask & probe_mask
            for metric in DIAGNOSTIC_METRICS:
                values = masked_subject_means(diagnostic_arrays[metric], mask)
                mean, ci_lower, ci_upper = mean_ci(values)
                rows.append(
                    {
                        **metadata,
                        "diagnostic_setting": diagnostic_setting,
                        "diagnostic_cue_scale": diagnostic_cue_scale,
                        "grouping": "recognition_position",
                        "group_value": position,
                        "probe_type": probe_type,
                        "metric": metric,
                        "value": mean,
                        "ci_lower": ci_lower,
                        "ci_upper": ci_upper,
                    }
                )

    old_mask = labels.astype(bool)
    n_serial_positions = int(np.max(serial_positions))
    for serial_position in range(1, n_serial_positions + 1):
        serial_mask = old_mask & (serial_positions == serial_position)
        for metric in DIAGNOSTIC_METRICS:
            values = masked_subject_means(diagnostic_arrays[metric], serial_mask)
            mean, ci_lower, ci_upper = mean_ci(values)
            rows.append(
                {
                    **metadata,
                    "diagnostic_setting": diagnostic_setting,
                    "diagnostic_cue_scale": diagnostic_cue_scale,
                    "grouping": "studied_film_serial_position",
                    "group_value": serial_position,
                    "probe_type": "old",
                    "metric": metric,
                    "value": mean,
                    "ci_lower": ci_lower,
                    "ci_upper": ci_upper,
                }
            )


def write_hist_rows(
    path: Path,
    fieldnames: list[str],
    condition_evidence: list[dict],
) -> None:
    all_values = np.concatenate([
        entry["old_evidence"]
        for entry in condition_evidence
    ] + [
        entry["foil_evidence"]
        for entry in condition_evidence
    ])
    lo = float(np.nanpercentile(all_values, 0.5))
    hi = float(np.nanpercentile(all_values, 99.5))
    if np.isclose(lo, hi):
        lo -= 0.5
        hi += 0.5
    pad = 0.05 * (hi - lo)
    bins = np.linspace(lo - pad, hi + pad, 33)
    rows = []
    for entry in condition_evidence:
        for probe_type, values in [
            ("old", entry["old_evidence"]),
            ("foil", entry["foil_evidence"]),
        ]:
            counts, edges = np.histogram(values, bins=bins, density=False)
            density = counts / max(1, np.sum(counts)) / np.diff(edges)
            for index, value in enumerate(counts):
                rows.append(
                    {
                        **entry["metadata"],
                        "probe_type": probe_type,
                        "bin_left": float(edges[index]),
                        "bin_right": float(edges[index + 1]),
                        "bin_center": float((edges[index] + edges[index + 1]) / 2),
                        "count": int(value),
                        "density": float(density[index]),
                    }
                )
    write_rows(path, fieldnames, rows)


def recognition_diagnostic_settings() -> list[tuple[str, float]]:
    return [
        ("sequential_update", RECOGNITION_CUE_REINSTATEMENT),
        ("no_probe_update", 0.0),
    ]


def run_sweep():
    root = project_root()
    fit_path = root / FIT_PATH
    data_dir = root / DATA_DIR
    data_base = data_dir / OUTPUT_PREFIX

    params, _ = load_fit_params(fit_path)
    paradigm = Paradigm(
        n_film=N_FILM,
        n_break=N_BREAK,
        n_interference=N_INTERFERENCE,
        n_filler=N_FILLER,
        n_foils=N_FOILS,
        experiment_count=EXPERIMENT_COUNT,
    )
    factory = make_factory(
        is_emotional=make_is_emotional(
            paradigm,
            film_emotional=FILM_EMOTIONAL,
            interference_emotional=INTERFERENCE_EMOTIONAL,
            foil_emotional=FOIL_EMOTIONAL,
        ),
        is_target=make_is_target(paradigm),
    )
    base_fixed_scales = {**BASE_FIXED_SCALES, **EXTRA_FIXED_SCALES}

    prepared_cache = {}
    for reminder_condition, reminder_scales in REMINDER_CONDITIONS.items():
        for task_scale in TASK_MCF_VALUES:
            fixed_scales = {
                **base_fixed_scales,
                **reminder_scales,
                "interference_mcf_scale": float(task_scale),
            }
            pre_cache_scales, _ = split_scales_for_cache(fixed_scales, CACHE_AFTER)
            prepared_cache[(reminder_condition, float(task_scale))] = prepare_sweep(
                params,
                paradigm,
                factory,
                cache_after=CACHE_AFTER,
                **pre_cache_scales,
            )

    recognition_rows = []
    diagnostic_summary_rows = []
    diagnostic_probe_rows = []
    condition_evidence = []
    rng = random.PRNGKey(RNG_SEED + 13000)
    total = len(REMINDER_CONDITIONS) * len(TASK_MCF_VALUES)
    index = 0

    for reminder_condition, reminder_scales in REMINDER_CONDITIONS.items():
        for task_scale in TASK_MCF_VALUES:
            index += 1
            print(
                f"Condition {index}/{total}: {reminder_condition}, "
                f"task={task_scale:g}"
            )
            fixed_scales = {
                **base_fixed_scales,
                **reminder_scales,
                "interference_mcf_scale": float(task_scale),
            }
            _, post_cache_scales = split_scales_for_cache(fixed_scales, CACHE_AFTER)
            prepared = prepared_cache[(reminder_condition, float(task_scale))]
            ready_models = configure_rates(
                prepared.models,
                **post_cache_scales,
                **RETRIEVAL_FIXED_SCALES,
                start_drift_scale=0.0,
                film_source_start_drift_rate=PRIMARY_SOURCE_ORIENTATION,
                film_item_support_boost=0.0,
            )
            metadata = {
                "reminder_condition": reminder_condition,
                "task_condition": TASK_MCF_LABELS[float(task_scale)],
                "condition_label": condition_label(reminder_condition, float(task_scale)),
                "task_mcf_scale": float(task_scale),
                "film_source_start_drift_rate": PRIMARY_SOURCE_ORIENTATION,
                "recognition_threshold": RECOGNITION_THRESHOLD,
                "recognition_sensitivity": RECOGNITION_SENSITIVITY,
                "recognition_cue_reinstatement": RECOGNITION_CUE_REINSTATEMENT,
                "recognition_temporal_weight": RECOGNITION_TEMPORAL_WEIGHT,
                "recognition_source_weight": RECOGNITION_SOURCE_WEIGHT,
                "n_foils": N_FOILS,
                "experiment_count": EXPERIMENT_COUNT,
            }

            rngs, rng = sweep_rngs(
                rng,
                prepared.n_subjects,
                prepared.experiment_count,
            )
            for diagnostic_setting, diagnostic_cue_scale in recognition_diagnostic_settings():
                (
                    _,
                    labels,
                    serial_positions,
                    recognition_positions,
                    diagnostics,
                ) = batched_recognition_diagnostics(
                    ready_models,
                    rngs,
                    paradigm.film_items,
                    paradigm.foil_items,
                    paradigm.interference_items,
                    diagnostic_cue_scale,
                    RECOGNITION_THRESHOLD,
                    RECOGNITION_SENSITIVITY,
                    RECOGNITION_TEMPORAL_WEIGHT,
                    RECOGNITION_SOURCE_WEIGHT,
                )
                labels_np = np.asarray(labels)
                serial_positions_np = np.asarray(serial_positions)
                recognition_positions_np = np.asarray(recognition_positions)
                diagnostic_arrays = {
                    name: np.asarray(getattr(diagnostics, name))
                    for name in DIAGNOSTIC_METRICS
                }
                append_diagnostic_summary_rows(
                    diagnostic_summary_rows,
                    metadata,
                    diagnostic_setting,
                    diagnostic_cue_scale,
                    labels_np,
                    recognition_positions_np,
                    diagnostic_arrays,
                )
                append_grouped_diagnostic_rows(
                    diagnostic_probe_rows,
                    metadata,
                    diagnostic_setting,
                    diagnostic_cue_scale,
                    labels_np,
                    recognition_positions_np,
                    serial_positions_np,
                    diagnostic_arrays,
                )
                if diagnostic_setting == "sequential_update":
                    evidences_np = diagnostic_arrays["mfc_current_context_evidence"]
                    old_probabilities_np = diagnostic_arrays["old_probability"]
                    summary = recognition_summary_stats(
                        labels_np,
                        evidences_np,
                        old_probabilities_np,
                    )
                    for metric, values in summary.items():
                        mean, ci_lower, ci_upper = values
                        recognition_rows.append(
                            {
                                **metadata,
                                "metric": metric,
                                "value": mean,
                                "ci_lower": ci_lower,
                                "ci_upper": ci_upper,
                            }
                        )
                    old_mask = labels_np.astype(bool)
                    condition_evidence.append(
                        {
                            "metadata": metadata,
                            "old_evidence": evidences_np[old_mask],
                            "foil_evidence": evidences_np[~old_mask],
                        }
                    )

    recognition_summary_path = data_base.with_name(
        f"{OUTPUT_PREFIX}_recognition_summary.csv"
    )
    evidence_hist_path = data_base.with_name(f"{OUTPUT_PREFIX}_evidence_hist.csv")
    diagnostic_summary_path = data_base.with_name(
        f"{OUTPUT_PREFIX}_recognition_diagnostic_summary.csv"
    )
    diagnostic_probe_path = data_base.with_name(
        f"{OUTPUT_PREFIX}_recognition_probe_diagnostics.csv"
    )

    common_fields = [
        "reminder_condition",
        "task_condition",
        "condition_label",
        "task_mcf_scale",
        "film_source_start_drift_rate",
        "recognition_threshold",
        "recognition_sensitivity",
        "recognition_cue_reinstatement",
        "recognition_temporal_weight",
        "recognition_source_weight",
        "n_foils",
        "experiment_count",
    ]
    write_rows(
        recognition_summary_path,
        common_fields + ["metric", "value", "ci_lower", "ci_upper"],
        recognition_rows,
    )
    write_rows(
        diagnostic_summary_path,
        common_fields
        + [
            "diagnostic_setting",
            "diagnostic_cue_scale",
            "probe_window",
            "probe_type",
            "metric",
            "value",
            "ci_lower",
            "ci_upper",
        ],
        diagnostic_summary_rows,
    )
    write_rows(
        diagnostic_probe_path,
        common_fields
        + [
            "diagnostic_setting",
            "diagnostic_cue_scale",
            "grouping",
            "group_value",
            "probe_type",
            "metric",
            "value",
            "ci_lower",
            "ci_upper",
        ],
        diagnostic_probe_rows,
    )
    write_hist_rows(
        evidence_hist_path,
        common_fields
        + [
            "probe_type",
            "bin_left",
            "bin_right",
            "bin_center",
            "count",
            "density",
        ],
        condition_evidence,
    )
    print(recognition_summary_path)
    print(diagnostic_summary_path)
    print(diagnostic_probe_path)
    print(evidence_hist_path)
    return recognition_summary_path, diagnostic_summary_path, diagnostic_probe_path, evidence_hist_path


if __name__ == "__main__":
    run_sweep()
