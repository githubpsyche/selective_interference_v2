# Abstract

> In the trauma-film paradigm, participants typically encode a trauma film, then after some delay, receive a film reminder, and perform a visuospatial intervention task. The visuospatial task can reduce the frequency of film-related intrusions while leaving voluntary memory relatively intact. This selective interference effect is often treated as evidence that involuntary and deliberate remembering depend on different memory representations. We propose instead that the dissociation can reflect differences in how retrieval is cued and controlled. We implement this account in an emotional Context Maintenance and Retrieval (eCMR) model that simulates film, reminder, and task and predicts sequences of film and non-film recall events. In the model, a film reminder reinstates film-associated context. Task items are then encoded in association with that context, so later, film- associated context can cue task competitors as well as film items. We show that the differential impact of this intervention on involuntary and deliberate recall depends on the nature of the deliberate memory test. Deliberate recall is less affected when a maintained film-retrieval goal gives film candidates an additional source of support without equally supporting task competitors. Recognition is less affected than recall because recognition memory decisions in the model are a function of the item’s fit to context, an evaluation that is not affected by the presence of task competitors. Interpreting selective interference this way motivates better-matched tests of intrusive and voluntary remembering and situates trauma-film findings within a broader computational account of episodic retrieval.

About first sentence, Deborah argues:

> Seems too petty for the start, and the phrasing is awkward (later film reminder?)

She suggested a different wording:

> In the trauma-film paradigm, participants typically encode a trauma film, then after some delay, receive a film reminder, and perform a visuospatial intervention task. 

But this still seems to make the same error of starting with a "petty" detail. Our shift to a more general framing of our research problem should be reflected in the abstract and solve this issue more comprehensively.

Moving on, she also replaced "film-related" with "film-associated". This is probably more technically accurate. I'll look to enforce this change throughout the manuscript.

She also suggests phrasing "visuospatial intervention task" instead of just "visuospatial task", but only for the first mention. After that, she treats "visuospatial task" as fine.

Replaced "task encoding" with just "task".

Makes more explicit the rationale for why recognition is less affect than context-guided recall. 

Uses the phrase "recall" for the non-recognition paradigms. I find this phrasing a bit ambiguous, but it seems to be well-precedented in the literature to use "recall" to refer to generating a memory without the target being present. If this is an established terminology, I might reinstate and wield it more consistently throughout the manuscript alongside a literature review centering on the distinction between recall and recognition. Still, I'm kind of suspicious. "Recall" is just such an open-ended term in common usage, and it seems like it could be confusing to readers who are not familiar with the literature.

Suggests:

> We show that the differential impact of this intervention on involuntary and deliberate recall depends on the nature of the deliberate memory test. Deliberate recall is less affected when a maintained film-retrieval goal gives film candidates an additional source of support without equally supporting task competitors. Recognition is less affected than recall because recognition memory decisions in the model are a function of the item’s fit to context, an evaluation that is not affected by the presence of task competitors. 

As a sum-up of our results, but this feels too narrow. It seems to suggest that it's just a test format difference that matters, but the model also predicts that the nature of the film reminder, the timing of the intervention, and the similarity of the film and task contexts also matter. And of course we have a positive explanation for why retrieval intentionality matters, which is that it enacts control processes that can help to resolve competition. 

So along with updating the opening framing of the abstract to center on a more general research problem, we should also update the summary of our results to reflect the broader set of factors that our model predicts will influence the selective interference effect. Without just dumping a list of underspecified terms in the reader's lap.

# Introduction Opening

Really liked:

> Explaining how episodic memory preserves consequential events while regulating their retrieval is therefore a shared target for both clinical science and mechanistic theories of memory.

And liked the whole first paragraph. I guess I should be careful superceding it.

Next, in sentence:

> In such research, intrusion frequency can be weakly related to voluntary-memory performance, such that the two measures dissociate (Holmes et al., 2004; James et al., 2016). 

She comments emphasizing "is often only weakly". She is suggesting we should use that language instead of "can be weakly". I think this is a good point, and we should make that change.

Then in sentence:

> These reminder-plus-Tetris procedures can also reduce subsequent intrusions (James et al., 2015; Kessler et al., 2020).

She comments: "More strongly, only they work, without reminder no joy". I interpret this as meaning she wants to emphasize that the reminder is a critical component of the intervention, and that without it, the intervention does not work. We should make that point more explicitly.

Then in sentence:

> Related procedures have been extended beyond analogue trauma films to real-life and occupational trauma, including motor vehicle accidents, emergency caesarean section, refugee trauma, and health-care work during COVID-19 (Beckenstrom et al., 2026; Horsch et al., 2017; Iyadurai et al., 2018, 2023; Kanstrup et al., 2021, 2024; Ramineni et al., 2023). At the same time, recent reviews and replication attempts caution against treating the effect as settled or uniform (Asselbergs et al., 2023; McConnell et al., 2026; Varma et al., 2024; Wessel et al., 2025). 

She comments: "I think this is discussion material". I interpret this as meaning that she thinks this is more appropriate for the discussion section, and that we should consider moving it there. I'm sort of ambivalent -- I think we need to motivate the paper in our introduction, and part of that task is demonstrating that the procedure and effect is 1) widely demonstrated and 2) has real-world relevance. From there, we have to acknowledge 3) that the effect is not uniform and that there are open questions. An alternative strategy might be to more clearly motivate these points in the introduction so that sentences like these do not feel out of place. 

About: 

> Figure 1 schematizes this target as an interaction among reminder timing, task condition, and retrieval condition.

She comments: "This is unclear." Yeah, this is just doing that list-of-underspecified-terms thing again. 

Then about: 

> Intrusive re-experiencing is linked especially to sensory-bound representations, whereas deliberate remembering depends more on contextualized episodic representations (Brewin et al., 2010; Brewin, 2014). 

She comments: "I think we should add something here from the burgess review, about hippocampus vs. not".

About:

> Because later intrusions are assumed to arise especially from sensory-bound representations, this competition should reduce intrusions while leaving voluntary-memory performance relatively preserved (Deeprose et al., 2012; Holmes et al., 2009, 2010; Lau-Zhu et al., 2019). 

She comments: "Above you already commit that it does?", referring to "should reduce". I interpret this as a problem with the tense of the verb. If the theory asserts that the competition reduces intrusions, then we should phrase it as a statement of fact rather than a conditional. She may also be complaining that we are saying something we already said.

About:

> Across these variants, selectivity is explained as a stronger effect on the memory basis for intrusions than for voluntary remembering.

She comments: "Weak phrase - suggest sticking to sensory bound representation.", highlighting the "memory basis" phrasing as weak. I dunno; I feel like we want to extract the broader principle that the effect is selective, and that this selectivity is explained by the nature of the memory representations. But I can see how "memory basis" is a bit vague and could be improved.

About:

> Here we argue that preserved voluntary memory does not, by itself, establish that a separate representation was spared. Selective interference can instead arise from differences in how film memories are cued and controlled at retrieval. 

She says: "I think this paragraph can be expanded to make the conceptual point we discussed earlier today. That there could be one representation that can be accessed more/less readily. You could give example from recognition failure of recallable words - it’s about retrieval not storage."

The conceptual point she's talking about is one she and I are maybe not on the same page about. I need to clarify my own thinking, work with her to understand her perspective and agree on a shared position, then make room in the introduction to explain that position. I think the point she's making is that the selective interference effect does not necessarily imply that there are two separate memory representations for film and task material, but rather that there is one representation that can be accessed more or less readily depending on the retrieval conditions. But this does not quite seem right. I genuinely think that the visuospatial task intervention changes part of the memory representation while leaving a different part (probed during deliberate recall) relatively intact. So I do think it's about storage, not just retrieval. 

Then about:

> In the account developed below, a film reminder reinstates context associated with the film before task material is encoded. Task material then becomes linked to that context. When later remembering is guided by film-related context, task and film material compete, interfering with film recall. The task interferes less when retrieval depends less on context to access film material. Deliberate recall can be less affected when a maintained film-retrieval goal gives film candidates an additional source of support without equally supporting task competitors. Tasks like recognition can also be less affected, because the test presents a candidate film item for judgment rather than requiring film material to be brought to mind. On this account, the selective-interference effect emerges when retrieval conditions differ in how much they depend on film-related context that also cues task material.

She says: "It’s not clear what this is about. I think  you are specifying details of a simulation, but the ‘account’ is a general thing, perhaps what you write about in the above paragraph. Perhaps - we simulate a study where…. Even more - the specific study of James". 

Then: "In the next sentence you already foreshadow results. You’ve not yet told people you are doing model simulations."

Then: "When you next say ‘We formalize this retrieval account it’s not clear to me because the above was already from a formal account. "

I don't think this is just specifying the details of a simulation, yet it may still be too low-level for this stage of the draft? Perhaps we need to extract a higher-level distillation of the theoretical claim before this comes here. My idea of what counts as a formal account is probably different from hers. The broader point is that I need to give a higher-level presentation of the theoretical claim even before I describe how the theory reframes the DRA interpretation of the effect that I presented earlier.

There's the separate question of whether I can target a specific study like James here. I kind of doubt it? Yet naming an empirical target was a goal of Figures 1 and 2 and I might need to work out my decisions more explicitly in the "approach" part of this opening. 

About:

> We use simulations of emotional CMR to explore what the formalized account predicts about when and how the dissociation should appear. The simulations first show how a film reminder can make task material compete with film recall by linking task encoding to film-associated context. They then decompose when this competition has effects, and how these vary across retrieval conditions. We observe that deliberate recall can give film material a more selective basis for recall, and recognition-like tests can present the candidate item for judgment rather than requiring it to be brought to mind. The result is a mechanistic account of the selective-interference effect that does not rely on the presence of separate memory representations. It clarifies boundary conditions for the dissociation and motivates better-matched tests of intrusive and voluntary remembering.

She highlights "and recognition-like tests can present the candidate item for judgment rather than requiring it to be brought to mind." and comments:  "This is given - probably not what you meant to say. This paragraph seems the same as the one before last". She's right that there's a lot of stuff here repeated in the theory-walkthrough paragraph, though the two certainly have different roles.

Suggests a fuller statement distinguishing our account from the DRA account:
> The result is a mechanistic account of the selective-interference effect that does not rely on the presence of separate memory representations

However, I'm no longer willing to say that our account does not rely on the presence of separate memory representations, so a different kind of distinguishing statement is needed. Hmmm.

About:

> It clarifies boundary conditions for the dissociation and motivates better-matched tests of intrusive and voluntary remembering.

She highlights "the dissociation" and comments: "Maybe remind the reader between what?"

===

Right. 

A retrospective on this past push on the manuscript is that while I scheduled milestones for sections of the manuscript, over time I let the milestones slip and continued to work on sections or materials that -- I guess by my view -- had not yet reached a satisfactory state. Worse, sometimes my work on milestones pushed the manuscript into a non-ready state by the day's end because of the scope of the changes I made (but had not yet finished!). So there were either two problems with how I planned and worked that week. Either I planned less time than I needed to get a section to a satisfactory state, or the scope of the changes I set out to make to the text was too large for the time I had made available. To an extent, I feel like committed both errors at different times. When I allocated time for each section, I did not always accurately estimate how much time I would need to get the section to a satisfactory state. And when I started working on a section, I did not constrain the scale of my work to match the time allocated.