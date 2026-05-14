Below is a refactored contract. I have treated it as a specification document, not a prose draft. Each manuscript object has one owner; later sections reference that object by ID instead of redefining it.

# 1. Project Charter

## 1.1 Target journals

| Role             | Journal                                                     | Consequence for this draft                                                                                                                                                                                                                                                                                                                        |
| ---------------- | ----------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Primary target   | *Psychonomic Bulletin & Review*, Theoretical/Review article | The manuscript should propose or modify a theoretical treatment, be readable to cognitive psychologists, and use simulations as evidence for a theoretical account rather than as a technical exercise. PB&R’s guidance says theoretical/review articles may include model simulations and should not rely on new empirical data. ([Springer][1]) |
| Secondary target | *Journal of Memory and Language*                            | Keep the memory-theory contribution clear and make the model/code reproducible. JML generally favors multiple experiments but explicitly allows significant theoretical or computational papers without new experimental findings. ([ScienceDirect][2])                                                                                           |

Psychological Review is not part of the v1 contract. Do not write the first complete draft as if it must support a field-level theory of intrusive memory, PTSD, reconsolidation, and voluntary/involuntary remembering.

## 1.2 Central thesis

**T1.** Selective interference can arise within a single retrieved-context system when reminders reinstate trauma-film context, interference tasks encode competitors into overlapping temporal/source context, and later tests differ in retrieval cue precision.

This is the only authoritative statement of what the paper is about. Other parts of the plan refer to T1; they should not re-summarize it independently.

## 1.3 Scope boundary

| In v1                                                                                        | Out of v1                                                       |
| -------------------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| Experimental selective-interference logic                                                    | Full PTSD or clinical treatment efficacy                        |
| Trauma-film and analogue paradigms as benchmark cases                                        | Full phenomenology of intrusive memories                        |
| Intrusion-like retrieval as trauma-item sampling                                             | Distress, vividness, appraisal, avoidance, symptom change       |
| Voluntary memory as a set of retrieval formats varying in cue precision                      | A complete theory of voluntary/involuntary remembering          |
| Temporal context, source context, reminder reinstatement, competitor encoding, cue precision | Exhaustive reconsolidation theory or dual-representation theory |
| Qualitative boundary conditions and design implications                                      | Whether Tetris is clinically effective                          |

## 1.4 Core explanatory variables

These are the only high-level degrees of freedom the paper is allowed to use.

| ID | Variable                  | Meaning                                                                                                   | Allowed explanatory role                             |
| -- | ------------------------- | --------------------------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| V1 | Competitor strength       | How strongly interference-task items are encoded and can later compete for retrieval                      | Explains magnitude of interference                   |
| V2 | Target–competitor overlap | How much interference items share temporal/source context with trauma-film items                          | Explains when interference is selective/effective    |
| V3 | Retrieval cue precision   | How strongly the test constrains retrieval toward film targets rather than broad context-to-item sampling | Explains voluntary sparing and test-format variation |

Everything in the model, simulations, and discussion must map to V1, V2, or V3.

## 1.5 Claim-strength policy

| Outcome of analyses                        | Authorized manuscript claim                                                                             |
| ------------------------------------------ | ------------------------------------------------------------------------------------------------------- |
| Robust across plausible parameter regions  | Retrieved-context competition provides a compact positive account of selective interference.            |
| Works under interpretable constraints      | The model identifies conditions under which a single-system account can explain selective interference. |
| Works only with fine tuning                | The model mainly clarifies constraints on single-system explanations.                                   |
| Fails to show reminder/overlap/cue effects | The current architecture should not be written up as the proposed account.                              |

This policy is the only place where rhetorical strength is decided.

---

# 2. Empirical Target Specification

This module defines what the manuscript must address. It is not a literature review. The final paper will cite specific studies inside the relevant sections, but the planning object here is the constraint itself.

| ID | Empirical/theoretical constraint                                                                                                                                                             | Why it matters                                                                                   | Model-facing requirement                                                                                 |
| -- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------- |
| E1 | Post-encoding or post-reminder interference can reduce subsequent intrusion reports relative to control conditions.                                                                          | Establishes the selective-interference phenomenon.                                               | The model must reduce trauma-film item sampling under interference.                                      |
| E2 | The same manipulation often leaves voluntary memory relatively preserved, especially when voluntary memory is measured with recognition-like or otherwise target-constrained tests.          | Drives the inference to separate intrusive and voluntary traces.                                 | The model must allow intrusion-like retrieval to decline more than target-cued/probe-specific retrieval. |
| E3 | Delayed interference effects are theoretically tied to reminder/reactivation: interference after reinstatement is expected to be stronger than interference encoded in an unrelated context. | Distinguishes contextual overlap from generic distraction or task load.                          | The model must make reminder-driven reinstatement increase target–competitor overlap.                    |
| E4 | Task class matters only if it affects representational/source overlap or competitor strength; “visuospatial” should not be treated as a primitive causal label.                              | Avoids simply restating the standard modality-specific account.                                  | The model must express task differences through V1 and V2.                                               |
| E5 | Test formats differ in retrieval demands: diary-like intrusions, vigilance-style cueing, free recall, cued recall, item recognition, and source/associative tests are not interchangeable.   | Provides the main design payoff and explains why effects may sharpen or blur across experiments. | The model must express test differences through V3.                                                      |
| E6 | A purely temporal account may imply local or late-film interference unless context drift is slow or a broader source context is included.                                                    | Motivates source context without making it a patch.                                              | Diagnostics must test whether source context is needed to avoid a recency-only explanation.              |

These six targets are the manuscript’s empirical constraint set. Do not add new empirical targets unless one of the analyses fails and forces a scope revision.

---

# 3. Model Interface Specification

This module defines the theoretical components. It does not define equations or implementation details.

| ID | Component                    | Interface definition                                                                                                                         | Maps to |
| -- | ---------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- | ------- |
| M1 | Temporal context             | A drifting state that links items by sequential proximity and can be reinstated by reminders.                                                | V2      |
| M2 | Source context               | Non-temporal context shared by items because of film source, arousal, imagery-like processing, visuospatial/task state, or related features. | V2      |
| M3 | Reminder reinstatement       | A process that moves current context toward the film-associated temporal/source region before interference encoding.                         | V2      |
| M4 | Competitor encoding          | Encoding of interference-task items into the current context, making them competitors during later retrieval.                                | V1, V2  |
| M5 | Context-to-item retrieval    | Competitive retrieval in which current context cues candidate items.                                                                         | V1, V2  |
| M6 | Cue precision                | A retrieval-control variable determining whether retrieval is broad/unguided or constrained toward film targets/probes.                      | V3      |
| M7 | Probe-specific retrieval     | A high-cue-precision retrieval mode approximating item-specific recognition or strong cueing.                                                | V3      |
| M8 | Source/associative retrieval | A voluntary retrieval mode that still requires contextual/source access and may therefore be more vulnerable than item recognition.          | V3      |

Implementation details such as matrix orientation, normalization, parameter values, and Luce choice rules belong in the formal model or supplement, not in this planning contract.

---

# 4. Analysis Registry

This is the single source of truth for simulations, diagnostics, figures, and result objects.

## A1. Core selective-interference dissociation

| Field                | Specification                                                                                                          |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| Role                 | Main analysis                                                                                                          |
| Question             | Can the final model reduce intrusion-like retrieval more than target-cued/probe-specific voluntary retrieval?          |
| Targets addressed    | E1, E2                                                                                                                 |
| Model components     | M1–M7                                                                                                                  |
| Manipulations        | Interference absent/weak vs strong-overlap interference; retrieval mode low vs high cue precision                      |
| Primary output       | Trauma-film sampling/access by interference condition and retrieval mode                                               |
| Artifact             | Figure 2                                                                                                               |
| Textual claim tested | The same competitor encoding can impair broad context-to-item sampling more than target-cued/probe-specific retrieval. |
| Failure implication  | If this fails, T1 is not supported in the current model.                                                               |

## A2. Boundary conditions: reminder × overlap × competitor strength

| Field                | Specification                                                                                                                              |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| Role                 | Main analysis                                                                                                                              |
| Question             | Does interference depend on reinstatement, target–competitor overlap, and competitor strength?                                             |
| Targets addressed    | E1, E3, E4                                                                                                                                 |
| Model components     | M1–M5                                                                                                                                      |
| Manipulations        | Reminder absent/present; low/high source overlap; weak/strong competitor encoding                                                          |
| Primary output       | Interference magnitude and competitor capture                                                                                              |
| Artifact             | Figure 3                                                                                                                                   |
| Textual claim tested | Interference is not generic post-film distraction; it depends on competitors being strong and encoded into overlapping reinstated context. |
| Failure implication  | If reminder/overlap/strength do not matter, the contextual-competition mechanism is not supported.                                         |

## A3. Cue-precision gradient

| Field                | Specification                                                                                                                                                |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Role                 | Main analysis                                                                                                                                                |
| Question             | Does retrieval cue precision determine whether the dissociation appears sharp or blurred?                                                                    |
| Targets addressed    | E2, E5                                                                                                                                                       |
| Model components     | M5–M8                                                                                                                                                        |
| Manipulations        | Retrieval modes ordered by cue precision: unguided sampling; directed recall-like retrieval; probe-specific retrieval; optional source/associative retrieval |
| Primary output       | Interference effect by retrieval mode                                                                                                                        |
| Artifact             | Figure 4                                                                                                                                                     |
| Textual claim tested | Voluntary memory is protected conditionally, depending on cue precision; recognition-like sparing is not architectural immunity.                             |
| Failure implication  | If cue precision does not affect vulnerability, demote test-format claims.                                                                                   |

## A4. Robustness and diagnostic package

| Field                | Specification                                                                                                                                                    |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Role                 | Main/supplementary analysis                                                                                                                                      |
| Question             | Are A1–A3 hand-tuned, and which components are necessary?                                                                                                        |
| Targets addressed    | E1–E6                                                                                                                                                            |
| Required diagnostics | Temporal-only diagnostic; source-context ablation; reminder ablation; overlap × competitor-strength sweep; cue-precision sensitivity; temporal-drift sensitivity |
| Primary output       | Criterion map or diagnostic table showing success/failure regions                                                                                                |
| Artifact             | Figure 5 or Supplementary Figure S1, depending on compactness                                                                                                    |
| Textual claim tested | The account is robust, constrained, or brittle according to the claim-strength policy.                                                                           |
| Failure implication  | Determines whether the manuscript is a positive account, constrained account, or not viable.                                                                     |

## D1. Temporal-only diagnostic

| Field             | Specification                                                               |
| ----------------- | --------------------------------------------------------------------------- |
| Role              | Required diagnostic, not automatically main text                            |
| Question          | Does temporal context alone produce a local/late-item interference pattern? |
| Targets addressed | E6                                                                          |
| Output            | Serial-position profile of interference with source context removed         |
| Placement         | Supplement unless theoretically central                                     |
| Use               | Determines whether source context is necessary or merely an extension.      |

D1 is listed separately because it must be run early but should not control manuscript order unless the result is theoretically decisive.

---

# 5. Manuscript Blueprint

This module defines the written paper. It references targets, model components, and analyses by ID rather than redefining them.

## Abstract

| Field          | Specification                                                                                             |
| -------------- | --------------------------------------------------------------------------------------------------------- |
| Purpose        | Compress the paper’s argument after results are known.                                                    |
| Inputs         | T1; E1–E5; A1–A4; claim-strength policy                                                                   |
| Required moves | Phenomenon → inference problem → retrieved-context proposal → simulation package → claim calibrated by A4 |
| Output         | A 180–230 word summary.                                                                                   |
| Constraint     | No polished abstract should be finalized until A1–A4 are known.                                           |

## Section 1. Introduction

| Field            | Specification                                                                                                                                                                                                                                                                                                                                                                                                |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Purpose          | Establish the inference problem and motivate T1.                                                                                                                                                                                                                                                                                                                                                             |
| Inputs           | T1; E1–E5                                                                                                                                                                                                                                                                                                                                                                                                    |
| Output           | Reader understands why selective interference is theoretically informative and why a single-system account is worth testing.                                                                                                                                                                                                                                                                                 |
| Text skeleton    | 1. Introduce selective interference as the empirical phenomenon. 2. Explain why the intrusion/voluntary-memory dissociation has architectural implications. 3. Present the standard separate-trace/reconsolidation inference. 4. State the underdetermination problem: retrieval dissociations do not uniquely identify storage architecture. 5. Introduce T1 as the alternative. 6. Preview analyses A1–A3. |
| Local constraint | Do not review PTSD, clinical treatment, or reconsolidation broadly; include only what is needed for E1–E5.                                                                                                                                                                                                                                                                                                   |

## Section 2. Empirical Target

| Field            | Specification                                                                                                                                                                                                                                   |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Purpose          | Define the empirical constraints the model will address.                                                                                                                                                                                        |
| Inputs           | E1–E6                                                                                                                                                                                                                                           |
| Output           | Reader knows what counts as the target phenomenon and what is outside the model’s scope.                                                                                                                                                        |
| Text skeleton    | 1. Distinguish empirical effects from theoretical interpretations. 2. Present E1–E6 in prose or table form. 3. State that intrusion occurrence is modeled as trauma-item sampling. 4. State that distress/vividness/symptoms are outside scope. |
| Artifact         | Table 1: E1–E6, using the Empirical Target Specification.                                                                                                                                                                                       |
| Local constraint | Do not introduce additional empirical targets here unless they are added to Section 2 of this contract.                                                                                                                                         |

## Section 3. Contextual-Competition Account

| Field            | Specification                                                                                                                                                                                                                                                                                                                                                                                        |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Purpose          | Explain the theory in prose before formalization.                                                                                                                                                                                                                                                                                                                                                    |
| Inputs           | T1; V1–V3; M1–M8                                                                                                                                                                                                                                                                                                                                                                                     |
| Output           | Reader understands the causal chain from reminder to interference to retrieval selectivity.                                                                                                                                                                                                                                                                                                          |
| Text skeleton    | 1. Film items bind to temporal and source context. 2. Reminder reinstates film-associated context. 3. Interference encodes competitors into that reinstated context. 4. Later unguided retrieval is vulnerable because competitors capture context-to-item probability. 5. Voluntary tests vary in cue precision rather than forming one uniform category. 6. The account predicts effects of V1–V3. |
| Artifact         | Figure 1: schematic of M1–M6 causal chain.                                                                                                                                                                                                                                                                                                                                                           |
| Local constraint | No equations; no parameter details; no implementation chronology.                                                                                                                                                                                                                                                                                                                                    |

## Section 4. Formal Model

| Field            | Specification                                                                                                                                                                                                                                                                                                                                        |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Purpose          | Define the computational implementation sufficiently for A1–A4.                                                                                                                                                                                                                                                                                      |
| Inputs           | M1–M8; V1–V3                                                                                                                                                                                                                                                                                                                                         |
| Output           | Reader can understand what was simulated and how manipulations map onto theory.                                                                                                                                                                                                                                                                      |
| Text skeleton    | 1. Define representations: items, temporal context, source context. 2. Define encoding and context update at a conceptual-mathematical level. 3. Define reminder reinstatement. 4. Define interference manipulations as V1 and V2. 5. Define retrieval modes as V3. 6. State parameter provenance and which quantities are manipulated versus fixed. |
| Artifact         | Table 2: M1–M8 with implementation status: fixed, manipulated, sensitivity-tested, or diagnostic.                                                                                                                                                                                                                                                    |
| Local constraint | Matrix orientation, full equations, long parameter tables, and implementation pseudocode go to supplement unless essential for comprehension.                                                                                                                                                                                                        |

## Section 5. Simulation Overview

| Field            | Specification                                                                                                                                                                                                                                                      |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Purpose          | Prepare the reader for A1–A4 and define success criteria before results.                                                                                                                                                                                           |
| Inputs           | A1–A4; claim-strength policy                                                                                                                                                                                                                                       |
| Output           | Reader knows what each analysis is for and how results will be interpreted.                                                                                                                                                                                        |
| Text skeleton    | 1. State that analyses test the three claims: core dissociation, boundary conditions, cue precision. 2. Introduce A1–A4 by role, not by implementation detail. 3. Define success criteria using the fields in A1–A4. 4. Explain that A4 calibrates claim strength. |
| Artifact         | Optional compact analysis roadmap table listing A1–A4.                                                                                                                                                                                                             |
| Local constraint | Do not add new success criteria outside the Analysis Registry.                                                                                                                                                                                                     |

## Section 6. Results

### 6.1 A1: Core dissociation

| Field         | Specification                                                                                                                                                                                                                                                                                                                    |
| ------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Purpose       | Establish the core sufficiency result.                                                                                                                                                                                                                                                                                           |
| Inputs        | A1                                                                                                                                                                                                                                                                                                                               |
| Output        | Reader can assess whether the model produces selective impairment of intrusion-like retrieval.                                                                                                                                                                                                                                   |
| Text skeleton | 1. State the question from A1. 2. Explain the contrast between broad sampling and target/probe-specific retrieval. 3. Describe the manipulated conditions. 4. Present Figure 2. 5. Interpret whether the pattern supports the core dissociation. 6. Note limitations if impairment is small, floor-like, or parameter-sensitive. |
| Artifact      | Figure 2                                                                                                                                                                                                                                                                                                                         |

### 6.2 A2: Boundary conditions

| Field         | Specification                                                                                                                                                                                                                                                                                                                                                        |
| ------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Purpose       | Show whether the effect depends on contextual competition rather than generic task load.                                                                                                                                                                                                                                                                             |
| Inputs        | A2; E3–E4                                                                                                                                                                                                                                                                                                                                                            |
| Output        | Reader can assess whether reminder, overlap, and competitor strength are necessary or influential.                                                                                                                                                                                                                                                                   |
| Text skeleton | 1. State the boundary-condition question. 2. Explain why generic distraction would not predict the same dependence on reminder/overlap. 3. Describe the factorial manipulation. 4. Present Figure 3. 5. Interpret whether the strongest effects occur under reinstated, high-overlap, strong-competitor conditions. 6. State any constraints exposed by the pattern. |
| Artifact      | Figure 3                                                                                                                                                                                                                                                                                                                                                             |

### 6.3 A3: Cue precision

| Field         | Specification                                                                                                                                                                                                                                                                                                                                                              |
| ------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Purpose       | Establish the test-format payoff.                                                                                                                                                                                                                                                                                                                                          |
| Inputs        | A3; E5                                                                                                                                                                                                                                                                                                                                                                     |
| Output        | Reader can assess whether voluntary sparing is conditional on cue precision.                                                                                                                                                                                                                                                                                               |
| Text skeleton | 1. State the cue-precision question. 2. Explain why voluntary-memory tests are not interchangeable. 3. Describe the retrieval-mode anchors. 4. Present Figure 4. 5. Interpret whether cue precision sharpens or blurs selectivity. 6. State implications for recognition-like, free-recall-like, and source/associative tests without overclaiming about any one paradigm. |
| Artifact      | Figure 4                                                                                                                                                                                                                                                                                                                                                                   |

### 6.4 A4: Robustness and diagnostics

| Field         | Specification                                                                                                                                                                                                                                                             |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Purpose       | Calibrate claim strength and show whether the account is hand-tuned.                                                                                                                                                                                                      |
| Inputs        | A4; D1; claim-strength policy                                                                                                                                                                                                                                             |
| Output        | Reader knows whether the model is robust, constrained, or brittle.                                                                                                                                                                                                        |
| Text skeleton | 1. State why robustness matters for this account. 2. Summarize required diagnostics. 3. Present Figure 5 if compact; otherwise summarize and point to supplement. 4. Apply the claim-strength policy. 5. Identify which assumptions are necessary, optional, or unstable. |
| Artifact      | Figure 5 or Supplementary Figure S1                                                                                                                                                                                                                                       |

## Section 7. Discussion

| Field            | Specification                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Purpose          | Interpret the results without expanding scope.                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| Inputs           | T1; E1–E6; A1–A4 outcomes; claim-strength policy                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| Output           | Reader understands what the account contributes, what it does not settle, and what experiments it suggests.                                                                                                                                                                                                                                                                                                                                                                                                        |
| Text skeleton    | 1. State the result-calibrated version of T1. 2. Explain the implication for the separate-trace inference. 3. Compare with separate-trace/reconsolidation interpretations at the level of E1–E5, not as a full theory review. 4. Explain why source context matters for task specificity and recency concerns. 5. Explain why cue precision matters for experimental design. 6. Separate framework-level, variant-specific, and implementation-specific predictions. 7. State limitations from the scope boundary. |
| Local constraint | Do not add new model commitments in the Discussion.                                                                                                                                                                                                                                                                                                                                                                                                                                                                |

## Section 8. Open Practices and Supplement

| Field               | Specification                                                                                                                                                             |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Purpose             | Satisfy transparency and reproducibility requirements.                                                                                                                    |
| Inputs              | A1–A4 implementation; target journal policies                                                                                                                             |
| Output              | Reader/reviewer can locate code, parameters, supplementary equations, and diagnostics.                                                                                    |
| Text skeleton       | 1. State code/model availability. 2. State data availability if no new data are collected. 3. State preregistration status if applicable. 4. List supplementary contents. |
| Supplement contents | Full equations; parameter tables; matrix/index conventions; pseudocode; extended A4 diagnostics; D1 if not main text.                                                     |

---

# 6. Implementation Workflow

The workflow references the Analysis Registry. It does not redefine analyses.

## Step 1. Build the shared model scaffold

Implement M1–M8 in one codebase with a shared configuration file. Include parameter logging and random seeds from the start.

## Step 2. Run D1

Run the temporal-only diagnostic before committing to the final source-context implementation. Use D1 only to decide how source context is motivated and whether it appears in the main text or supplement.

## Step 3. Freeze the main model variant for A1–A3

Define the main model configuration, fixed parameters, manipulated quantities, and sensitivity-tested quantities. Do not tune A1–A3 independently.

## Step 4. Run A1

Apply the A1 failure implications. If A1 fails, stop and revise the model before running the remaining main analyses.

## Step 5. Run A2

Apply the A2 failure implications. If reminder/overlap/competitor strength do not matter, the current theory is not supported.

## Step 6. Run A3

Apply the A3 failure implications. If cue precision does not alter vulnerability, demote the test-format payoff.

## Step 7. Run A4

Run the required robustness and diagnostic package. Apply the claim-strength policy before drafting the introduction or discussion.

## Step 8. Draft Results first

Draft Section 6 using the A1–A4 text skeletons. This prevents the Introduction from promising a stronger result than the simulations support.

## Step 9. Draft Sections 3–5

Write the conceptual account, formal model, and simulation overview using the final model and completed analyses.

## Step 10. Draft Sections 1–2

Write the Introduction and Empirical Target sections after the result-calibrated story is stable.

## Step 11. Draft Sections 7–8 and supplement

Use the claim-strength policy for the Discussion. Prepare reproducibility materials and supplementary technical details.

---

# 7. Deferred Backlog

These are excluded from v1 unless a failure in A1–A4 forces them into scope.

| Backlog item                                                                                   | Reason deferred                                                   |
| ---------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| Full vigilance-intrusion-task implementation                                                   | A3 only needs cue-precision anchors for v1.                       |
| Separate diary, VIT, free recall, cued recall, item recognition, and source recognition models | Too large; v1 uses a cue-precision continuum.                     |
| Clinical intervention simulations                                                              | Outside PB&R v1 scope.                                            |
| Distress/vividness/appraisal modeling                                                          | Outside sampling-level target.                                    |
| Emotional-arousal versus visuospatial-source model comparison                                  | Useful later, but v1 treats source context as umbrella construct. |
| Individual-difference theory                                                                   | Not needed for T1.                                                |
| Extensive serial-position prediction program                                                   | D1 covers only the diagnostic need.                               |

[1]: https://link.springer.com/journal/13423/submission-guidelines?utm_source=chatgpt.com "Submission guidelines | Psychonomic Bulletin & Review"
[2]: https://www.sciencedirect.com/journal/journal-of-memory-and-language/publish/guide-for-authors?utm_source=chatgpt.com "Guide for authors - Journal of Memory and Language"
