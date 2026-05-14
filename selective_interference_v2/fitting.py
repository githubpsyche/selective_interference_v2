"""Fit-artifact loading utilities."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Mapping

import jax
import jax.numpy as jnp


def _as_1d_array(value) -> jax.Array:
    arr = jnp.asarray(value)
    if arr.ndim == 0:
        return arr.reshape((1,))
    return arr


def _extract_fit_params(results: Mapping) -> dict[str, jax.Array]:
    if "fits" not in results:
        raise ValueError("Fit JSON must contain a top-level 'fits' object")

    fits = results["fits"]
    if not isinstance(fits, Mapping):
        raise ValueError("Fit JSON 'fits' field must be a mapping")

    return {
        key: _as_1d_array(value)
        for key, value in fits.items()
        if key != "subject"
    }


def load_fit_params(fit_path: str | Path) -> tuple[dict[str, jax.Array], int]:
    """Load fitted parameters from a jaxcmr fit JSON artifact.

    Parameters
    ----------
    fit_path : str or Path
        Path to a fit JSON with a top-level ``fits`` mapping.

    Returns
    -------
    tuple[dict[str, jax.Array], int]
        Loaded parameter arrays and number of fitted subjects/parameter sets.

    """
    fit_path = Path(fit_path)
    with fit_path.open() as handle:
        results = json.load(handle)

    params = _extract_fit_params(results)
    if not params:
        raise ValueError("Fit JSON contains no fitted parameters")

    n_subjects = len(next(iter(params.values())))
    return params, n_subjects
