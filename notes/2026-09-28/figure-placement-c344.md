# Figure placement: c344

Status: implemented and rendered, 28 September 2026.
Jordan approved the manuscript-wide placement audit and the reply drafted in chat.

Rik’s comment asked for an explanatory citation before each figure, particularly the positional diagnostic now numbered Figure 10.
The same issue also occurred in the earlier simulations.
Figures 1–4, 6, 10 and 11 already had suitable introductions and were left in place.

| Figure | Accepted placement |
|---|---|
| 5 | After the aggregate-result sentences ending “under fixed retrieval settings”, before the Figure 6 positional explanation. |
| 7 | After the first three recognition-result sentences, before the explanation of the access route and the transition to Simulation 3. |
| 8 | After its existing explanatory results paragraph. |
| 9 | After its existing control-comparison paragraph, before the sensitivity results. |

Each figure moved together with its image and caption, preserving its identifier, numbering, original contents and all pending wording/image suggestions.
The same relocations and necessary paragraph boundaries were applied to `reference.qmd`.
No revised wording, comment decision or current replacement image was copied into that comparison reference.
The original pooled Word file was unchanged.
The comparison contains only the pre-existing whitespace edit, with no relocation redlines.

The approved reply was added to c344 under Jordan’s name, and c344 was resolved.
c346, Rik’s pending numerical deletion s267, and c357 were left unchanged.
A separate pending suggestion, s436, adds this sentence to the Simulation 1 mechanism paragraph:

> The reminder increases similarity between film- and task-encoding contexts ([Supplementary Figure S1](../../index.qmd#suppfig-context-similarity)).

## Verification

All previous suggestion contents, authors and decisions were preserved, as were all original comment bodies and anchors.
Figure order remained unchanged in both the working and comparison sources.
Removing the figures and rejecting the new pointer recovers the prior prose sequence, apart from paragraph spacing.
Source parsing and comparison checks passed.
Regular HTML and APA Word were rebuilt, without browser inspection.
The HTML front-matter check passed.
Word checks verified the four placements, the exact c344 reply and resolved state, c346/c357 remaining open, and the supplementary pointer remaining tracked.
No commit was made.
