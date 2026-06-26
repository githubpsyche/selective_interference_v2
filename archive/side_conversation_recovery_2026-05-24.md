# Side Conversation Recovery

Date: 2026-05-24

This transcript was cleaned from the user-pasted conversation text. Speaker labels and Markdown structure were restored from the visible turn order and wording. User wording, including typos, was preserved.

## User - 1:01 PM

Cue-support predictions need to be aligned with Lau-Zhu et al. 2021.
They explicitly manipulated associative cues and found cue presence enhanced retrieval but did not clearly moderate the selective-interference effect.
So Simulation 4 must distinguish weak associative cues from stronger supplied-item cueing or test-phase reinstatement.

tell me more about this? im specifically interested in how clearly they evinced that cue presence did not moderate the selective interference effect

## Assistant - after 1:01 PM

_Worked for 1m 12s_

They evinced it reasonably, but not decisively.

What they actually showed in Lau-Zhu et al. 2021:

- **Design:** reminder + Tetris vs reminder only crossed with cue type.
- **Cue type:** trauma-film associative cues versus foil/unseen-film cues.
- They applied this logic to a vigilance-intrusion task and a modified recognition task.

For the vigilance-intrusion task:

- Cue presence worked as a manipulation check: trauma-film cues produced more intrusions than foil cues, `F(1,34) = 19.61`, `p < .001`, `ηp² = .366`.
- The interference group also had fewer intrusions overall, `F(1,34) = 6.64`, `p = .014`, `ηp² = .163`.
- The critical moderation test was the `Group × Cue Type` interaction.
- That was not significant: `F(1,34) = 2.38`, `p = .132`, `ηp² = .065`, `90% CI [0, .22]`.

Means were:

- Trauma-film cues: Tetris `7.56`, control `17.94`.
- Foil cues: Tetris `4.39`, control `11.39`.

So the interference effect was present under both cue conditions, and the difference between those effects was not statistically reliable. See published lines 611-629 and Table 2 lines 647-649 here.

For the modified recognition task:

- Cue type trended in the predicted direction, `F(1,34) = 3.25`, `p = .080`.
- There was no main effect of interference group, `F(1,34) = 2.40`, `p = .131`.
- There was also no `Group × Cue Type` interaction, `F(1,34) = 0.59`, `p = .447`, `ηp² = .017`, `90% CI [0, .14]`.

This supports their claim that voluntary recognition remained spared even when the recognition test included associative cues. See lines 664-680 here.

How strong is the evidence?

I would phrase it as:

> Lau-Zhu et al. found no evidence that associative cue presence moderated the selective-interference effect, even though the cues increased retrieval/accessibility.

I would not phrase it as:

> Lau-Zhu et al. conclusively showed that cue support cannot moderate selective interference.

Reason: they explicitly note that they were powered for medium-to-large interactions, not small interactions; see lines 883-889 here. Also, the intrusion interaction estimate was not zero; it was just not reliable in `n = 36`.

For our Simulation 4, the key distinction is that their "associative cues" were not the same as a strong CMR supplied-item cue or test-phase context reinstatement. Their cues enhanced accessibility but did not erase the selective-interference pattern. So our draft should not imply that any cue support must eliminate the dissociation. It should distinguish weak/moderate associative cueing from stronger item-cued or context-reinstating test formats.

## User - 1:04 PM

It looks like your reply is a bit unfocused/wide-ranging.  im specifically interested in how clearly they evinced that cue presence did not moderate the selective interference effect. not merely that cue presence increased trauma film item recalls across both retrieval intentionality conditions. and im not interested in recognition at all

## Assistant - after 1:04 PM

For the intrusion/vigilance task only, the evidence is suggestive but not especially strong.

They tested whether cue presence moderated the interference effect with a `Group × Cue Type` interaction:

- **Group:** reminder + Tetris vs reminder only
- **Cue type:** trauma-film cues vs foil cues
- **Outcome:** number of intrusions in the vigilance-intrusion task

The interaction was not significant: `F(1,34) = 2.38`, `p = .132`, `ηp² = .065`, `90% CI [0, .22]`.
They interpret this as no evidence that the intrusion-reduction effect depended on same-film cue presence.

But the means do not make this look like a clean null moderation result:

- Trauma-film cues: control `17.94`, Tetris `7.56`, difference `10.38`
- Foil cues: control `11.39`, Tetris `4.39`, difference `7.00`

So the interference effect was numerically larger when trauma-film cues were present.
That difference in effect sizes just was not statistically reliable in their small sample (`n = 36`).

They also explicitly acknowledge limited power for interactions: enough for medium-to-large interactions, not small ones.

So the best characterization is:

> Lau-Zhu et al. found that reminder-plus-Tetris reduced intrusions under both cue conditions and found no reliable `Group × Cue Type` interaction, but the study did not provide strong evidence for the absence of cue moderation. The data are compatible with no moderation or with modest moderation.

That matters for our draft because we should not use Lau-Zhu et al. 2021 as evidence that cue support cannot matter. At most, it constrains us to say their associative cues did not clearly moderate the intrusion-reduction effect under that specific vigilance-task implementation.

## User - 1:04 PM

so they had an IV where participants saw foil cues instead of trauma film cues? in distinct recall periods?

## Assistant - after 1:04 PM

Yes, for the vigilance-intrusion task they had two cue conditions in distinct task blocks/periods.

From the method description:

- Participants completed vigilance-intrusion tasks while doing a simple go/no-go task.
- One version included trauma-film associative cues.
- Another version included foil cues from unseen/different films.
- These were separate vigilance-intrusion tasks, not intermixed trial-by-trial within one continuous recall period.

Important detail: they were not fully counterbalanced.
The trauma-film cue version came after the foil-cue version, and they discuss this as a limitation. They argue the cue effect is unlikely to be just time/order because intrusions should normally decline over time, yet more intrusions occurred with trauma-film cues administered later.

So, in design terms:

- **Between-subjects:** reminder + Tetris vs reminder only
- **Within-subjects/block:** foil-cue vigilance task and trauma-film-cue vigilance task
- **Outcome:** number of intrusions during each task block

That setup supports "trauma-film cues increased intrusions" reasonably well, but makes the moderation question less clean because cue type is also block/order/context.

## User - 1:05 PM

Right okay. And they found that trauma film items were recalled more in the film cue condition than in the foil cue condition. but that selective interference was the same?

## Assistant - after 1:05 PM

Yes, with two qualifications.

What they found in the vigilance-intrusion task:

- Trauma-film cues produced more intrusions than foil cues overall.
- Means collapsed informally across groups:

```text
Trauma-film cues: (7.56 + 17.94) / 2 = 12.75
Foil cues:        (4.39 + 11.39) / 2 = 7.89
```

- The cue main effect was reliable: `F(1,34) = 19.61`, `p < .001`.
- Reminder-plus-Tetris reduced intrusions in both cue conditions.

Differences:

```text
Trauma-film cues: 17.94 - 7.56 = 10.38 fewer intrusions.
Foil cues:        11.39 - 4.39 = 7.00 fewer intrusions.
```

The moderation test was not reliable.

```text
Group × Cue Type: F(1,34) = 2.38, p = .132.
```

So their conclusion is basically:

> Same-film cues increased intrusion retrieval, but there was no reliable evidence that the Tetris interference effect depended on whether those cues were present.

But I would not say "selective interference was the same" without qualification.
Numerically, the Tetris-control difference was larger with trauma-film cues than foil cues.
The study supports "no clear/reliable moderation," not "equivalent effects."

## User - 1:06 PM

This seems challenging for the retrieved-context account!

## Assistant - after 1:06 PM

Yes. It is a real challenge, especially for a simple cue-support story.

If our account says "film-related cues should protect film retrieval by steering search toward film context," Lau-Zhu et al. 2021 pushes back:

- same-film cues increased intrusions, so they were effective retrieval cues;
- reminder-plus-Tetris still reduced intrusions under same-film cues;
- there was no reliable evidence that same-film cue presence reduced the Tetris effect.

So we should not frame Simulation 4 as "any film cue should eliminate/narrow selective interference."

A retrieved-context interpretation can still survive, but it has to be more specific:

1. **Their cues may have increased opportunity for retrieval without changing retrieval control.**

   Trauma-film cues can raise the rate at which film-related memories are sampled while leaving the sampling process broadly unguided. More opportunities for intrusions does not necessarily mean better protection from task competitors.

2. **Same-film cues may cue both film hotspots and task competitors.**

   If task items are bound to film-associated context, then reinstating film context can support task competitors as well as film items. Cueing film context is not automatically protective unless it is sufficiently target-specific.

3. **Cue support may increase overall retrieval while preserving proportional interference.**

   In their means, same-film cues increased intrusions in both groups. The Tetris-control gap was numerically larger with film cues, but not reliably moderated. That is compatible with cues multiplying access while the interference manipulation still shifts the competition landscape.

4. **Recognition-like supplied-item cues are different from associative background cues.**

   Their vigilance cues were associative triggers: neutral/early scenes intended to provoke hotspots. They were not direct probes of a specific film item with a recognition decision. In CMR terms, they may be broad film-context cues rather than supplied-item probes that bypass context-to-item search.

5. **Test-phase cue effects may depend on specificity and task demands.**

   A broad film cue can increase intrusive access; a target-specific cue plus deliberate decision could reduce reliance on broad context-guided sampling. That distinction needs to be built into Simulation 4.

So the revised prediction should be:

> Retrieved-context theory does not predict that all film-related cues reduce selective interference. Broad associative film cues can increase film-memory sampling while leaving interference intact, especially if they reinstate contexts that also cue task competitors. The protective cue-support prediction should be limited to cues or test formats that make retrieval more target-specific, such as supplied film items, strong film-directed start cues, or recognition-like probes with explicit film-target decisions.

This means Simulation 4 should probably distinguish at least two cue types:

- **Broad film-context cue:** can increase overall film access but may not reduce interference.
- **Target-specific supplied-item cue:** should reduce reliance on context-to-item competition and therefore narrow the dissociation.

That is more faithful to Lau-Zhu et al. and actually makes the model more interesting.

## User - 1:06 PM

I'm okay describing this as a prediction of the retrieved-context account if it really is, even if it contradicts a published work's findings.

## Assistant - after 1:06 PM

Yes, but only if we specify the prediction sharply enough.

A broad prediction like:

> Film cues should reduce the selective-interference effect.

is probably not a safe retrieved-context prediction, and Lau-Zhu 2021 is direct friction.

A sharper retrieved-context prediction can be:

> Cues should reduce selective interference only when they shift retrieval away from broad context-to-item sampling and toward target-specific access.

That is genuinely retrieved-context in character, because it depends on whether the cue changes the retrieval operation:

- Broad associative film cues reinstate film-related context.
- They can increase film-memory access but may also cue competitors if task items were bound to that context.
- So they need not reduce the interference effect.
- Target-specific supplied-item cues probe item-to-context memory or provide direct item support.
- They reduce reliance on broad context-to-item competition.
- These should narrow interference.
- Start-of-list or test-phase film-context reinstatement is intermediate.
- It can help if it reinstates context that preferentially supports film items rather than task/filler competitors.

So the prediction is not contradicted if Lau-Zhu's cues were broad associative cues rather than target-specific supplied-item cues. But if we want to predict that their exact trauma-film cues should moderate the Tetris effect, then yes, we'd be taking on a published non-significant interaction.

I'd phrase the prediction as:

> Retrieved-context theory predicts that cue support should moderate selective interference when the cue changes the balance of context-to-item competition in favor of film targets.
> Broad associative cues may increase retrieval frequency without narrowing the interference effect if they reinstate contexts that also support task competitors.

That gives us room to cite Lau-Zhu 2021 as a useful constraint rather than a contradiction.

## User - 1:07 PM

You need to convince me that "Film cues should reduce the selective-interference effect." is not predicted by RCT. I'm already convinced that it contradicts the Lau-Zhu paper, but I'm not convinced that RCT doesn't force it.

## Assistant - 1:08 PM

RCT does not force "film cues reduce the selective-interference effect" because, in RCT/CMR, a cue helps only by changing the support distribution over candidates.
A film cue is not intrinsically protective.
It is protective only if it increases film-item support more than it increases competitor support.

In CMR terms:

```text
Retrieval samples from context-to-item support:
support_i = [M^{CF} c]_i
```

A film cue changes context by retrieving or reinstating film-associated context through `M^{FC}`.
But if the interference task was encoded in film-associated context, then the reinstated film context can cue both:

- film items, and
- task items associated with that same context.

So a film cue can have three possible effects:

1. **Target-specific protection**

   If the cue reinstates context that strongly supports film items and weakly supports task items, film recall improves and interference narrows.

2. **Nonselective access boost**

   If the cue increases support for film items and task competitors together, overall film access may rise but the relative Tetris/control difference need not shrink.

3. **Competitor amplification**

   If task items are especially strongly bound to the reinstated film context, a film cue can even increase task competition.

That is why the broad prediction "film cues should reduce selective interference" is too strong.
RCT predicts a conditional:

> Film cues reduce selective interference only when they shift the film/task support ratio in favor of film items.

Lau-Zhu's associative cues plausibly increased film-memory access without necessarily improving that ratio.
They were not target-specific probes; they were background cues intended to trigger associated film hotspots.
In CMR terms, that is closer to broad context reinstatement than to supplying a particular film item for recognition-like access.

So RCT forces this instead:

> Cue effects depend on cue specificity and on whether task competitors share the reinstated context.

That is a stronger and more precise prediction than "film cues help."

## User - 1:08 PM

Okay, I see. If we take seriously that interference task and film items are associated with overlapping context, then an intervention that reinstates overlapping context should not necessarily reduce interference. However, this is in tension with our results finding, for example, that start-of-list context reinstatement at beginning of recall facilitates film-item recall, which we find because the current modeling paradigm does not literally assign perfectly overlapping context across film and task items.

## Assistant - 1:11 PM

Exactly. The key is that "film-associated context" is not a single undifferentiated cue in the model.

In CMR, film and task items can overlap in context enough to compete, while still differing in which parts of context they are most strongly associated with.

That gives the model room for both results:

1. **Broad film-context reinstatement need not reduce interference.**

   If a cue reinstates context components shared by film and task items, it can support both.
   This is the Lau-Zhu-style issue: same-film associative cues can increase film access while leaving the interference effect intact.

2. **Start-of-list context reinstatement can protect film recall.**

   In your simulations, the start-of-list state is most similar to early film positions and less similar to task positions.
   Task items are encoded after reminder and drift, so their context overlap with film items is partial, not perfect.
   Reinstating the start state shifts support toward early film items rather than toward task/filler items.

3. **A cue's effect depends on what subset of film-associated context it reinstates.**

   "Film cue" is too coarse.
   A start-of-list cue, a reminder montage cue, a hotspot-associated cue, a supplied film item, and a broad trauma-film context cue can all have different support distributions.

So the prediction should probably be:

> Cue support narrows interference only when it reinstates context that discriminates film targets from task competitors. Cues that reinstate shared film-task context can increase film retrieval without reducing interference.

That is a very useful refinement, and it resolves the apparent contradiction.

It also suggests Simulation 4 should not just vary "cue present versus absent."
It should vary cue specificity:

- **Broad/shared context cue:** reinstates context components common to film and task, increasing overall retrieval but not necessarily reducing interference.
- **Start-of-list cue:** favors early film items because task items are less tied to that context.
- **Supplied item cue:** probes item-to-context associations for a specific film item and may bypass broad context-to-item competition.
- **Possibly hotspot cue:** may be intermediate or even risky if task encoding occurred after a reminder for that same hotspot context.

This would make Simulation 4 theoretically sharper and better aligned with Lau-Zhu 2021.

## User - 1:11 PM

I guess I worry that there's a difference between refinement and crutch. How does their pre-task reminder phase substantively differ from the kinds of reminders presented during test-phase? If they aren't very different, one might wonder why the latter is interpreting as a "broad" film context cue while reminder phase stuff isn't to extent that start-of-list context reinstatement si effectiec as a control mechanism.

## Assistant - 1:14 PM

That worry is legitimate. If "broad cue" versus "protective cue" is just a post hoc label, it becomes a crutch.

The substantive distinction cannot be "pre-task reminder = film-context reinstatement" and "test cue = broad film-context cue" unless the model specifies different cue content or different operations. In CMR terms, the cue's effect depends on at least three concrete things:

1. **Which film context is reinstated.**

   Start-of-list reinstatement is protective in your current simulations because it targets the start context, which is closer to early film items than to task items.
   A film montage/hotspot cue may reinstate later or broader film context, including context more similar to the reminder/task transition.

2. **When the cue is applied relative to task encoding.**

   A pre-task reminder makes task items competitors because it changes the context active during task encoding.
   A test-phase cue does not create new task associations, but it can retrieve already learned film/task competitors depending on the context it reinstates.

3. **Whether the cue is paired with control.**

   Start-of-list context reinstatement in Simulation 2 is not merely "a film cue"; it is a deliberate-recall control operation followed by retrieval selectivity/monitoring.
   Lau-Zhu's vigilance cues were associative prompts during an intrusion-monitoring task, not deliberate target-list retrieval with monitoring.

So the distinction is defensible only if we describe it this way:

> Cues differ not only in whether they are film-related, but in the context components they reinstate and in the retrieval operation they enter.

Then the prediction becomes:

- A pre-task reminder increases interference when it makes task encoding occur in film-associated context.
- A test-phase film cue can increase access without reducing interference if it reinstates context shared by film and task items under broadly cue-driven retrieval.
- A deliberate start cue can protect recall if it reinstates context that differentially supports film targets and is embedded in film-directed control.

That also exposes a possible weakness of current Simulation 2:
start-of-list reinstatement is effective partly because of the simulated phase structure, not because all film reminders should protect recall.
We should not generalize it as "film cues protect."
We should describe it as targeted start-of-list context reinstatement.

For Simulation 4, the model should probably not just compare cue/no cue. It should compare:

- broad film reminder context;
- start-of-list context;
- sequential film-item cues;
- supplied film-item probes;
- under unguided versus deliberate retrieval.

That would prevent "broad vs protective cue" from becoming a vague rescue distinction.
