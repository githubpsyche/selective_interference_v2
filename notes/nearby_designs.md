The clearest conclusion so far is: I have not found one existing dataset that clears the full bar. Two research families each provide half of what we need.

| Candidate | Same material target vs intrusion? | Context-binding manipulation? | Sequence/monitoring data? | Verdict |
|---|---:|---:|---:|---|
| Kiley & Parks (2020) | Yes | Yes | Apparently limited | Closest positive analogue |
| Kiley & Parks (2022) | Yes | Yes, via internal state | Apparently limited | Useful replication/generalization |
| Hupbach et al. (2007) | Across experiments | Yes | Limited | Foundational, but already modeled |
| Wahlheim et al. (2017) | Yes | No independent manipulation | Excellent | Best control-mechanism dataset |
| Wahlheim et al. (2019) | Yes | Arguably, but imperfect | Excellent | Richest near-match, with null aggregate effects |

The most important findings are these.

1. Kiley and Parks (2020) is the closest positive design match

Participants learned List 1 and then List 2. List 2 was learned either in the same spatial context as List 1 or in a different context. On the final day, participants received separate source-specific recall tests for both lists, with test order counterbalanced.

Consequently, the same List-2 items had two statuses:

- During Recall List 1, they were unintended intrusions.
- During Recall List 2, they were intended responses.

Learning List 2 in the same spatial context increased List-2 intrusions into List-1 recall, while correct recall of the two lists was not detectably changed. Thus, reversing the contrast, changing context reduced unintended access to List-2 material without reducing deliberate access to it. The manipulation also has a direct context-binding interpretation: reinstating the List-1 setting during List-2 encoding allows List-2 items to become associated with List-1 context. [Kiley & Parks, 2020](https://journals.sagepub.com/doi/10.1177/1747021820922555)

This is recognizably analogous to selective interference, but it is not identical to the manuscript’s present mechanism. It shows contextual binding selectively increasing access to later material when it is off-target. It does not show later competitors reducing unintended retrieval of the earlier focal material.

The data also appear insufficient for identifying all three mechanisms. Recall was not externalized, and responses could be used only once across the two tests, making the second test dependent on the first. I found no public response-level archive.

2. Kiley and Parks (2022) provides a related internal-context result

This study manipulated whether mood states matched across List-1 learning, List-2 learning, and retrieval. Both lists were again tested separately. Matching states produced asymmetric List-2 intrusions into List-1 recall without corresponding differences in correct list recall. [Kiley & Parks, 2022](https://journalofcognition.org/articles/10.5334/joc.198)

It strengthens the general contextual-binding interpretation, but it is a weaker benchmark for us:

- mood is an internal state rather than specifically temporal context;
- List 1 was always tested first;
- the public-data statement points vaguely to OSF and author contact, but I did not locate the archive;
- there is no externalized sequence exposing rejected candidates.

3. Hupbach is the foundational version, but not a sufficiently novel benchmark alone

Hupbach et al. used a reminder before List-2 learning. In one experiment, List-2 items were intrusions during List-1 recall; in another, List 2 was deliberately recalled. The reminder increased List-2 intrusions into List-1 recall without reducing deliberate List-2 recall. [Hupbach et al., 2007](https://pmc.ncbi.nlm.nih.gov/articles/PMC1838545/)

This is an unusually close conceptual precursor because the reminder can be interpreted as reinstating List-1 temporal context before List-2 encoding. However:

- intended and unintended retrieval were compared across experiments;
- response dynamics were not richly measured;
- Sederberg and colleagues have already explained the central aggregate result with a temporal-context model. [Sederberg et al., 2011](https://pmc.ncbi.nlm.nih.gov/articles/PMC3432313/)

Our novelty could therefore not simply be “CMR explains Hupbach.”

4. The Wahlheim datasets provide the richest control-mechanism evidence

The 2017 dual-list externalized-recall experiment comes closest to what we need for retrieval dynamics. After studying two lists, participants were postcued to recall List 1, List 2, or both. They reported every candidate that came to mind, classified it as target or nontarget, and rated confidence. The same items therefore switch between targets and intrusions depending on the retrieval instruction. [Wahlheim et al., 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5459665/)

Healey and Wahlheim subsequently used these data to distinguish pre-retrieval context reinstatement from a backward search through recent material. Their analysis demonstrates why output order and rejected candidates can adjudicate mechanisms that aggregate recall cannot. [Healey & Wahlheim, 2024](https://pubmed.ncbi.nlm.nih.gov/37782445/)

These data offer:

- first-response source and serial position;
- target and nontarget production across output positions;
- explicit monitoring judgments;
- confidence;
- identical learned material under different retrieval goals.

But they contain no independent manipulation of competitor formation or shared context. They can test retrieval control, not the selective-interference interaction.

5. Wahlheim et al. (2019) is the nearest attempt to combine both halves

This experiment crossed:

- a postcue to recall List 1 or List 2;
- externalized reporting and target/nontarget classification;
- an interpolated exemplar-generation versus two-back task between the lists.

It therefore contains detailed response order, source status, serial positions, first recalls, and an intervention interpreted as changing context. [Wahlheim et al., 2019](https://pubmed.ncbi.nlm.nih.gov/30725377/)

However, it does not provide the hoped-for positive analogue. The interpolated-task manipulation produced no aggregate effect on correct recall or within-trial intrusions. Moreover, the manipulation is normally interpreted as separating the two list contexts, not as strengthening associations between articulable competitors and focal-list context. It is therefore potentially valuable as a boundary-condition or model-falsification dataset, but not as the paper’s decisive positive demonstration.

6. The earlier candidates should remain dropped

Pastötter et al. does not instantiate the desired design cleanly. The same material changes status across an immediate test and a later cumulative test, not through matched retrieval instructions applied to the same encoded materials. The public information also appears too coarse for sequence-level modeling.

The directed-forgetting studies likewise tend to lack an independent competitor-binding manipulation, produce very few intrusions, or preserve only participant-level totals. The study asking participants to signal List-1 intrusions during List-2 learning is conceptually interesting, but only a handful of participants reported such intrusions and it does not supply the matched postcue comparison we need.

So the present state is:

- **Best positive context-binding analogue:** Kiley and Parks (2020).
- **Best dataset for identifying retrieval-control mechanisms:** Wahlheim et al. (2017), as modeled by Healey and Wahlheim.
- **Closest dataset containing both an intervention and externalized postcued recall:** Wahlheim et al. (2019), but its intervention result is null and the theoretical mapping is imperfect.
- **No existing dataset yet found that combines a positive selective-interference analogue with enough trialwise output information to identify all three mechanisms convincingly.**

I stopped before exhausting the remaining reconsolidation descendants, context-boundary experiments, and archival-data searches. No local files were changed.

===

Yes. We should let the dataset search go.

After roughly 21 minutes on this final search, on top of the earlier searches, I found no dataset that crosses all the necessary factors. The closest studies divide into separate traditions:

- Laboratory involuntary-memory paradigms manipulate whether A is deliberately or involuntarily retrieved, sometimes with identical cues, but do not independently manipulate whether never-target B competitors are encoded in A-associated context. [Staugaard & Berntsen, 2014](https://pure.au.dk/ws/files/85033932/Involuntary_Memories_of_Emotional_Scenes_The_Effects_of_Cue_Discriminability_and_Emotion_over_Time_2014_.pdf), [Kobelt et al., 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12364361/)
- Reminder-interference studies provide the contextual-intervention logic and the selective interference effect, but Tetris is not a set of reportable B memories and the archives lack ordered A/B candidate sequences. [James et al., 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC4526368/), [James et al. archive](https://osf.io/ideta/), [Lau-Zhu et al., 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC7116494/)
- List-before-last and context-change studies provide articulable intrusions and sometimes detailed recall sequences, but do not independently make A the target versus an intrusion while keeping B permanently off-target. [Jang & Huber, 2008](https://www.colorado.edu/lab/cemnl/media/36)
- Pastötter et al. provide the closest phenotypic analogue: an interpolated activity reduced prior-list intrusions without a corresponding loss on later cumulative recall. But the manipulation does not selectively vary A-context reinstatement before identifiable B encoding, retrieval status is confounded with test occasion, and no suitable public response-sequence archive appears available. [Pastötter et al., 2011](https://baeuml.app.uni-regensburg.de/paper/papers_open/PSNB%282011%29.pdf)

Combining datasets would not solve this. It could show that each component exists separately, but it could not test the crucial factorial prediction that contextual competitor formation affects A differently depending on whether A is deliberately targeted.

The productive conclusion is that the proposed experiment is genuinely missing:

> Encode A → reinstate A-associated versus shifted context → encode identical, reportable B competitors → independently test A through deliberate recall or an incidental task in which A can occur only as an intrusion.

B is never targeted. Every A and B candidate is externalized, source-classified, ordered, and timed. The critical outcome is an interaction in which A-context binding of B reduces A intrusions while leaving deliberate A recall relatively preserved. First outputs, serial positions, B entries, rejection decisions, and post-B transitions can then distinguish the three control mechanisms. Semantic overlap between A and B could be added as a further manipulation of goal-cue diagnosticity.

That should become a sharply specified near-final Discussion proposal. I would say in the meeting that we searched for an archival test, found strong precedents for each component but no dataset containing their conjunction, and therefore regard the factorial experiment itself as a novel empirical consequence of the model.

===