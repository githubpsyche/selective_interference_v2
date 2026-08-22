#!/usr/bin/env python3
"""Independently verify a completed control-sensitivity result package."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

import numpy as np
import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("results_dir", type=Path)
    return parser.parse_args()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_json(path: Path):
    with path.open() as handle:
        return json.load(handle)


def condition_map(frame: pd.DataFrame) -> dict[str, float]:
    if frame["condition_id"].nunique() != 4:
        raise ValueError("Incomplete 2 x 2 design in batch summaries")
    return dict(zip(frame["condition_id"], frame["film_items_recalled"], strict=True))


def recompute_primary(batch: pd.DataFrame) -> pd.DataFrame:
    baseline = batch[
        (batch["mechanism_family"] == "no_category_grid")
        & np.isclose(batch["beta_start_effective"], 0.0)
        & np.isclose(batch["kappa"], 1.0)
        & np.isclose(batch["film_item_support_boost"], 0.0)
    ]
    baseline_by_batch = {
        int(batch_id): condition_map(group)
        for batch_id, group in baseline.groupby("batch_id")
    }
    rows = []
    for (parameter_id, batch_id), group in batch.groupby(
        ["parameter_id", "batch_id"], sort=False
    ):
        candidate = condition_map(group)
        unguided = baseline_by_batch[int(batch_id)]
        candidate_sensitivity = (
            candidate["reminder_weak"]
            - candidate["reminder_strong"]
            - candidate["no_reminder_weak"]
            + candidate["no_reminder_strong"]
        )
        baseline_sensitivity = (
            unguided["reminder_weak"]
            - unguided["reminder_strong"]
            - unguided["no_reminder_weak"]
            + unguided["no_reminder_strong"]
        )
        candidate_endpoint_loss = (
            candidate["no_reminder_weak"] - candidate["reminder_strong"]
        )
        baseline_endpoint_loss = (
            unguided["no_reminder_weak"] - unguided["reminder_strong"]
        )
        rows.append(
            {
                "parameter_id": parameter_id,
                "batch_id": int(batch_id),
                "primary_recomputed": baseline_sensitivity - candidate_sensitivity,
                "endpoint_recomputed": (
                    baseline_endpoint_loss - candidate_endpoint_loss
                ),
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    args = parse_args()
    results_dir = args.results_dir.resolve()
    manifest = read_json(results_dir / "run_manifest.json")
    checks: dict[str, dict] = {}

    output_mismatches = {}
    for filename, expected in manifest["output_sha256"].items():
        path = results_dir / filename
        observed = sha256_file(path) if path.exists() else None
        if observed != expected:
            output_mismatches[filename] = {"expected": expected, "observed": observed}
    checks["output_hashes"] = {
        "pass": not output_mismatches,
        "mismatches": output_mismatches,
    }

    project_root = Path(manifest["project_root"])
    source_mismatches = {}
    for relative, expected in manifest["source_sha256"].items():
        path = project_root / relative
        observed = sha256_file(path) if path.exists() else None
        if observed != expected:
            source_mismatches[relative] = {"expected": expected, "observed": observed}
    checks["source_hashes"] = {
        "pass": not source_mismatches,
        "mismatches": source_mismatches,
    }

    batch = pd.read_csv(results_dir / "batch_summaries.csv")
    saved_batches = pd.read_csv(results_dir / "estimand_batches.csv")
    recomputed = recompute_primary(batch)
    comparison = saved_batches.merge(
        recomputed,
        on=["parameter_id", "batch_id"],
        how="outer",
        validate="one_to_one",
        indicator=True,
    )
    primary_error = float(
        np.max(
            np.abs(
                comparison["primary_selective_protection"]
                - comparison["primary_recomputed"]
            )
        )
    )
    checks["primary_estimand_recomputed"] = {
        "pass": bool((comparison["_merge"] == "both").all() and primary_error < 1e-8),
        "maximum_absolute_error": primary_error,
    }
    endpoint_error = float(
        np.max(
            np.abs(
                comparison["endpoint_protection"]
                - comparison["endpoint_recomputed"]
            )
        )
    )
    checks["endpoint_estimand_recomputed"] = {
        "pass": bool((comparison["_merge"] == "both").all() and endpoint_error < 1e-8),
        "maximum_absolute_error": endpoint_error,
    }

    saved_summary = pd.read_csv(results_dir / "estimand_summary.csv")
    recomputed_means = recomputed.groupby("parameter_id", as_index=False)[
        "primary_recomputed"
    ].mean()
    mean_comparison = saved_summary.merge(
        recomputed_means, on="parameter_id", how="outer", validate="one_to_one"
    )
    summary_error = float(
        np.max(
            np.abs(
                mean_comparison["primary_selective_protection_mean"]
                - mean_comparison["primary_recomputed"]
            )
        )
    )
    checks["primary_summary_recomputed"] = {
        "pass": summary_error < 1e-8,
        "maximum_absolute_error": summary_error,
    }

    forbidden = [
        column
        for column in saved_summary.columns
        if "weighted" in column.lower() or column.lower() in {"score", "winner"}
    ]
    checks["no_posthoc_score_columns"] = {
        "pass": not forbidden,
        "forbidden_columns": forbidden,
    }

    runner_verification = read_json(results_dir / "verification.json")
    checks["runner_verification"] = {
        "pass": bool(runner_verification["pass"]),
    }
    result = {"pass": all(item["pass"] for item in checks.values()), "checks": checks}
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["pass"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
