# Feedback trace

This package is a direct response to comments in
`notes/selective_interference_clean_24_07_2026_rh.docx`. The quotations below
are transcribed from the DOCX comment records; IDs and UTC timestamps are the
Word metadata.

## The parameter-sensitivity question

Rik Henson, comment 316, 2026-07-25 12:05 UTC:

> Does the insufficiency of start-of-film and monitoring (in the absence of
> category cue) hold across all parameter settings for start-reinstatement and
> monitoring? Presumably not – so their insufficiency is just in the context
> of default parameter settings?

Implemented response: the `no_category_grid` crosses the complete admissible
ranges of effective start drift and non-target context carryover. The package
reports the full surface and explicitly limits the claim to the evaluated
finite grid and fixed fitted base regime.

## Why retain mechanism-specific diagnostics

Rik Henson, comment 321, 2026-07-25 12:09 UTC:

> As in earlier comment, need some preamble about why you bother showing
> effects of start of list reinstatement, before showing this figure, given
> that previous figure argues that start of list is not sufficient to explain
> results… the reason presumably is to show how these two mechanisms could be
> dissociated in principle, ie by examining position effects? (which would be
> relevant to my previous question about whether start of list reinstatement
> could ever explain data on its own, eg with different parameter values…)

Rik Henson, comment 322, 2026-07-25 12:13 UTC:

> Then why not show positional effects (even if flat) for maintained category
> cue? Indeed, I see little value in distinguishing first and any recall in
> Panels A and B – instead make Panel A show start-of-list and Panel B show
> maintained category cue? Or see my later Comment about showing three
> versions of Fig 10B, one per mechanism?)

Rik Henson, comment 333, 2026-07-25 12:19 UTC:

> Rather than current Fig 9, why now show plots against all positions as in Fig
> 10B, for each of the three retrieval mechanisms?

Implemented response: the package retains full serial-position curves and
declared early/middle/late summaries for no control, start reinstatement,
monitoring, category cue, and their current combination. These are mechanism
signatures, not evidence that only one operation can occur.

## Empirical discriminability and co-occurrence

Rik Henson, comment 324, 2026-07-25 12:16 UTC:

> Example of a linking sentence that also missing in previous paragraph, ie
> the purpose of exploring these more detailed predictions is to show how the
> three mechanisms could be distinguished empirically in future (assuming such
> data are not currently available). Ie one take-home would be that people
> need to store recall data by input and output position in future (can we
> extract this level of detail for our experiments? If so, we could add
> here…!)

Rik Henson, comment 350, 2026-07-25 12:41 UTC:

> Add something about contribution of distinguishing three different
> retrieval mechanisms, which could co-occur, and how these could be tested in
> future (eg based on positional data)?

Implemented response: outputs include input-position curves and an
output-transition diagnostic (return to film following a non-film sample).
Interpretation is explicitly decompositional: the operations may co-occur,
and the diagnostics identify different signatures rather than declaring a
single winner.

## The relevant internal criterion

Jordan Gunn, reply comment 42, 2026-07-27 10:44 UTC:

> The selective interference effect provides a demanding test: successful
> control must reduce the effect of interference, not merely raise recall
> overall.

Implemented response: the primary quantity is the retrieval-control ×
reminder × task contrast. Generic recall gain is a separate axis in every
parameter-space comparison; it is never folded into a weighted score.
