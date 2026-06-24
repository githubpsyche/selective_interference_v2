from pathlib import Path
import csv
import os
import warnings

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


warnings.filterwarnings("ignore")

PROJECT_ROOT = ""
FIT_PATH = "work/fitting/Dupertuys2026_eCMR_source_only_phi_no_shared_support_best_of_1.json"
DATA_DIR = "work/simulation2_control_cued_parameter_exploration"
OUTPUT_PREFIX = os.environ.get(
    "SIM2_OUTPUT_PREFIX",
    "simulation2_control_cued_parameter_exploration",
)
RNG_SEED = 0

TASK_MCF_VALUES = [1.0, 2.0]
TASK_MCF_LABELS = {
    1.0: "Weak task encoding",
    2.0: "Strong task encoding",
}

def parse_float_list(env_name, default):
    value = os.environ.get(env_name)
    if not value:
        return default
    return [float(item.strip()) for item in value.split(",") if item.strip()]


def parse_int_list(env_name, default):
    value = os.environ.get(env_name)
    if not value:
        return default
    return [int(item.strip()) for item in value.split(",") if item.strip()]


START_DRIFT_CANDIDATES = parse_float_list(
    "SIM2_START_DRIFT_CANDIDATES",
    [0.5, 0.75, 1.0, 1.25, 1.5],
)
KAPPA_CANDIDATES = parse_float_list(
    "SIM2_KAPPA_CANDIDATES",
    [0.25, 0.5, 0.75],
)
CUE_INTERVAL_CANDIDATES = parse_int_list(
    "SIM2_CUE_INTERVAL_CANDIDATES",
    [1, 2, 3, 4, 6, 8],
)

FILM_CUE_REINSTATEMENT = 0.90
FIRST_CUE_AFTER = 0
PRIMARY_SOURCE_ORIENTATION = 0.0

N_FILM = 16
N_BREAK = 16
N_INTERFERENCE = 16
N_FILLER = 16
EXPERIMENT_COUNT = int(os.environ.get("SIM2_EXPERIMENT_COUNT", "2500"))
MAX_RECALL = 48

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

RETRIEVAL_FIXED_SCALES = {
    "tau_scale": 1.0,
    "target_recall_drift_scale": 1.0,
    "recall_drift_scale": 1.0,
}


def project_root():
    return Path(PROJECT_ROOT).expanduser() if PROJECT_ROOT else Path(__file__).resolve().parents[2]


def position_phase_labels(paradigm):
    return (
        ["film"] * paradigm.n_film
        + ["break"] * paradigm.n_break
        + ["task"] * paradigm.n_interference
        + ["filler"] * paradigm.n_filler
    )


def write_rows(path, fieldnames, rows):
    os.makedirs(path.parent, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def phase_recall_totals(spc, position_phase):
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


def build_retrieval_settings():
    settings = [(0.0, 1.0)]
    for start_drift_scale in START_DRIFT_CANDIDATES:
        for kappa in KAPPA_CANDIDATES:
            settings.append((float(start_drift_scale), float(kappa)))
    return settings


def run_sweep():
    root = project_root()
    fit_path = root / FIT_PATH
    data_dir = root / DATA_DIR
    output_base = data_dir / OUTPUT_PREFIX

    params, _ = load_fit_params(fit_path)
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

    phase_rows = []
    spc_rows = []
    retrieval_settings = build_retrieval_settings()
    rng = random.PRNGKey(RNG_SEED + 7000)
    total_conditions = (
        len(CUE_INTERVAL_CANDIDATES)
        * len(retrieval_settings)
        * len(REMINDER_CONDITIONS)
        * len(TASK_MCF_VALUES)
    )
    condition_index = 0

    for cue_interval in CUE_INTERVAL_CANDIDATES:
        for start_drift_scale, kappa in retrieval_settings:
            for reminder_condition, reminder_scales in REMINDER_CONDITIONS.items():
                for task_scale in TASK_MCF_VALUES:
                    condition_index += 1
                    if condition_index == 1 or condition_index % 24 == 0:
                        print(f"Condition {condition_index}/{total_conditions}")
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
                        start_drift_scale=float(start_drift_scale),
                        rejected_recall_drift_scale=float(kappa),
                        film_source_start_drift_rate=float(PRIMARY_SOURCE_ORIENTATION),
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
                        int(cue_interval),
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
                    totals = phase_recall_totals(spc, position_phase)
                    metadata = {
                        "cue_interval": int(cue_interval),
                        "film_cue_reinstatement": FILM_CUE_REINSTATEMENT,
                        "first_cue_after": FIRST_CUE_AFTER,
                        "start_drift_scale": float(start_drift_scale),
                        "rejected_recall_drift_scale": float(kappa),
                        "reminder_condition": reminder_condition,
                        "task_condition": TASK_MCF_LABELS[float(task_scale)],
                        "task_mcf_scale": float(task_scale),
                        "film_source_start_drift_rate": float(PRIMARY_SOURCE_ORIENTATION),
                        "experiment_count": EXPERIMENT_COUNT,
                    }
                    for phase, total in totals.items():
                        phase_rows.append({**metadata, "phase": phase, "recall_probability_mass": total})
                    for position, probability in enumerate(spc, start=1):
                        spc_rows.append(
                            {
                                **metadata,
                                "position": position,
                                "phase": position_phase[position - 1],
                                "recall_probability": float(probability),
                            }
                        )

    phase_path = output_base.with_name(f"{OUTPUT_PREFIX}_phase_totals.csv")
    spc_path = output_base.with_name(f"{OUTPUT_PREFIX}_spc.csv")
    write_rows(
        phase_path,
        [
            "cue_interval",
            "film_cue_reinstatement",
            "first_cue_after",
            "start_drift_scale",
            "rejected_recall_drift_scale",
            "reminder_condition",
            "task_condition",
            "task_mcf_scale",
            "film_source_start_drift_rate",
            "experiment_count",
            "phase",
            "recall_probability_mass",
        ],
        phase_rows,
    )
    write_rows(
        spc_path,
        [
            "cue_interval",
            "film_cue_reinstatement",
            "first_cue_after",
            "start_drift_scale",
            "rejected_recall_drift_scale",
            "reminder_condition",
            "task_condition",
            "task_mcf_scale",
            "film_source_start_drift_rate",
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


def score_candidates(phase_path):
    import pandas as pd

    phase = pd.read_csv(phase_path)
    film = phase[phase.phase.eq("film")].copy()
    reminders = ["No reminder", "With reminder"]
    tasks = ["Weak task encoding", "Strong task encoding"]
    rows = []
    for cue_interval in sorted(film.cue_interval.unique()):
        baseline = film[
            film.cue_interval.eq(cue_interval)
            & film.start_drift_scale.eq(0.0)
            & film.rejected_recall_drift_scale.eq(1.0)
        ]
        ung = baseline.pivot_table(
            index="reminder_condition",
            columns="task_condition",
            values="recall_probability_mass",
        )
        ung_vals = {(r, t): float(ung.loc[r, t]) for r in reminders for t in tasks}
        ung_no_drop = ung_vals[("No reminder", "Weak task encoding")] - ung_vals[("No reminder", "Strong task encoding")]
        ung_rem_drop = ung_vals[("With reminder", "Weak task encoding")] - ung_vals[("With reminder", "Strong task encoding")]
        for start_drift_scale in START_DRIFT_CANDIDATES:
            for kappa in KAPPA_CANDIDATES:
                candidate = film[
                    film.cue_interval.eq(cue_interval)
                    & film.start_drift_scale.eq(start_drift_scale)
                    & film.rejected_recall_drift_scale.eq(kappa)
                ]
                piv = candidate.pivot_table(
                    index="reminder_condition",
                    columns="task_condition",
                    values="recall_probability_mass",
                )
                vals = {(r, t): float(piv.loc[r, t]) for r in reminders for t in tasks}
                advantages = [vals[key] - ung_vals[key] for key in vals]
                delib_no_drop = vals[("No reminder", "Weak task encoding")] - vals[("No reminder", "Strong task encoding")]
                delib_rem_drop = vals[("With reminder", "Weak task encoding")] - vals[("With reminder", "Strong task encoding")]
                min_drop = min(ung_no_drop, ung_rem_drop, delib_no_drop, delib_rem_drop)
                drop_gap = ung_rem_drop - delib_rem_drop
                hard_pass = min(advantages) > 0 and drop_gap > 0 and min_drop > 0
                visible_pass = hard_pass and delib_no_drop >= 0.10 and delib_rem_drop >= 0.10
                score = (
                    2.2 * min(advantages)
                    + 2.8 * drop_gap
                    + 1.5 * min_drop
                    + 0.25 * float(np.mean(advantages))
                    - 0.15 * abs(delib_rem_drop - 0.8)
                )
                rows.append(
                    {
                        "cue_interval": int(cue_interval),
                        "start_drift_scale": float(start_drift_scale),
                        "rejected_recall_drift_scale": float(kappa),
                        "hard_pass": hard_pass,
                        "visible_pass": visible_pass,
                        "score": score,
                        "min_delib_advantage_vs_unguided": min(advantages),
                        "mean_delib_advantage_vs_unguided": float(np.mean(advantages)),
                        "unguided_no_reminder_drop": ung_no_drop,
                        "unguided_film_reminder_drop": ung_rem_drop,
                        "delib_no_reminder_drop": delib_no_drop,
                        "delib_film_reminder_drop": delib_rem_drop,
                        "drop_gap_film_reminder_ung_minus_delib": drop_gap,
                        "delib_no_weak": vals[("No reminder", "Weak task encoding")],
                        "delib_no_strong": vals[("No reminder", "Strong task encoding")],
                        "delib_rem_weak": vals[("With reminder", "Weak task encoding")],
                        "delib_rem_strong": vals[("With reminder", "Strong task encoding")],
                        "ung_no_weak": ung_vals[("No reminder", "Weak task encoding")],
                        "ung_no_strong": ung_vals[("No reminder", "Strong task encoding")],
                        "ung_rem_weak": ung_vals[("With reminder", "Weak task encoding")],
                        "ung_rem_strong": ung_vals[("With reminder", "Strong task encoding")],
                    }
                )
    root = project_root()
    output = root / DATA_DIR / f"{OUTPUT_PREFIX}_scores.csv"
    write_rows(output, list(rows[0].keys()), rows)
    print(output)
    return output


def main():
    phase_path, _ = run_sweep()
    score_candidates(phase_path)


if __name__ == "__main__":
    main()
