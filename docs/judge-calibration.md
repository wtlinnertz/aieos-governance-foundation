# Judge Calibration (FR-014)

Who validates the validator? Every freeze gate in AIEOS is enforced by an
LLM-backed judge, and the 2026-07-15 dogfood run produced receipts (G-9)
that the judge can be wrong in both directions: it failed an artifact for
a requirement the spec explicitly exempts, and it returned opposite
verdicts on identical input in back-to-back runs. Calibration is the
governance answer: measure each judge against a human-labeled gold set,
and let nothing unattended trust an unmeasured judge.

## The two design moves

1. **Calibrate at the gate level, not the artifact level.** Validators
   return a per-gate verdict map. A 12-case gold set against a 14-gate
   validator yields roughly 168 labeled gate verdicts -- real statistical
   power from a small labeling investment, and a single-gate flip (the
   G-9 failure shape) is caught directly instead of blurred into an
   artifact score.
2. **The CI path is deterministic; only the calibration run costs
   money.** A `calibration.lock` at kit root pins each validator to the
   judge identity it was measured under (`prompt_sha256`, `model`).
   Per-push CI compares hashes -- no LLM call, no judge judging the
   judge. The paid gold-set run happens only on three triggers: judge
   model change, validator prompt change, schedule.

## Contracts (defined once, in aieos-schema)

- `schema/gold-case.yaml` -- one human-labeled case. Labels are per hard
  gate; input content is a pinned fixture (sha256, LF-normalized). Gold
  labels are human-assigned or copied from frozen higher-tier references,
  never judge-generated. Activation floor: 12 cases per validator,
  balanced PASS/FAIL, at least 2 spec-exemption-adherence cases.
- `schema/calibration-report.yaml` -- the evidence record of one run,
  committed beside the gold set. Carries the per-role thresholds and the
  fixed 3-runs-per-case constant that implementations read.
- `schema/calibration-lock.yaml` -- the deterministic CI contract.

## Scoring is asymmetric by design

The dangerous direction is the lenient judge: a false PASS becomes a
frozen artifact contaminating everything downstream. For freeze-gating
validators the hard gates are **zero false-PASS on gold-FAIL cases** and
**stability** (three runs on byte-identical input at temperature 0; any
gate flip is a calibration FAIL regardless of aggregate score). Gate
agreement must reach 0.9 for freeze-gate roles, 0.75 for advisory
(lens) roles, which carry no false-PASS bar. Cohen's kappa is computed
and stored as the drift-trend metric; no verdict logic reads it.

## Growing gold sets: the accretion rule

Every disputed verdict in a real run becomes a gold case -- the
regression-test discipline applied to judges. Whoever changes a
validator's spec relabels the affected gold cases in the same PR;
enforcement is free because the spec change alters the prompt, the
prompt sha diverges from the lock, and CI reports stale until
recalibration.

## Enforcement surfaces

| Surface | Check | Cost |
|---------|-------|------|
| Kit CI (`kit-ci.yml` -> `scripts/check-calibration-lock.py`) | Prompt-sha half of staleness; no-op for kits without a lock (adoption is per-validator) | Zero LLM calls |
| `harness calibrate --check-only` | Both halves (prompt sha + model) against harness config | Zero LLM calls |
| `harness calibrate` | Full gold-set run; writes the report always, the lock only on PASS | ~36 judge calls per validator (12 cases x 3 runs) |
| Dark-factory conductor (slice 4, planned) | Refuses an UNATTENDED walk if any validator on the path has a stale or failing lock; attended runs warn | Zero LLM calls |

The conductor row is what makes "FR-014 keeps a human at every promotion
gate" mechanical rather than aspirational, and it defines how unattended
promotion becomes trustable: per-validator, as calibration coverage
arrives.

## Tier 3 test category

Calibration runs are Tier 3 (agent-dependent, on-trigger, never
per-push), alongside A5 agent integration tests. See
`docs/healthcheck-playbook.md` section A6 for triggers, commands, and
remediation.

## Known v1 limitations

- Calibration requests carry the artifact and spec only
  (`upstream_artifacts` is empty), so gold labels are context-relative:
  they assert what a correct strict judge should conclude given the
  artifact and spec alone. Validators whose prompts request upstream
  documents (PRD, ACF) are judged without them during calibration. If
  this materially distorts a gate, the v2 path is upstream fixture
  references in the gold-case schema.
- Kit CI checks the prompt half of staleness only; the model half
  requires harness config and is enforced by `--check-only` and the
  conductor precondition.
- Distilled-judge cost guidance is documented, not enforced (no
  distilled-judge sourcing exists yet).

## References

- Roadmap FR-014; build spec and slice plan in the operator's vault
- G-9 / G-10 in the v1.3 interoperability gap register
- `aieos-agent-harness/src/calibration.py` (engine),
  `harness calibrate` (CLI)
