import numpy as np
import jax.numpy as jnp
from jax import vmap

from selective_interference_v2 import configure_rates, make_factory


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


def test_film_source_start_drift_rate_is_set_directly():
    factory = make_factory()
    models = vmap(lambda p: factory(6, p, None))(_minimal_params())

    configured = configure_rates(
        models,
        film_source_start_drift_rate=0.6,
    )
    np.testing.assert_allclose(
        np.asarray(configured.film_source_start_drift_rate),
        np.asarray([0.6]),
        rtol=1e-6,
    )


def test_source_learning_baseline_is_set_directly():
    factory = make_factory()
    models = vmap(lambda p: factory(6, p, None))(_minimal_params())

    configured = configure_rates(models, source_learning_baseline=1.0)

    np.testing.assert_allclose(
        np.asarray(configured.source_learning_baseline),
        np.asarray([1.0]),
        rtol=1e-6,
    )


def test_neutral_source_input_scale_controls_neutral_source_feature():
    factory = make_factory(is_emotional=jnp.array([1, 0, 0, 0, 0, 0]))
    models = vmap(lambda p: factory(6, p, None))(_minimal_params())

    configured = configure_rates(models, neutral_source_input_scale=0.0)

    actual = np.asarray(configured.emotion_mfc.state[0])
    np.testing.assert_allclose(actual[0, 1], 0.5, rtol=1e-6)
    np.testing.assert_allclose(actual[1:, 2], np.zeros(5), rtol=1e-6)


def test_source_learning_baseline_gives_neutral_items_source_learning():
    factory = make_factory(is_emotional=jnp.zeros(6))
    scalar_params = {key: value[0] for key, value in _minimal_params().items()}
    model = factory(6, scalar_params, None)

    baseline_off = model.replace(source_learning_baseline=jnp.asarray(0.0))
    baseline_on = model.replace(source_learning_baseline=jnp.asarray(1.0))

    np.testing.assert_allclose(
        np.asarray(baseline_off._emotional_mcf_learning_rate()),
        np.asarray(0.0),
        rtol=1e-6,
    )
    np.testing.assert_allclose(
        np.asarray(baseline_on._emotional_mcf_learning_rate()),
        np.asarray(1.5),
        rtol=1e-6,
    )


def test_recall_drift_scale_multiplies_recall_drift_rate():
    factory = make_factory()
    models = vmap(lambda p: factory(6, p, None))(_minimal_params())

    configured = configure_rates(models, recall_drift_scale=0.5)

    np.testing.assert_allclose(
        np.asarray(configured.recall_drift_rate),
        0.5 * np.asarray(models.recall_drift_rate),
        rtol=1e-6,
    )


def test_target_recall_drift_scale_is_set_directly():
    factory = make_factory()
    models = vmap(lambda p: factory(6, p, None))(_minimal_params())

    configured = configure_rates(models, target_recall_drift_scale=1.5)

    np.testing.assert_allclose(
        np.asarray(configured.target_recall_drift_scale),
        np.asarray([1.5]),
        rtol=1e-6,
    )


def test_primacy_override_recomputes_primacy_vector():
    factory = make_factory()
    models = vmap(lambda p: factory(6, p, None))(_minimal_params())

    configured = configure_rates(models, primacy_scale=0.0, primacy_decay=1.5)

    np.testing.assert_allclose(
        np.asarray(configured.primacy),
        np.ones((1, 6)),
        rtol=1e-6,
    )
