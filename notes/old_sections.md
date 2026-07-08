## Simulation 3: Test-Phase Film Cues and Retrieval Intentionality

Simulation 3 abstracts the cueing feature of vigilance-intrusion tasks.
The model does not simulate the full task; it simulates the moment when a film cue is presented during an ongoing retrieval period.
Each cue is implemented as a randomly selected film cue supplied after every fourth retrieval attempt.
The cue updates temporal and source context through feature-to-context associations, after which ordinary context-to-item retrieval resumes.
The supplied cue does not occupy a response slot, does not make the cued item unavailable for later recall, and adds no new learning.
Cue strength controls how strongly each supplied cue pulls context toward the film state associated with that cue.
The plotted values express that pull relative to the fitted recall context-update rate $\beta_{rec}$.
The vertical reference line in @fig-simulation3-film-cue-inclusion marks the point at which a supplied cue would move context by about the same amount as one ordinary encoding update, approximately $\beta_{enc}$.

::: {#fig-simulation3-film-cue-inclusion fig-pos="H"}
![](work/simulation3_film_cue_inclusion/simulation3_film_cue_inclusion.png)

**Test-phase film cues boost film recall, but deliberate recall remains advantaged.**
Simulation 3 compares unguided retrieval with deliberate recall while varying the strength of film cues supplied during retrieval.
**(A)** Numbered boxes represent ordinary retrieval attempts.
After every fourth attempt, the test supplies a film cue; the cue updates context before the next retrieval attempt, is not counted as a response, and adds no new learning.
**(B)** The left plot shows total film recall mass for unguided retrieval and deliberate recall as cue strength increases; the right plot shows the deliberate-minus-unguided gap.
Film recall increases with cue strength, but deliberate recall remains higher than unguided retrieval across weak-to-moderate cue values.
Only stronger cue values begin to narrow the gap.
**(C-D)** Curves plot recall probability at the retrieval test by encoded position, with darker lines indicating stronger film cue strength.
Under unguided retrieval, film cues modestly raise film recall but task and filler competitors remain prominent.
Under deliberate recall, film recall is already supported by start-of-list control, and these cues produce additional film recall without eliminating task competition.
:::

Panel B gives the primary test of the Simulation 3 prediction.
Weak-to-moderate test-phase film cues help unguided retrieval, especially relative to its low baseline, but they do not eliminate the deliberate-recall advantage.
For example, increasing film cue strength from 0.00 to 0.675 raises film recall mass from 0.008 to 0.210 under unguided retrieval and from 2.229 to 2.400 under deliberate recall, while the deliberate-minus-unguided gap changes only from 2.221 to 2.190.
This pattern separates greater film access from reduced interference.
A film cue can pull context toward film-associated states and increase film recall, especially during unguided retrieval.
The same cue need not remove the task competitors learned after the reminder, so the deliberate-minus-unguided gap can remain largely intact.
At stronger cue values, the gap begins to narrow because cue-driven reinstatement becomes strong enough to make film items dominate subsequent retrieval.

Panels C and D show how this effect unfolds over the full encoded sequence.
The cue manipulation does not remove the task competitors created by reminder-driven task encoding.
Instead, it changes the context available to subsequent search.
The result is a graded cue effect: film items supplied during retrieval can increase film recall, but they reduce selective interference only to the extent that the reinstated context favors film targets over task and filler competitors.

## Simulation 4: Context-to-Item and Item-to-Context Test Formats

Simulation 4 turns from vigilance-style cueing to recognition.
Recognition tests in the trauma-film literature present candidate film stills and ask participants to judge whether they appeared in the film [@lau2021selectively].
Retrieved-context models have also been extended to recognition more generally: a test probe can reinstate its associated context, and the match between reinstated context and the current retrieval context can contribute to an old-new decision [@healey2016four; @kahana2020computational].
Related recognition findings show that temporal context retrieved by one probe can influence recognition of nearby studied probes [@schwartz2005shadows].
The present simulation does not model decision criteria, foil familiarity, or confidence.
It isolates the supplied-item access step that recognition provides: the candidate film item is available first and can reinstate associated context before any need for that item to win a free-recall competition.
@fig-simulation4-test-format-schematic schematizes this distinction.
When recall requires context-to-item selection, overlapping context can support both film and task candidates, so interference can enter at item selection.
When the test supplies the film item, selection of that item is no longer the first step; the model instead asks what context the supplied item reinstates and whether access remains sensitive to the task associations created during encoding.
This provides a test-format consequence of the same bidirectional item-context loop examined in Simulation 3.

::: {#fig-simulation4-test-format-schematic fig-pos="H"}
![](work/simulation4_test_format_schematic/simulation4_test_format_schematic.png)

**Retrieval format changes where interference can enter.**
Simulation 4 demonstrates a test-format consequence of context-to-item recall versus supplied-item access.
**(A)** When recall requires selecting an item from current context, the same context state can support multiple candidates; task items therefore compete with film items when both have been encoded in overlapping contexts.
When the test supplies a film item, that item reinstates its associated context instead, so the task item is not an equivalent competitor at the point of access.
**(B)** In CMR, this asymmetry corresponds to two retrieval directions: context-to-feature associations cue candidate items, whereas feature-to-context associations reinstate context from a supplied item.
Simulation 4 uses this distinction to show how recognition tests can preserve access even when context-guided recall remains sensitive to interference.
:::

## Simulation 5: Task Specificity and Source-Context Overlap

Simulation 5 explores why some post-film tasks should produce stronger interference than others.
The model does not treat "visuospatial" and "comparison" as built-in task categories.
Instead, a task matters through the properties of the material it adds to memory: how strongly task items are encoded, how much their temporal context overlaps with film context, and whether they share source context with film items.
These factors can vary independently, so a task label is interpretable only through its consequences for competitor strength, temporal-context overlap, and source-context overlap.

The task-specificity simulations therefore decompose three candidate routes to interference.
Increasing the task encoding multiplier changes how strongly task items win once cued.
Changing temporal overlap alters whether task items are cued alongside film items.
Changing source-context overlap tests whether non-temporal source matching can amplify competition beyond temporal proximity alone.
The predicted outcomes are film access, task-competitor retrieval, and retrieval outcomes by encoded phase or position.
