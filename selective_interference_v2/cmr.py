"""Phase-aware source-only eCMR for selective-interference simulations.

The model in this module keeps the phase methods needed by the
selective-interference paradigm while matching the source-context pathway used
by ``jaxcmr.models.ecmr``.  The primary v2 variant is source-only phi eCMR:
emotion modulates emotional/source context-to-item learning, while temporal
context-to-item learning remains primacy-driven unless an explicit non-primary
broad-phi flag is supplied.
"""

from typing import Callable, Mapping, Optional

from jax import lax
from jax import numpy as jnp
from simple_pytree import Pytree

import jaxcmr.components.context as TemporalContext
import jaxcmr.components.linear_memory as LinearMemory
from jaxcmr.components.termination import PositionalTermination
from jaxcmr.math import exponential_primacy_decay, lb, power_scale
from jaxcmr.typing import (
    Array,
    ContextCreateFn,
    Float,
    Float_,
    Int_,
    MemoryCreateFn,
    TerminationPolicyCreateFn,
)


class PhasedSourceOnlyECMR(Pytree):
    """Source-only eCMR with selective-interference phase methods."""

    def __init__(
        self,
        list_length: int,
        parameters: Mapping[str, Float_],
        is_emotional: Optional[Float[Array, " items"]] = None,
        is_target: Optional[Float[Array, " items"]] = None,
        mfc_create_fn: MemoryCreateFn = LinearMemory.init_mfc,
        mcf_create_fn: MemoryCreateFn = LinearMemory.init_mcf,
        context_create_fn: ContextCreateFn = TemporalContext.init,
        termination_policy_create_fn: TerminationPolicyCreateFn = PositionalTermination,
    ):
        """Initialize phase-aware source-only eCMR.

        Parameters
        ----------
        list_length : int
            Number of item slots in the current sweep tier.
        parameters : Mapping[str, Float_]
            Model parameters.  The primary source-only variant fixes
            ``phi_emot_modulates_temporal=False`` and
            ``modulate_emotion_by_primacy=True``.
        is_emotional : Float[Array, " items"] or None, optional
            Per-item emotional/source flag.  Missing values default to neutral.
        is_target : Float[Array, " items"] or None, optional
            Per-item target flag for retrieval monitoring.  Missing values
            default to non-target.
        mfc_create_fn, mcf_create_fn, context_create_fn,
        termination_policy_create_fn
            Component factories matching ``jaxcmr`` model factories.
        """
        self.encoding_drift_rate = parameters["encoding_drift_rate"]
        self.start_drift_rate = parameters["start_drift_rate"]
        self.recall_drift_rate = parameters["recall_drift_rate"]

        if "emotion_drift_rate" in parameters:
            self.emotion_encoding_drift_rate = parameters["emotion_drift_rate"]
            self.emotion_recall_drift_rate = parameters["emotion_drift_rate"]
        else:
            self.emotion_encoding_drift_rate = parameters.get(
                "emotion_encoding_drift_rate",
                1.0,
            )
            self.emotion_recall_drift_rate = parameters.get(
                "emotion_recall_drift_rate",
                self.recall_drift_rate,
            )

        self.primacy_scale = parameters["primacy_scale"]
        self.primacy_decay = parameters["primacy_decay"]
        self.mfc_learning_rate = parameters["learning_rate"]
        self.mcf_sensitivity = parameters["choice_sensitivity"]
        self.learn_after_context_update = jnp.asarray(
            parameters.get("learn_after_context_update", True),
            dtype=bool,
        )
        self.allow_repeated_recalls = jnp.asarray(
            parameters.get("allow_repeated_recalls", False),
            dtype=bool,
        )
        self.modulate_emotion_by_primacy = jnp.asarray(
            parameters.get("modulate_emotion_by_primacy", True),
            dtype=bool,
        )
        self.phi_emot_modulates_temporal = jnp.asarray(
            parameters.get("phi_emot_modulates_temporal", False),
            dtype=bool,
        )
        self.modulate_temporal_emotion_by_primacy = jnp.asarray(
            parameters.get("modulate_temporal_emotion_by_primacy", False),
            dtype=bool,
        )

        self.emotion_scale = parameters.get("emotion_scale", 0.0)
        self.temporal_emotion_scale = parameters.get(
            "temporal_emotion_scale",
            self.emotion_scale,
        )
        self.source_learning_baseline = parameters.get(
            "source_learning_baseline",
            0.0,
        )
        self.neutral_source_input_scale = parameters.get(
            "neutral_source_input_scale",
            1.0,
        )
        self.rejected_recall_drift_scale = parameters.get(
            "rejected_recall_drift_scale",
            1.0,
        )
        self.target_recall_drift_scale = parameters.get(
            "target_recall_drift_scale",
            1.0,
        )
        self.film_source_start_drift_rate = parameters.get(
            "film_source_start_drift_rate",
            0.0,
        )
        self.film_item_support_boost = parameters.get(
            "film_item_support_boost",
            0.0,
        )
        _is_emotional = (
            is_emotional if is_emotional is not None else jnp.zeros(list_length)
        )
        self.is_emotional = jnp.array(_is_emotional, dtype=jnp.float32)
        _is_target = is_target if is_target is not None else jnp.zeros(list_length)
        self.is_target = jnp.array(_is_target, dtype=jnp.float32)
        self.phi_emot = self.emotion_scale * self.is_emotional
        self.temporal_phi_emot = self.temporal_emotion_scale * self.is_emotional

        # Phase-specific rates default to base eCMR rates.
        self.break_drift_rate = parameters.get(
            "break_drift_rate",
            self.encoding_drift_rate,
        )
        self.break_mcf_scale = parameters.get("break_mcf_scale", 1.0)
        self.interference_drift_rate = parameters.get(
            "interference_drift_rate",
            self.encoding_drift_rate,
        )
        self.interference_mcf_scale = parameters.get("interference_mcf_scale", 1.0)
        self.filler_drift_rate = parameters.get(
            "filler_drift_rate",
            self.encoding_drift_rate,
        )
        self.filler_mcf_scale = parameters.get("filler_mcf_scale", 1.0)
        self.reminder_start_drift_rate = parameters.get(
            "reminder_start_drift_rate",
            self.start_drift_rate,
        )
        self.reminder_drift_rate = parameters.get(
            "reminder_drift_rate",
            self.encoding_drift_rate,
        )

        self.shared_support = parameters["shared_support"]
        self.n_film = list_length

        self.item_count = list_length
        self.items = jnp.eye(self.item_count)
        self.primacy = exponential_primacy_decay(
            jnp.arange(list_length),
            self.primacy_scale,
            self.primacy_decay,
        )

        self.context = context_create_fn(list_length)
        self.mfc = mfc_create_fn(list_length, parameters, self.context)
        self.mcf = mcf_create_fn(list_length, parameters, self.context)
        self.termination_policy = termination_policy_create_fn(
            list_length,
            parameters,
        )

        # eCMR source context: [start-of-list, emotional pole, neutral pole].
        self.emotion_context = TemporalContext.TemporalContext(
            item_count=2,
            size=3,
        )
        is_neutral = 1.0 - self.is_emotional
        emotion_mfc_state = jnp.zeros((list_length, 3))
        emotion_mfc_state = emotion_mfc_state.at[:, 1].set(
            (1 - self.mfc_learning_rate) * self.is_emotional
        )
        emotion_mfc_state = emotion_mfc_state.at[:, 2].set(
            (1 - self.mfc_learning_rate)
            * self.neutral_source_input_scale
            * is_neutral
        )
        self.emotion_mfc = LinearMemory.LinearMemory(emotion_mfc_state)
        self.emotion_mcf = LinearMemory.LinearMemory(jnp.zeros((3, list_length)))

        self.recalls = jnp.zeros(self.item_count, dtype=int)
        self.studied = jnp.zeros(self.item_count, dtype=bool)
        self.recallable = jnp.zeros(self.item_count, dtype=bool)
        self.is_active = jnp.array(True)
        self.recall_total = jnp.array(0, dtype=int)
        self.study_index = jnp.array(0, dtype=int)

    @property
    def mcf_learning_rate(self) -> Float[Array, ""]:
        """Temporal context-to-item learning at the current study position."""
        return self.primacy[self.study_index]

    def _temporal_mcf_learning_rate(self) -> Float[Array, ""]:
        p = self.mcf_learning_rate
        temporal_phi = jnp.maximum(0.0, self.temporal_phi_emot[self.study_index])

        def _multiplicative():
            return p * (1.0 + temporal_phi)

        def _additive():
            return p + jnp.maximum(-p, temporal_phi)

        return lax.cond(
            self.phi_emot_modulates_temporal,
            lambda: lax.cond(
                self.modulate_temporal_emotion_by_primacy,
                _multiplicative,
                _additive,
            ),
            lambda: p,
        )

    def _emotional_mcf_learning_rate(self) -> Float[Array, ""]:
        p = self.mcf_learning_rate
        phi = jnp.maximum(0.0, self.phi_emot[self.study_index])
        baseline = jnp.maximum(0.0, self.source_learning_baseline)

        def _multiplicative():
            return p * (baseline + phi)

        def _additive():
            return p * baseline + p + jnp.maximum(-p, phi)

        return lax.cond(self.modulate_emotion_by_primacy, _multiplicative, _additive)

    def experience_item(
        self,
        item_index: Int_,
        drift_rate: Float_,
        mcf_lr_scale: Float_,
    ) -> "PhasedSourceOnlyECMR":
        """Encode one item using the active phase drift and learning scale."""
        item = self.items[item_index]

        context_input = self.mfc.probe(item)
        new_context = self.context.integrate(context_input, drift_rate)
        learning_state = lax.cond(
            self.learn_after_context_update,
            lambda: new_context.state,
            lambda: self.context.state,
        )

        emotion_input = self.emotion_mfc.probe(item)
        new_emotion_context = self.emotion_context.integrate(
            emotion_input,
            self.emotion_encoding_drift_rate,
        )
        emotion_learning_state = lax.cond(
            self.learn_after_context_update,
            lambda: new_emotion_context.state,
            lambda: self.emotion_context.state,
        )

        return self.replace(
            context=new_context,
            mfc=self.mfc.associate(item, learning_state, self.mfc_learning_rate),
            mcf=self.mcf.associate(
                learning_state,
                item,
                mcf_lr_scale * self._temporal_mcf_learning_rate(),
            ),
            emotion_context=new_emotion_context,
            emotion_mfc=self.emotion_mfc.associate(
                item,
                emotion_learning_state,
                self.mfc_learning_rate,
            ),
            emotion_mcf=self.emotion_mcf.associate(
                emotion_learning_state,
                item,
                mcf_lr_scale * self._emotional_mcf_learning_rate(),
            ),
            studied=self.studied.at[item_index].set(True),
            recallable=self.recallable.at[item_index].set(True),
            study_index=self.study_index + 1,
        )

    def experience(
        self,
        choice: Int_,
        drift_rate: Float_,
        mcf_lr_scale: Float_,
    ) -> "PhasedSourceOnlyECMR":
        """Encode a 1-indexed study choice; zero is treated as padding."""
        return lax.cond(
            choice == 0,
            lambda: self,
            lambda: self.experience_item(choice - 1, drift_rate, mcf_lr_scale),
        )

    def experience_film(self, choice: Int_) -> "PhasedSourceOnlyECMR":
        """Encode a film-phase item."""
        return self.experience(choice, self.encoding_drift_rate, 1.0)

    def experience_break(self, choice: Int_) -> "PhasedSourceOnlyECMR":
        """Encode a break-phase item."""
        return self.experience(choice, self.break_drift_rate, self.break_mcf_scale)

    def experience_interference(self, choice: Int_) -> "PhasedSourceOnlyECMR":
        """Encode an interference-phase item."""
        return self.experience(
            choice,
            self.interference_drift_rate,
            self.interference_mcf_scale,
        )

    def experience_filler(self, choice: Int_) -> "PhasedSourceOnlyECMR":
        """Encode a filler-phase item."""
        return self.experience(choice, self.filler_drift_rate, self.filler_mcf_scale)

    def start_reminders(self) -> "PhasedSourceOnlyECMR":
        """Transition into the reminder phase."""
        new_context = self.context.integrate(
            self.context.initial_state,
            self.reminder_start_drift_rate,
        )
        new_emotion_context = self.emotion_context.integrate(
            self.emotion_context.initial_state,
            self.reminder_start_drift_rate,
        )
        return self.replace(
            context=new_context,
            emotion_context=new_emotion_context,
        )

    def remind(self, choice: Int_) -> "PhasedSourceOnlyECMR":
        """Reinstate a film item's contexts without additional learning."""

        def _remind_item(model):
            item = model.items[choice - 1]
            new_context = model.context.integrate(
                model.mfc.probe(item),
                model.reminder_drift_rate,
            )
            new_emotion_context = model.emotion_context.integrate(
                model.emotion_mfc.probe(item),
                model.reminder_drift_rate,
            )
            return model.replace(
                context=new_context,
                emotion_context=new_emotion_context,
            )

        return lax.cond(choice == 0, lambda: self, lambda: _remind_item(self))

    def start_retrieving(self) -> "PhasedSourceOnlyECMR":
        """Transition from study to retrieval."""
        start_context = self.context.integrate(
            self.context.initial_state,
            self.start_drift_rate,
        )
        start_emotion_context = self.emotion_context.integrate(
            self.emotion_context.initial_state,
            self.start_drift_rate,
        )
        film_source_input = jnp.zeros_like(start_emotion_context.state)
        film_source_input = film_source_input.at[1].set(1.0 - self.mfc_learning_rate)
        start_emotion_context = start_emotion_context.integrate(
            film_source_input,
            self.film_source_start_drift_rate,
        )
        return self.replace(
            context=start_context,
            emotion_context=start_emotion_context,
        )

    def retrieve(self, choice: Int_) -> "PhasedSourceOnlyECMR":
        """Apply a 1-indexed retrieval choice or terminate on zero."""
        return lax.cond(
            choice == 0,
            lambda: self.replace(is_active=False),
            lambda: self._retrieve_item(choice - 1),
        )

    def _retrieve_item(self, item_index: Int_) -> "PhasedSourceOnlyECMR":
        item = self.items[item_index]
        drift_scale = jnp.where(
            self.is_target[item_index] > 0.0,
            self.target_recall_drift_scale,
            self.rejected_recall_drift_scale,
        )
        new_context = self.context.integrate(
            self.mfc.probe(item),
            drift_scale * self.recall_drift_rate,
        )
        new_emotion_context = self.emotion_context.integrate(
            self.emotion_mfc.probe(item),
            drift_scale * self.emotion_recall_drift_rate,
        )
        return self.replace(
            context=new_context,
            emotion_context=new_emotion_context,
            recalls=self.recalls.at[self.recall_total].set(item_index + 1),
            recallable=self.recallable.at[item_index].set(
                self.allow_repeated_recalls
            ),
            recall_total=self.recall_total + 1,
        )

    def candidate_activations(
        self,
        candidates: Float[Array, " item_count"],
    ) -> Float[Array, " item_count"]:
        """Compute decision-scaled activations for a candidate mask."""
        temporal = self.mcf.probe(self.context.state) * candidates
        source = self.emotion_mcf.probe(self.emotion_context.state) * candidates
        film_boost = self.film_item_support_boost * self.is_target * candidates
        combined = temporal + source + film_boost
        return (power_scale(combined, self.mcf_sensitivity) + lb) * candidates

    def activations(self) -> Float[Array, " item_count"]:
        """Compute decision-scaled activations for currently recallable items."""
        return self.candidate_activations(self.recallable)

    def stop_probability(self) -> Float[Array, ""]:
        """Compute the probability of terminating recall."""
        return self.termination_policy.stop_probability(self)

    def outcome_probability(self, choice: Int_) -> Float[Array, ""]:
        """Compute the probability of a 1-indexed recall outcome."""
        p_stop = self.stop_probability()
        return lax.cond(
            choice == 0,
            lambda: p_stop,
            lambda: lax.cond(
                jnp.logical_or(p_stop == 1.0, ~self.recallable[choice - 1]),
                lambda: 0.0,
                lambda: (1 - p_stop) * self._item_probability(choice - 1),
            ),
        )

    def _item_probability(self, item_index: Int_) -> Float[Array, ""]:
        item_activations = self.activations()
        return item_activations[item_index] / jnp.sum(item_activations)

    def outcome_probabilities(self) -> Float[Array, " recall_outcomes"]:
        """Compute probabilities for termination and all recallable items."""
        p_stop = self.stop_probability()
        item_activation = self.activations()
        item_activation_sum = jnp.sum(item_activation)
        return jnp.hstack(
            (
                p_stop,
                (
                    (1 - p_stop)
                    * item_activation
                    / lax.select(item_activation_sum == 0, 1.0, item_activation_sum)
                ),
            )
        )

def make_factory(
    mfc_create_fn: MemoryCreateFn = LinearMemory.init_mfc,
    mcf_create_fn: MemoryCreateFn = LinearMemory.init_mcf,
    context_create_fn: ContextCreateFn = TemporalContext.init,
    termination_policy_create_fn: TerminationPolicyCreateFn = PositionalTermination,
    is_emotional: Optional[Float[Array, " items"]] = None,
    is_target: Optional[Float[Array, " items"]] = None,
) -> Callable:
    """Build a phase-aware source-only eCMR factory for sweeps."""

    def factory(
        list_length: int,
        parameters: Mapping[str, Float_],
        connections: Optional[Float[Array, " n n"]] = None,
    ) -> PhasedSourceOnlyECMR:
        del connections
        if is_emotional is None:
            trial_is_emotional = jnp.zeros(list_length)
        else:
            trial_is_emotional = jnp.zeros(list_length).at[
                : is_emotional.shape[0]
            ].set(is_emotional)
        if is_target is None:
            trial_is_target = jnp.zeros(list_length)
        else:
            trial_is_target = jnp.zeros(list_length).at[
                : is_target.shape[0]
            ].set(is_target)
        return PhasedSourceOnlyECMR(
            list_length,
            parameters,
            is_emotional=trial_is_emotional,
            is_target=trial_is_target,
            mfc_create_fn=mfc_create_fn,
            mcf_create_fn=mcf_create_fn,
            context_create_fn=context_create_fn,
            termination_policy_create_fn=termination_policy_create_fn,
        )

    return factory
