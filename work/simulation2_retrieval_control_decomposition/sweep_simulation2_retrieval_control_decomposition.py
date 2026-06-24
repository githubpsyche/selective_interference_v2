from __future__ import annotations

import csv
import os
from pathlib import Path

from jax import random
from jaxcmr.analyses.spc import fixed_pres_spc
from jaxcmr.helpers import find_project_root
import numpy as np

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
    sweep_rngs,
)


PROJECT_ROOT = ""
FIT_PATH = "work/fitting/Dupertuys2026_eCMR_source_only_phi_no_shared_support_best_of_1.json"
DATA_DIR = "work/simulation2_retrieval_control_decomposition"
OUTPUT_PREFIX = os.environ.get(
    "SIM2_RETRIEVAL_CONTROL_DECOMP_PREFIX",
    "simulation2_retrieval_control_decomposition",
)
RNG_SEED = 0

N_FILM = 16
N_BREAK = 16
N_INTERFERENCE = 16
N_FILLER = 16
EXPERIMENT_COUNT = int(os.environ.get("SIM2_RETRIEVAL_CONTROL_DECOMP_EXPERIMENT_COUNT", "5000"))
MAX_RECALL = 48

START_DRIFT_ON = float(os.environ.get("SIM2_START_DRIFT_ON", "1.0"))
TARGET_MONITORING_ON = float(os.environ.get("SIM2_TARGET_MONITORING_ON", "0.0"))
FILM_GOAL_BOOST_ON = float(os.environ.get("SIM2_FILM_GOAL_BOOST_ON", "1.0"))
TARGET_MONITORING_OFF = 1.0

PRIMARY_SOURCE_ORIENTATION = 0.0
FILM_CUE_REINSTATEMENT = 0.90
CUE_INTERVAL = 4
FIRST_CUE_AFTER = 0

FILM_EMOTIONAL = True
INTERFERENCE_EMOTIONAL = False
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

ENDPOINTS = [
    {
        "endpoint": "No reminder + weak task encoding",
        "endpoint_short": "Low endpoint",
        "reminder_condition": "No reminder",
        "reminder_start_drift_scale": 0.0,
        "reminder_drift_scale": 0.0,
        "task_condition": "Weak task encoding",
        "task_mcf_scale": 1.0,
    },
    {
        "endpoint": "Film reminder + strong task encoding",
        "endpoint_short": "High endpoint",
        "reminder_condition": "With reminder",
        "reminder_start_drift_scale": 1.0,
        "reminder_drift_scale": 1.0,
        "task_condition": "Strong task encoding",
        "task_mcf_scale": 2.0,
    },
]


def project_root() -> Path:
    return Path(PROJECT_ROOT).expanduser() if PROJECT_ROOT else Path(__file__).resolve().parents[2]


def position_phase_labels(paradigm: Paradigm) -> list[str]:
    return (
        ["film"] * paradigm.n_film
        + ["break"] * paradigm.n_break
        + ["task"] * paradigm.n_interference
        + ["filler"] * paradigm.n_filler
    )


def write_rows(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def phase_totals(spc: np.ndarray, position_phase: list[str]) -> dict[str, float]:
    totals = {}
    for phase in sorted(set(position_phase)):
        positions = [idx for idx, value in enumerate(position_phase) if value == phase]
        totals[phase] = float(np.sum(spc[positions]))
    return totals


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


def retrieval_packages() -> list[dict]:
    rows = []
    package_index = 0
    for film_goal in [False, True]:
        for start_reinstatement, target_monitoring in [
            (False, False),
            (False, True),
            (True, False),
            (True, True),
        ]:
            package_index += 1
            if start_reinstatement and target_monitoring:
                within_group_label = "Reinstatement\n+ monitoring"
            elif start_reinstatement:
                within_group_label = "Start-of-film\nreinstatement"
            elif target_monitoring:
                within_group_label = "Target\nmonitoring"
            else:
                within_group_label = "None"
            control_parts = []
            if film_goal:
                control_parts.append("film-source goal")
            if start_reinstatement:
                control_parts.append("start-of-film reinstatement")
            if target_monitoring:
                control_parts.append("target monitoring")
            package_label = " + ".join(control_parts) if control_parts else "No deliberate control"
            rows.append(
                {
                    "package_index": package_index,
                    "film_goal_included": film_goal,
                    "start_reinstatement_included": start_reinstatement,
                    "target_monitoring_included": target_monitoring,
                    "goal_group": "Film-source goal present" if film_goal else "Film-source goal absent",
                    "within_group_label": within_group_label,
                    "retrieval_control_package": package_label,
                    "start_drift_scale": START_DRIFT_ON if start_reinstatement else 0.0,
                    "film_item_support_boost": FILM_GOAL_BOOST_ON if film_goal else 0.0,
                    "rejected_recall_drift_scale": (
                        TARGET_MONITORING_ON if target_monitoring else TARGET_MONITORING_OFF
                    ),
                }
            )
    return rows


def run_sweep():
    root = project_root()
    data_dir = root / DATA_DIR
    output_base = data_dir / OUTPUT_PREFIX

    params, _ = load_fit_params(root / FIT_PATH)
    paradigm = Paradigm(
        n_film=N_FILM,
        n_break=N_BREAK,
        n_interference=N_INTERFERENCE,
        n_filler=N_FILLER,
        experiment_count=EXPERIMENT_COUNT,
        max_recall=MAX_RECALL,
    )
    factory = make_factory(
        is_emotional=make_is_emotional(
            paradigm,
            film_emotional=FILM_EMOTIONAL,
            interference_emotional=INTERFERENCE_EMOTIONAL,
        ),
        is_target=make_is_target(paradigm),
    )
    position_phase = position_phase_labels(paradigm)
    n_presented = len(position_phase)
    base_fixed_scales = {**BASE_FIXED_SCALES, **EXTRA_FIXED_SCALES}

    prepared_cache = {}
    for endpoint in ENDPOINTS:
        fixed_scales = {
            **base_fixed_scales,
            "reminder_start_drift_scale": endpoint["reminder_start_drift_scale"],
            "reminder_drift_scale": endpoint["reminder_drift_scale"],
            "interference_mcf_scale": endpoint["task_mcf_scale"],
        }
        pre_cache_scales, _ = split_scales_for_cache(fixed_scales, CACHE_AFTER)
        prepared_cache[endpoint["endpoint"]] = prepare_sweep(
            params,
            paradigm,
            factory,
            cache_after=CACHE_AFTER,
            **pre_cache_scales,
        )

    phase_rows = []
    spc_rows = []
    packages = retrieval_packages()
    rng = random.PRNGKey(RNG_SEED + 11500)
    total = len(packages) * len(ENDPOINTS)
    index = 0

    for package in packages:
        for endpoint in ENDPOINTS:
            index += 1
            print(
                f"Condition {index}/{total}: {package['retrieval_control_package']}; "
                f"{endpoint['endpoint']}"
            )
            fixed_scales = {
                **base_fixed_scales,
                "reminder_start_drift_scale": endpoint["reminder_start_drift_scale"],
                "reminder_drift_scale": endpoint["reminder_drift_scale"],
                "interference_mcf_scale": endpoint["task_mcf_scale"],
            }
            _, post_cache_scales = split_scales_for_cache(fixed_scales, CACHE_AFTER)
            prepared = prepared_cache[endpoint["endpoint"]]
            ready_models = configure_rates(
                prepared.models,
                **post_cache_scales,
                tau_scale=1.0,
                target_recall_drift_scale=1.0,
                recall_drift_scale=1.0,
                rejected_recall_drift_scale=package["rejected_recall_drift_scale"],
                start_drift_scale=package["start_drift_scale"],
                film_source_start_drift_rate=PRIMARY_SOURCE_ORIENTATION,
                film_item_support_boost=package["film_item_support_boost"],
            )
            rngs, rng = sweep_rngs(
                rng,
                prepared.n_subjects,
                prepared.experiment_count,
            )
            recalls, _, _ = batched_cued_recall(
                ready_models,
                rngs,
                paradigm.film_items,
                FILM_CUE_REINSTATEMENT,
                paradigm.max_recall,
                CUE_INTERVAL,
                FIRST_CUE_AFTER,
            )
            raw_recalls = np.asarray(recalls).reshape(-1, recalls.shape[-1])
            remapped_recalls = np.asarray(
                standard_remap(
                    raw_recalls,
                    paradigm,
                    show_break=True,
                )
            )
            spc = np.asarray(fixed_pres_spc(remapped_recalls, n_presented), dtype=float)
            metadata = {
                "package_index": package["package_index"],
                "retrieval_control_package": package["retrieval_control_package"],
                "goal_group": package["goal_group"],
                "within_group_label": package["within_group_label"],
                "film_goal_included": package["film_goal_included"],
                "start_reinstatement_included": package["start_reinstatement_included"],
                "target_monitoring_included": package["target_monitoring_included"],
                "start_drift_scale": package["start_drift_scale"],
                "film_item_support_boost": package["film_item_support_boost"],
                "rejected_recall_drift_scale": package["rejected_recall_drift_scale"],
                "endpoint": endpoint["endpoint"],
                "endpoint_short": endpoint["endpoint_short"],
                "reminder_condition": endpoint["reminder_condition"],
                "task_condition": endpoint["task_condition"],
                "task_mcf_scale": endpoint["task_mcf_scale"],
                "film_source_start_drift_rate": PRIMARY_SOURCE_ORIENTATION,
                "film_cue_reinstatement": FILM_CUE_REINSTATEMENT,
                "cue_interval": CUE_INTERVAL,
                "first_cue_after": FIRST_CUE_AFTER,
                "experiment_count": EXPERIMENT_COUNT,
            }
            for phase, value in phase_totals(spc, position_phase).items():
                phase_rows.append(
                    {
                        **metadata,
                        "phase": phase,
                        "recall_probability_mass": value,
                    }
                )
            for position, phase in enumerate(position_phase, start=1):
                spc_rows.append(
                    {
                        **metadata,
                        "position": position,
                        "phase": phase,
                        "recall_probability": float(spc[position - 1]),
                    }
                )

    phase_path = output_base.with_name(f"{OUTPUT_PREFIX}_phase_totals.csv")
    spc_path = output_base.with_name(f"{OUTPUT_PREFIX}_spc.csv")
    write_rows(
        phase_path,
        [
            "package_index",
            "retrieval_control_package",
            "goal_group",
            "within_group_label",
            "film_goal_included",
            "start_reinstatement_included",
            "target_monitoring_included",
            "start_drift_scale",
            "film_item_support_boost",
            "rejected_recall_drift_scale",
            "endpoint",
            "endpoint_short",
            "reminder_condition",
            "task_condition",
            "task_mcf_scale",
            "film_source_start_drift_rate",
            "film_cue_reinstatement",
            "cue_interval",
            "first_cue_after",
            "experiment_count",
            "phase",
            "recall_probability_mass",
        ],
        phase_rows,
    )
    write_rows(
        spc_path,
        [
            "package_index",
            "retrieval_control_package",
            "goal_group",
            "within_group_label",
            "film_goal_included",
            "start_reinstatement_included",
            "target_monitoring_included",
            "start_drift_scale",
            "film_item_support_boost",
            "rejected_recall_drift_scale",
            "endpoint",
            "endpoint_short",
            "reminder_condition",
            "task_condition",
            "task_mcf_scale",
            "film_source_start_drift_rate",
            "film_cue_reinstatement",
            "cue_interval",
            "first_cue_after",
            "experiment_count",
            "position",
            "phase",
            "recall_probability",
        ],
        spc_rows,
    )
    print(phase_path)
    print(spc_path)
    return phase_path, spc_path


if __name__ == "__main__":
    run_sweep()
