# Citation-Fit Audit for Current Draft

Audit date: 2026-05-19

Scope: `selective_interference_v2/index.qmd`, current Introduction citation clusters only.
The abstract currently contains no citations.

This audit separates two questions:

1. **Bibliographic identity**: does the citation key identify the intended article?
2. **Claim-source fit**: does the cited source support the sentence or claim it is attached to?

## Executive Summary

The bibliography identity pass is mostly solid: all 25 cited keys in `index.qmd` have matching DOI-backed entries in `references.bib`.
The more important weakness is claim-source fit.
Several citation clusters include sources that are appropriate for the general area but not precise support for the full sentence.

Highest-risk issues:

- **Line 51 over-bundles multiple claims.** Some cited sources support intrusion reduction, some support post-reminder effects, and only a subset directly support "voluntary memory shows little measurable impairment." `lau2019intrusive` is the strongest current source for that selective dissociation.
- **Line 52 overstates the real-world trauma evidence.** The cited clinical/real-world studies support reduced intrusive memories after brief visuospatial interventions, but they are weaker support for "leaving deliberate recall relatively intact" as an empirically measured outcome.
- **Line 59 compresses interpretation and finding.** `holmes2009can` and `james2015computer` support the visuospatial/reconsolidation interpretation, but the sentence also attributes a full dual-representation mechanism and voluntary-memory sparing that would be better separated or additionally supported.
- **Line 70 cites established retrieved-context/contextual-binding theory but also states the paper's own model extension.** The sources support item-context binding and context-driven retrieval, but they do not themselves establish that film reminders and interference are encoded in the exact selective-interference sequence proposed here.

Recommended immediate action:

- Keep the DOI-verified `references.bib`.
- Before manuscript submission, revise citation placement and wording around lines 51, 52, 59, and 70.
- Consider adding `lau2021selectively`, `hagenaars2017tetris`, `talmi2019retrieved`, and possibly `sederberg2008context` or `polyn2009task` if later prose needs stronger support for associative memory, delayed interference, emotional CMR, or source/task context.

## Sentence-by-Sentence Audit

Verdict labels:

- `supports directly`: source supports the claim as written.
- `supports partially`: source supports part of the claim but not the whole sentence.
- `review/background support only`: source is useful context but not primary support for the exact claim.
- `weak or misplaced`: source is not a good fit for the attached claim.
- `needs stronger/different source`: claim needs a better citation or rewording.

| Line | Claim being supported | Current citations | Verdict | Recommended action |
|---:|---|---|---|---|
| 41 | Intrusive memories return without deliberate search and are poorly matched to present goals/context. | `ehlers2000cognitive`; `brewin2010intrusive`; `krans2009intrusive`; `iyadurai2019intrusive` | `supports directly` for intrusive/involuntary imagery and clinical relevance; `supports partially` for "not well matched to demands of the present." | Keep, but consider making the claim slightly less broad or moving `ehlers2000cognitive` to the "current threat/contextualization" part of the sentence if expanded. |
| 44 | Trauma-film paradigm is a controlled setting for comparing intrusive and voluntary memory for the same event. | `holmes2008inducing`; `james2016trauma` | `supports directly` | Keep. These are appropriate review sources for the paradigm. |
| 47 | Voluntary memory can be preserved, and intrusion frequency can be weakly related to voluntary-memory measures. | `holmes2004trauma`; `james2016trauma` | `supports directly` for `holmes2004trauma`; `review/background support only` for `james2016trauma`. | Keep `holmes2004trauma`; `james2016trauma` is acceptable as a review citation but not necessary if the sentence is meant as direct empirical support. |
| 48 | The same encoded episode can support uncontrolled and controlled access that empirically dissociate. | `holmes2004trauma`; `iyadurai2019intrusive` | `supports partially` | `holmes2004trauma` supports dissociation between intrusions and recall/recognition measures; `iyadurai2019intrusive` supports the broader cognitive-clinical distinction. Sentence is interpretive, so fit is acceptable but not as direct as line 47. |
| 51 | Brief tasks such as Tetris after film encoding or later reminder can reduce intrusions while voluntary memory shows little impairment. | `holmes2009can`; `holmes2010key`; `deeprose2012imagery`; `james2015computer`; `kessler2020visuospatial`; `lau2019intrusive`; `asselbergs2023systematic` | `supports partially`; cluster is over-broad. | Split into two claims or cite more selectively. Use `holmes2009can`, `holmes2010key`, `james2015computer`, `kessler2020visuospatial`, and `asselbergs2023systematic` for intrusion reduction/intervention evidence. Use `lau2019intrusive` as the main support for "voluntary memory spared." `deeprose2012imagery` is weaker for voluntary-memory sparing. |
| 52 | Similar post-reminder interventions reduce intrusions for real-life trauma and leave deliberate recall intact. | `iyadurai2018preventing`; `horsch2017reducing`; `kanstrup2021single` | `supports partially`; `needs stronger/different source` for deliberate-recall intact. | Reword unless deliberate recall was measured in these studies. Safer: "real-life trauma studies have extended this intervention logic to motor vehicle accidents, emergency caesarean section, and refugees, with reductions in intrusive memories." Add a separate source if claiming preserved deliberate recall. |
| 53 | Evidence base is heterogeneous; recent reviews and replications caution against treating effect as settled or uniform. | `asselbergs2023systematic`; `varma2024experimental`; `wessel2025evidence` | `supports directly` | Keep. `wessel2025evidence` is especially apt for replication caution; reviews support heterogeneity and limits. |
| 57 | A prominent interpretation treats selective interference as evidence for separable memory representations. | `brewin1996dual`; `brewin2014episodic` | `supports partially` | Good sources for separable/dual-representation theory, but the sentence ties that theory to "selective interference" more strongly than these sources alone. Keep but consider adding an intervention-specific source in the same paragraph, such as `holmes2009can` or `james2015computer`, or rephrase as "is often interpreted within..." |
| 58 | Dual-representation account posits sensory/contextual traces supporting involuntary re-experiencing and deliberate recall. | `brewin2010intrusive`; `brewin2014episodic` | `supports directly` | Keep. `brewin1996dual` could also be cited here if the paragraph wants the original theory attached to the mechanism statement. |
| 59 | Visuospatial interference competes for perceptual resources needed to consolidate sensory trace, reducing intrusions while sparing contextual/voluntary memory. | `holmes2009can`; `james2015computer` | `supports partially` | `holmes2009can` supports visuospatial competition and recognition not differing; `james2015computer` supports reminder/reactivation plus Tetris and reconsolidation-update. The sentence overstates the "contextual trace" part unless tied back to dual-representation sources. Consider splitting into: intervention evidence; then theory interpretation. |
| 60 | At longer delays, reminder reactivates sensory trace and interference disrupts restabilization during reconsolidation window. | `kindt2009beyond`; `james2015computer` | `supports directly` for reconsolidation concept and James selective-interference application; `supports partially` for "sensory trace." | Keep, but recognize `kindt2009beyond` is fear-conditioning/reconsolidation background, not trauma-film/Tetris evidence. `james2015computer` is the direct selective-interference source. |
| 70 | Event, reminder, and interference are encoded by binding item representations to evolving context; later model account will use this machinery. | `yonelinas2019contextual`; `howard2002distributed`; `polyn2009context` | `supports partially` | These sources directly support context binding/evolving context/CMR, but the sentence also states the present paper's application to reminder and interference phases. Consider wording as "Retrieved-context models provide the machinery for..." rather than implying the cited papers establish the entire selective-interference sequence. |

## Source-by-Source Appendix

### `asselbergs2023systematic`

- Metadata status: DOI metadata verified.
- Claim-fit basis: publisher/ScienceDirect abstract and metadata.
- Appropriate support: systematic review/meta-analysis of cognitive interventions to prevent intrusive memories in the trauma-film paradigm; useful for intervention evidence and heterogeneity.
- Current best use: line 53 heterogeneity/review support; partial support on line 51 for intrusion reduction.
- Caution: not primary support for voluntary-memory sparing.

### `brewin1996dual`

- Metadata status: DOI metadata verified.
- Claim-fit basis: abstract/metadata for Psychological Review article.
- Appropriate support: original dual-representation theory proposing verbally accessible and situationally/automatically accessible memory representations.
- Current best use: lines 57-58.
- Caution: not by itself a source for later Tetris/selective-interference effects.

### `brewin2010intrusive`

- Metadata status: DOI metadata verified.
- Claim-fit basis: publisher/university record and accessible PDF snippets.
- Appropriate support: intrusive images across psychological disorders; updated dual-representation/neural account.
- Current best use: line 41 intrusive image background; line 58 dual-representation mechanism.
- Caution: not specific to trauma-film selective interference.

### `brewin2014episodic`

- Metadata status: DOI metadata verified.
- Claim-fit basis: UCL record/abstract.
- Appropriate support: updated theory distinguishing episodic and perceptual memory and reviewing claims about voluntary/involuntary trauma-memory dissociations.
- Current best use: lines 57-58.
- Caution: supports the theoretical account, not a specific intervention result.

### `deeprose2012imagery`

- Metadata status: DOI metadata verified.
- Claim-fit basis: PMC full text.
- Appropriate support: post-film cognitive tasks modulating involuntary memories; theoretical emphasis on imagery/visuospatial competition.
- Current best use: intrusion-reduction/intervention logic in line 51.
- Caution: weak support for "voluntary memory shows little measurable impairment"; the paper itself notes need for broader voluntary-memory measures.

### `ehlers2000cognitive`

- Metadata status: DOI metadata verified.
- Claim-fit basis: abstract/metadata and accessible summaries.
- Appropriate support: cognitive model of PTSD emphasizing current threat, poor elaboration/contextualization, associative memory, and perceptual priming.
- Current best use: line 41, especially "not well matched to demands of the present."
- Caution: does not specifically define the trauma-film paradigm or selective-interference effects.

### `holmes2004trauma`

- Metadata status: DOI metadata verified.
- Claim-fit basis: PubMed abstract and article records.
- Appropriate support: trauma film, intrusive memory development, concurrent tasks, and weak relation of intrusions to recall/recognition measures.
- Current best use: lines 47-48.
- Caution: mostly peri-film/concurrent task evidence, not the post-film Tetris procedure emphasized later.

### `holmes2008inducing`

- Metadata status: DOI metadata verified.
- Claim-fit basis: publisher record/abstract.
- Appropriate support: review of the trauma-film paradigm as a method for inducing and modulating intrusive emotional memories.
- Current best use: line 44.
- Caution: broad review, not direct evidence for any one intervention result.

### `holmes2009can`

- Metadata status: DOI metadata verified.
- Claim-fit basis: PLOS article and PubMed record.
- Appropriate support: post-film Tetris/visuospatial task reduces flashbacks over one week; recognition memory did not differ between groups.
- Current best use: line 51 intervention claim and line 59 visuospatial-competition interpretation.
- Caution: use carefully for "voluntary memory" because the voluntary measure was recognition, not all voluntary-memory formats.

### `holmes2010key`

- Metadata status: DOI metadata verified.
- Claim-fit basis: PLOS/PDF records.
- Appropriate support: post-film Tetris versus verbal Pub Quiz/no-task; diary flashback reduction and recognition memory comparison.
- Current best use: line 51.
- Caution: supports a specific post-film task comparison, not post-reminder delay effects.

### `horsch2017reducing`

- Metadata status: DOI metadata verified.
- Claim-fit basis: publisher/ScienceDirect and accessible PDF snippets.
- Appropriate support: emergency caesarean section proof-of-principle study showing fewer intrusive traumatic memories after brief Tetris intervention.
- Current best use: line 52 for real-life trauma intrusion reduction.
- Caution: not strong support for "post-reminder" as a general label or preserved deliberate recall unless that outcome is explicitly documented.

### `howard2002distributed`

- Metadata status: DOI metadata verified.
- Claim-fit basis: publisher abstract and accessible PDF records.
- Appropriate support: Temporal Context Model; evolving temporal context and retrieved contextual states.
- Current best use: line 70 for evolving context.
- Caution: does not include CMR source context or selective-interference application.

### `iyadurai2018preventing`

- Metadata status: DOI metadata verified; current bib uses print/publication year 2018, while Crossref issued online metadata is 2017.
- Claim-fit basis: Nature article page and institutional repository records.
- Appropriate support: motor vehicle accident emergency-department intervention with reminder cue plus Tetris reducing intrusive memories.
- Current best use: line 52 for motor vehicle accident real-world trauma intrusion reduction.
- Caution: not clean support for "deliberate recall relatively intact" unless cited with a source that establishes preserved recall as an outcome.

### `iyadurai2019intrusive`

- Metadata status: DOI metadata verified.
- Claim-fit basis: PMC full text.
- Appropriate support: review bridging cognitive science and clinical application; intrusive memories as involuntary, imagery-based, clinically relevant target; real-world intervention summary.
- Current best use: line 41 and line 48 as background.
- Caution: review/background source; not primary evidence for a specific selective-interference comparison.

### `james2015computer`

- Metadata status: DOI metadata verified.
- Claim-fit basis: PMC full text and publisher abstract.
- Appropriate support: delayed reminder/reactivation plus Tetris reduces intrusive memories; both reactivation and Tetris required; interpreted as reconsolidation-update.
- Current best use: lines 51, 59, and 60.
- Caution: good for post-reminder and reconsolidation framing, but should not be overextended to all voluntary-memory measures without specifying what was tested.

### `james2016trauma`

- Metadata status: DOI metadata verified.
- Claim-fit basis: publisher/repository records.
- Appropriate support: trauma-film paradigm review and methodological overview.
- Current best use: line 44; background support on line 47.
- Caution: not direct evidence for a specific voluntary-memory dissociation.

### `kanstrup2021single`

- Metadata status: DOI metadata verified; current bib uses print year 2021, while online publication was 2020.
- Claim-fit basis: PubMed abstract and publisher metadata.
- Appropriate support: single case series with refugees using visuospatial task interference to reduce visual intrusive memories.
- Current best use: line 52 for refugee/real-life trauma extension.
- Caution: single case series is not strong general evidence, and does not by itself support preserved deliberate recall.

### `kessler2020visuospatial`

- Metadata status: DOI metadata verified.
- Claim-fit basis: publisher abstract and accessible PDF snippets.
- Appropriate support: Tetris after a film reminder delivered three days after trauma-film exposure reduces intrusive memories relative to control conditions; recognition memory was reported as comparable in accessible PDF snippets.
- Current best use: line 51 delayed reminder/intervention evidence.
- Caution: support for voluntary-memory sparing is recognition-specific.

### `kindt2009beyond`

- Metadata status: DOI metadata verified.
- Claim-fit basis: Nature article page/abstract.
- Appropriate support: human fear-memory reconsolidation background; reactivated fear memories can be disrupted.
- Current best use: line 60 as reconsolidation background.
- Caution: not a trauma-film or Tetris source; should not carry the selective-interference claim alone.

### `krans2009intrusive`

- Metadata status: DOI metadata verified.
- Claim-fit basis: DOI metadata and review records.
- Appropriate support: review/functional analysis of intrusive trauma memories.
- Current best use: line 41.
- Caution: background review, not selective-interference evidence.

### `lau2019intrusive`

- Metadata status: DOI metadata verified.
- Claim-fit basis: PMC full text.
- Appropriate support: direct evidence that post-encoding reminder-plus-Tetris reduced diary and vigilance intrusions while sparing free recall and recognition in matched voluntary-memory measures; explicit theoretical discussion of intrusive versus voluntary memory.
- Current best use: line 51 and possibly line 47/48.
- Caution: because it argues findings are more compatible with separate-trace accounts, it is a dialectically important source when cited in a paper arguing for a single-system alternative.

### `polyn2009context`

- Metadata status: DOI metadata verified.
- Claim-fit basis: publisher abstract and accessible PDF records.
- Appropriate support: CMR model; internally maintained context representation with stimulus/source features; context-to-item associations and memory search.
- Current best use: line 70.
- Caution: source is free-recall modeling, not emotional memory or selective interference.

### `varma2024experimental`

- Metadata status: DOI metadata verified.
- Claim-fit basis: Nature Human Behaviour page and PMC full text.
- Appropriate support: systematic review/meta-analysis of experimental methods for modulating intrusive memories after lab-analogue trauma, including heterogeneity and limits on generalization.
- Current best use: line 53.
- Caution: broad lab-analogue review; not specific support for voluntary-memory sparing.

### `wessel2025evidence`

- Metadata status: DOI metadata verified; article number `130791` used as pages/article number.
- Claim-fit basis: publisher/repository records and DOI metadata.
- Appropriate support: multilab replication showing immediate but not subsequent daily intrusion reduction after Tetris, supporting caution about robustness/uniformity.
- Current best use: line 53.
- Caution: its main result cuts against a broad "Tetris reduces later daily intrusions" claim, so avoid citing it in a cluster that only asserts efficacy.

### `yonelinas2019contextual`

- Metadata status: DOI metadata verified.
- Claim-fit basis: PMC full text.
- Appropriate support: contextual binding theory, item-context binding, context reinstatement, and interference/context logic in episodic memory.
- Current best use: line 70.
- Caution: broad episodic-memory theory; not CMR and not selective-interference specific.

## Metadata Corrections Needed

No objective errors were found in the current `selective_interference_v2/references.bib` during this audit.

Notes:

- `iyadurai2018preventing` is printed in 2018 but DOI metadata has online issue/issued dates in 2017; the current year choice is defensible for APA-style print issue citation.
- `kanstrup2021single` is printed in 2021 but DOI metadata has online publication in 2020; the current year choice is defensible for APA-style print issue citation.
- `wessel2025evidence` has article number `130791` rather than conventional page range; current `pages = {130791}` is acceptable for rendering.
- The fresh `references.bib` corrected several likely metadata problems from older local clue files, including `holmes2010key` author initial/name, `deeprose2012imagery` author names, and several accented names.

## Coverage Verification

Citation-bearing manuscript lines covered:

- 41
- 44
- 47
- 48
- 51
- 52
- 53
- 57
- 58
- 59
- 60
- 70

All 25 currently cited keys appear in the source-by-source appendix.

Audit limitations:

- Full text was inspected when openly available through PMC, PLOS, publisher pages, or institutional PDFs.
- For some paywalled or partially accessible articles, claim-fit assessment used abstracts, publisher metadata, repository summaries, and reliable full-text snippets.
- This audit evaluates current citation fit; it does not rewrite claims or insert replacement citations.
