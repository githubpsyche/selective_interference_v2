import numpy as np
import jax.numpy as jnp

from selective_interference_v2 import (
    Paradigm,
    make_factory,
    make_is_emotional,
    make_is_target,
    recognition_context_to_item_support,
    recognition_evidence,
    recognition_probe_similarity,
    simulate_sequential_recognition_diagnostics,
    simulate_sequential_recognition,
)


def _minimal_params():
    return {
        "encoding_drift_rate": jnp.asarray(1.0),
        "start_drift_rate": jnp.asarray(0.0),
        "recall_drift_rate": jnp.asarray(0.6),
        "primacy_scale": jnp.asarray(0.5),
        "primacy_decay": jnp.asarray(0.5),
        "learning_rate": jnp.asarray(0.5),
        "choice_sensitivity": jnp.asarray(3.0),
        "shared_support": jnp.asarray(0.0),
        "item_support": jnp.asarray(0.1),
        "stop_probability_scale": jnp.asarray(0.01),
        "stop_probability_growth": jnp.asarray(0.3),
    }


def test_default_paradigm_keeps_existing_standard_geometry():
    paradigm = Paradigm()

    assert paradigm.n_foils == 0
    assert paradigm.list_length == 64
    np.testing.assert_array_equal(np.asarray(paradigm.film_items), np.arange(1, 17))
    np.testing.assert_array_equal(np.asarray(paradigm.filler_items), np.arange(49, 65))
    assert np.asarray(paradigm.foil_items).size == 0


def test_foil_items_append_after_study_phases():
    paradigm = Paradigm(
        n_film=2,
        n_break=1,
        n_interference=2,
        n_filler=1,
        n_foils=3,
    )
    studied = np.concatenate([
        np.asarray(paradigm.film_items),
        np.asarray(paradigm.break_items),
        np.asarray(paradigm.interference_items),
        np.asarray(paradigm.filler_items),
    ])

    assert paradigm.list_length == 9
    np.testing.assert_array_equal(np.asarray(paradigm.foil_items), np.array([7, 8, 9]))
    assert np.intersect1d(studied, np.asarray(paradigm.foil_items)).size == 0


def test_foils_can_be_source_matched_without_being_targets():
    paradigm = Paradigm(
        n_film=2,
        n_break=1,
        n_interference=2,
        n_filler=1,
        n_foils=3,
    )

    is_emotional = make_is_emotional(
        paradigm,
        film_emotional=True,
        foil_emotional=True,
    )
    is_target = make_is_target(paradigm)

    np.testing.assert_array_equal(
        np.asarray(is_emotional),
        np.array([1, 1, 0, 0, 0, 0, 1, 1, 1], dtype=float),
    )
    np.testing.assert_array_equal(
        np.asarray(is_target),
        np.array([1, 1, 0, 0, 0, 0, 0, 0, 0], dtype=float),
    )


def test_sequential_recognition_updates_context_only():
    paradigm = Paradigm(n_film=1, n_break=0, n_interference=0, n_filler=0, n_foils=1)
    factory = make_factory(
        is_emotional=make_is_emotional(
            paradigm,
            film_emotional=True,
            foil_emotional=True,
        ),
        is_target=make_is_target(paradigm),
    )
    model = factory(paradigm.list_length, _minimal_params(), None)
    model = model.experience_film(jnp.int32(1)).start_retrieving()

    before = model
    final_model, evidences, old_probabilities = simulate_sequential_recognition(
        model,
        jnp.array([1, 2], dtype=jnp.int32),
        cue_scale=0.9,
        threshold=0.5,
        sensitivity=20.0,
    )

    assert evidences.shape == (2,)
    assert old_probabilities.shape == (2,)
    assert not np.allclose(
        np.asarray(final_model.context.state),
        np.asarray(before.context.state),
    )
    np.testing.assert_allclose(
        np.asarray(final_model.mfc.state),
        np.asarray(before.mfc.state),
        rtol=1e-6,
    )
    np.testing.assert_allclose(
        np.asarray(final_model.mcf.state),
        np.asarray(before.mcf.state),
        rtol=1e-6,
    )
    np.testing.assert_allclose(
        np.asarray(final_model.emotion_mfc.state),
        np.asarray(before.emotion_mfc.state),
        rtol=1e-6,
    )
    np.testing.assert_allclose(
        np.asarray(final_model.emotion_mcf.state),
        np.asarray(before.emotion_mcf.state),
        rtol=1e-6,
    )
    np.testing.assert_array_equal(
        np.asarray(final_model.recalls),
        np.asarray(before.recalls),
    )
    np.testing.assert_array_equal(
        np.asarray(final_model.recallable),
        np.asarray(before.recallable),
    )


def test_recognition_diagnostics_allow_no_probe_context_update():
    paradigm = Paradigm(n_film=1, n_break=0, n_interference=0, n_filler=0, n_foils=1)
    factory = make_factory(
        is_emotional=make_is_emotional(
            paradigm,
            film_emotional=True,
            foil_emotional=True,
        ),
        is_target=make_is_target(paradigm),
    )
    model = factory(paradigm.list_length, _minimal_params(), None)
    model = model.experience_film(jnp.int32(1)).start_retrieving()

    final_model, diagnostics = simulate_sequential_recognition_diagnostics(
        model,
        jnp.array([1, 2], dtype=jnp.int32),
        cue_scale=0.0,
        threshold=0.5,
        sensitivity=20.0,
        film_items=paradigm.film_items,
        task_items=paradigm.interference_items,
    )

    assert diagnostics.mfc_current_context_evidence.shape == (2,)
    assert diagnostics.cmr_ia_temporal_similarity.shape == (2,)
    np.testing.assert_allclose(
        np.asarray(final_model.context.state),
        np.asarray(model.context.state),
        rtol=1e-6,
    )
    np.testing.assert_allclose(
        np.asarray(final_model.emotion_context.state),
        np.asarray(model.emotion_context.state),
        rtol=1e-6,
    )


def test_studied_film_probe_has_more_temporal_evidence_than_foil():
    paradigm = Paradigm(n_film=1, n_break=0, n_interference=0, n_filler=0, n_foils=1)
    factory = make_factory(
        is_emotional=make_is_emotional(
            paradigm,
            film_emotional=True,
            foil_emotional=True,
        ),
        is_target=make_is_target(paradigm),
    )
    model = factory(paradigm.list_length, _minimal_params(), None)
    model = model.experience_film(jnp.int32(1)).start_retrieving()

    old_evidence = recognition_evidence(
        model,
        jnp.int32(1),
        temporal_weight=1.0,
        source_weight=0.0,
    )
    foil_evidence = recognition_evidence(
        model,
        jnp.int32(2),
        temporal_weight=1.0,
        source_weight=0.0,
    )

    assert float(old_evidence) > float(foil_evidence)


def test_probe_similarity_is_normalized_current_context_evidence():
    paradigm = Paradigm(n_film=1, n_break=0, n_interference=0, n_filler=0, n_foils=1)
    factory = make_factory(
        is_emotional=make_is_emotional(
            paradigm,
            film_emotional=True,
            foil_emotional=True,
        ),
        is_target=make_is_target(paradigm),
    )
    model = factory(paradigm.list_length, _minimal_params(), None)
    model = model.experience_film(jnp.int32(1)).start_retrieving()

    temporal_evidence = recognition_evidence(
        model,
        jnp.int32(1),
        temporal_weight=1.0,
        source_weight=0.0,
    )
    source_evidence = recognition_evidence(
        model,
        jnp.int32(1),
        temporal_weight=0.0,
        source_weight=1.0,
    )
    temporal_similarity, source_similarity = recognition_probe_similarity(
        model,
        jnp.int32(1),
    )
    item = model.items[0]
    temporal_norm = jnp.linalg.norm(model.mfc.probe(item))
    source_norm = jnp.linalg.norm(model.emotion_mfc.probe(item))

    np.testing.assert_allclose(
        np.asarray(temporal_similarity * temporal_norm),
        np.asarray(temporal_evidence),
        rtol=1e-6,
    )
    np.testing.assert_allclose(
        np.asarray(source_similarity * source_norm),
        np.asarray(source_evidence),
        rtol=1e-6,
    )


def test_zero_probe_has_zero_similarity_and_support():
    paradigm = Paradigm(n_film=1, n_break=0, n_interference=1, n_filler=0, n_foils=1)
    factory = make_factory(
        is_emotional=make_is_emotional(paradigm, film_emotional=True),
        is_target=make_is_target(paradigm),
    )
    model = factory(paradigm.list_length, _minimal_params(), None)
    model = (
        model
        .experience_film(jnp.int32(1))
        .experience_interference(jnp.int32(2))
        .start_retrieving()
    )

    temporal_similarity, source_similarity = recognition_probe_similarity(
        model,
        jnp.int32(0),
    )
    probe_support, _, _, _ = recognition_context_to_item_support(
        model,
        jnp.int32(0),
        paradigm.film_items,
        paradigm.interference_items,
    )

    assert float(temporal_similarity) == 0.0
    assert float(source_similarity) == 0.0
    assert float(probe_support) == 0.0


def test_context_to_item_diagnostics_respond_to_interference_mcf_scale():
    paradigm = Paradigm(n_film=1, n_break=0, n_interference=1, n_filler=0, n_foils=1)
    factory = make_factory(
        is_emotional=make_is_emotional(paradigm, film_emotional=True),
        is_target=make_is_target(paradigm),
    )
    base = factory(paradigm.list_length, _minimal_params(), None)
    base = base.experience_film(jnp.int32(1)).start_reminders().remind(jnp.int32(1))

    weak = (
        base
        .replace(interference_mcf_scale=jnp.asarray(1.0))
        .experience_interference(jnp.int32(2))
        .start_retrieving()
    )
    strong = (
        base
        .replace(interference_mcf_scale=jnp.asarray(3.0))
        .experience_interference(jnp.int32(2))
        .start_retrieving()
    )
    _, _, weak_task_mass, _ = recognition_context_to_item_support(
        weak,
        jnp.int32(1),
        paradigm.film_items,
        paradigm.interference_items,
    )
    _, _, strong_task_mass, _ = recognition_context_to_item_support(
        strong,
        jnp.int32(1),
        paradigm.film_items,
        paradigm.interference_items,
    )

    assert float(strong_task_mass) > float(weak_task_mass)
