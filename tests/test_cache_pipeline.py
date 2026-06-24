import numpy as np
import os
import pytest
import jax.numpy as jnp
from jax import random

from selective_interference_v2 import (
    Paradigm,
    make_factory,
    make_is_emotional,
    make_is_target,
    prepare_sweep,
    run_sweep,
    split_scales_for_cache,
)


def _minimal_params():
    return {
        "encoding_drift_rate": jnp.asarray([0.4]),
        "start_drift_rate": jnp.asarray([0.7]),
        "recall_drift_rate": jnp.asarray([0.6]),
        "primacy_scale": jnp.asarray([0.5]),
        "primacy_decay": jnp.asarray([0.5]),
        "learning_rate": jnp.asarray([0.5]),
        "choice_sensitivity": jnp.asarray([3.0]),
        "shared_support": jnp.asarray([0.0]),
        "item_support": jnp.asarray([0.1]),
        "stop_probability_scale": jnp.asarray([0.01]),
        "stop_probability_growth": jnp.asarray([0.3]),
    }


def test_split_scales_for_cache_uses_phase_boundaries():
    scales = {
        "shared_support_scale": 0.1,
        "source_learning_baseline": 0.2,
        "reminder_drift_scale": 0.3,
        "interference_mcf_scale": 0.4,
        "filler_mcf_scale": 0.5,
        "target_recall_drift_scale": 0.6,
    }

    pre, post = split_scales_for_cache(scales, "creation")
    assert pre == {"shared_support_scale": 0.1}
    assert post == {
        "source_learning_baseline": 0.2,
        "reminder_drift_scale": 0.3,
        "interference_mcf_scale": 0.4,
        "filler_mcf_scale": 0.5,
        "target_recall_drift_scale": 0.6,
    }

    pre, post = split_scales_for_cache(scales, "reminder")
    assert pre == {
        "shared_support_scale": 0.1,
        "source_learning_baseline": 0.2,
        "reminder_drift_scale": 0.3,
    }
    assert post == {
        "interference_mcf_scale": 0.4,
        "filler_mcf_scale": 0.5,
        "target_recall_drift_scale": 0.6,
    }

    pre, post = split_scales_for_cache(scales, "filler")
    assert pre == {
        "shared_support_scale": 0.1,
        "source_learning_baseline": 0.2,
        "reminder_drift_scale": 0.3,
        "interference_mcf_scale": 0.4,
        "filler_mcf_scale": 0.5,
    }
    assert post == {"target_recall_drift_scale": 0.6}


def test_split_scales_for_cache_rejects_unknown_scale():
    with pytest.raises(ValueError, match="Unknown scale"):
        split_scales_for_cache({"not_a_scale": 1.0}, "reminder")


@pytest.mark.skipif(
    os.environ.get("RUN_SLOW_TESTS") != "1",
    reason="JAX integration validation; set RUN_SLOW_TESTS=1 to run.",
)
def test_filler_cache_matches_creation_cache_for_retrieval_sweep():
    paradigm = Paradigm(
        n_film=2,
        n_break=1,
        n_interference=2,
        n_filler=1,
        max_recall=6,
        experiment_count=2,
    )
    factory = make_factory(
        is_emotional=make_is_emotional(paradigm, film_emotional=True),
        is_target=make_is_target(paradigm),
    )
    fixed_scales = {
        "source_learning_baseline": 0.05,
        "reminder_start_drift_scale": 1.0,
        "reminder_drift_scale": 1.0,
        "interference_mcf_scale": 1.5,
        "filler_mcf_scale": 1.0,
    }
    sweep = {"target_recall_drift_scale": [0.5, 1.0]}

    def run_cached(cache_after):
        pre_cache, post_cache = split_scales_for_cache(fixed_scales, cache_after)
        prepared = prepare_sweep(
            _minimal_params(),
            paradigm,
            factory,
            cache_after=cache_after,
            **pre_cache,
        )
        recalls, _ = run_sweep(
            prepared,
            random.PRNGKey(0),
            **post_cache,
            **sweep,
        )
        return np.asarray(recalls)

    np.testing.assert_array_equal(
        run_cached("creation"),
        run_cached("filler"),
    )
