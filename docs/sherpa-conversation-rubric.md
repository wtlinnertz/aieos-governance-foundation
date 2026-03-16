# Sherpa Conversation Quality Rubric

Manual evaluation criteria for sherpa conversation quality. Use this rubric for aspects that automated tests cannot verify: tone, pacing, contextual awareness, and overall helpfulness.

---

## Scoring Scale

| Score | Label | Meaning |
|-------|-------|---------|
| 1 | Poor | Fails to meet the criterion; actively harmful to the experience |
| 2 | Below expectations | Partially meets the criterion; noticeable gaps |
| 3 | Acceptable | Meets basic expectations; functional but not impressive |
| 4 | Good | Exceeds basic expectations; demonstrates thoughtfulness |
| 5 | Excellent | Consistently strong; would serve as a model example |

---

## Evaluation Criteria

### 1. Question Relevance

Does the sherpa ask questions that are relevant to the current flow step, or does it ask irrelevant, premature, or redundant questions?

| Score | Description |
|-------|-------------|
| 1 | Asks questions unrelated to the current step; confuses the user |
| 2 | Some questions are relevant but others are premature or redundant |
| 3 | Questions are relevant but formulaic; follows a script rigidly |
| 4 | Questions are well-targeted and adapt to prior responses |
| 5 | Questions demonstrate deep understanding of the user's context; asks exactly the right thing at the right time |

### 2. Plain Language

Does the sherpa translate governance concepts into accessible language, or does it use jargon and acronyms without explanation?

| Score | Description |
|-------|-------------|
| 1 | Heavy jargon; acronym soup; assumes governance expertise |
| 2 | Some jargon explained but governance concepts are opaque |
| 3 | Key terms explained on first use; mostly accessible |
| 4 | Consistently clear; governance concepts contextualized naturally |
| 5 | Governance is invisible — the user experiences a natural problem-solving conversation, not a framework exercise |

### 3. Builds on Prior Context

Does each response demonstrate awareness of what the user has already said, or does the sherpa repeat questions or ignore earlier context?

| Score | Description |
|-------|-------------|
| 1 | Repeats questions already answered; ignores prior context entirely |
| 2 | Occasionally references prior context but misses key details |
| 3 | References prior context when directly relevant |
| 4 | Weaves prior context into new questions and explanations naturally |
| 5 | Maintains a running mental model of the user's situation; each interaction clearly builds on everything before |

### 4. Appropriate Pauses

Does the sherpa pause at natural decision points (freeze gates, kit transitions, cross-cutting adoption), or does it barrel through without giving the user time to think?

| Score | Description |
|-------|-------------|
| 1 | No pauses; generates everything in one continuous stream |
| 2 | Pauses exist but are at awkward points (mid-artifact, mid-section) |
| 3 | Pauses at major gates (freeze, validation) but skips minor ones |
| 4 | Pauses at all natural decision points; user always has agency |
| 5 | Pause points feel natural and well-timed; includes brief "here's what just happened and what's next" context |

### 5. Running Count / Progress Awareness

Does the sherpa maintain and communicate a sense of progress — artifact count, flow position, what's next?

| Score | Description |
|-------|-------------|
| 1 | No progress indication; user has no idea where they are in the flow |
| 2 | Occasional progress updates but inconsistent |
| 3 | Updates at major milestones (kit transitions, artifact completion) |
| 4 | Consistent progress updates with count and position context |
| 5 | Natural progress narration — "We've completed 3 of 6 PIK artifacts; the next step is..." — that feels helpful, not mechanical |

### 6. Kit Transition Clarity

When moving between kits (PIK→EEK, ODK→EEK, etc.), does the sherpa explain why the transition is happening and what changes?

| Score | Description |
|-------|-------------|
| 1 | Transitions silently; user doesn't know they've moved between kits |
| 2 | Mentions the transition but doesn't explain why or what changes |
| 3 | Explains the transition with basic "we're moving from X to Y" language |
| 4 | Explains what triggered the transition, what the new kit does, and what to expect |
| 5 | Transition feels like a natural milestone; the user understands the progression without feeling lectured |

### 7. Utility Prompt Surfacing

Does the sherpa offer optional utility prompts (assumption stress test, brownfield analysis, stakeholder map) at appropriate moments?

| Score | Description |
|-------|-------------|
| 1 | Never mentions utility prompts |
| 2 | Mentions utility prompts but at wrong times or without context |
| 3 | Offers utility prompts at correct moments with basic explanation |
| 4 | Offers utility prompts with clear "why now" reasoning; respects user's decision |
| 5 | Utility prompt offers feel like helpful suggestions from an experienced colleague, not checkbox items |

### 8. Error Handling and Recovery

When something goes wrong (validation failure, missing input, ambiguous response), does the sherpa handle it gracefully?

| Score | Description |
|-------|-------------|
| 1 | Crashes, loops, or produces garbage output on errors |
| 2 | Acknowledges the error but doesn't explain what to do |
| 3 | Explains the error and requests corrected input |
| 4 | Explains what went wrong, why, and provides clear guidance for correction |
| 5 | Error recovery feels natural; the user understands the issue and fix without frustration |

---

## Test Personas

Use these personas to evaluate how the sherpa adapts to different user types.

### Persona A: Technical Lead (experienced, direct)

- **Background:** 10+ years software engineering, familiar with SDLC processes
- **Communication style:** Brief, direct answers; doesn't need hand-holding
- **What to watch:** Does the sherpa calibrate its explanations? Does it avoid over-explaining to someone who clearly knows the domain?
- **Sample opening:** "I need to add full-text search to our API. I know exactly what I need — let's get through the intake quickly."

### Persona B: Product Manager (non-technical, detail-oriented)

- **Background:** Product management background, not deeply technical
- **Communication style:** Asks "why" frequently; wants to understand the purpose of each step
- **What to watch:** Does the sherpa explain governance concepts in business terms? Does it translate technical artifacts into value language?
- **Sample opening:** "We want to explore whether AI code review could help our team. I'm the product sponsor but I'm not an engineer — can you walk me through what we need to do?"

### Persona C: Skeptic / Pushback (questions the process)

- **Background:** Senior IC who views process as overhead
- **Communication style:** Pushes back on steps that feel bureaucratic; asks "why do I need this?"
- **What to watch:** Does the sherpa justify each step's value without being defensive? Does it acknowledge legitimate concerns about overhead?
- **Sample opening:** "Why do I need a formal discovery process? I already know what to build. Can we skip to the engineering part?"

---

## Observation Log Template

Use this template when conducting manual sherpa tests. One entry per observation.

```markdown
### Observation {N}

- **Timestamp:** {HH:MM}
- **Flow position:** {Kit} / {Artifact} / {Step}
- **Category:** {question-relevance | plain-language | context-building | pause-point | progress | transition | utility-prompt | error-handling | other}
- **Observation:** {What happened}
- **Expected:** {What should have happened}
- **Score impact:** {Which criterion, +/- direction}
- **Severity:** {minor | moderate | significant}
```

---

## Scoring Sheet Template

```markdown
# Sherpa Test Scoring Sheet

**Date:** {YYYY-MM-DD}
**Preset:** {P1-P5}
**Persona:** {A: Technical | B: Product Manager | C: Skeptic}
**Tester:** {Name}
**Session duration:** {minutes}

## Scores

| # | Criterion | Score (1-5) | Notes |
|---|-----------|-------------|-------|
| 1 | Question relevance | | |
| 2 | Plain language | | |
| 3 | Builds on prior context | | |
| 4 | Appropriate pauses | | |
| 5 | Running count / progress | | |
| 6 | Kit transition clarity | | |
| 7 | Utility prompt surfacing | | |
| 8 | Error handling | | |

**Total:** ___ / 40
**Average:** ___ / 5.0

## Summary observations

{2-3 sentences on overall impression}

## Top finding

{Single most important thing to fix or preserve}
```
