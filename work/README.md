# Research packages and manuscript figures

The scientific model code is in [selective_interference_v2](../selective_interference_v2/)
and its tests in [tests](../tests/). This folder holds analyses, their inputs and
results, and figure sources. Earlier document-workflow experiments have moved to
[the archive](../archive/legacy-word-workflow/README.md).

Folder numbers reflect the paper's development history. They do not determine
current manuscript simulation order. Prefer stable mechanism names for new work;
retain existing paths until notebook/script dependencies are deliberately migrated.

## Current imported manuscript figures

[figure-map.yml](figure-map.yml) records each active image's exact source Word
media part, checksum, manuscript location, and related analysis/figure package.
The Word source mapping is verified by hashes. Related-code pointers are based
on caption/topic and are explicitly distinguished from a verified reproduction.
Only one imported figure has an exact byte match among the current work PNGs.
Do not replace an imported figure with a newer export implicitly.

The current draft still presents competitor formation, retrieval control, and
recognition in its pooled-source order. Proposals to reorder those sections are
separate manuscript decisions. This directory cleanup applies no such changes.

## Package index

The table identifies available entry points, not a declaration that every stored
result is current or selected. CSV/PNG/PDF/SVG outputs are retained beside their
analysis sources. Use each documented package's run/verification instructions.

| Package | Question or purpose | Available entry points | Status |
| --- | --- | --- | --- |
| [empirical_target](empirical_target/) | Empirical comparison data, paradigm schematics, and their figures | [render_empirical_selective_interference_examples.py](empirical_target/render_empirical_selective_interference_examples.py) | Retained research package; selection is documented separately in the figure map. |
| [retrieved_context_account](retrieved_context_account/) | Encoding and retrieval diagrams | Figure assets; no generator script in this folder. | Retained research package; selection is documented separately in the figure map. |
| [captioned_exports](captioned_exports/) | Captioned figure composites for earlier exports | [render_caption_composites.py](captioned_exports/render_caption_composites.py) | Historical figure/export support. |
| [fitting](fitting/) | Model parameter fitting notebooks | [fitting_Dupertuys2026_eCMR_source_only_phi_no_shared_support_best_of_1.ipynb](fitting/fitting_Dupertuys2026_eCMR_source_only_phi_no_shared_support_best_of_1.ipynb) | Retained research package; selection is documented separately in the figure map. |
| [interference_sweeps](interference_sweeps/) | Reminder/interference parameter explorations | 9 notebooks/scripts in the folder; filenames preserve their parameter settings. | Exploratory/development record; not automatically a selected manuscript result. |
| [retrieval_parameter_sweeps](retrieval_parameter_sweeps/) | Retrieval-parameter explorations | [rejected_recall_drift_scale.ipynb](retrieval_parameter_sweeps/rejected_recall_drift_scale.ipynb); [retrieval_start_drift_scale.ipynb](retrieval_parameter_sweeps/retrieval_start_drift_scale.ipynb); [retrieval_tau_scale.ipynb](retrieval_parameter_sweeps/retrieval_tau_scale.ipynb) | Exploratory/development record; not automatically a selected manuscript result. |
| [repeated_recall_recurrence](repeated_recall_recurrence/) | Repeated-recall and recurrence analysis | [run_repeated_recall_recurrence.py](repeated_recall_recurrence/run_repeated_recall_recurrence.py) | Retained research package; selection is documented separately in the figure map. |
| [general_memory_followup](general_memory_followup/) | Reserved general-memory follow-up workspace | Figure assets; no generator script in this folder. | Retained research package; selection is documented separately in the figure map. |
| [simulation1_context_binding](simulation1_context_binding/) | Context binding and competitor formation | [simulation1_context_binding.ipynb](simulation1_context_binding/simulation1_context_binding.ipynb) | Retained research package; selection is documented separately in the figure map. |
| [simulation1_monitoring_cued_retrieval](simulation1_monitoring_cued_retrieval/) | Earlier monitoring/cued-retrieval exploration | [simulation1_monitoring_cued_retrieval.ipynb](simulation1_monitoring_cued_retrieval/simulation1_monitoring_cued_retrieval.ipynb) | Exploratory/development record; not automatically a selected manuscript result. |
| [simulation1_unguided_cued](simulation1_unguided_cued/) | Unguided film recall, positional curves, sequences, and context overlap | [render_simulation1_unguided_cued_context_overlap.py](simulation1_unguided_cued/render_simulation1_unguided_cued_context_overlap.py); [render_simulation1_unguided_cued_recall_distributions.py](simulation1_unguided_cued/render_simulation1_unguided_cued_recall_distributions.py); [render_simulation1_unguided_cued_sequence_summary.py](simulation1_unguided_cued/render_simulation1_unguided_cued_sequence_summary.py); [simulation1_unguided_cued_retrieval.ipynb](simulation1_unguided_cued/simulation1_unguided_cued_retrieval.ipynb) | Retained research package; selection is documented separately in the figure map. |
| [simulation2_control_cued_behavioral](simulation2_control_cued_behavioral/) | Control mechanisms and behavioral selectivity | [generate_simulation2_control_cued_behavioral_data.py](simulation2_control_cued_behavioral/generate_simulation2_control_cued_behavioral_data.py); [render_simulation2_control_cued_behavioral.py](simulation2_control_cued_behavioral/render_simulation2_control_cued_behavioral.py) | Retained research package; selection is documented separately in the figure map. |
| [simulation2_control_cued_parameter_exploration](simulation2_control_cued_parameter_exploration/) | Earlier exploratory control-parameter rankings | [explore_simulation2_control_parameter_space.py](simulation2_control_cued_parameter_exploration/explore_simulation2_control_parameter_space.py) | Exploratory/development record; not automatically a selected manuscript result. |
| [simulation2_control_parameter_sensitivity](simulation2_control_parameter_sensitivity/) | Feedback-linked parameter-robustness analysis | [run_parameter_sensitivity.py](simulation2_control_parameter_sensitivity/run_parameter_sensitivity.py); [verify_results.py](simulation2_control_parameter_sensitivity/verify_results.py) | Documented analysis package; see its README, METHODS, and FEEDBACK_TRACE. |
| [simulation2_film_item_boost](simulation2_film_item_boost/) | Film-item support and control parameter sweeps | [sweep_simulation2_film_item_boost_2x2.py](simulation2_film_item_boost/sweep_simulation2_film_item_boost_2x2.py) | Exploratory/development record; not automatically a selected manuscript result. |
| [simulation2_film_retrieval_goal_context_overlap](simulation2_film_retrieval_goal_context_overlap/) | Film-goal cue and context-overlap analysis | [render_simulation2_film_retrieval_goal_context_overlap.py](simulation2_film_retrieval_goal_context_overlap/render_simulation2_film_retrieval_goal_context_overlap.py) | Retained research package; selection is documented separately in the figure map. |
| [simulation2_retrieval_control_decomposition](simulation2_retrieval_control_decomposition/) | Decomposition of retrieval-control mechanisms | [render_simulation2_retrieval_control_decomposition.py](simulation2_retrieval_control_decomposition/render_simulation2_retrieval_control_decomposition.py); [sweep_simulation2_retrieval_control_decomposition.py](simulation2_retrieval_control_decomposition/sweep_simulation2_retrieval_control_decomposition.py) | Retained research package; selection is documented separately in the figure map. |
| [simulation2_retrieval_selectivity](simulation2_retrieval_selectivity/) | Retrieval selectivity and output transitions | [simulation2_retrieval_selectivity.ipynb](simulation2_retrieval_selectivity/simulation2_retrieval_selectivity.ipynb) | Retained research package; selection is documented separately in the figure map. |
| [simulation2_start_context_reinstatement](simulation2_start_context_reinstatement/) | Start-context reinstatement and position effects | [render_simulation2_start_context_reinstatement.py](simulation2_start_context_reinstatement/render_simulation2_start_context_reinstatement.py); [render_simulation2_start_context_reinstatement_film_positions_candidate.py](simulation2_start_context_reinstatement/render_simulation2_start_context_reinstatement_film_positions_candidate.py); [simulation2_start_context_reinstatement.ipynb](simulation2_start_context_reinstatement/simulation2_start_context_reinstatement.ipynb) | Retained research package; selection is documented separately in the figure map. |
| [simulation2_target_monitoring_diagnostic](simulation2_target_monitoring_diagnostic/) | Post-sampling monitoring diagnostics | [render_simulation2_target_monitoring_diagnostic.py](simulation2_target_monitoring_diagnostic/render_simulation2_target_monitoring_diagnostic.py) | Retained research package; selection is documented separately in the figure map. |
| [simulation3_film_cue_inclusion](simulation3_film_cue_inclusion/) | Film-cue inclusion during retrieval | [simulation3_film_cue_inclusion.ipynb](simulation3_film_cue_inclusion/simulation3_film_cue_inclusion.ipynb) | Retained research package; selection is documented separately in the figure map. |
| [simulation3_recall_drift_intentionality](simulation3_recall_drift_intentionality/) | Recall drift and intentionality contrasts | [simulation3_recall_drift_intentionality.py](simulation3_recall_drift_intentionality/simulation3_recall_drift_intentionality.py) | Retained research package; selection is documented separately in the figure map. |
| [simulation3_recognition_test_format](simulation3_recognition_test_format/) | Recognition/test-format simulations and evidence diagnostics | [render_simulation3_recognition_test_format.py](simulation3_recognition_test_format/render_simulation3_recognition_test_format.py); [sweep_simulation3_recognition_test_format.py](simulation3_recognition_test_format/sweep_simulation3_recognition_test_format.py) | Retained research package; selection is documented separately in the figure map. |
| [simulation4_recognition_full_figure](simulation4_recognition_full_figure/) | Recognition composite figure assets | Figure assets; no generator script in this folder. | Retained research package; selection is documented separately in the figure map. |
| [simulation4_test_format_schematic](simulation4_test_format_schematic/) | Test-format schematic assets | Figure assets; no generator script in this folder. | Retained research package; selection is documented separately in the figure map. |
| [templates](templates/) | Reusable notebook templates | [fitting_evosaxde.ipynb](templates/fitting_evosaxde.ipynb); [interference_sweep.ipynb](templates/interference_sweep.ipynb) | Template source. |

The earlier standalone figure bundle is preserved in
[archive/legacy-figure-bundle](../archive/legacy-figure-bundle/README.md).
It is not a maintained output of the current review manuscript.
