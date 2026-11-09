# Governed autonomy loop

Use this pattern when an agent works toward an outcome on its own, with no human at each step. The agent plans the work at the level an expert would, does it, and can't declare it finished. An independent judge decides that, the agent can't change the judge, and every verdict lands in a record a human can audit.

[`review-convergence-loop.md`](review-convergence-loop.md) corrects one artifact that failed one validator. This pattern wraps that loop in three things it doesn't cover: choosing the outcome, planning the work and defending the judge against an agent that games it.

This is a workflow pattern. It needs no four-file tool set.

## Terms

| Term | Definition |
|------|-----------|
| Outcome | The end state the work is for, one level above the task as asked. "No high or critical findings in these repositories" is an outcome. "Bump this library" is a task. |
| Success signal | A check a tool or a third party can run that says whether the outcome was reached. A test suite, a scanner result or a threshold on a metric. |
| Judge | Whatever runs the success signal and returns PASS or FAIL. Validators in the governance model are judges. |
| Judge lock | A checksum of the judge recorded before the first change. |
| Protected set | The checks and configuration the judge depends on. Adding to it during a run is allowed. Modifying or deleting it is not. |
| Holdout check | A check the agent never sees. It lives outside the agent's reach and its output is never shown to the agent. |
| Integrity monitor | A separate model that reads the run's transcript and reports whether the agent gamed the checks. |
| Gate | An action that always stops for human approval: destructive, irreversible, production or shared-environment changes. |
| Run record | One structured line per verdict plus one summary line per run. |

## When to use

- The work has an outcome a tool or a third party can check.
- The agent runs unattended across several steps or sessions.
- A wrong "done" would cost more than the run itself.

Use [`review-convergence-loop.md`](review-convergence-loop.md) alone when the unit of work is a single artifact that failed a validator. Keep creative or open-ended work at the task level. Outcomes the agent can't check turn into confident guesses.

## Core invariants

1. The judge is fixed before the first change. The command, its configuration and its thresholds are recorded with a checksum. A changed judge voids the run.
2. The producer never grades its own work. This restates invariant 1 of the convergence loop.
3. Judges are chosen in a fixed order. A deterministic tool first. Then a check against primary sources. Then a judge on a different model from the producer. A same-model judge comes last and its verdict is marked weak, because models rate output that reads like their own more highly.
4. The protected set can grow but can't shrink or change. Modifying or deleting a protected file fails the run, including changes the agent committed.
5. A pass needs fresh evidence from this run. A sub-agent's report of success is a claim. Verify it.
6. Fix loops are bounded at 3. This is invariant 7 of the convergence loop, unchanged.
7. Gates hold at every level of autonomy. No stage, setting or verdict lets an agent skip a gate.
8. Every verdict is recorded. That includes fails, voids and runs that gave up.

## Stages

Stages 1, 2, 3, 5 and 6 run on every task. Stage 4 runs only on critical work, because it costs several times a single agent. The agent records the size it chose and why.

### Stage 1: size the task

Classify the task as routine, important or critical, and record the classification.

### Stage 2: set the outcome

- Write the outcome in one sentence: what the task is for.
- Write a success signal a tool or third party can check.
- List the access the outcome needs: logs, repositories, environments, data. If something is missing, record the gap and work at the highest level the available access supports.
- Lock the judge and record the protected set before any change. For a numeric signal, measure the baseline now.

### Stage 3: plan like an expert

Answer four questions before the work starts:

1. What would a top professional in this field do here that the request does not ask for?
2. What is the rawest material they would start from?
3. Which methods and tools would they use?
4. What, other than the requester or the producer, would show the result is right?

Rewrite the task to ask for exactly that. A rewrite that changes only vocabulary doesn't count. It has to change inputs, methods, tools or the check. Set a stretch target: a specific numeric goal past what was asked. If it proves out of reach, record the best result and the blocker.

### Stage 4: widen the view (critical only)

- Restate the deliverable as a verb: what it has to make someone believe, decide or do.
- Assemble 2 to 4 roles from fields that serve that verb, chosen to disagree, plus a red team that argues the plan is wrong and a reviewer that argues it is too big.
- When a single proposal is under review, add one role that argues for its most ambitious version.
- Give every role the same facts, an objective, an output format and boundaries. Roles work independently before they see each other's output.
- Split execution across agents only for parts that are independent. Work with shared state stays with one agent and the other roles critique it.
- A unanimous verdict from same-model roles is one model agreeing with itself. It shapes the plan. Only the judge decides whether the work passes.

### Stage 5: execute and judge

- Do the work, then run the judge.
- On FAIL, run Pattern A of [`review-convergence-loop.md`](review-convergence-loop.md) with the judge's findings as the correction constraint set.
- On staleness, and before any escalation, return to stage 2. Check that the outcome and approach are still right, and name one approach not yet tried. A switch is recorded.

### Stage 6: record

Write the run summary to the run record (see below).

## Integrity controls

Agents that run against a judge sometimes raise the score instead of doing the work: editing the tests, hard-coding expected values, special-casing the visible inputs or exiting early with a success code. These controls detect that.

| Control | Detects | Action |
|---------|---------|--------|
| Judge lock | Any edit to the judge after the run starts | Void the run and escalate |
| Protected set diff against the run's starting commit | Checks modified, deleted or renamed, committed or not | FAIL with the file list |
| Holdout check | Fixes fitted to the visible checks only | FAIL with a generic message that never reveals the holdout |
| Integrity monitor | Gaming visible in the transcript | FAIL with the monitor's evidence. An unavailable monitor counts as FAIL. |
| Score-jump review | A large sudden improvement | Inspect the diff for gaming before the result is accepted |

Two detection methods catch different cases, so run more than one when the stakes justify it.

All five controls detect tampering. None of them prevents it. An agent with write access to the judge or the holdout can still change them. To prevent tampering, place the judge and the holdout where the agent has no write access, such as a CI job or an operating-system sandbox.

## Optimization variant

When the success signal is a number and the goal is to improve it:

- Measure a baseline before any change.
- Make one change at a time. Keep it only if the score improves. Revert it otherwise.
- An equal score with less code or complexity counts as an improvement. A tiny gain that adds a lot of complexity does not.
- Stop at the target, at the budget set for the run or after 3 attempts in a row with no improvement.

This variant is not a convergence loop. No attempt corrects a failed one, and each is judged on its own. Its budget is set per run and recorded.

## Stopping rules

| Condition | Detection | Action |
|-----------|-----------|--------|
| Converged | Judge, protected set, holdout and monitor all pass | Proceed to human freeze where the artifact requires it |
| Max iterations | 3 fix cycles without a pass | Escalate |
| Staleness or oscillation | As defined in the convergence loop | Escalate |
| Void | Judge lock mismatch | Escalate. The run starts over with a new lock. |
| Gate reached | The next action is destructive, irreversible or touches production | Stop for approval |
| Wrong outcome | The stage 2 check finds the outcome or signal was wrong | Escalate with the evidence |

## Run record

One line per verdict:

- timestamp, session, project, round, result (`pass`, `fail`, `void`, `gave-up`), reason, judge checksum, starting commit

One line per run:

- task summary, size, stages run, judge type (`tool`, `source`, `other-model`, `weak`), rounds, final result, stretch target met or not, up to three notes on what slowed or failed the run

Plain structured lines (one JSON object per line) in a local file are enough. Ship that file to whatever log platform the environment already has. The record is the audit trail, and it is the input for improving the loop itself.

### Improving the loop

Changes to the loop's own instructions follow the optimization variant. Each change is scored against a fixed set of tasks with runnable judges, with about 30% of the tasks held out. A change is kept only if the main score rises and the held-out score doesn't fall. A human approves the task set once and it is never edited during tuning.

The tuner may never weaken the invariants, the gates, the integrity controls or the iteration limit.

## Anti-patterns

| Anti-pattern | Why it fails |
|-------------|-------------|
| Writing the judge after the work | The judge measures what was built instead of what was needed |
| Letting the agent fix the tests | The score rises and the outcome doesn't move |
| Showing holdout output to the agent | The holdout becomes one more visible test to fit fixes to |
| A same-model judge as the only judge | It favors output that reads like its own |
| Treating a sub-agent's "done" as a pass | A claim isn't evidence |
| Running wide review on every task | It costs several times a single agent and buys nothing on routine work |
| Splitting tightly coupled work across agents | The parts don't fit back together |
| Raising the iteration limit to get a pass | Hides a stale or oscillating loop |
| Outcomes no one can check | The agent reports confidence instead of results |

## Relationship to other documents

| Document | Relationship |
|----------|-------------|
| [`review-convergence-loop.md`](review-convergence-loop.md) | Stage 5 runs Pattern A for every FAIL. Its invariants, stopping rules and iteration ledger apply unchanged. |
| [`judge-calibration.md`](judge-calibration.md) | An unattended run trusts its judge. LLM-backed judges used here need the calibration that document defines. |
| [`philosophy.md`](philosophy.md) §5 | Validators are hard gates. The judge here follows the same rule. |
| [`governance-model.md`](../governance-model.md) §13 | Process invariant 8a bounds correction loops. This pattern keeps that bound. |
| [`sub-agent-orchestration.md`](sub-agent-orchestration.md) | Stage 4 roles are sub-agents and follow its orchestration rules. |
| [`escalation-protocols.md`](escalation-protocols.md) | Escalations from this pattern use those protocols. |
