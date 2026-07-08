Theory overview:
central theoretical claim -> neutral regularities -> modeling proposal -> mechanism -> selective-interference payoff

Model specification:
central implementation claim -> formal requirement -> representation/operation -> parameterization -> simulation role

===

Yes, my previous framing under-specified the parallel.

The theoretical overview’s organizing unit was a **warranted theoretical commitment**:

> Because these empirical regularities exist, this modeling move is justified, and it helps explain this part of selective interference.

The model specification’s organizing unit should be a **formal implementation commitment**:

> Given the account we just warranted, the model must represent this object or operation in this specific way, with these parameters, so the simulations can test this consequence.

So the right parallel is not just “say what the model contains.” It is:

```markdown
theoretical commitment → implementation requirement → formal operation → simulation consequence
```

That is the model-spec analogue of:

```markdown
empirical regularity → modeling proposal → mechanistic explanation → selective-interference payoff
```

The “why” is that the model spec is no longer earning the theory from the literature. It is **discharging obligations created by the theory section**. Each subsection should answer: *what must be implemented for the preceding theoretical claim to become a simulation-ready model?*

A better section-level template would be:

```markdown
## [Heading]

Central implementation claim:
One sentence stating which theoretical commitment this subsection formalizes.

Implementation requirement:
What the account requires the model to distinguish or preserve.

Formal objects:
The vectors, matrices, item classes, phases, or parameters introduced here.

Operations:
The equations or update rules that act on those objects.

Simulation role:
Which simulation manipulation or readout depends on this part of the model.

Guardrail:
What this formalization does not imply.
```

Then body paragraphs can follow a tighter version:

```markdown
1. Requirement:
What the theory section has made necessary.

2. Representation:
What model object instantiates that requirement.

3. Operation:
How the object changes during encoding, reminder, retrieval, or recognition.

4. Parameterization:
Which parameter controls the operation, or whether it is fixed.

5. Consequence:
What this enables the simulations to test.
```

Example:

```markdown
## Reminder-Linked Task Encoding

Central implementation claim:
The model implements the reminder-linked task intervention by reinstating film-associated context before task events are encoded, so task events acquire associations with context that also supports film items.
```

That subsection should not re-review reminders or intrusions. It should specify:

- what counts as a reminder cue;
- how the reminder updates context;
- whether the reminder is itself encoded as a recallable item;
- how task events are encoded after reminder-driven context reinstatement;
- which task-encoding-strength parameter is varied;
- why film-item associations remain fixed across reminder/no-reminder conditions.

That is the exact model-spec analogue of the overview, but with a different source of constraint. In the overview, the constraint is empirical/theoretical. In the model spec, the constraint is architectural: the formal model must preserve the distinctions the account depends on.