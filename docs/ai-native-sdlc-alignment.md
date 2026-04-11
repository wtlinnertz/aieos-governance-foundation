# AIEOS Alignment Assessment: AI-Native SDLC Framework v3.1

Version: v1.0
Assessment Date: 2026-03-24
Source Document: AI-Native SDLC: Principles, Patterns & Practices v3.1 (Todd, curated with Claude)
AIEOS Version: As of 2026-03-24 (16 layers, 15 built kits, roadmap.md last updated 2026-03-21)

---

## Executive Summary

AIEOS demonstrates **strong structural alignment** with the AI-Native SDLC Framework v3.1. Of 328 scored items, 92% are Fully Embodied or Partially Aligned. The 21 gaps identified are concentrated in **LLMOps observability**, **AI adoption measurement**, and **operational AI practices** — areas where AIEOS governs the artifact lifecycle but doesn't yet extend to AI pipeline operations. The framework's core architecture (four-file system, freeze-before-promote, validator-as-judge, convergence loops) directly embodies the document's most foundational principles.

**Overall Alignment:**

| Cluster | Items | FE | PA | GAP | N/A | FE% (excl. N/A) |
|---------|-------|----|----|-----|-----|-----------------|
| Principles (P1-P158) | 153 | 58 | 63 | 8 | 24 | 45% |
| Patterns (PA1-PA48) | 69 | 23 | 36 | 0 | 10 | 39% |
| Practices (PR1-PR98) | 106 | 27 | 44 | 13 | 22 | 32% |
| **Total** | **328** | **108** | **143** | **21** | **56** | **40%** |

FE+PA combined (excl. N/A): **92%** (251 of 272 applicable items)

**Top 5 Strengths:**
1. **Specification & Planning** (P1-P3, PA1-PA3a-ext) — AIEOS IS spec-driven development. The four-file system, artifact hierarchy, and five specification primitives are direct structural embodiments. 12/12 items FE.
2. **Anti-Slop Engineering** (P67-P71, PA28-PA34) — Convergence loops ("re-generate, don't patch"), freeze-before-promote ("clean input begets clean output"), and validators-as-hooks score 10 FE across these sections.
3. **Rejection & Taste Scaling** (P72-P75) — Validators are institutionalized rejection with three dimensions (recognition via hard gates, articulation via blocking_issues, encoding via specs). 3/4 FE.
4. **Human Oversight Architecture** (P12-P16, PA8-PA8b) — AIEOS is a HITL framework: freeze-as-human-decision, six-layer HITL architecture, governance-proportional-to-risk. 8/10 FE.
5. **The Four-Layer Prompting Stack** (P80-P84) — AIEOS's architecture maps directly to all four prompting disciplines: prompt craft (governed prompts), context engineering (briefing distillation), intent engineering (principles files), specification engineering (the spec system). 4/5 FE.

**Top 5 Gaps:**
1. **AI pipeline observability & LLMOps** (P114-P117, PR61-PR63) — No governance of LLM call tracing, prompt regression, or cost anomaly alerting. 4 GAPs.
2. **AI adoption quality measurement** (P120, PR6a, PR6c, PR65) — No DORA baselines, adoption quality metrics, or quarterly reviews. 4 GAPs.
3. **Data privacy in AI context** (P106, PR78) — No governance of GDPR data minimization in agent context or context snapshots for SOX audit. Already on roadmap as GAP-002.
4. **Constraint library as queryable asset** (PR32, PR34) — Specs serve as distributed constraints but no queryable library or MCP-served rejection patterns. 2 GAPs.
5. **Review capacity management** (P156, PR85, PR86) — No governance of senior engineer review burden or review rotation. 3 GAPs.

**Roadmap Additions Proposed:** 6 new items (FR-014 through FR-019), 4 existing items validated

---

## Scoring Scale

| Score | Label | Definition |
|-------|-------|-----------|
| **FE** | Fully Embodied | AIEOS addresses this through framework design, governed specs/validators, or demonstrated practice (aieos-console). Concrete, citable evidence. |
| **PA** | Partially Aligned | AIEOS addresses the spirit but incompletely — advisory not enforced, some aspects only, or mechanism exists but thin. |
| **GAP** | Gap | AIEOS does not address this, and it's relevant to AIEOS's domain. Actionable roadmap finding. |
| **N/A** | Not Applicable | Outside AIEOS scope (runtime infrastructure, commercial pricing, etc.) OR addressed by consuming projects not the framework. |

**Evidence Channels:** FD = Framework Design, GS = Governance Spec, PF = Principles File, WE = Worked Example, CT = Cross-cutting Tool, RP = Roadmap/Planned, NA = Not Addressed.

**Bias Acknowledgment:** AIEOS was built by the assessor. Conservative scoring applied: PA preferred over FE when evidence is circumstantial; GAP preferred over N/A when AIEOS could reasonably address the concern. FE requires a citable file path — "implied by design" is insufficient.

---

## Part 1: Principles

### 1.1 — Specification & Intent (P1-P3)

| ID | Name | Score | Ch. | Rationale | AIEOS Reference |
|----|------|-------|-----|-----------|-----------------|
| P1 | Spec First, Code Second | **FE** | FD, GS | AIEOS's entire architecture treats specs as first-class versioned artifacts that drive implementation. Every artifact type starts with a spec file that governs generation. The four-file system (spec → template → prompt → validator) makes specs the entry point for all work. | `governance-model.md` §Four-File System; `philosophy.md` §Explicit Over Implicit |
| P2 | Humans Must Think Rigorously for Agents to Work Well | **FE** | FD, PF | AIEOS requires disciplined specification before AI generation. Elicitation protocol mandates pre-generation reasoning. Context graphs are explicit (navigation map with ~70 nodes, ~140 edges). Hierarchy is clean (layer model, kit structure standard). | `elicitation-protocol.md`; `navigation-map.md`; `philosophy.md` §Structure Enables Speed |
| P3 | Context Engineering Supersedes Prompt Engineering | **FE** | FD, CT | AIEOS manages both deterministic context (specs, frozen upstream artifacts, principles files, templates) and probabilistic context (sherpa's artifact store queries, cross-initiative scans). Briefing distillation compresses frozen artifacts for downstream prompt consumption. CLAUDE.md per kit provides managed context. | `briefing-distillation-spec.md`; sherpa Phase 3 steps 3-5; kit CLAUDE.md files |

**Section Summary:** 3 FE / 0 PA / 0 GAP / 0 N/A. AIEOS's foundational architecture directly embodies specification-first, rigorous thinking, and context engineering.

### 1.2 — Simplicity & Architecture (P4-P6)

| ID | Name | Score | Ch. | Rationale | AIEOS Reference |
|----|------|-------|-----|-----------|-----------------|
| P4 | Ancient Engineering Principles Still Apply | **FE** | FD, PF | AIEOS explicitly builds on decades-old engineering: separation of concerns (four-file), immutability (freeze semantics), single source of truth (specs), interface contracts (governance model). Philosophy doc anchors in established SE practices. | `philosophy.md` §Structure Enables Speed; `code-craftsmanship.md` §1.8 Dependency Direction |
| P5 | Simple Scales Better Than Complex | **FE** | FD | AIEOS favors simplicity: Markdown-only artifacts, no compilation, no package manager. Sequential-default/parallel-optional flows. Each kit is independent. No orchestration framework — just files, specs, and a governance model as the interface contract. | `philosophy.md` §Independent Kits; `flow-reference.md` §4 Parallelism Rules |
| P6 | Deterministic Where It Matters, Non-Deterministic Where It Helps | **FE** | FD, GS | AIEOS makes validation deterministic (hard gates with PASS/FAIL, standardized JSON output) while allowing AI judgment in generation (prompts guide, don't constrain). CI pipeline (check-structure.sh, pytest) is deterministic. Generation is non-deterministic by design. | `governance-model.md` §Validator Output Format; `healthcheck-playbook.md` Tier 1-2 |

**Section Summary:** 3 FE / 0 PA / 0 GAP / 0 N/A. AIEOS's design philosophy directly reflects simplicity, durability, and appropriate determinism.

### 1.3 — Data & Environment (P7-P8)

| ID | Name | Score | Ch. | Rationale | AIEOS Reference |
|----|------|-------|-----|-----------|-----------------|
| P7 | Data Dominates — Fix the Environment, Not the Agent | **FE** | FD, PF | AIEOS's core thesis: fix the specs, templates, and principles — the environment — not the AI model. When artifacts fail validation, the correction loop fixes inputs (spec constraints, upstream frozen artifacts) not the model. Philosophy doc states this explicitly. | `philosophy.md` §Structure Enables Speed; `review-convergence-loop.md` §Correction Session |
| P8 | Deep Codebase Understanding Is the Foundation | **PA** | GS, CT | AIEOS governs codebase understanding through SAD (architecture documentation), TDD (technical design), and artifact store (cross-initiative indexing). However, AIEOS doesn't govern how AI tools achieve codebase awareness at runtime (embedding models, indexed repos). It governs the documentation artifacts, not the tooling. | `sad-spec.md`; `tdd-spec.md`; `aieos-artifact-store` (ECO-003) |

**Section Summary:** 1 FE / 1 PA / 0 GAP / 0 N/A.

### 1.4 — Measurement & Uncertainty (P9-P11)

| ID | Name | Score | Ch. | Rationale | AIEOS Reference |
|----|------|-------|-----|-----------|-----------------|
| P9 | Measure Before You Optimize | **PA** | GS, WE | AIEOS governs measurement through RRK (SLOs, baselines in SRP), QAK (test coverage in TCR), and validator completeness scores. However, AIEOS doesn't explicitly require pre-optimization baselines for AI pipeline performance (latency, response quality, golden test sets for LLM behavior). It measures artifact quality, not AI tool performance. | `srer-spec.md` (SLO baselines); `tcr-spec.md` (test coverage); `qgr-spec.md` |
| P10 | Bounded Uncertainty Is an Engineering Discipline | **FE** | FD, GS | AIEOS's validator design is explicitly built for bounded uncertainty: completeness scores (0-100) define acceptable ranges, not exact outputs. Hard gates define what must be true; warnings capture uncertainty. The convergence loop bounds correction attempts (max 3). | `governance-model.md` §Validator Output; `review-convergence-loop.md` §Stopping Rules |
| P11 | AI Accelerates WIP, Not Necessarily Throughput | **PA** | GS | AIEOS governs downstream quality gates (QAK, PRK, REK) that prevent AI-generated artifacts from overwhelming validation. Freeze-before-promote ensures throughput can't outrun validation. But AIEOS doesn't explicitly track WIP metrics or address Little's Law dynamics. | `flow-reference.md` §10 Flow Validation Rules; QAK playbook |

**Section Summary:** 1 FE / 2 PA / 0 GAP / 0 N/A.

### 1.5 — Human Oversight & Governance (P12-P16)

| ID | Name | Score | Ch. | Rationale | AIEOS Reference |
|----|------|-------|-----|-----------|-----------------|
| P12 | Human-in-the-Loop Is Non-Negotiable — But It's a Spectrum | **FE** | FD, GS | AIEOS explicitly designs HITL as a spectrum: AI generates → validator judges → human freezes (approval gate). Convergence loops allow bounded autonomy (3 iterations) before human escalation. Every freeze is a human decision. The philosophy doc states "AI-Native, Not AI-Replaced." | `philosophy.md` §AI-Native, Not AI-Replaced; `review-convergence-loop.md` §Escalation |
| P13 | Humans Contribute at Three Distinct Points | **PA** | FD | AIEOS addresses runtime oversight (freeze gates, validation) and tuning (principles files shape AI behavior). Training-time contribution is outside AIEOS scope (AIEOS doesn't govern model training). Two of three points are well-covered. | `governance-model.md` §Freeze Semantics; principles files per kit |
| P14 | Agents Optimize Away Non-Negotiables Unless You Define Them Explicitly | **FE** | FD, GS | AIEOS's spec system explicitly defines non-negotiables as hard gates. Validators enforce them structurally (FAIL on any hard gate failure). Prompts reference specs for constraints. The four-file separation prevents prompts from quietly dropping rules. | `governance-model.md` §Kit Invariants; every `*-spec.md` with named hard gates |
| P15 | The Bottleneck Shifts from Generation to Validation | **FE** | FD, GS | AIEOS's entire architecture reflects this: generation is one step, but validation (validators), peer review (PRK 12 lenses), quality assurance (QAK), and freeze approval are the bulk of the process. The framework invests more structure in validation than generation. | QAK kit; PRK kit (12 lenses); validator pattern; `review-convergence-loop.md` |
| P16 | Customization Over One-Size-Fits-All Agents | **FE** | FD | AIEOS's kit architecture is inherently customizable: each kit is independent, principles files are per-organization, tool bindings absorb environment specifics, initiative presets define 5 different flows. The adapter conformance spec enables different tool integrations per team. | `initiative-presets.md` (5 paths); `adapter-conformance-spec.md`; `philosophy.md` §Adapt the Edges |

**Section Summary:** 4 FE / 1 PA / 0 GAP / 0 N/A. Strong alignment — AIEOS is fundamentally a human oversight and governance framework.

### 1.6 — Architecture & Durability (P17-P22)

| ID | Name | Score | Ch. | Rationale | AIEOS Reference |
|----|------|-------|-----|-----------|-----------------|
| P17 | Architecture Is Portable, Tools Are Not | **FE** | FD | AIEOS's explicit design principle: tool-agnostic policy. Specs define patterns, bindings map to tools, adapters implement. The three-layer model (spec → binding → adapter) makes architecture portable. AI transparency principles require AI-portable artifacts. | `philosophy.md` §Tool-Agnostic Policy; `adapter-conformance-spec.md`; `ai-transparency-principles.md` §Provider Neutrality |
| P18 | Bet on Foundations with Staying Power (Lindy Effect) | **FE** | FD | AIEOS is built entirely on Markdown files, directories, and text — technologies from the 1970s-1990s. No database, no framework, no compilation. The governance model is a text document. Tests use bash and pytest. The sherpa's navigation map is a markdown file. | Repository structure; `philosophy.md` §Adapt the Edges |
| P19 | Principles Beat Rules for Agent Guidance | **FE** | FD, PF | AIEOS explicitly separates principles (philosophy docs per kit) from rules (specs). Principles files provide guidance that adapts to context ("Readability Over Cleverness"). Specs provide hard rules for validation. Both are governed but serve different purposes. | `philosophy.md` §Principles vs Specs distinction; `code-craftsmanship.md`; kit principles files |
| P20 | Technical Skills Amplify in the AI Era | **PA** | PF | AIEOS doesn't directly address skill amplification as a concept, but the framework's design requires deep technical understanding to write specs, principles, and evaluate validator output. The worked example (aieos-console) demonstrated that framework knowledge amplifies AI output quality. | Implicit in framework design; `aieos-console` as demonstration |
| P21 | Design Systems for Both Human and Agent Navigation | **FE** | FD, CT | AIEOS explicitly designs for dual navigation: humans use playbooks and getting-started guides; AI agents use the navigation map, decision tables, and machine-readable state blocks in ERs. Both use the same underlying Markdown files. Sherpa is the AI navigator; playbook is the human navigator. | `navigation-map.md`; `getting-started.md`; ER §1b State Block; sherpa-prompt.md |
| P22 | If the Agent Builds It, the Agent Can Maintain It | **FE** | FD, WE | AIEOS preserves conversation context through Engagement Records, Sherpa Journals, and frozen artifacts. The aieos-console initiative demonstrated this: the ER tracks all decisions, the journal records rationale, and any AI can resume by reading the ER and journal. Session resumption is a core sherpa capability. | `engagement-record-spec.md`; sherpa journal; sherpa session resumption protocol |

**Section Summary:** 5 FE / 1 PA / 0 GAP / 0 N/A. Architecture and durability is a core AIEOS strength.

### 1.7 — Change Management & Adoption (P23-P34)

| ID | Name | Score | Ch. | Rationale | AIEOS Reference |
|----|------|-------|-----|-----------|-----------------|
| P23 | Don't Sell AI as New — Anchor in What Engineers Already Know | **FE** | FD, PF | AIEOS explicitly anchors in established SE practices: separation of concerns, immutability, single source of truth, interface contracts. Philosophy doc states "ancient data engineering practices applied in new ways" is the thesis. | `philosophy.md` §Structure Enables Speed |
| P24 | The Human Throttle Is the Real Bottleneck | **PA** | FD | AIEOS builds decision infrastructure (audit logs via ER/journal, reversible processes via re-entry protocol, sandbox via convergence loops) that enables appropriate autonomy. But AIEOS doesn't explicitly address organizational inertia or trust-building mechanisms. | `review-convergence-loop.md`; `flow-reference.md` §6 Re-Entry |
| P25 | AI Is a Management Skill, Not a Tool Skill | **PA** | PF | AIEOS's design implicitly requires management skills (task decomposition in WDD, quality judgment in validators, iterative refinement in convergence loops). But AIEOS doesn't explicitly frame AI as a management discipline or provide training/adoption guidance. | WDD task decomposition; validator judgment pattern |
| P26 | The Training Market Has Skipped the Middle (The 201 Gap) | **N/A** | NA | AIEOS is a governance framework, not a training program. The getting-started guide and playbooks provide some 201-level guidance on applied judgment, but addressing the broader training gap is outside AIEOS scope. | `getting-started.md`; kit playbooks |
| P27 | AI Is Jagged — the 201 Skill Is Knowing Where the Frontier Is | **PA** | GS | AIEOS's validator pattern enforces frontier recognition: validators catch where AI output falls outside acceptable ranges. The convergence loop's stopping rules (staleness, oscillation) detect when AI is outside its capability frontier. But this is structural, not a skill-building mechanism. | `review-convergence-loop.md` §Stopping Rules; validator FAIL as frontier signal |
| P28 | The Apprenticeship Model Is Collapsing | **N/A** | NA | Workforce development is outside AIEOS's governance scope. AIEOS's constraint library equivalent (specs + principles) could partially address this by encoding senior judgment, but AIEOS doesn't explicitly target junior development pathways. | — |
| P29 | The Right Question Is "What's Now Possible?" | **N/A** | NA | Strategic framing of AI investment is outside AIEOS's governance scope. SDK (Layer 1) addresses strategic direction but not this specific reframing question. | — |
| P30 | Execution Cost Dropped 10-100x | **N/A** | NA | Economic observation about AI cost dynamics. Outside AIEOS governance scope. | — |
| P31 | Every Company Is Now a Platform | **N/A** | NA | Strategic observation about platform dynamics. Outside AIEOS governance scope, though PINFK governs infrastructure decisions. | — |
| P32 | All Knowledge Work Roles Are Converging | **N/A** | NA | Workforce evolution observation. Outside AIEOS scope. | — |
| P33 | Software-Shaped Intent Is the Missing Skill for Non-Engineers | **PA** | CT | AIEOS's sherpa system enables non-engineers to navigate the framework through conversational guidance. The sherpa translates plain language to framework concepts (intent resolution). But AIEOS doesn't explicitly teach "software-shaped intent" as a skill. | Sherpa Phase 1 (intent resolution); sherpa ideation mode |
| P34 | Expertise Depreciates Unless Continuously Updated | **N/A** | NA | Observation about expertise half-life. Outside AIEOS governance scope. | — |

**Section Summary:** 2 FE / 4 PA / 0 GAP / 6 N/A. Many items in this section are strategic/workforce observations outside AIEOS's governance domain.

### 1.8 — Cognitive Architecture & Builder Mindset (P35-P39)

| ID | Name | Score | Ch. | Rationale | AIEOS Reference |
|----|------|-------|-----|-----------|-----------------|
| P35 | The Bottleneck Has Shifted from Capability to Systems Thinking | **PA** | FD | AIEOS's layer model and navigation map embody systems thinking (16 layers, cross-cutting dependencies, flow permutations). But AIEOS doesn't explicitly address cognitive architecture or altitude-shifting as practitioner skills. | `layer-model.md`; `navigation-map.md`; `flow-reference.md` |
| P36 | Adopt the Engineering Manager Mindset | **PA** | FD | AIEOS's structure mirrors EM responsibilities: defining guardrails (specs), endpoints (freeze criteria), missions (initiative presets), and definitions of done (hard gates). But this is structural, not an explicit teaching of the EM mindset. | Spec hard gates as "definition of done"; initiative presets as "missions" |
| P37 | Develop Strategic Deep-Diving — Fluid Altitude Changes | **PA** | CT | Sherpa's health monitoring (position checks at freeze #3, #6, #9, #12) and cross-artifact consistency checks enable altitude changes. But AIEOS doesn't explicitly coach practitioners on when to dive deep vs. stay high. | Sherpa position checks; cross-artifact consistency checks |
| P38 | Experience Is Not Compressible | **PA** | FD | AIEOS preserves experiential loops through IEK (feedback back to discovery), ER key decisions, and sherpa journal rationale replay. But AIEOS doesn't explicitly address the tension between AI speed and human understanding depth. | IEK Layer 7 feedback loop; ER key decisions; sherpa journal |
| P39 | Two Architectures: Technical Patterns vs Taste | **FE** | FD, GS | AIEOS explicitly separates these: specs/validators enforce technical patterns (delegatable to AI), while principles files and PRK peer review embody taste (human judgment). PRK's 12 specialized lenses are explicitly about human expert judgment, not AI automation. | PRK kit (12 lenses); principles files; `philosophy.md` §AI-Native, Not AI-Replaced |

**Section Summary:** 1 FE / 4 PA / 0 GAP / 0 N/A.

### 1.8a — The Five Levels & The Dark Factory (P40-P43)

| ID | Name | Score | Ch. | Rationale | AIEOS Reference |
|----|------|-------|-----|-----------|-----------------|
| P40 | The Five Levels of AI-Assisted Development | **PA** | FD | AIEOS operates primarily at Level 2-3 (AI handles multi-file artifact generation, human reviews at freeze level). The sherpa approaches Level 4 (spec in → artifacts out → human checks). AIEOS doesn't explicitly map to or reference this framework. | Sherpa as Level 3-4 operation; freeze gates as human review |
| P41 | The J-Curve Is Real | **N/A** | NA | Empirical observation about adoption speed. Outside AIEOS governance scope. | — |
| P42 | The Bottleneck Has Moved to Spec Quality | **FE** | FD, GS | AIEOS's entire architecture validates this: the four-file system invests most heavily in spec quality. Spec versioning standard, hard gates per spec, failure examples, and the spec-file-standard all prioritize specification quality as the key input. | `spec-file-standard.md`; every `*-spec.md`; `philosophy.md` §Explicit Over Implicit |
| P43 | Most Enterprise Software Is Brownfield | **PA** | RP | AIEOS doesn't have a dedicated brownfield/legacy governance pattern. The roadmap doesn't address this explicitly. However, EEK Path B (enhancement) and ODK (incident-triggered fixes) handle brownfield scenarios indirectly. | `initiative-presets.md` P2 (Enhancement), P4 (Performance Fix); `flow-reference.md` §2 |

**Section Summary:** 1 FE / 2 PA / 0 GAP / 1 N/A.

### 1.8b — Agent Strategy (P44-P46)

| ID | Name | Score | Ch. | Rationale | AIEOS Reference |
|----|------|-------|-----|-----------|-----------------|
| P44 | Agentic Trust Delegation Is the Core Strategic Decision | **PA** | FD | AIEOS's adapter conformance spec addresses trust delegation at the integration layer (where agents run, how they authenticate, what they can access). But AIEOS doesn't govern the strategic decision of where on the trust spectrum to sit for agent product selection. | `adapter-conformance-spec.md` §auth_externalized; `ai-transparency-principles.md` §Provider Neutrality |
| P45 | Relentless Simplification — Agents Compress the Interface Layer | **N/A** | NA | Product strategy observation about agent market dynamics. Outside AIEOS governance scope. | — |
| P46 | Category-Defining Products Set the Axes of Competition | **N/A** | NA | Market dynamics observation. Outside AIEOS governance scope. | — |

**Section Summary:** 0 FE / 1 PA / 0 GAP / 2 N/A.

### 1.9 — Agent Security (P47-P55)

| ID | Name | Score | Ch. | Rationale | AIEOS Reference |
|----|------|-------|-----|-----------|-----------------|
| P47 | Autonomy Combined with Weak Guardrails Is the Core Risk | **FE** | FD, GS | AIEOS's design thesis: strong guardrails (specs as hard gates, validators as enforcement, freeze as human approval) combined with bounded autonomy (convergence loops capped at 3, escalation to humans). SCK's Threat Model artifact explicitly addresses agent-related security surfaces. | `governance-model.md`; `review-convergence-loop.md`; SCK `tm-spec.md` |
| P48 | Avoid Super-Agency — Design for High Cohesion | **FE** | FD | AIEOS's kit architecture is high-cohesion by design: each kit governs one layer, each artifact type has one spec, each validator judges one thing. No "super-kit" that does everything. Cross-cutting kits are independent and don't block each other. | `layer-model.md` §Kit Independence; `flow-reference.md` §10 Rule 6 |
| P49 | Agents Can't Reliably Distinguish Instructions from Content | **PA** | GS | AIEOS mitigates this structurally: specs (instructions) and artifacts (content) are separate files. Validators consume both but treat specs as authoritative. However, AIEOS doesn't explicitly govern prompt injection defense or content-instruction confusion at runtime. | Four-file separation; SCK TM would cover this for consuming projects |
| P50 | The Agentic Supply Chain Is a Live, Continuously Exploitable Surface | **PA** | GS | SCK's DAR (Dependency Audit Record) governs dependency verification. Adapter conformance spec requires auth externalization and health checks. But AIEOS doesn't govern MCP server verification or dynamic plugin loading security specifically. | SCK `dar-spec.md`; `adapter-conformance-spec.md` |
| P51 | Memory Persistence Makes Poisoning Attacks Durable | **PA** | GS | AIEOS's ER and sherpa journal are append-only (tamper-resistant by design). Frozen artifacts are immutable (modification detected by re-entry protocol). But AIEOS doesn't explicitly govern memory poisoning defense for AI agent memory systems. | ER append-only design; freeze immutability; `ai-transparency-principles.md` §Session State on Disk |
| P52 | The Human Is the Final Execution Path — and the Weakest Link | **FE** | FD | AIEOS addresses this directly: every freeze is a human decision, but validators provide structured evidence (hard gates, blocking issues, completeness score) so humans review against explicit criteria, not just agent summaries. PRK provides multi-lens expert review. | Validator output format; PRK 12 lenses; freeze-as-human-decision |
| P53 | The Paradigm Shift: Deterministic → Probabilistic, Evaluation-First | **FE** | FD | AIEOS is evaluation-first by design: validators exist before artifacts are generated (spec defines what passes, validator enforces it). The framework prioritizes measuring outcomes (hard gates, completeness scores) over implementation details. | Four-file system (validator is first-class); `philosophy.md` §Validators Are Hard Gates |
| P54 | Agents Need Non-Human Identities | **N/A** | NA | Runtime agent identity management is outside AIEOS governance scope. AIEOS governs what artifacts agents produce, not how they authenticate. The adapter conformance spec requires auth externalization but doesn't define identity schemes. | `adapter-conformance-spec.md` §auth_externalized (tangential) |
| P55 | Compromised Agents Are Attack Amplifiers at Machine Speed | **PA** | GS | AIEOS's convergence loop bounds (max 3 iterations) and escalation protocols provide circuit-breaker behavior. SCK TM governs threat modeling. But AIEOS doesn't explicitly govern agent compromise detection or real-time containment at machine speed. | `review-convergence-loop.md` §Max Iterations; SCK `tm-spec.md` |

**Section Summary:** 4 FE / 4 PA / 0 GAP / 1 N/A. Strong structural alignment with security principles through the governance model and SCK.

### 1.10 — The Memory Wall & Contextual Stewardship (P56-P66)

| ID | Name | Score | Ch. | Rationale | AIEOS Reference |
|----|------|-------|-----|-----------|-----------------|
| P56 | The Gap Between Task Capability and Job Capability | **FE** | FD | AIEOS bridges this gap: the Engagement Record tracks multi-month initiative state, the sherpa journal preserves decision context across sessions, and frozen artifacts accumulate institutional knowledge. Session resumption explicitly reconstructs job-level context from task-level artifacts. | ER as cross-session state; sherpa journal; session resumption |
| P57 | The Agent Memory Wall Is Getting Worse | **PA** | FD | AIEOS's architecture mitigates the memory wall through persistent artifacts (frozen, immutable, on disk) rather than in-context memory. But AIEOS doesn't explicitly address long-term memory architecture for AI agents or the degradation problem. | Frozen artifacts as durable memory; ER as persistent state |
| P58 | Contextual Stewardship Is the Senior Human Role | **FE** | FD, PF | AIEOS embodies this: principles files encode senior judgment, specs define what "right" looks like, PRK lenses encode expert perspectives, and the freeze decision is the stewardship moment. The framework makes contextual stewardship a structural role, not an implicit one. | Principles files; PRK 12 lenses; freeze-as-stewardship; `philosophy.md` §AI-Native Not AI-Replaced |
| P59 | Evals Are the Bridge Between Human Judgment and Agent Execution | **FE** | FD, GS | AIEOS's validators ARE evals — they encode human judgment (hard gates) into tests that run on every artifact. The three-tier testing strategy (structural, framework, behavioral) is exactly this pattern. Eval design is a senior activity (spec authors define what passes). | Validator pattern; `healthcheck-playbook.md`; three-tier testing |
| P60 | Writing Code and Maintaining Code Are Different Skills | **PA** | GS | AIEOS governs both creation (generation prompts, specs) and maintenance (IEK feedback loop, RRK health reviews, DKK document health reviews). But the distinction between generation quality and maintenance quality isn't explicitly addressed as different concerns in specs. | IEK Layer 7; RRK RHR; DKK DHR |
| P61 | Context Windows Are Not Memory | **FE** | FD | AIEOS explicitly treats context windows as scratch pads and puts durable state on disk: ER, frozen artifacts, sherpa journal, state block. AI transparency principles require "session state on disk" — context window is convenience, files are system of record. | `ai-transparency-principles.md` §Session State on Disk; ER as persistent state |
| P62 | Memory Is a System, Not a Location | **PA** | FD | AIEOS distributes memory across specialized stores: ER (initiative state), frozen artifacts (decisions), sherpa journal (operational log), artifact store (cross-initiative index), principles files (organizational knowledge). But this isn't explicitly designed as a layered memory architecture — it emerged organically. | ER, frozen artifacts, journal, artifact store, principles — distributed but not architected as "memory system" |
| P63 | Summaries Are Compression Artifacts, Not Memory | **FE** | FD, CT | AIEOS's briefing distillation spec explicitly treats compression as lossy and secondary to canonical frozen artifacts. Distilled briefings reference the source artifact (with hash/ID). The canonical store is always the frozen artifact, never the summary. | `briefing-distillation-spec.md` §fidelity_preserved gate; frozen artifacts as canonical |
| P64 | Automatic Recall Beats Manual Search | **PA** | CT | Sherpa's pre-prompt auto-recall (artifact store queries, cross-initiative scans) removes the decision point before generation. Template pre-population auto-injects upstream context. But this is sherpa-specific, not a framework-level requirement for all AI consumers. | Sherpa Phase 3 steps 3-5; template pre-population |
| P65 | Supersede, Never Delete | **FE** | FD | AIEOS's lifecycle states explicitly include supersession: Deprecated (superseded, retained for audit). Frozen artifacts are immutable — changes create new versions via re-entry protocol, never modify originals. ER is append-only. | `governance-model.md` §Lifecycle States; ER append-only; freeze immutability |
| P66 | Bootstrap Files Are a Per-Call Tax | **PA** | FD | AIEOS's CLAUDE.md files per kit serve as bootstrap files. The kit-structure-standard requires them but doesn't set a token budget. The sherpa skill file is lightweight (17 lines). But there's no explicit governance around bootstrap file size or index-vs-warehouse discipline. | Kit CLAUDE.md files; sherpa skill file |

**Section Summary:** 6 FE / 5 PA / 0 GAP / 0 N/A. Strong alignment on contextual stewardship and memory principles — this is a core AIEOS strength.

### 1.11 — Agentic Code Quality & Anti-Slop (P67-P71)

| ID | Name | Score | Ch. | Rationale | AIEOS Reference |
|----|------|-------|-----|-----------|-----------------|
| P67 | Slop Is an Engineering Problem, Not an LLM Problem | **FE** | FD, PF | AIEOS's entire architecture treats quality failure as an environment problem: fix the spec, fix the principles, fix the upstream artifacts — then regenerate. The convergence loop diagnoses what caused failure, fixes the environment (constraints), and reruns. | `review-convergence-loop.md` §Correction Session; `philosophy.md` §Structure Enables Speed |
| P68 | Never Fix Bad Agent Output — Diagnose, Reset, Rerun | **FE** | FD | AIEOS's convergence loop explicitly follows this pattern: validator identifies failure → correction session re-invokes generation prompt with additional constraints → new artifact generated from scratch (not patched). The loop is "re-generation with additional constraints, not in-place editing." | `review-convergence-loop.md` §Invariant 3: "Correction is re-generation" |
| P69 | Input Token Quality Is Recursive | **FE** | FD | AIEOS's freeze-before-promote rule ensures downstream artifacts receive only validated, high-quality upstream inputs. Each layer inherits clean input from frozen upstream, producing cleaner output that becomes clean input for the next layer. This is the "pit of success" implemented structurally. | `governance-model.md` §Freeze-Before-Promote; `flow-reference.md` §10 |
| P70 | A Focused Agent Is a Correct Agent — One Task, One Prompt | **FE** | FD | AIEOS's prompt design follows this exactly: each artifact type has one dedicated prompt file that generates one artifact type. Validators each judge one artifact type. Session separation ensures generation and validation are distinct, focused tasks. | Four-file system (one prompt per artifact type); session separation invariant |
| P71 | An Isolated Agent Is a Safe Agent | **PA** | FD | AIEOS's session separation (generation and validation must be separate sessions) provides process isolation. But AIEOS doesn't govern per-agent work tree isolation or concurrent agent interference at the runtime level — that's consuming project tooling. | `governance-model.md` §Separate Generation and Validation Sessions |

**Section Summary:** 4 FE / 1 PA / 0 GAP / 0 N/A. Anti-slop is deeply embedded in AIEOS's convergence loop and freeze-before-promote architecture.

### 1.12 — Rejection as Skill & Scaling Taste (P72-P75)

| ID | Name | Score | Ch. | Rationale | AIEOS Reference |
|----|------|-------|-----|-----------|-----------------|
| P72 | Rejection Is the Real AI Skill | **FE** | FD, GS | AIEOS's validators are institutionalized rejection: they encode expert judgment about what "wrong" looks like into hard gates that persist across all future interactions. PRK's 12 lenses encode specialized rejection perspectives. Every validator FAIL is a structured rejection with gate, description, and location. | Validator pattern; PRK 12 lenses; `governance-model.md` §Validator Output |
| P73 | Rejection Has Three Dimensions: Recognition, Articulation, Encoding | **FE** | FD, GS | AIEOS covers all three: Recognition (validator hard gates detect what's wrong), Articulation (blocking_issues field requires gate + description + location), Encoding (hard gates persist in spec files, surviving tool changes and personnel turnover). The finding accumulator captures novel issues for upstream spec improvement. | Validator output schema; sherpa finding accumulator; spec versioning |
| P74 | The Frontier of AI Value = Frontier of Organizational Taste | **FE** | FD, PF | AIEOS's specs and principles files ARE the encoded organizational taste. The more complete and nuanced they are, the more reliable AI output becomes. Hard gates define the quality frontier. Organizations with better specs get better artifacts — exactly this principle. | Specs as encoded taste; principles files; hard gate completeness |
| P75 | Scaling Taste Is the Largest Structural Gap | **PA** | FD | AIEOS's spec + validator pattern is a taste-scaling mechanism (encoded judgment accessible to all). But AIEOS doesn't have a dedicated constraint library pattern or systematic rejection capture workflow. Rejection knowledge lives in specs, not in a queryable library. | Specs as partial constraint library; no dedicated rejection capture workflow |

**Section Summary:** 3 FE / 1 PA / 0 GAP / 0 N/A. AIEOS's validator pattern is a strong embodiment of institutionalized rejection.

### 1.13 — Architecture, Community & Build Patterns (P76-P79)

| ID | Name | Score | Ch. | Rationale | AIEOS Reference |
|----|------|-------|-----|-----------|-----------------|
| P76 | Learn the Pattern, Not the Tool | **FE** | FD | AIEOS's tool-agnostic policy, three-layer adapter model (spec → binding → adapter), and AI provider neutrality are direct implementations. AIEOS teaches architecture (four-file system, freeze-before-promote) not tool tutorials. | `adapter-conformance-spec.md`; `ai-transparency-principles.md` §Provider Neutrality |
| P77 | Community Is a Living Pattern Library | **N/A** | NA | Community building is outside AIEOS governance scope. AIEOS is open-source (MIT) but doesn't govern community interaction patterns. | — |
| P78 | Design for Infrastructure, Not Just Tool | **FE** | FD | AIEOS is infrastructure, not a tool: it's a governance system that other projects build on top of. The ecosystem roadmap (7 projects) treats AIEOS as the foundation that enables artifact store, evaluation engine, analytics, compliance reporting. | `ecosystem-roadmap.md`; `roadmap.md` ECO-001 through ECO-008 |
| P79 | The Implementation Gap Is Now AI's Problem | **PA** | WE | The aieos-console project demonstrated this: the AIEOS framework + AI (Claude Code) produced a working system from specs. But AIEOS doesn't explicitly address or govern the collapsing implementation gap. | aieos-console as demonstration |

**Section Summary:** 2 FE / 1 PA / 0 GAP / 1 N/A.

### 1.14 — The Four-Layer Prompting Stack (P80-P84)

| ID | Name | Score | Ch. | Rationale | AIEOS Reference |
|----|------|-------|-----|-----------|-----------------|
| P80 | Prompting Has Split Into Four Distinct Disciplines | **FE** | FD | AIEOS addresses all four layers: (1) Prompt Craft — governed prompt files per artifact type. (2) Context Engineering — briefing distillation, template pre-population, CLAUDE.md. (3) Intent Engineering — principles files encode organizational purpose. (4) Specification Engineering — the entire spec system. | Four-file system; `briefing-distillation-spec.md`; principles files; spec system |
| P81 | The Synchronous Prompting Model Is Structurally Broken for Long-Running Agents | **FE** | FD | AIEOS is designed for asynchronous, long-running work: frozen artifacts persist across sessions, ER tracks state, sherpa journal preserves context, session resumption reconstructs position. All intent is encoded before the agent starts (in specs, principles, upstream frozen artifacts). | ER; sherpa journal; session resumption; specs as pre-encoded intent |
| P82 | Intent Engineering — Context Tells Agents What to Know; Intent Tells Agents What to Want | **FE** | FD, PF | AIEOS separates these explicitly: specs and frozen artifacts provide context (what to know). Principles files provide intent (what to want — organizational values, quality standards, trade-off hierarchies). The four-file system structurally prevents context-intent conflation. | Principles files as intent; specs/artifacts as context; four-file separation |
| P83 | Specification Engineering — Treat the Document Corpus as Agent-Readable | **FE** | FD | AIEOS's entire document corpus is agent-readable by design: Markdown, structured sections, machine-readable navigation map, standardized artifact IDs, typed state blocks. The AI transparency principles require agent-portable artifacts. The spec hierarchy (PRD → SAD → TDD → WDD) is exactly this. | `ai-transparency-principles.md` §AI-Portable; navigation map; artifact ID convention |
| P84 | Organizational Politics Is Often Bad Context Engineering at Scale | **PA** | FD | AIEOS's spec-quality communication (self-contained, explicit, constraint-defined) indirectly addresses this. But AIEOS doesn't explicitly frame its governance as an organizational communication improvement tool. | Specs as explicit communication; freeze-before-promote as surfacing assumptions |

**Section Summary:** 4 FE / 1 PA / 0 GAP / 0 N/A. The four-layer prompting stack maps remarkably well to AIEOS's architecture.

### 1.15 — The Intent Gap & Organizational AI Alignment (P85-P90)

| ID | Name | Score | Ch. | Rationale | AIEOS Reference |
|----|------|-------|-----|-----------|-----------------|
| P85 | The AI Race Is Now an Intent Race | **PA** | FD | AIEOS's principles files + spec system constitute "organizational intent infrastructure." But AIEOS doesn't frame itself in these terms or explicitly address the intelligence-vs-intent distinction. | Principles files as intent infrastructure; specs as encoded organizational knowledge |
| P86 | The Three-Layer Intent Gap | **PA** | FD | AIEOS addresses Layer 1 (unified context infrastructure via navigation map, artifact store) and partially Layer 2 (coherent toolkit via sherpa, four-file system). Layer 3 (intent engineering) is addressed through principles files but not as a formal discipline. | Navigation map (L1); sherpa (L2); principles files (L3 partial) |
| P87 | The Shadow Agents Problem | **PA** | GS | AIEOS's adapter conformance spec and tool governance spec provide governed channels for agent integration. But AIEOS doesn't explicitly address the shadow agents problem or provide a sanctioned-vs-unsanctioned agent framework. | `adapter-conformance-spec.md`; `tool-governance-spec.md` |
| P88 | OKRs Were Designed for Humans — They Cannot Be Directly Handed to Agents | **PA** | FD | AIEOS's spec system translates high-level intent into agent-actionable specifications (hard gates, acceptance criteria, constraint architecture). But AIEOS doesn't explicitly address OKR-to-agent translation as a discipline. | Specs as translated intent; hard gates as machine-actionable criteria |
| P89 | The Two-Cultures Problem | **PA** | CT | AIEOS's sherpa bridges the two cultures: non-technical users navigate through conversational guidance while the framework enforces technical rigor. But AIEOS doesn't explicitly address the executive-engineer gap or propose cross-functional roles. | Sherpa as bridge; ideation mode for non-technical users |
| P90 | The "Humans Just Know" Era Is Ending — Make the Implicit Explicit | **FE** | FD | AIEOS's core design principle. Philosophy doc: "Explicit Over Implicit." Specs make rules explicit. Principles files make values explicit. ERs make decisions explicit. Nothing relies on tacit knowledge — everything that matters is written down in a governed document. | `philosophy.md` §Explicit Over Implicit; ER key decisions; principles files |

**Section Summary:** 1 FE / 5 PA / 0 GAP / 0 N/A.

### 1.16 — DORA 2025: AI as Amplifier (P91-P96)

| ID | Name | Score | Ch. | Rationale | AIEOS Reference |
|----|------|-------|-----|-----------|-----------------|
| P91 | AI Is a Mirror and Amplifier | **PA** | FD | AIEOS's architecture ensures AI amplifies organizational quality (better specs → better artifacts). Diagnostic value: when artifacts fail validation, it surfaces organizational gaps (finding accumulator). But AIEOS doesn't explicitly frame itself as a diagnostic mirror. | Sherpa finding accumulator; validator FAIL as diagnostic |
| P92 | "Trust but Verify" Is the Mature AI Adoption Posture | **FE** | FD | AIEOS is structurally "trust but verify": AI generates (trust), validators check (verify), humans freeze (final verify). This is the default posture, not optional. No artifact reaches frozen status without verification. | Validator pattern; freeze-as-verification; three-tier testing |
| P93 | Friction Shifts — It Doesn't Vanish | **PA** | FD | AIEOS shifts friction from generation to validation/review (QAK, PRK, freeze gates) — recognizing the shift. But AIEOS doesn't explicitly address whether net friction decreases or just relocates. | QAK/PRK as friction relocation points |
| P94 | Control Systems Must Evolve 2x as Fast as What They Control | **PA** | FD | AIEOS's healthcheck playbook includes automated structural and framework validation that runs on every commit. But AIEOS doesn't explicitly address control system velocity relative to AI generation speed. | `healthcheck-playbook.md` §Schedule (per-commit, per-freeze) |
| P95 | Organizational AI Use Is Still Primarily Synchronous | **PA** | FD | AIEOS supports both synchronous (sherpa conversation) and asynchronous (frozen artifacts, session resumption) modes. AI transparency principles state "parallel optional, sequential works." But AIEOS doesn't explicitly address the synchronous-vs-agentic adoption gap. | `ai-transparency-principles.md` §Parallel Optional; sherpa session modes |
| P96 | Organizations Are Systems — AI Gains Are Blocked at System Boundaries | **FE** | FD | AIEOS's layer model explicitly models the organization as a system with defined boundaries. Cross-kit handoffs, boundary contracts, and the engagement record ensure AI gains propagate across system boundaries rather than stopping at kit edges. | `layer-model.md`; boundary contracts (entry-from-*.md); ER as cross-boundary tracker |

**Section Summary:** 2 FE / 4 PA / 0 GAP / 0 N/A.

### 1.17 — AI Coding Workflow & Cognitive Discipline (P97-P98)

| ID | Name | Score | Ch. | Rationale | AIEOS Reference |
|----|------|-------|-----|-----------|-----------------|
| P97 | AI Fills Gaps with Plausible Inventions — Ungiven Context Is the Root Cause | **FE** | FD, GS | AIEOS addresses this structurally: specs provide complete context for generation, frozen upstream artifacts provide inherited context, briefing distillation compresses context for downstream. AI transparency principles forbid inferred-as-fact. Validators catch invented content (hard gate failures). | `ai-transparency-principles.md` §No Inferred-as-Fact; specs as complete context; `briefing-distillation-spec.md` |
| P98 | Over-Reliance on AI Dulls Your Own Instincts | **PA** | FD | AIEOS's freeze-as-human-decision and PRK peer review keep humans engaged with substance. But AIEOS doesn't explicitly address the over-reliance risk or prescribe countermeasures (occasional human-only work, AI-as-teacher mode). | Freeze as human engagement; PRK as expert review |

**Section Summary:** 1 FE / 1 PA / 0 GAP / 0 N/A.

### 1.18 — Retrieval Infrastructure for Agents (P99-P101)

| ID | Name | Score | Ch. | Rationale | AIEOS Reference |
|----|------|-------|-----|-----------|-----------------|
| P99 | Agents Stress-Test Retrieval Infrastructure | **N/A** | NA | Runtime retrieval infrastructure scaling is outside AIEOS governance scope. AIEOS artifact store (ECO-003) uses LanceDB but this is an ecosystem project, not governance. | ECO-003 (tangential) |
| P100 | Context Windows Are Not Retrieval | **PA** | FD | AIEOS distinguishes between session context (context window) and persistent state (ER, frozen artifacts). Briefing distillation manages what enters the context window. But AIEOS doesn't govern retrieval infrastructure architecture. | `briefing-distillation-spec.md`; `ai-transparency-principles.md` §Session State on Disk |
| P101 | The Unicorn Is the Retrieval Stack — Hybrid Beats Single Tech | **N/A** | NA | Retrieval stack architecture is outside AIEOS governance scope. The artifact store uses hybrid search but this is an ecosystem implementation choice. | ECO-003 (tangential) |

**Section Summary:** 0 FE / 1 PA / 0 GAP / 2 N/A.

### 1.19 — Cost Modeling & ROI (P102-P104)

| ID | Name | Score | Ch. | Rationale | AIEOS Reference |
|----|------|-------|-----|-----------|-----------------|
| P102 | Total Cost of AI Adoption Has Five Components | **GAP** | RP | AIEOS doesn't govern AI adoption cost modeling. GAP-005 on the roadmap proposes cost tracking but focuses on initiative costs, not AI tooling costs. The five-component model (licensing, infra, engineering labor, governance overhead, rework) is relevant to AIEOS adopters. | `roadmap.md` GAP-005 (partial) |
| P103 | Measure AI ROI Against Organizational Outcomes | **PA** | GS | AIEOS governs outcome measurement through RRK (SLOs, RHR health metrics) and IEK (evolution signals). But AIEOS doesn't explicitly connect these to AI ROI measurement or DORA metrics. | RRK SRP (SLOs); IEK ES; no explicit AI ROI framework |
| P104 | Jevons Paradox Applies to AI Cost | **N/A** | NA | Economic observation about AI cost dynamics. Outside AIEOS governance scope. | — |

**Section Summary:** 0 FE / 1 PA / 1 GAP / 1 N/A. First gap identified: AI adoption cost governance.

### 1.20 — Compliance & Regulatory (P105-P107c)

| ID | Name | Score | Ch. | Rationale | AIEOS Reference |
|----|------|-------|-----|-----------|-----------------|
| P105 | Agent-Generated Code Requires Same Compliance Controls Plus Traceability | **FE** | FD, GS | AIEOS provides traceability: artifact IDs, spec versions, principles versions, GM version in every artifact's Document Control. Frozen artifacts are immutable. AI transparency principles require provenance. SCK CER (Compliance Evidence Record) governs compliance evidence. | `ai-transparency-principles.md` §Provenance; SCK `cer-spec.md`; artifact provenance fields |
| P106 | GDPR and Data Minimization Apply to Agent Context Windows | **GAP** | RP | AIEOS doesn't govern data privacy in agent context windows. GAP-002 proposes a Data Classification Record in SCK, but this is planned, not built. No current spec addresses GDPR data minimization for AI processing. | `roadmap.md` GAP-002 (planned, not built) |
| P107 | SOX: Human Accountability Cannot Be Delegated to Agent | **FE** | FD | AIEOS's freeze mechanism is exactly this: every freeze is a human decision. The human reviewer's approval is the accountability gate. ER tracks who approved what and when. No artifact can reach production-relevant status without human authorization. | Freeze-as-human-decision; ER artifact tables (track approval) |
| P139 | NIST AI Risk Management Framework | **PA** | GS | AIEOS partially maps to NIST AI RMF: GOVERN (governance model, specs), MAP (SCK threat modeling), MEASURE (validators, QAK), MANAGE (convergence loops, escalation). But AIEOS doesn't explicitly reference NIST AI RMF or provide a formal mapping. | Governance model (GOVERN); SCK TM (MAP); validators (MEASURE); convergence loops (MANAGE) |
| P107b | FedRAMP and Federal AI Governance | **N/A** | NA | Federal compliance specifics are outside AIEOS scope. SCK governs compliance evidence generically but doesn't address FedRAMP-specific requirements. | SCK CER (generic compliance) |
| P107c | State AI Laws Creating Patchwork Compliance | **N/A** | NA | Specific regulatory landscape tracking is outside AIEOS scope. | — |

**Section Summary:** 2 FE / 1 PA / 1 GAP / 2 N/A. Data privacy governance (GAP-002) is the key gap, already on roadmap.

### 1.21 — Enterprise Tool Integration (P108-P110)

| ID | Name | Score | Ch. | Rationale | AIEOS Reference |
|----|------|-------|-----|-----------|-----------------|
| P108 | Enterprise Tool Integration Is the Last Mile | **PA** | GS, RP | AIEOS has the architecture (adapter conformance spec, tool bindings for GitHub/Confluence) but no executable adapters yet. INT-001 through INT-005 on the roadmap address this. The gap between static documentation and working integrations is explicitly acknowledged. | `adapter-conformance-spec.md`; `roadmap.md` INT-001 through INT-005 |
| P109 | MCP Is the Integration Architecture | **PA** | GS | AIEOS's adapter conformance spec defines a three-layer integration model (spec → binding → adapter) that is MCP-compatible but not MCP-specific (tool-agnostic by design). Sherpa's MCP connections exist for Claude Code but aren't governed as framework-level infrastructure. | `adapter-conformance-spec.md`; sherpa skill MCP connections |
| P110 | Jira Integration: AI Should Generate Stories, Not Manage Them | **PA** | GS, RP | AIEOS's WDD generates work items with acceptance criteria. The work-item-sync tool spec + Jira binding (planned in INT-001) would create Jira stories from frozen WDD items. But this is planned, not built. | WDD spec (work item generation); `roadmap.md` INT-001 (Jira binding planned) |

**Section Summary:** 0 FE / 3 PA / 0 GAP / 0 N/A. Integration architecture exists but execution is in progress.

### 1.22 — Testing Patterns for AI-Generated Code (P111-P113)

| ID | Name | Score | Ch. | Rationale | AIEOS Reference |
|----|------|-------|-----|-----------|-----------------|
| P111 | AI-Generated Code Requires Testing Philosophy Shift | **PA** | GS, PF | AIEOS's TDD spec governs test design with hard gates. Code-craftsmanship.md addresses testing philosophy. EEK execution spec includes review checks for test quality. But AIEOS doesn't explicitly require behavioral verification, property-based testing, or mutation testing as governance-level concerns. | `tdd-spec.md`; `code-craftsmanship.md`; `execution-spec.md` review checks |
| P112 | Treat AI Test Generation with Same Skepticism | **PA** | GS | EEK execution spec requires test review. Playbook requires regression checks. But AIEOS doesn't have a specific hard gate requiring skeptical review of AI-generated tests (e.g., "explain what each test catches"). | `execution-spec.md`; EEK playbook work group gates |
| P113 | Mutation Testing Closes the Gap | **GAP** | NA | AIEOS doesn't govern mutation testing or include it as a quality gate. QAK's verification plan doesn't require it. This is a specific testing technique that could strengthen QAK/EEK. | Not addressed |

**Section Summary:** 0 FE / 2 PA / 1 GAP / 0 N/A.

### 1.23 — AI Observability & LLMOps (P114-P117)

| ID | Name | Score | Ch. | Rationale | AIEOS Reference |
|----|------|-------|-----|-----------|-----------------|
| P114 | AI Pipelines Require Different Observability Stack | **PA** | GS | RRK governs observability for production systems (SRP SLOs, IR incident records). PRK has an observability lens. But AIEOS doesn't specifically govern AI pipeline observability (output quality, token economics, prompt drift, retrieval quality). | RRK `srp-spec.md`; PRK observability lens |
| P115 | Trace Every LLM Call | **PA** | GS | AIEOS's AI transparency principles require provenance traceability. Adapter conformance spec requires audit logging. But AIEOS doesn't govern per-LLM-call structured logging (prompt, response, tokens, latency, model version, correlation ID). | `ai-transparency-principles.md` §Provenance; `adapter-conformance-spec.md` §audit_logging |
| P116 | Monitor for Prompt Regression After Every Model Update | **GAP** | NA | AIEOS doesn't govern prompt regression testing or model update management. Specs are versioned, but prompt behavior after model changes isn't tested. | Not addressed |
| P117 | Cost Observability Is an Operational Requirement | **GAP** | RP | AIEOS doesn't govern AI cost observability. GAP-005 on the roadmap addresses cost tracking at the initiative level, not the operational AI pipeline level. | `roadmap.md` GAP-005 (partial) |

**Section Summary:** 0 FE / 2 PA / 2 GAP / 0 N/A. LLMOps observability is a gap area.

### 1.24 — Platform Engineering + AI Enablement (P118-P120)

| ID | Name | Score | Ch. | Rationale | AIEOS Reference |
|----|------|-------|-----|-----------|-----------------|
| P118 | Platform Team's AI Role Is Enabling Safe, Scalable Access | **PA** | FD | AIEOS provides the governance layer a platform team would use (golden paths via presets, shared standards via specs, approved tool catalog via tool governance). But AIEOS doesn't explicitly address the platform team's AI enablement role. | Initiative presets; tool governance spec; adapter conformance |
| P119 | Golden Paths for AI Make the Safe Choice the Easy Choice | **FE** | FD | AIEOS's initiative presets are exactly golden paths: 5 pre-defined flows (New Feature, Enhancement, Compliance, Performance Fix, Exploratory) that encode the correct sequence. Sherpa guides users down these paths. Getting-started guide provides onboarding. | `initiative-presets.md` (5 golden paths); sherpa routing; `getting-started.md` |
| P120 | Measure AI Adoption Quality, Not Just Adoption Rate | **GAP** | NA | AIEOS doesn't govern AI adoption quality metrics (activation, integration depth, output quality signal, feedback loop). This is relevant but not currently addressed. ECO-006 (Governance Analytics) on the ecosystem roadmap could address this. | `roadmap.md` ECO-006 (planned ecosystem project) |

**Section Summary:** 1 FE / 1 PA / 1 GAP / 0 N/A.

### 1.25 — Prompt & Agent Lifecycle Management (P121-P124)

| ID | Name | Score | Ch. | Rationale | AIEOS Reference |
|----|------|-------|-----|-----------|-----------------|
| P121 | Prompts Are Code — Versioning, Testing, Deployment Discipline | **FE** | FD, GS | AIEOS treats prompts as first-class governed artifacts: version-controlled in git, part of the four-file system, subject to structural validation (check-structure.sh), and tested through integration tests. Prompt changes require the same discipline as spec changes. | Four-file system; `check-structure.sh` validates prompt existence; Tier 3 integration tests |
| P122 | Model Version Pinning Is a Production Stability Requirement | **N/A** | NA | Runtime model version management is outside AIEOS governance scope. AIEOS is tool-agnostic and doesn't govern which AI models are used or how they're pinned. | — |
| P123 | A/B Testing Prompt Changes | **N/A** | NA | Runtime prompt A/B testing is outside AIEOS governance scope. | — |
| P124 | Prompt Deprecation Is as Important as Prompt Creation | **PA** | FD | AIEOS's lifecycle states include Deprecated (retained for audit). Spec versioning standard tracks changes. But prompt-specific deprecation lifecycle isn't explicitly governed — prompts evolve with their kits, not through a formal deprecation process. | `governance-model.md` §Lifecycle States; `spec-file-standard.md` |

**Section Summary:** 1 FE / 1 PA / 0 GAP / 2 N/A.

### 1.26 — AI for Incident Response & Ops (P125-P128)

| ID | Name | Score | Ch. | Rationale | AIEOS Reference |
|----|------|-------|-----|-----------|-----------------|
| P125 | AI-Assisted Incident Response Follows the Same Pattern: Context First | **FE** | GS | ODK's DCR (Diagnostic Context Record) is exactly this: full context assembly (log window, change history, system topology, dependent services, historical incidents) before AI-assisted diagnosis. It's the first artifact in the incident flow, not the diagnosis itself. | ODK `dcr-spec.md`; ODK playbook |
| P126 | AI's Highest-Value Ops Use Cases Are Synthesis and Pattern Recognition | **PA** | GS | ODK governs synthesis (INR investigates, PMR documents) and pattern recognition (RRK RHR identifies trends). But AIEOS doesn't explicitly restrict autonomous remediation or apply the HITL spectrum to ops AI specifically. | ODK (INR, PMR); RRK (RHR patterns) |
| P127 | Runbook Generation Is the Highest-ROI Ops AI Application | **PA** | GS | AIEOS governs runbooks through ORD (operational readiness, which includes runbook verification gate) and DKK (support knowledge articles). But AIEOS doesn't govern AI-assisted runbook generation or maintenance as a specific practice. | EEK `ord-spec.md` §runbook_verification; DKK `ska-spec.md` |
| P128 | AI-Assisted Postmortems Increase Institutional Learning | **FE** | GS | ODK's PMR (Postmortem Record) is exactly this: structured postmortem with contributing factors, timeline, action items. PMR feeds back to EEK (corrective actions) and IEK (institutional learning). The framework closes the loop. | ODK `pmr-spec.md`; ODK→EEK escalation; IEK feedback loop |

**Section Summary:** 2 FE / 2 PA / 0 GAP / 0 N/A.

### 1.27 — Platform Team AI Adoption Playbook (P129-P131)

| ID | Name | Score | Ch. | Rationale | AIEOS Reference |
|----|------|-------|-----|-----------|-----------------|
| P129 | Staged AI Rollout: Crawl → Walk → Run | **PA** | FD | AIEOS's initiative presets provide graduated complexity (P5 Exploratory → P2 Enhancement → P1 New Feature). The getting-started guide provides onboarding. UX-001 proposes a 15-minute tutorial. But AIEOS doesn't explicitly define a staged rollout methodology for organizational adoption. | `initiative-presets.md`; `getting-started.md`; `roadmap.md` UX-001 |
| P130 | Build a Community of Practice | **N/A** | NA | Community building is outside AIEOS governance scope. | — |
| P131 | Define Your AI Adoption Maturity Model | **GAP** | NA | AIEOS doesn't define an AI adoption maturity model for teams. This is relevant — AIEOS could define maturity levels tied to framework adoption depth (Level 1: using presets; Level 2: customizing specs; Level 3: contributing findings; Level 4: extending kits). | Not addressed |

**Section Summary:** 0 FE / 1 PA / 1 GAP / 1 N/A.

### 1.28 — GitOps & Kubernetes Platform Engineering with AI (P132-P135)

| ID | Name | Score | Ch. | Rationale | AIEOS Reference |
|----|------|-------|-----|-----------|-----------------|
| P132 | GitOps Reconciliation Loops Are a Natural Model for Agentic Feedback Loops | **PA** | FD | AIEOS's convergence loop (desired state in spec → agent generates → validator detects drift → correction) is structurally similar to GitOps reconciliation. But AIEOS doesn't explicitly draw this parallel or leverage GitOps patterns. | `review-convergence-loop.md` as reconciliation pattern |
| P133 | AI-Assisted IaC Requires Same Quality Discipline | **PA** | GS | PINFK governs infrastructure decisions (PDR, ISPEC, EM). EEK execution spec includes review checks. But AIEOS doesn't have IaC-specific quality gates (kubeval, helm lint, pinned chart versions). | PINFK specs; EEK execution-spec review checks |
| P134 | AI Context Management for K8s Manifest Drift Detection | **N/A** | NA | Kubernetes-specific drift detection is outside AIEOS governance scope. PINFK governs infrastructure decisions but not runtime cluster state management. | — |
| P135 | Agent-Driven Cluster State Management Requires HITL Spectrum | **N/A** | NA | Runtime cluster management is outside AIEOS governance scope. | — |

**Section Summary:** 0 FE / 2 PA / 0 GAP / 2 N/A.

### 1.29 — Multi-Tenant AI Platform Architecture (P140-P143)

| ID | Name | Score | Ch. | Rationale | AIEOS Reference |
|----|------|-------|-----|-----------|-----------------|
| P140 | AI Platform Team Serves Two Customers | **N/A** | NA | Multi-tenant AI platform architecture is outside AIEOS governance scope. | — |
| P141 | K8s Namespace Isolation for Multi-Tenant AI Workloads | **N/A** | NA | Runtime infrastructure patterns outside AIEOS scope. | — |
| P142 | AI API Gateway Has Four Non-Negotiable Jobs | **N/A** | NA | Runtime infrastructure patterns outside AIEOS scope. | — |
| P143 | Centralized vs Federated: Decision Is About Governance | **PA** | FD | AIEOS's governance model supports both: centralized (governance foundation as canonical authority) and federated (independent kits, per-kit principles). The hybrid model (shared governance + kit-owned artifacts) maps to the recommended approach. | `governance-model.md`; `philosophy.md` §Independent Kits, Compatible System |

**Section Summary:** 0 FE / 1 PA / 0 GAP / 3 N/A.

### 1.30 — Agent Output Provenance and Reproducibility (P144-P146)

| ID | Name | Score | Ch. | Rationale | AIEOS Reference |
|----|------|-------|-----|-----------|-----------------|
| P144 | Provenance Is Architecturally Distinct from Tracing | **FE** | FD, GS | AIEOS separates these: tracing is operational (adapter audit logs, sherpa journal entries). Provenance is architectural (artifact Document Control with Spec Version, Principles Version, GM Version, Prompt Version — linking output to production conditions). | Artifact provenance fields (4 fields); `spec-file-standard.md` §Recording in Artifacts |
| P145 | A SOX-Compliant AI Artifact Requires Five Provenance Elements | **PA** | FD | AIEOS provides 4 of 5: (1) Spec hash — spec version recorded ✓, (2) Model version — not tracked, (3) Context snapshot — not tracked, (4) Human approval — freeze date + reviewer ✓, (5) Output hash — not tracked. Model version and context snapshot are gaps. | Artifact provenance fields (partial); no model version or context snapshot |
| P146 | Provenance Graphs Are the Right Data Structure | **PA** | FD | AIEOS's navigation map is a directed graph of artifact dependencies. The ER tracks artifact relationships. But AIEOS doesn't produce W3C PROV-style provenance graphs or formally model entity-activity-agent relationships. | `navigation-map.md`; ER artifact tables |

**Section Summary:** 1 FE / 2 PA / 0 GAP / 0 N/A.

### 1.31 — Hallucination-Resilient System Design (P147-P150)

| ID | Name | Score | Ch. | Rationale | AIEOS Reference |
|----|------|-------|-----|-----------|-----------------|
| P147 | Design Systems Robust to Confident AI Incorrectness | **FE** | FD | AIEOS is designed for hallucination resilience: validators catch incorrect output regardless of AI confidence, session separation prevents self-validation bias, convergence loops bound the damage of persistent incorrectness. The system assumes AI WILL be wrong and designs for it. | Validator pattern; session separation; convergence loops; `philosophy.md` §Validators Are Hard Gates |
| P148 | Dual-Validation Architecture | **PA** | FD | AIEOS's session separation (generate in one session, validate in another) provides independent assessment. PRK adds multi-lens review. But AIEOS doesn't use two independent model calls with divergence detection — it uses structured validation against explicit criteria instead. | Session separation; PRK multi-lens; validators as structured (not model-based) check |
| P149 | Confidence-Gated Automation | **PA** | GS | AIEOS's completeness score (0-100) provides a confidence signal. Hard gates are binary (PASS/FAIL). Convergence loop stopping rules detect when the agent can't reliably improve. But AIEOS doesn't use token-level probabilities or semantic consistency checks for confidence gating. | Completeness score; convergence stopping rules |
| P150 | Sandboxed Execution Environments | **PA** | GS | AIEOS's convergence loop runs generation in bounded cycles before affecting downstream artifacts. QAK provides a testing gate. But AIEOS doesn't govern sandboxed execution environments for agent-generated code specifically. | Convergence loops as bounded execution; QAK as pre-release gate |

**Section Summary:** 1 FE / 3 PA / 0 GAP / 0 N/A.

### 1.32 — AI-Assisted Knowledge Management (P151-P153)

| ID | Name | Score | Ch. | Rationale | AIEOS Reference |
|----|------|-------|-----|-----------|-----------------|
| P151 | Organizational Knowledge Has a Half-Life | **PA** | GS | DKK's DHR (Document Health Review) addresses knowledge staleness with periodic reviews and health scores. Healthcheck playbook B9 checks initiative staleness. But AIEOS doesn't govern AI-assisted cross-referencing of docs against system state. | DKK `dhr-spec.md`; `healthcheck-playbook.md` B9 |
| P152 | Agent-Readable Documentation Is a Different Standard | **FE** | FD | AIEOS's entire doc corpus follows agent-readable standards: explicit cross-references, unambiguous scope, freshness metadata (version, date), structured data (navigation map, state blocks), machine-parseable structure (consistent headers, standardized formats). | `ai-transparency-principles.md` §AI-Portable; artifact structure standards; navigation map |
| P153 | Knowledge Currency Is an Ongoing Operational Discipline | **PA** | GS | DKK DHR provides periodic review. Healthcheck playbook defines audit schedules. But monthly AI-assisted documentation audits aren't built into the framework — healthchecks are structural, not content-aware. | DKK `dhr-spec.md`; `healthcheck-playbook.md` schedules |

**Section Summary:** 1 FE / 2 PA / 0 GAP / 0 N/A.

### 1.33 — Developer Cognitive Load (P154-P156)

| ID | Name | Score | Ch. | Rationale | AIEOS Reference |
|----|------|-------|-----|-----------|-----------------|
| P154 | AI Removes Natural Speed Governors — Cognitive Limits Remain | **PA** | FD | AIEOS's freeze gates and validation requirements act as structural speed governors (you can't ship faster than you can validate). But AIEOS doesn't explicitly address cognitive load management or the "brain fry" phenomenon. | Freeze gates as speed governors; QAK/PRK as validation pace-setters |
| P155 | AI Shifts Cognitive Load from Implementation to Evaluation | **PA** | FD | AIEOS's architecture reflects this shift: more structure invested in validation than generation. But AIEOS doesn't explicitly govern the cognitive burden of evaluation or prescribe countermeasures. | Validator-heavy architecture; PRK 12 lenses as evaluation load |
| P156 | Senior Engineer Review Burden Is a Platform Team Design Problem | **GAP** | NA | AIEOS doesn't address review capacity management or the distribution of review burden across teams. This is relevant — PRK could include review capacity as a consideration. | Not addressed |

**Section Summary:** 0 FE / 2 PA / 1 GAP / 0 N/A.

### 1.34 — The Redefined Senior Engineer Role (P157-P158)

| ID | Name | Score | Ch. | Rationale | AIEOS Reference |
|----|------|-------|-----|-----------|-----------------|
| P157 | AI Is Seniority-Biased Technology | **PA** | FD | AIEOS's design implicitly requires senior judgment: spec authoring, principles definition, PRK review, and freeze decisions all require experienced practitioners. But AIEOS doesn't explicitly address the seniority bias or junior developer impact. | Spec authoring; PRK lenses; freeze decisions |
| P158 | The Redefined Senior Role: Contextual Stewardship, Rejection Skill, Eval Design | **FE** | FD | AIEOS structurally defines these as senior activities: (1) Contextual Stewardship — principles files, CLAUDE.md, spec authoring. (2) Rejection Skill — validator hard gate design, PRK review criteria. (3) Eval Design — spec hard gates, QAK verification plans, three-tier test strategy. | Principles files (stewardship); validators (rejection); spec hard gates (eval design) |

**Section Summary:** 1 FE / 1 PA / 0 GAP / 0 N/A.

---

## Part 2: Patterns

### 2.1 — Specification & Planning Patterns (PA1-PA3h)

| ID | Name | Score | Ch. | Rationale | AIEOS Reference |
|----|------|-------|-----|-----------|-----------------|
| PA1 | Spec-Driven Development Pipeline | **FE** | FD | AIEOS is SDD: specs drive generation, which drives validation, which drives freeze. The entire four-file system is this pattern. | Four-file system; every kit playbook |
| PA2 | Constitution-Driven Agent Behavior | **FE** | FD | AIEOS's CLAUDE.md per kit, governance model, and principles files serve as the agent constitution. Versioned, repository-resident, referenced by all prompts. | Kit CLAUDE.md files; governance-model.md; principles files |
| PA3 | Planner-Worker Architecture | **FE** | FD | AIEOS's artifact hierarchy (PRD → ACF → SAD → TDD → WDD → execution) IS planner-worker: upstream artifacts plan, downstream artifacts execute. Quality ceiling is set in planning phase (DPRD quality determines everything downstream). | Artifact hierarchy; `flow-reference.md` §2 Pipeline Flows |
| PA3a | The Five Specification Primitives | **FE** | FD, GS | AIEOS implements all five: (1) Self-contained problem statement — spec §Purpose + upstream references. (2) Acceptance criteria — hard gates. (3) Constraint architecture — spec musts/must-nots, principles. (4) Task decomposition — WDD breaks TDD into items. (5) Evaluation design — validator hard gates + QAK VP. | Spec structure; hard gates; WDD; validators; QAK VP |
| PA3a-ext | SDLC Artifact Hierarchy | **FE** | FD | AIEOS's hierarchy mirrors this exactly: DPRD → PRD → ACF → SAD → DCF → TDD → WDD → Stories (work items). Each inherits constraints from above, human approval gate between each stage. | EEK artifact flow; `flow-reference.md` |
| PA3b | Intent Infrastructure Pattern | **FE** | FD, PF | AIEOS's principles files ARE intent infrastructure: what good enough looks like, what AI can decide vs. escalate, organizational values for trade-offs. Made available as context to prompts. | Principles files; sherpa fast-path criteria |
| PA3c | Organizational Capability Map | **PA** | GS | AIEOS doesn't maintain a formal agent-ready/augmented/human-only classification. But the Assignee Type field in WDD (AI/Human/Either) is a per-task capability classification. | WDD `wdd-spec.md` §Assignee Type |
| PA3d | Delegation Framework | **PA** | FD | AIEOS encodes judgment through specs (authorization scope, constraints, hard limits) and principles (trade-off hierarchy, escalation triggers). But this isn't formalized as a per-agent-role delegation framework. | Specs as encoded delegation; principles as trade-off hierarchy |
| PA3e | Intent Alignment Feedback Loop | **FE** | FD | AIEOS's IEK (Layer 7) closes the intent alignment loop: evolution signals feed back to Layer 2. Finding accumulator detects drift. Healthcheck playbook audits governance consistency. RRK RHR detects operational drift. | IEK feedback loop; sherpa finding accumulator; `healthcheck-playbook.md` |
| PA3f | DORA AI Capabilities Model — Seven Amplifiers | **PA** | FD | AIEOS provides several amplifiers: clear AI stance (governed prompts), version control (git-based artifacts), small batches (per-artifact freeze), quality platform (governance infrastructure). But AIEOS doesn't explicitly map to or measure against the seven DORA amplifiers. | Governed prompts; git-based; per-artifact granularity |
| PA3g | VSM as AI Force Multiplier | **PA** | FD | AIEOS's layer model is a value stream map (idea → discovery → design → test → release → ops → learning). But AIEOS doesn't explicitly frame itself as VSM or require value stream mapping before adoption. | `layer-model.md` as implicit value stream |
| PA3h | Augment vs Evolve — Two Transformation Paths | **PA** | FD | AIEOS supports both: augmentation (use AIEOS with existing tools via adapters) and evolution (redesign workflows around AIEOS governance). But AIEOS doesn't explicitly present these as transformation paths. | Adapter conformance (augment); full kit adoption (evolve) |

**Section Summary:** 7 FE / 5 PA / 0 GAP / 0 N/A. Specification and planning patterns are AIEOS's strongest cluster.

### 2.2 — Context & Memory Patterns (PA4-PA6d)

| ID | Name | Score | Ch. | Rationale | AIEOS Reference |
|----|------|-------|-----|-----------|-----------------|
| PA4 | Anchored Iterative Summarization | **PA** | CT | Sherpa maintains context through ER state block updates and journal entries. Briefing distillation compresses frozen artifacts. But AIEOS doesn't govern structured context compression for long-running sessions explicitly. | ER state block; sherpa journal; `briefing-distillation-spec.md` |
| PA5 | Milestone-Based Agent Lifecycle | **FE** | FD | AIEOS's freeze points are milestones: each frozen artifact is a clean handoff point. Session resumption picks up from the last frozen artifact. Sherpa position checks at freeze #3, #6, #9, #12 are explicit milestone reviews. | Freeze-as-milestone; sherpa session resumption; position checks |
| PA5a | Recursive Language Models | **N/A** | NA | RLM architecture is outside AIEOS governance scope. | — |
| PA6 | Three Primitives Stack (Memory + Proactivity + Tools) | **PA** | FD | AIEOS provides memory (ER, frozen artifacts, journal) and tools (adapter conformance, navigation tools). Proactivity is limited — sherpa offers utility prompts but doesn't wake up and act on schedules. | ER (memory); adapters (tools); sherpa (limited proactivity) |
| PA6a | Foundation Agent + Composition Pattern | **PA** | FD | Sherpa acts as a foundation agent that delegates to specialized kit prompts/validators. But AIEOS doesn't govern multi-agent orchestration protocols (A2A, JSON-RPC). | Sherpa as orchestrator; kit prompts as specialized agents |
| PA6b | Agent Cards for Discovery and Delegation | **PA** | CT | AIEOS's navigation map nodes describe artifact types with purpose and capabilities. Tool specs describe tool capabilities. But these aren't formal agent cards in the A2A sense. | Navigation map nodes; tool specs as capability descriptions |
| PA6c | Three Interaction Modes for Inter-Agent Communication | **N/A** | NA | Inter-agent communication protocols are outside AIEOS governance scope. | — |
| PA6d | MCP as Universal Agent-to-Tool Integration Layer | **PA** | GS | AIEOS's adapter conformance spec defines a universal integration pattern (push/verify/health) that is MCP-compatible. Tool governance spec standardizes capability description. But MCP isn't explicitly adopted as the integration standard. | `adapter-conformance-spec.md`; `tool-governance-spec.md` |

**Section Summary:** 1 FE / 5 PA / 0 GAP / 2 N/A.

### 2.3 — Quality & Review Patterns (PA7-PA10)

| ID | Name | Score | Ch. | Rationale | AIEOS Reference |
|----|------|-------|-----|-----------|-----------------|
| PA7 | Agent-Augmented Code Review | **FE** | GS | AIEOS governs this through PRK (12 specialized review lenses: security, reliability, cost, operability, observability, etc.) and EEK execution spec review checks. PRK is explicitly AI-augmented multi-perspective review. | PRK kit (12 lenses); `prr-spec.md`; `execution-spec.md` review checks |
| PA8 | Governance-Proportional-to-Risk | **FE** | FD | AIEOS implements this: different presets apply different governance depth (P5 Exploratory is lightweight, P3 Compliance is heavy). Cross-cutting kit adoption is optional based on trigger criteria. Fast-path detection skips unnecessary governance. | `initiative-presets.md` (graduated governance); sherpa fast-path detection |
| PA8a | HITL Runtime Patterns | **FE** | FD | AIEOS implements all three: confidence thresholds (completeness score), approval gates (freeze decision), escalation queues (convergence loop escalation after 3 attempts). Combined per the governance-proportional-to-risk principle. | Completeness score; freeze gate; convergence escalation |
| PA8b | Six-Layer HITL Architecture | **FE** | FD | AIEOS implements all six: (1) Input/Intent — specs + principles. (2) Planning — prompts plan generation. (3) Human Review — validator output reviewed. (4) Controlled Execution — bounded convergence. (5) Observability — sherpa journal, position checks. (6) Feedback — IEK, finding accumulator. | Specs (1); prompts (2); validators (3); convergence (4); journal (5); IEK (6) |
| PA9 | Strict Linting (inferred from section) | **PA** | GS | AIEOS's check-structure.sh enforces structural linting. Tier 2 pytest enforces framework invariants. But code-level linting governance is in EEK execution spec (review check), not a structural enforcement. | `check-structure.sh`; `execution-spec.md` review checks |
| PA10 | Agent Readiness Framework | **PA** | GS | AIEOS's healthcheck playbook (Scope A) assesses framework readiness. Kit structure standard defines readiness checklist. But AIEOS doesn't assess codebase readiness for AI agent deployment specifically. | `healthcheck-playbook.md` Scope A; `kit-structure-standard.md` |

**Section Summary:** 4 FE / 2 PA / 0 GAP / 0 N/A.

### 2.4 — Operations & Feedback Patterns (PA11-PA13)

| ID | Name | Score | Ch. | Rationale | AIEOS Reference |
|----|------|-------|-----|-----------|-----------------|
| PA11 | Autonomous Feedback Loop (SRE → Dev) | **FE** | GS | AIEOS governs this loop: ODK detects → investigates → PMR documents → escalation to EEK (corrective action) → IEK captures learning. The feedback loop is explicit in the layer model. | ODK→EEK escalation (T1); IEK feedback; `flow-reference.md` §5 |
| PA12 | Sandbox Evaluation Environment | **PA** | GS | AIEOS's convergence loop provides bounded evaluation. QAK provides pre-release testing. But AIEOS doesn't govern sandbox environments where reviewers interact with running code. | Convergence loops; QAK as testing gate |
| PA13 | Capability-Based Routing | **FE** | FD, CT | AIEOS's sherpa routes to appropriate kits based on initiative type (decision tables). Navigation map's decision tables route at each junction. WDD assigns tasks by capability (AI/Human/Either). | Sherpa decision tables; navigation map junctions; WDD Assignee Type |

**Section Summary:** 2 FE / 1 PA / 0 GAP / 0 N/A.

### 2.5-2.6 — Agent Selection & Security Patterns (PA14-PA19c)

| ID | Name | Score | Ch. | Rationale | AIEOS Reference |
|----|------|-------|-----|-----------|-----------------|
| PA14 | Three-Axis Agent Evaluation Framework | **N/A** | NA | Agent product evaluation is outside AIEOS governance scope. | — |
| PA15 | Sovereignty vs Delegation Spectrum | **PA** | FD | AIEOS supports full sovereignty (local Markdown, no cloud dependency). AI transparency principles require provider neutrality. But AIEOS doesn't govern the organizational decision about where to sit on this spectrum. | `ai-transparency-principles.md` §Provider Neutrality |
| PA15a | Centaur vs Cyborg Working Modes | **PA** | FD | AIEOS supports centaur mode (clean human/AI division at freeze gates). Sherpa conversation is more cyborg (fluid human-AI). But AIEOS doesn't explicitly define or recommend working modes. | Freeze gates (centaur); sherpa conversation (cyborg) |
| PA15b | Expert Frontier Mapping | **PA** | FD | AIEOS's specs define the AI capability frontier per artifact type (what AI can generate well). PRK lenses are expert-mapped review boundaries. But this isn't explicit frontier mapping. | Specs as implicit frontier; PRK as expert review boundaries |
| PA15c | The Six 201 Skills Framework | **PA** | FD | AIEOS exercises all six through its design: context assembly (briefing distillation), quality judgment (validators), task decomposition (WDD), iterative refinement (convergence), workflow integration (sherpa), frontier recognition (convergence stopping rules). But not as a teaching framework. | Structural exercise of all six skills |
| PA15d | Risk × Capability Quadrant for Agent Classification | **PA** | GS | SCK's threat model could classify agents by risk/capability. AIEOS's governance-proportional-to-risk design aligns. But AIEOS doesn't have a formal agent classification quadrant. | SCK TM; governance-proportional-to-risk |
| PA16 | Task-Scoped, Time-Bound Permissions | **PA** | GS | AIEOS's adapter conformance spec requires auth externalization. Session separation bounds agent scope temporally. But AIEOS doesn't govern per-task permission scoping or automatic revocation. | `adapter-conformance-spec.md` §auth_externalized; session separation |
| PA17 | Defense-in-Depth for Agent Input Surfaces | **PA** | FD | AIEOS layers validation: structural (check-structure.sh), framework (pytest), behavioral (integration tests), content (validators), expert (PRK). But this is defense-in-depth for artifact quality, not specifically for agent input surfaces. | Three-tier testing + validators + PRK as layered defense |
| PA18 | Agent Supply Chain Verification | **PA** | GS | SCK DAR governs dependency audits. Adapter conformance requires health checks. But AIEOS doesn't govern agent tool/plugin supply chain verification specifically (signed registries, hash verification). | SCK `dar-spec.md`; `adapter-conformance-spec.md` §health_check |
| PA19 | Cascading Failure Circuit Breakers | **FE** | FD | AIEOS's convergence loop is a circuit breaker: max 3 iterations, escalation on failure. Cross-cutting kits don't block each other (except QAK). Decision outcome taxonomy includes "Block" and "Rollback." | `review-convergence-loop.md` §Max Iterations; `flow-reference.md` §10 Rule 6, §11 |
| PA19a | AI Firewall / Proxy Gateway | **N/A** | NA | Runtime AI gateway infrastructure is outside AIEOS governance scope. | — |
| PA19b | Agent DevSecOps Lifecycle | **PA** | FD | AIEOS's layer model covers Plan (PIK/SDK) → Build (EEK) → Test (QAK) → Deploy (REK) → Monitor (RRK) → Learn (IEK). Security is integrated via SCK. But this maps to SDLC lifecycle, not specifically agent DevSecOps. | Layer model as DevSecOps analog; SCK integration |
| PA19c | Continuous Agent Drift Monitoring | **PA** | GS | RRK governs drift detection for production systems (RHR). Healthcheck playbook B3 checks frozen artifact immutability. But AIEOS doesn't govern continuous monitoring of agent behavior drift specifically. | RRK RHR; `healthcheck-playbook.md` B3 |

**Section Summary:** 1 FE / 10 PA / 0 GAP / 2 N/A.

### 2.6a — Dark Factory & Autonomous Development (PA19d-PA19f)

| ID | Name | Score | Ch. | Rationale | AIEOS Reference |
|----|------|-------|-----|-----------|-----------------|
| PA19d | Scenarios as Holdout Sets | **PA** | GS | AIEOS's validators judge against spec criteria that are separate from the generation prompt — a form of holdout. QAK's TCR (Test Coverage Record) documents test scope. But AIEOS doesn't govern external holdout test sets that agents never see during development. | Validators as separate-from-prompt judgment; QAK TCR |
| PA19e | Digital Twin Development Environments | **N/A** | NA | Runtime development environment architecture is outside AIEOS governance scope. | — |
| PA19f | Spec-to-Software Pipeline (Dark Factory) | **PA** | FD | AIEOS is moving toward this: spec → sherpa reads specs → AI generates artifacts → validators test → freeze. The aieos-console initiative demonstrated spec-to-working-software. But AIEOS doesn't operate at Level 5 (no human reviews code). | Sherpa as spec-to-artifact pipeline; aieos-console as demonstration |

**Section Summary:** 0 FE / 2 PA / 0 GAP / 1 N/A.

### 2.7-2.9 — Evaluation, Memory Architecture, Anti-Slop (PA20-PA33)

| ID | Name | Score | Ch. | Rationale | AIEOS Reference |
|----|------|-------|-----|-----------|-----------------|
| PA20 | Environment-Aware Eval Gates | **FE** | GS | AIEOS's validators check environmental context: is the upstream artifact frozen? Does the artifact reference the correct upstream IDs? Are all dependencies satisfied? ORD checks operational readiness before release. | Validators check freeze status; ORD §no_open_blockers gate |
| PA21 | Contextual Eval Design (Senior-Led) | **FE** | FD | AIEOS's spec authoring is senior-led eval design: hard gates encode what "right" looks like in organizational context, not just surface correctness. Spec failure examples prevent generic evaluation. | Spec hard gates as contextual evals; failure examples; PRK expert lenses |
| PA22 | Decision Context Documentation | **FE** | FD, GS | AIEOS's ER key decisions section, sherpa journal decision entries, and frozen artifacts all preserve decision context (constraints, trade-offs, rationale). FR-007 on roadmap proposes a dedicated Decision Register. | ER §Key Decisions; sherpa journal; `roadmap.md` FR-007 |
| PA23 | Constraint Library as Institutional Taste Asset | **PA** | FD | AIEOS's specs collectively form a constraint library. But there's no dedicated queryable constraint library or MCP server that surfaces accumulated rejection patterns. Specs are the closest analog. | Specs as distributed constraint library; no dedicated constraint library |
| PA24 | Five-Layer Agent Memory Stack | **PA** | FD | AIEOS provides analogs: session memory (sherpa conversation), cross-session recall (ER + journal), durable canonical facts (frozen artifacts), operational logs (sherpa journal), pre-prompt auto-recall (sherpa artifact store queries). But not architecturally designed as a layered memory system. | ER, journal, frozen artifacts, artifact store — emergent, not designed as memory layers |
| PA25 | Canonical Fact Store with Atomic Schema | **PA** | FD | Frozen artifacts serve as canonical facts. ER is append-only. But there's no atomic fact schema (ID, fact, category, status, access count). Facts are embedded in artifact structure. | Frozen artifacts as canonical; ER as append-only |
| PA26 | Pre-Prompt Auto-Recall Orchestrator | **PA** | CT | Sherpa's Phase 3 runs artifact store queries and template pre-population before generation. But this is sherpa-specific, not a framework-level requirement. | Sherpa Phase 3 steps 3-5 |
| PA27 | PARA File System for Agent Knowledge Organization | **PA** | FD | AIEOS uses directory-based organization per kit (specs/, artifacts/, prompts/, validators/) — inspectable, correctable, migration-proof. But it's not PARA-structured, and it's not designed as an agent knowledge organization system. | Kit directory structure; Markdown-based, inspectable |
| PA28 | Hooks as Agent Quality Harness | **FE** | FD | AIEOS's validators ARE hooks: post-generation quality gates that enforce constraints, produce traceability logs (JSON output), and stop destructive changes (FAIL blocks freeze). Check-structure.sh is a pre-commit hook equivalent. | Validators as post-generation hooks; `check-structure.sh` as structural hook |
| PA29 | Hard Blocks — Capability Restrictions by Agent Role | **PA** | GS | AIEOS's prompts define scope ("Generate content that satisfies all rules in the spec" — not "do whatever you think is right"). Validators enforce boundaries. But per-agent hard blocks (can't write to X, can't delete Y) aren't governed at the framework level. | Prompts as scope definition; validators as enforcement |
| PA30 | Per-Agent Work Tree Isolation | **N/A** | NA | Runtime agent isolation is outside AIEOS governance scope. | — |
| PA31 | Inter-Agent Quality Gate (Before Every Handoff) | **FE** | FD | AIEOS's freeze-before-promote is exactly this: every kit transition requires frozen (validated, all gates PASS) artifacts. No downstream work begins until the quality gate passes. | Freeze-before-promote; boundary contracts (entry-from-*.md) |
| PA32 | Agent Traceability Log | **FE** | FD | AIEOS's sherpa journal, ER artifact tables, and adapter audit logs provide traceability. Every artifact has provenance fields. Every freeze is timestamped. | Sherpa journal; ER; artifact provenance fields; `adapter-conformance-spec.md` §audit_logging |
| PA33 | Agent Scope Definition (What's Off-Limits) | **PA** | GS | AIEOS's specs define scope by inclusion (what must be addressed). Prompts define scope ("do not modify upstream frozen artifacts"). But explicit exclusion lists (what directories/files are off-limits) aren't governed. | Spec scope rules; prompt constraints |

**Section Summary:** 6 FE / 7 PA / 0 GAP / 1 N/A.

### 2.10-2.14 — Architecture, DORA, Coding, Retrieval, Routing (PA34-PA48)

| ID | Name | Score | Ch. | Rationale | AIEOS Reference |
|----|------|-------|-----|-----------|-----------------|
| PA34 | Writer-Critic Loop | **FE** | FD | AIEOS's generate-then-validate pattern IS writer-critic: prompt generates (writer), validator critiques (critic). Session separation ensures independence. Convergence loop iterates until critic passes. | Four-file system; session separation; convergence loop |
| PA35 | Session-Based vs Always-On Agent Architecture | **PA** | FD | AIEOS is session-based by design (sherpa conversations, freeze-at-session-end). Always-on monitoring is governed through RRK. But the choice isn't explicitly documented as an architectural decision. | Sherpa as session-based; RRK as always-on monitoring |
| PA36 | On-Demand AI-Generated Interfaces | **N/A** | NA | UI generation patterns are outside AIEOS governance scope. | — |
| PA37 | Four-Role Session Prompting | **PA** | FD | AIEOS's four-file system parallels this: spec (planner), prompt (implementer), validator (tester), and the artifact itself (output). Sherpa summarizes between steps. But this is structural, not a within-session prompting technique. | Four-file system as structural analog |
| PA38 | Explicit Approval Gate | **FE** | FD | AIEOS's freeze is the explicit approval gate. Sherpa Phase 3 requires validation before freeze — no artifact proceeds without human approval. The sherpa rule "never skip artifacts" enforces this. | Freeze-as-approval-gate; sherpa validation-before-freeze |
| PA39 | Three-Signal Evaluation for Retrieval Infrastructure | **N/A** | NA | Retrieval infrastructure evaluation is outside AIEOS governance scope. | — |
| PA40 | AI-Assisted Architecture Decision Records | **PA** | GS | AIEOS's SAD (Software Architecture Document) captures architectural decisions with trade-offs. ACF (Architecture Concept Framework) evaluates options. But these are AIEOS-specific artifacts, not traditional ADRs. | EEK `sad-spec.md`; `acf-spec.md` |
| PA41 | Brownfield Specification Excavation | **PA** | FD | AIEOS's EEK Path B (enhancement) handles brownfield entry. But AIEOS doesn't have a specific brownfield excavation pattern (document what exists → capture constraints → generate scenarios → incrementally formalize). | EEK Path B; no explicit excavation pattern |
| PA47 | Multi-Model Router Pattern | **N/A** | NA | Runtime model routing is outside AIEOS governance scope. | — |
| PA48 | Router Feedback Loop | **N/A** | NA | Runtime routing feedback is outside AIEOS governance scope. | — |

**Section Summary:** 2 FE / 4 PA / 0 GAP / 4 N/A.

---

## Part 3: Practices

### 3.1 — Specification & Setup (PR1-PR3c)

| ID | Name | Score | Ch. | Rationale | AIEOS Reference |
|----|------|-------|-----|-----------|-----------------|
| PR1 | Generate Specs Before Assigning Agents | **FE** | FD | AIEOS's entire flow: specs exist before generation prompts run. Every artifact type has a pre-existing spec. | Four-file system; playbook "read spec before generating" |
| PR2 | Maintain a Versioned agents.md | **FE** | FD | AIEOS maintains CLAUDE.md per kit — versioned, repository-resident, governing AI behavior. | Kit CLAUDE.md files; `kit-structure-standard.md` |
| PR3 | Evaluate Agent Readiness Before Deployment | **PA** | GS | AIEOS's healthcheck playbook evaluates framework readiness. But codebase agent readiness (linting, build, testing, docs, dev env) is governed through EEK specs, not a specific readiness assessment. | `healthcheck-playbook.md` Scope A; EEK specs |
| PR3a | Decompose Every Task to 2-Hour Granularity | **FE** | GS | AIEOS's WDD spec requires atomic work items with explicit granularity hard gate. WDD-spec §Granularity Rule enforces bounded task size. | `wdd-spec.md` §granularity gate |
| PR3b | Write Three Sentences of Acceptance Criteria | **FE** | GS | AIEOS's WDD spec requires acceptance criteria per work item (hard gate). Given/When/Then format for AI items, verification checklist for human items. | `wdd-spec.md` §acceptance_criteria gate |
| PR3c | Keep agents.md Under 2,500 Tokens | **PA** | FD | AIEOS's kit CLAUDE.md files and sherpa skill file are relatively compact. But there's no explicit token budget governance for bootstrap files. | Kit CLAUDE.md files (compact but ungoverned size) |

**Section Summary:** 4 FE / 2 PA / 0 GAP / 0 N/A.

### 3.2 — Measurement & Evaluation (PR4-PR6c)

| ID | Name | Score | Ch. | Rationale | AIEOS Reference |
|----|------|-------|-----|-----------|-----------------|
| PR4 | Baseline Agent Performance with Golden Test Sets | **FE** | FD | AIEOS's Tier 3 integration tests are golden test sets: pre-scripted scenarios with expected artifacts, frozen states, and behavioral checks. Sherpa rubric provides manual golden evaluation. | Tier 3 integration tests; sherpa rubric (15 criteria) |
| PR5 | Use "Film Review" Loops | **PA** | CT | AIEOS's sherpa self-scoring and retrospective provide post-initiative review. Sherpa rubric tests are structured "film review." But this isn't a general practice — it's sherpa-specific. | Sherpa self-scoring; sherpa rubric tests |
| PR6 | Measure Throughput, Not Just Velocity | **PA** | GS | AIEOS tracks artifact completion through ER (not just generation speed). RRK tracks operational metrics. But AIEOS doesn't explicitly track DORA metrics or distinguish velocity from throughput. | ER artifact tracking; RRK SLOs |
| PR6a | Establish DORA Baselines Before AI Rollout | **GAP** | NA | AIEOS doesn't govern DORA metric baselining. RRK governs SLO baselines but not specifically DORA metrics pre-AI-rollout. | Not addressed specifically |
| PR6b | Add Eval Test Case After Every Agent Failure | **FE** | FD | AIEOS's finding accumulator captures framework gaps at runtime. Sherpa behavioral checks are expanded when new failure modes are discovered (SH-024: expanded from initial set to 53 checks). | Sherpa finding accumulator; `roadmap.md` SH-024 |
| PR6c | Track and Report AI Adoption Quality Quarterly | **GAP** | NA | AIEOS doesn't govern adoption quality reporting. ECO-006 (Governance Analytics) on ecosystem roadmap could address this. | `roadmap.md` ECO-006 (planned) |

**Section Summary:** 2 FE / 2 PA / 2 GAP / 0 N/A.

### 3.3 — Quality & Review (PR7-PR9c)

| ID | Name | Score | Ch. | Rationale | AIEOS Reference |
|----|------|-------|-----|-----------|-----------------|
| PR7 | Run AI Code Quality Scans in Every PR | **PA** | GS | EEK execution spec includes review checks. PRK provides AI-augmented review. But AIEOS doesn't govern per-PR automated AI quality scanning as a specific pipeline requirement. | `execution-spec.md` review checks; PRK |
| PR8 | Enforce Strict Linting on Agent-Generated Code | **PA** | GS, PF | `code-craftsmanship.md` establishes linting standards. EEK execution spec includes linting review check. But strictness level isn't governed as a hard gate. | `code-craftsmanship.md`; `execution-spec.md` |
| PR9 | Implement Automated Bias and Stress Testing | **PA** | GS | QAK VP (Verification Plan) defines test dimensions. QAK TCR (Test Coverage Record) documents coverage. But bias testing and stress testing aren't called out as specific required dimensions. | QAK `vp-spec.md`; `tcr-spec.md` |
| PR9a | Run SAST/DAST on All Agent-Generated Code | **PA** | GS | SCK SAR (Security Assessment Record) governs security assessment. But SAST/DAST as mandatory pipeline steps for agent-generated code isn't a hard gate. | SCK `sar-spec.md` |
| PR9b | Track Rejection Patterns | **PA** | FD | AIEOS's finding accumulator and sherpa journal capture some rejection patterns. But there's no systematic rejection tracking practice or shared rejection log. | Sherpa finding accumulator; sherpa journal |
| PR9c | Review AI-Generated Tests with Same Rigor | **PA** | GS | EEK execution spec includes test review checks. Playbook requires regression checks. But there's no specific gate requiring skeptical review of AI-generated tests. | `execution-spec.md`; EEK playbook work group gates |

**Section Summary:** 0 FE / 6 PA / 0 GAP / 0 N/A.

### 3.4-3.5 — Operations, Architecture, Agent Infra (PR10-PR17b)

| ID | Name | Score | Ch. | Rationale | AIEOS Reference |
|----|------|-------|-----|-----------|-----------------|
| PR10 | Maintain Deterministic CI/CD Pipelines | **PA** | GS | PINFK governs infrastructure decisions. EEK execution spec addresses deployment. But AIEOS doesn't have a specific hard gate requiring deterministic CI/CD pipelines. | PINFK specs; `execution-spec.md` |
| PR11 | Deploy SRE Agents with Sub-Agent Architecture | **N/A** | NA | Runtime SRE agent architecture is outside AIEOS governance scope. ODK governs incident investigation process, not agent deployment. | — |
| PR12 | Document AI Decision-Making Processes | **FE** | FD | AIEOS documents AI decisions through: sherpa journal (every decision logged), ER key decisions, validator output (reasoning visible in gates/issues), artifact provenance fields. | Sherpa journal; ER §Key Decisions; validator output |
| PR13 | Match Models to Tasks | **N/A** | NA | Model selection is outside AIEOS governance scope (tool-agnostic by design). | — |
| PR13a | Canary Deploy AI-Assisted Changes | **PA** | GS | REK governs release strategy (RP includes exposure strategy). But canary deployment as a specific practice for AI-generated changes isn't a hard gate. | REK `rp-spec.md` §exposure_specification |
| PR13b | Maintain Explicit Rollback Plan | **FE** | GS | REK RP spec has `rollback_specification` as a hard gate. Every release plan must include explicit rollback. AIEOS demonstrated this in aieos-console RR. | REK `rp-spec.md` §rollback_specification gate; `aieos-console/docs/sdlc/36-rp.md` |
| PR14 | Reduce Human Input to Single Action | **PA** | CT | Sherpa reduces human input: answer questions, approve freezes. Template pre-population auto-fills from upstream. But the "single action" principle isn't explicitly governed. | Sherpa; template pre-population |
| PR15 | Separate Memory from Compute from Interface | **FE** | FD | AIEOS separates: memory (frozen artifacts, ER), compute (any AI model — tool-agnostic), interface (sherpa conversation, playbook reading, CLI). You can swap AI providers without affecting the governance layer. | Tool-agnostic design; `ai-transparency-principles.md` §Provider Neutrality |
| PR16 | Preserve Agent Build Context as Documentation | **FE** | FD | AIEOS preserves build context: sherpa journal, ER key decisions, frozen artifacts with provenance fields, conversation context in artifact structure. | Sherpa journal; ER; artifact provenance |
| PR17 | Build Agentic Ticket Triage Pipelines | **N/A** | NA | Ticket triage pipeline architecture is outside AIEOS governance scope. | — |
| PR17a | Make All Agent State Transitions Observable | **FE** | FD | AIEOS makes transitions observable: ER state block (current position), sherpa journal (every action timestamped), validator output (decision rationale), freeze events (state change). | ER §1b State Block; sherpa journal; validator output |
| PR17b | Run Agent Workflows Against Sandbox Copy | **PA** | GS | QAK provides pre-release testing. Convergence loops run in bounded cycles. But sandbox-with-production-data testing isn't a governed practice. | QAK; convergence loops |

**Section Summary:** 5 FE / 4 PA / 0 GAP / 3 N/A.

### 3.6-3.7 — Agent Selection, Security (PR18-PR25)

| ID | Name | Score | Ch. | Rationale | AIEOS Reference |
|----|------|-------|-----|-----------|-----------------|
| PR18 | Apply Three-Axis Test to Every Agent Product | **N/A** | NA | Agent product evaluation is outside AIEOS governance scope. | — |
| PR19 | Decide Your Sovereignty Position | **N/A** | NA | Agent product strategy is outside AIEOS governance scope. | — |
| PR19a | Invest in 201-Level Training | **N/A** | NA | Training program design is outside AIEOS governance scope. | — |
| PR19b | Define Guardrails That Say "Yes" | **PA** | FD | AIEOS defines positive usage: initiative presets say "yes, here's the right path." Sherpa guides toward correct use. But AIEOS doesn't explicitly frame its guidance as permission-granting vs. restriction. | Initiative presets; sherpa guidance |
| PR19c | Create AI Labs with Power Users AND Non-Technical Staff | **N/A** | NA | Organizational team formation is outside AIEOS governance scope. | — |
| PR19d | Share Failure Cases Systematically | **PA** | FD | AIEOS's finding accumulator captures failures. Spec failure examples share known failure modes. But there's no systematic cross-team failure sharing mechanism. | Finding accumulator; spec failure examples |
| PR19e | Kill the Contribution Badge | **N/A** | NA | Individual prompting practice is outside AIEOS governance scope. | — |
| PR19f | Build Deliberate Reflect Cycles | **PA** | FD | AIEOS builds reflection into the process: IEK (Layer 7) is a formal reflection cycle. Sherpa retrospective at initiative end. Healthcheck playbook provides periodic reflection. But per-session reflection isn't governed. | IEK; sherpa retrospective; healthcheck playbook |
| PR19g | Practice Strategic Deep Diving | **N/A** | NA | Individual cognitive practice is outside AIEOS governance scope. | — |
| PR19h | Separate Technical Patterns from Taste | **FE** | FD | AIEOS does this explicitly: specs/validators enforce technical patterns (delegatable); principles files and PRK encode taste (human judgment). | Specs (patterns) vs. principles (taste); PRK as taste layer |
| PR19i | Design Staged AI Skill Progression | **N/A** | NA | Career development framework is outside AIEOS governance scope. | — |
| PR20 | Conduct OWASP Agentic AI Threat Modeling | **PA** | GS | SCK TM (Threat Model) governs threat modeling. But OWASP Agentic AI Top 10 isn't specifically required as the framework. | SCK `tm-spec.md` |
| PR21 | Implement Agent Identity and Credential Scoping | **PA** | GS | Adapter conformance requires auth externalization. But per-agent identity and credential scoping isn't governed as a practice. | `adapter-conformance-spec.md` §auth_externalized |
| PR22 | Validate Agent Tool Registries and MCP Servers | **PA** | GS | SCK DAR governs dependency audits. But MCP server and tool registry validation isn't specifically governed. | SCK `dar-spec.md` |
| PR23 | Implement Inter-Agent Authentication | **N/A** | NA | Runtime inter-agent authentication is outside AIEOS governance scope. | — |
| PR24 | Set Delegation Depth Limits | **FE** | FD | AIEOS's convergence loop has a hard iteration limit (3). Cross-cutting kits don't cascade. Escalation paths are bounded. | `review-convergence-loop.md` §Max Iterations; `flow-reference.md` §10 |
| PR25 | Require Independent Verification | **FE** | FD | AIEOS requires independent verification: session separation (generator can't self-validate), PRK multi-lens review (multiple independent perspectives), QAK (independent quality gate). | Session separation; PRK; QAK |

**Section Summary:** 3 FE / 5 PA / 0 GAP / 8 N/A.

### 3.8-3.9 — Evaluation, Stewardship, Rejection (PR26-PR34)

| ID | Name | Score | Ch. | Rationale | AIEOS Reference |
|----|------|-------|-----|-----------|-----------------|
| PR26 | Write Environment-Aware Evals | **FE** | GS | AIEOS validators check environmental context: frozen status of upstream, correct artifact IDs, dependency satisfaction. ORD checks operational readiness. | Validators; ORD gates |
| PR27 | Assign Eval Design to Senior Experts | **PA** | FD | Spec authoring is implicitly a senior activity (requires domain expertise). But AIEOS doesn't explicitly require senior assignment for eval/spec design. | Implicit in spec authoring complexity |
| PR28 | Document Decision Context | **FE** | FD | ER key decisions, sherpa journal, frozen artifacts all document decision context (what, why, alternatives, constraints). | ER §Key Decisions; sherpa journal |
| PR29 | Run Evals Before, During, and After Agent Actions | **FE** | FD | AIEOS runs: pre-execution (freeze status check, dependency validation), in-flight (convergence loop monitoring, position checks), post-execution (validator judgment, completeness scoring). | Freeze checks (pre); convergence (during); validators (post) |
| PR30 | Make Contextual Stewardship Visible | **PA** | FD | AIEOS's healthcheck playbook and sherpa quality scoring make some stewardship visible. But there's no explicit "eval reporting" practice for leadership visibility. | Healthcheck playbook; sherpa quality scoring |
| PR31 | Track Your Rejection Patterns | **PA** | FD | Sherpa finding accumulator captures some patterns. But no systematic rejection tracking. | Finding accumulator |
| PR32 | Build a Constraint Library via MCP Server | **GAP** | NA | AIEOS doesn't have a constraint library or MCP-served rejection patterns. Specs serve as distributed constraints but aren't queryable as a library. | Not addressed |
| PR33 | Practice Articulation — Explain WHY | **FE** | GS | AIEOS's validator output requires gate + description + location for every blocking issue. Findings require description. This is structural articulation — not just "FAIL" but "FAIL because X at Y." | Validator output schema (blocking_issues: gate, description, location) |
| PR34 | Use Constraint Libraries to Accelerate Junior Development | **GAP** | NA | No constraint library exists. Specs are the closest analog but aren't designed for junior development acceleration. | Not addressed |

**Section Summary:** 4 FE / 3 PA / 2 GAP / 0 N/A.

### 3.10-3.12 — Memory, Anti-Slop, Spec Engineering (PR35-PR49)

| ID | Name | Score | Ch. | Rationale | AIEOS Reference |
|----|------|-------|-----|-----------|-----------------|
| PR35 | Audit Bootstrap Files for Token Bloat | **GAP** | NA | AIEOS doesn't govern bootstrap file token budgets or audit practices. | Not addressed |
| PR36 | Verify Agent Memory Retrieval Is Firing | **PA** | CT | Sherpa integration tests verify behavioral checks (artifact store queries, cross-initiative scans). But this is testing infrastructure, not a general practice for all agent deployments. | Tier 3 integration tests; behavioral checks |
| PR37 | Apply the 30-Day Rule for Facts | **N/A** | NA | Agent memory management practice is outside AIEOS governance scope. | — |
| PR38 | Restart Gateway After Config Changes | **N/A** | NA | Runtime agent configuration management is outside AIEOS scope. | — |
| PR39 | Never Patch Agent Slop — Diagnose and Rerun | **FE** | FD | AIEOS's convergence loop invariant 3: "Correction is re-generation with additional constraints, not in-place editing." | `review-convergence-loop.md` §Invariant 3 |
| PR40 | Enforce Anti-Mocking as Testing Standard | **PA** | PF | `code-craftsmanship.md` addresses testing philosophy. But anti-mocking isn't a named, enforced standard in AIEOS specs. | `code-craftsmanship.md` |
| PR41 | Run Strictest Possible Linting and Type-Checking | **PA** | GS | EEK execution spec includes linting review checks. But "strictest possible" isn't a governed hard gate. | `execution-spec.md` |
| PR42 | Require 100% Test Pass Before Handoff | **FE** | FD | AIEOS requires all hard gates PASS before freeze. Any FAIL blocks promotion. This is 100% pass rate at every handoff. | `governance-model.md` §Validator: "FAIL if any hard gate fails" |
| PR43 | Define Hard Block Lists Per Agent Role | **PA** | GS | AIEOS's prompts define scope constraints. But per-agent hard block lists aren't a governed practice. | Prompt scope constraints |
| PR44 | Standardize Agent Output Location and Naming | **FE** | FD | AIEOS enforces standardized output: artifact naming convention (`{TYPE}-{INITIATIVE}-{NNN}`), file location convention (`docs/specs/`, `docs/artifacts/`), validated by check-structure.sh. | `governance-model.md` §Naming Conventions; `check-structure.sh` |
| PR45 | Write a Personal Context Layer | **PA** | FD | AIEOS's kit CLAUDE.md files serve as project-level context layers. But personal context layers for individual practitioners aren't governed. | Kit CLAUDE.md files |
| PR46 | Practice Self-Contained Problem Statements | **FE** | GS | AIEOS's spec structure requires self-contained problem statements: purpose, scope, upstream references, hard gates. Every spec is self-contained (references upstream, doesn't assume implicit knowledge). | Spec structure; `spec-file-standard.md` |
| PR47 | Before Delegating, Write Three Sentences That Define "Done" | **FE** | GS | AIEOS's hard gates ARE "done" definitions. Every spec defines done as "all hard gates PASS." WDD acceptance criteria define done per work item. | Spec hard gates; WDD acceptance criteria |
| PR48 | Write Constraint Architecture (Musts, Must-Nots, Preferences, Escalations) | **FE** | FD | AIEOS's specs define musts (hard gates), must-nots (failure examples), preferences (principles files), and escalations (convergence loop escalation). The four categories are structurally present. | Specs (musts/must-nots); principles (preferences); convergence (escalations) |
| PR49 | Build 3-5 Eval Test Cases for Every Recurring Task | **FE** | FD | AIEOS's Tier 3 integration tests provide 3-5+ test cases per preset (11 scenarios with 30+ behavioral checks each). Run after every major change. | Tier 3 integration tests; 11 scenarios |

**Section Summary:** 7 FE / 5 PA / 1 GAP / 2 N/A.

### 3.13-3.18 — DORA, Coding Workflow, Observability, Platform, Prompt Lifecycle, GitOps (PR50-PR73)

| ID | Name | Score | Ch. | Rationale | AIEOS Reference |
|----|------|-------|-----|-----------|-----------------|
| PR50 | Publish Clear AI Stance | **PA** | FD | AIEOS's governance model, philosophy, and AI transparency principles constitute a clear AI stance. But this is for framework users, not for an organization's developers broadly. | `philosophy.md`; `ai-transparency-principles.md` |
| PR51 | Treat Internal Data as Strategic Asset | **PA** | GS | AIEOS's artifact store (ECO-003) treats frozen artifacts as strategic data. DKK governs documentation quality. But data ecosystem governance beyond AIEOS artifacts isn't addressed. | ECO-003; DKK |
| PR52 | Conduct Value Stream Map Before Scaling AI | **PA** | FD | AIEOS's layer model IS a value stream map. But AIEOS doesn't require consuming organizations to map their value streams before adopting AIEOS. | `layer-model.md` |
| PR53 | Frequent Commits and Rollback Proficiency | **PA** | GS | AIEOS's freeze-before-promote and re-entry protocol embody version control discipline. But commit frequency and rollback proficiency aren't governed as practices. | Freeze semantics; re-entry protocol |
| PR54 | Work in Smaller Batches | **FE** | FD | AIEOS enforces small batches: per-artifact freeze (not batch release), WDD atomic work items, convergence loops process one artifact at a time. | Per-artifact freeze; WDD atomic items |
| PR55 | Form Cross-Functional AI Working Group | **N/A** | NA | Organizational team formation is outside AIEOS governance scope. | — |
| PR56 | Start Fresh Chat When Stuck | **PA** | FD | AIEOS's session separation and convergence loop stopping rules (staleness, oscillation) embody this. Sherpa session resumption enables fresh starts. | Convergence stopping rules; session resumption |
| PR57 | Ask for Explanation Before Fix | **PA** | FD | AIEOS's elicitation protocol mandates reasoning before generation. Sherpa's risk scanning runs before generation. But "explain before fix" isn't a governed practice for all AI interactions. | `elicitation-protocol.md`; sherpa risk scanning |
| PR58 | Always Ask "Which Version?" | **PA** | GS | AIEOS's spec versioning tracks versions. Artifact provenance includes spec and principles versions. But version verification for AI suggestions isn't a governed practice. | `spec-file-standard.md`; artifact provenance fields |
| PR59 | Curate Context — Don't Dump It | **FE** | FD, CT | AIEOS's briefing distillation spec is exactly this: compress frozen artifacts to the essential decisions, constraints, and scope for downstream consumption. Token budget governed. | `briefing-distillation-spec.md` (6 hard gates including length_constraint) |
| PR60 | Write Regression Tests Immediately After Bug Fix | **PA** | GS | EEK playbook requires regression checks in work group gates. But immediate regression testing after every fix isn't a specific hard gate. | EEK playbook work group gates |
| PR61 | Instrument Every AI Pipeline Before Production | **GAP** | NA | AI pipeline instrumentation isn't governed. | Not addressed |
| PR62 | Set Cost Anomaly Alerts | **GAP** | RP | AI cost alerting isn't governed. GAP-005 partially addresses. | `roadmap.md` GAP-005 |
| PR63 | Run Prompt Regression Suite After Model Update | **GAP** | NA | Prompt regression testing isn't governed. | Not addressed |
| PR64 | Build Shared MCP Server Catalog | **PA** | GS, RP | AIEOS's tool governance spec and adapter conformance provide the foundation. INT-001 plans expanded platform bindings. But a shared MCP catalog isn't built. | `tool-governance-spec.md`; `roadmap.md` INT-001 |
| PR65 | Run Quarterly AI Adoption Quality Review | **GAP** | NA | Adoption quality reviews aren't governed. | Not addressed |
| PR66 | Maintain "What Works Here" Document | **PA** | FD | AIEOS's getting-started guide and kit playbooks serve this function partially. But a living "what works" document updated by teams isn't governed. | `getting-started.md`; kit playbooks |
| PR67 | Treat Every Production Prompt as Versioned Artifact in Git | **FE** | FD | AIEOS does this: all prompts are git-versioned Markdown files. Changes go through the same governance as any other file. | Four-file system; git-based repository |
| PR68 | Schedule Prompt Reviews at Every Major Model Release | **GAP** | NA | Prompt review cadence tied to model releases isn't governed. | Not addressed |
| PR69 | Run kubeconform in Every FluxCD PR | **N/A** | NA | Kubernetes-specific CI practice is outside AIEOS governance scope. | — |
| PR70 | Maintain Cluster-Standards CLAUDE.md | **N/A** | NA | Kubernetes-specific practice outside AIEOS scope. | — |
| PR71 | Export Namespace State Before AI-Assisted Drift Diagnosis | **N/A** | NA | Kubernetes-specific practice outside AIEOS scope. | — |
| PR72 | Pin FluxCD HelmRelease Chart Versions | **N/A** | NA | Kubernetes-specific practice outside AIEOS scope. | — |
| PR73 | Use AI to Generate Kustomize Overlay Diffs | **N/A** | NA | Kubernetes-specific practice outside AIEOS scope. | — |

**Section Summary:** 2 FE / 9 PA / 5 GAP / 5 N/A.

### 3.19-3.25 — Multi-Tenant, Provenance, Hallucination, Knowledge, Routing, Cognitive, Senior Role (PR74-PR98)

| ID | Name | Score | Ch. | Rationale | AIEOS Reference |
|----|------|-------|-----|-----------|-----------------|
| PR74 | Assign Team Label to Every LLM API Call | **N/A** | NA | Runtime LLM call tagging is outside AIEOS scope. | — |
| PR75 | Enforce ResourceQuota on Token Consumption | **N/A** | NA | Kubernetes resource management outside AIEOS scope. | — |
| PR76 | Build Runaway Agent Kill Switch | **PA** | FD | AIEOS's convergence loop max iterations (3) is a kill switch analog. But runtime kill switches for agent cost/call volume aren't governed. | Convergence loop max iterations |
| PR77 | Hash Spec and Model Version Into Commit Metadata | **PA** | FD | AIEOS tracks spec version and principles version in artifact Document Control. But commit-level hashing of spec + model version isn't governed. | Artifact provenance fields (spec version, principles version) |
| PR78 | Store Context Snapshots for SOX-Scope Agent Runs | **GAP** | NA | Context snapshot storage isn't governed. P145 assessment identified this gap. | Not addressed |
| PR79 | Define Hallucination Severity Taxonomy | **PA** | FD | AIEOS's validator output distinguishes severity implicitly: hard gate failure (critical), warning (lower). But a formal hallucination severity taxonomy isn't governed. | Validator hard gates vs. warnings as implicit severity |
| PR80 | Run New Agent Workflows in Dry-Run Mode for Two Weeks | **PA** | GS | QAK provides pre-release testing. But a specific dry-run period requirement isn't governed. | QAK as pre-release gate |
| PR81 | Tag Every Document With Freshness Owner and Review Date | **PA** | GS | DKK DHR governs document health reviews with cadence. But per-document freshness owner and review date metadata isn't a hard gate in document specs. | DKK `dhr-spec.md` |
| PR82 | Run Monthly AI-Assisted Documentation Audit | **PA** | GS | DKK DHR provides periodic review. But monthly AI-assisted audits against system state aren't governed as a specific cadence. | DKK `dhr-spec.md` |
| PR83 | Build Model Capability Map Before Router | **N/A** | NA | Model routing is outside AIEOS scope. | — |
| PR84 | A/B Test Routing Decisions | **N/A** | NA | Runtime routing A/B testing outside AIEOS scope. | — |
| PR85 | Set Explicit Daily AI Review Budget for Senior Engineers | **GAP** | NA | Review capacity management isn't governed. | Not addressed |
| PR86 | Rotate AI Output Review Ownership | **GAP** | NA | Review rotation isn't governed. | Not addressed |
| PR87 | Design AI Workflows With Explicit Stopping Points | **PA** | FD | AIEOS's freeze points are natural stopping points. Sherpa position checks occur at defined intervals. But explicit cognitive recovery time isn't governed. | Freeze points; sherpa position checks |
| PR97 | Explicitly Redefine "Senior Engineer" in AI Adoption Language | **PA** | FD | AIEOS implicitly redefines senior roles through structural design (spec authors, PRK reviewers, freeze approvers). But this isn't explicitly communicated as "the redefined senior role." | Implicit in framework design |
| PR98 | Use Senior Engineers to Build Constraint Libraries | **PA** | FD | AIEOS's spec authoring is constraint building by seniors. But framing this explicitly as "build constraints, not review output" isn't governed. | Spec authoring as constraint building |

**Section Summary:** 0 FE / 8 PA / 3 GAP / 4 N/A.

---

## Gap Analysis

### High-Impact Gaps

| Gap ID | AI-Native Item(s) | Description | Proposed AIEOS Response | Roadmap Cross-Ref |
|--------|-------------------|-------------|------------------------|-------------------|
| AG-001 | P106, PR78 | **Data privacy in AI context / context snapshots** — AIEOS doesn't govern data privacy in agent context windows or require context snapshots for auditable agent runs. | Extend SCK with Data Classification Record (DCL). Add context snapshot requirement to adapter conformance spec for SOX-scope systems. | GAP-002 (existing, validates priority) |
| AG-002 | P116, PR63, PR68 | **Prompt/model regression testing** — AIEOS doesn't govern prompt regression testing after model updates or prompt review cadence tied to model releases. | Add prompt regression testing as a Tier 3 test category. Add model-update review trigger to healthcheck playbook. | New item |
| AG-003 | P120, PR6a, PR6c, PR65 | **AI adoption quality measurement** — AIEOS doesn't govern DORA baselines, adoption quality metrics, or quarterly adoption reviews. | Define adoption maturity levels (P131 gap). Add adoption quality section to healthcheck playbook Scope B. ECO-006 addresses analytics. | ECO-006 (existing, validates priority) |
| AG-004 | PR32, PR34 | **Constraint library as queryable asset** — AIEOS's specs serve as distributed constraints but there's no queryable constraint library for rejection patterns. | Create constraint library spec as a cross-cutting tool. Design for MCP server exposure. Feed from validator FAIL patterns and PRK findings. | New item |

### Medium-Impact Gaps

| Gap ID | AI-Native Item(s) | Description | Proposed AIEOS Response | Roadmap Cross-Ref |
|--------|-------------------|-------------|------------------------|-------------------|
| AG-005 | P102, P117, PR62 | **AI cost governance and observability** — AIEOS doesn't govern AI tooling costs or cost anomaly alerting. | Extend GAP-005 (Cost Tracking Record) to include AI tooling cost dimensions. | GAP-005 (existing, extend scope) |
| AG-006 | P113 | **Mutation testing as quality gate** — AIEOS doesn't include mutation testing in quality governance. | Add mutation testing as optional QAK VP dimension for high-risk modules. | New item (low urgency) |
| AG-007 | P131 | **AI adoption maturity model** — AIEOS doesn't define adoption maturity levels for teams. | Define 4-level maturity model tied to AIEOS adoption depth (preset use → spec customization → finding contribution → kit extension). | New item |
| AG-008 | P156, PR85, PR86 | **Review capacity management** — AIEOS doesn't address senior engineer review burden or review rotation. | Add review capacity estimation as an optional WDD consideration. Document as guidance in PRK playbook. | New item |
| AG-009 | PR35 | **Bootstrap file token budget governance** — AIEOS doesn't govern CLAUDE.md/agents.md token budgets. | Add token budget recommendation to kit-structure-standard.md (advisory, not hard gate). | New item (low urgency) |
| AG-010 | PR61, P114-P115 | **AI pipeline observability requirements** — AIEOS doesn't govern LLM call tracing or AI-specific observability. | Extend RRK or create guidance document for AI pipeline observability standards. | New item |

### Low-Impact / Deferred Gaps

| Gap ID | AI-Native Item(s) | Description | Notes |
|--------|-------------------|-------------|-------|
| AG-011 | P145 | Model version and context snapshot in provenance | Extend artifact provenance fields when ecosystem supports it (ECO-001 schema) |
| AG-012 | PA41 | Brownfield specification excavation pattern | Document as guidance when demand arises from real initiatives |

---

## Roadmap Integration

### New Roadmap Items Proposed

| ID | Description | Priority | Source Gaps |
|----|-------------|----------|-------------|
| **FR-014** | Prompt/model regression testing — add as Tier 3 test category and model-update trigger in healthcheck | High | AG-002 |
| **FR-015** | AI adoption maturity model — 4 levels tied to AIEOS adoption depth | Medium | AG-003, AG-007 |
| **FR-016** | Constraint library tool spec — queryable rejection patterns accessible via MCP | Medium | AG-004 |
| **FR-017** | AI pipeline observability guidance — LLM call tracing standards | Medium | AG-010 |
| **FR-018** | Review capacity estimation in WDD/PRK | Low | AG-008 |
| **FR-019** | Bootstrap file token budget recommendation | Low | AG-009 |

### Existing Roadmap Items Validated

| Existing ID | Validated By | Notes |
|-------------|-------------|-------|
| GAP-002 | AG-001 (P106, PR78) | Data privacy governance confirmed as high priority by multiple AI-Native SDLC items |
| GAP-005 | AG-005 (P102, P117) | Cost governance scope should extend to AI tooling costs, not just initiative costs |
| ECO-006 | AG-003 (P120, PR6c) | Governance Analytics project validated as addressing adoption quality measurement |
| ECO-001 | AG-011 (P145) | Schema project enables richer provenance tracking (model version, context hashes) |

---

## PA Thickening Analysis

The 21 GAP items above identify what's **missing**. This section analyzes the 143 PA (Partially Aligned) items — areas where AIEOS has a foundation but coverage is incomplete, indirect, or structural rather than explicit. These represent "thickening" opportunities: strengthening existing capabilities rather than building from scratch.

### Triage Methodology

PA items are categorized into three tiers:

| Tier | Definition | Action |
|------|-----------|--------|
| **Actionable** | AIEOS could address with spec edits, new guidance docs, or hard gate additions | Roadmap item created (AL-NNN) |
| **Advisory** | AIEOS could document as guidance without structural changes | Bundled into guidance documents |
| **Structural** | AIEOS addresses through design; making explicit would be over-engineering | No action — note for reference only |

### AL-001: Agent Security Hardening

**Priority:** High | **Effort:** Medium | **Sources:** P49, P50, P51, P55, P87, PA16, PA18, PR20, PR21, PR22

AIEOS has strong structural security (SCK, adapter conformance, session separation) but doesn't explicitly govern agent-specific attack surfaces.

| PA Item | Current State | Proposed Thickening |
|---------|--------------|---------------------|
| P49 | Four-file separation mitigates instruction/content confusion | Add prompt injection defense section to SCK TM spec — require threat surface analysis for agent input parsing |
| P50, PA18 | DAR governs dependencies; adapter spec requires health checks | Add agent tool/plugin verification requirements to DAR spec — signed registries, hash verification for MCP servers |
| P51 | ER and journal are append-only; frozen artifacts immutable | Add memory poisoning as a named threat category in TM spec template |
| P55 | Convergence loop bounds iterations; escalation exists | Add agent compromise detection patterns to TM spec — cost anomaly, output drift, scope creep as signals |
| P87 | Adapter conformance provides governed channels | Add shadow agent governance section to tool-governance-spec — sanctioned vs unsanctioned agent classification |
| PA16, PR21 | Auth externalized in adapter spec | Add task-scoped permission model to adapter conformance — time-bounded tokens, minimum-privilege per operation |
| PR20 | SCK TM governs threat modeling generically | Add OWASP Agentic AI Top 10 as a recommended framework reference in TM spec |
| PR22 | Tool governance and DAR exist | Add MCP server validation checklist to DAR spec or as new tool-governance appendix |

### AL-002: AI-Generated Code Testing Standards

**Priority:** High | **Effort:** Medium | **Sources:** P111, P112, PA9, PR7, PR8, PR9, PR9a, PR9c, PR40

AIEOS governs test design (TDD spec) and code quality (code-craftsmanship.md) but doesn't have AI-specific testing gates.

| PA Item | Current State | Proposed Thickening |
|---------|--------------|---------------------|
| P111 | TDD spec governs test design with hard gates | Add `ai_output_verification` dimension to TDD spec — behavioral verification, property-based testing as named strategies |
| P112, PR9c | Execution spec includes test review checks | Add hard gate to execution-spec: "AI-generated tests reviewed for false confidence" — tests must demonstrate failure capability |
| PA9, PR8 | code-craftsmanship.md establishes linting standards | Promote linting enforcement from advisory to execution-spec review check with strictness tier (warn → error) |
| PR7 | PRK provides AI-augmented review | Add AI code quality scanning as an optional QAK VP test dimension for P1/P3 presets |
| PR9 | QAK VP defines test dimensions generically | Add bias testing and stress testing as named optional VP dimensions |
| PR9a | SCK SAR governs security assessment | Add SAST/DAST as a recommended SAR activity for code-producing initiatives |
| PR40 | code-craftsmanship.md addresses testing philosophy | Add anti-mocking guidance to code-craftsmanship.md §testing — prefer real implementations for integration boundaries |

### AL-003: Agent Readiness & Delegation Framework

**Priority:** Medium | **Effort:** Medium | **Sources:** PA3c, PA3d, PA10, PA15b, PA15d, PA19b, PR3, P148, P149, P150

AIEOS assigns AI/Human/Either per WDD task but doesn't have a systematic agent capability assessment.

| PA Item | Current State | Proposed Thickening |
|---------|--------------|---------------------|
| PA3c | WDD Assignee Type per task | Add organizational capability map as optional EEK input — classify capabilities as agent-ready, augmented, or human-only |
| PA3d, PA15d | Specs encode constraints; principles encode values | Add delegation framework guidance to tool-governance-spec — authorization scope, constraint depth, escalation triggers per agent role |
| PA10, PR3 | Healthcheck Scope A assesses framework readiness | Add codebase agent readiness checklist to getting-started.md — build passes, tests green, linting configured, dev env documented, CLAUDE.md present |
| PA15b | Specs define implicit capability frontier | Add expert frontier mapping as optional WDD annotation — mark per-task whether AI is proven, experimental, or unsuitable for this task type |
| PA19b | Layer model maps to DevSecOps lifecycle | Add explicit DevSecOps mapping to layer-model.md as a cross-reference table |
| P148 | Session separation provides independent assessment | Document dual-validation as guidance: when high-risk artifacts warrant two independent AI assessments |
| P149 | Completeness score provides confidence signal | Add confidence-gated automation guidance to convergence loop doc — when completeness_score < threshold, require human review even if all gates pass |
| P150 | Convergence loops bound execution | Add sandboxed execution guidance to QAK playbook — pre-release environment verification for code-producing initiatives |

### AL-004: Knowledge Currency & Documentation Lifecycle

**Priority:** Medium | **Effort:** Low | **Sources:** P151, P153, PA41, PR66, PR81, PR82

DKK governs document health but lacks specific automation and lifecycle practices.

| PA Item | Current State | Proposed Thickening |
|---------|--------------|---------------------|
| P151, PR82 | DKK DHR provides periodic review | Add AI-assisted documentation audit as a DHR operational mode — compare docs against system state, flag stale content |
| P153 | Healthcheck playbook defines audit schedules | Add monthly AI doc audit as recommended DHR cadence for active systems (supplement semi-annual minimum) |
| PA41 | EEK Path B handles brownfield entry | Add brownfield specification excavation pattern to getting-started.md — document existing → capture constraints → generate scenarios → incrementally formalize |
| PR66 | Getting-started and playbooks serve partially | Add "What Works Here" living document recommendation to getting-started.md — team-maintained lessons learned per initiative |
| PR81 | DKK DHR governs health reviews | Add freshness_owner and review_date as recommended metadata fields in UDR and ARR templates |

### AL-005: Process & Workflow Hardening

**Priority:** Medium | **Effort:** Medium | **Sources:** P124, P129, P133, PA12, PA35, PR10, PR13a, PR53, PR60, PR87, P43, PR80

AIEOS has strong process governance but gaps in specific operational practices.

| PA Item | Current State | Proposed Thickening |
|---------|--------------|---------------------|
| P124 | Lifecycle states include Deprecated | Add prompt deprecation lifecycle section to spec-file-standard.md — version, deprecation notice, migration path, sunset date |
| P129 | Initiative presets provide graduated complexity | Add staged adoption methodology to getting-started.md — Crawl (P5 preset) → Walk (P2 preset) → Run (P1 preset) with readiness criteria between stages |
| P133 | PINFK governs infrastructure decisions | Add IaC quality gate recommendations to PINFK ISPEC spec — kubeval/helm lint equivalents as named verification steps |
| PA12 | QAK provides pre-release testing | Add sandbox review environment as optional QAK VP dimension — reviewers interact with running system, not just artifacts |
| PA35 | AIEOS is session-based by design | Document session-based vs always-on as an explicit architectural decision in philosophy.md |
| PR13a | REK RP includes exposure strategy | Add canary deployment as a named RP exposure pattern for AI-generated code changes |
| PR60 | EEK playbook requires regression checks | Strengthen to: regression test creation is mandatory immediately after bugfix execution (not just check existing tests) |
| PR80 | QAK provides pre-release gate | Add dry-run mode recommendation to QAK playbook — new agent workflows run in observation mode before full deployment |
| PR87 | Freeze points are natural stopping points | Add explicit cognitive recovery guidance to EEK playbook — recommended break after complex artifact validation sequences |
| P43 | EEK Path B handles brownfield | Add brownfield governance pattern reference to initiative-presets.md P2 (Enhancement) notes |

### AL-006: Enterprise Integration Readiness

**Priority:** Medium | **Effort:** Low | **Sources:** P108, P109, P110, P139, P146, PA6a, PA6b, PA6d, PR64

Integration architecture is defined but lacks explicit protocol mappings and interop standards.

| PA Item | Current State | Proposed Thickening |
|---------|--------------|---------------------|
| P139 | AIEOS partially maps to NIST AI RMF | Add NIST AI RMF cross-reference appendix to governance-model.md — GOVERN/MAP/MEASURE/MANAGE mapped to AIEOS components |
| PA6a, PA6b | Sherpa orchestrates, kit prompts specialize | Add agent interop guidance to adapter-conformance-spec — A2A/JSON-RPC compatibility notes, agent card format recommendation |
| PA6d, P109 | Adapter conformance is MCP-compatible | Add MCP as a recommended (not required) integration protocol in adapter-conformance-spec, preserving tool-agnostic principle |
| P146 | Navigation map is a directed graph | Add W3C PROV compatibility note to ER spec — entity-activity-agent mapping for audit-intensive environments |
| PR64 | Tool governance and adapter conformance exist | Add shared tool catalog pattern to tool-governance-spec — registry of governed tools with capability descriptions, discoverable by agents |

### AL-007: Memory Architecture Formalization

**Priority:** Low | **Effort:** Medium | **Sources:** P8, P57, P60, P62, P64, PA4, PA24, PA25, PA27

AIEOS has emergent memory architecture across ER, frozen artifacts, journal, and artifact store. Formalizing it would help consuming projects design their memory systems.

| PA Item | Current State | Proposed Thickening |
|---------|--------------|---------------------|
| P62, PA24 | Memory distributed across ER, journal, artifacts, store | Add memory architecture guidance document — name the five layers (session, cross-session, canonical, operational, index) and map to AIEOS components |
| PA25 | Frozen artifacts are canonical facts | Add canonical fact identification to ER — which artifact sections constitute organizational facts vs implementation decisions |
| PA4 | Sherpa maintains context through ER/journal | Add context compression protocol to briefing-distillation-spec — structured summarization at session boundaries, not just artifact distillation |
| P57, PA27 | Frozen artifacts on disk mitigate memory wall | Add memory architecture recommendations to philosophy.md — "persist on disk, recall on demand" as an explicit design principle |
| P60 | IEK feedback loop governs maintenance | Add generation-vs-maintenance quality distinction to code-craftsmanship.md — different review criteria for new code vs modifications |
| P64 | Auto-recall is sherpa-specific | Add pre-generation context assembly as a framework-level recommendation (not just sherpa behavior) |

### AL-008: Organizational AI Alignment

**Priority:** Low | **Effort:** Low | **Sources:** P20, P25, P27, P33, P35, P36, P37, P38, P85, P86, P88, P89, P98, P154, P155, P157, PA15a, PA15c, PR19b, PR19d, PR19f, PR30, PR31, PR50, PR52, PR97, PR98

This is the largest PA cluster (27 items) but the least actionable for a governance framework. These items are about organizational behavior, cognitive skills, and human factors — areas where AIEOS provides structural support but can't (and shouldn't) try to govern human behavior.

**Proposed action:** Single guidance document rather than spec changes.

| Theme | Items | Proposed Guidance |
|-------|-------|-------------------|
| Senior role redefinition | PR97, PR98, P157, P158 | Add "The AI-Era Senior Engineer" section to philosophy.md — spec authoring as constraint building, PRK as taste encoding, freeze as stewardship |
| Cognitive load management | P154, P155, PR87 | Add cognitive load advisory to EEK playbook — validation fatigue is real, schedule breaks, rotate reviewers |
| Working modes | PA15a | Add centaur/cyborg mode descriptions to getting-started.md — AIEOS supports both, here's when each applies |
| Organizational adoption | P129, PR50, PR52, P24, P25 | Addressed by staged adoption in AL-005 and UX-001 onboarding guide |
| Skill development | P20, P27, P33, P35, P36, P37, P38, PA15c | Outside governance scope — note as potential companion document "AIEOS Practitioner Skills Guide" |
| Feedback and reflection | PR19d, PR19f, PR30, PR31 | Partially addressed by finding accumulator and sherpa journal; add "share findings across initiatives" guidance to ER spec |
| Intent alignment | P85, P86, P88, P89 | Partially addressed by principles files as intent infrastructure; add cross-reference to AI-Native SDLC intent framework in philosophy.md |

### PA Items Requiring No Action (Structural)

These PA items are scored PA because AIEOS addresses them through fundamental design rather than explicit governance. Making them explicit would add documentation overhead without improving outcomes:

- **P13** (training-time contribution) — outside AIEOS scope by design
- **P79** (implementation gap) — demonstrated by aieos-console, not a governance concern
- **P84** (organizational politics as bad context engineering) — philosophical framing, not governance
- **P91** (AI as mirror/amplifier) — implicit in validator pattern
- **P93** (friction shifts) — architectural observation
- **P94** (control system velocity) — healthcheck playbook addresses operationally
- **P95** (synchronous AI use) — AIEOS supports both modes already
- **P100** (context windows not retrieval) — ecosystem project concern (ECO-003)
- **P143** (centralized vs federated) — hybrid model already works
- **PA3g** (VSM) — layer model IS a value stream map
- **PA3h** (augment vs evolve) — both paths supported
- **PA19f** (dark factory) — aspirational, not current governance need
- **PA37** (four-role session prompting) — structural analog already exists
- **PR5** (film review loops) — sherpa self-scoring addresses
- **PR14** (reduce human input to single action) — sherpa behavior, not framework spec
- **PR17b** (sandbox copy) — QAK addresses
- **PR36** (verify memory retrieval) — integration tests address
- **PR41** (strictest linting) — code-craftsmanship addresses
- **PR45** (personal context layer) — outside framework scope
- **PR53** (frequent commits) — git practice, not governance
- **PR56** (start fresh when stuck) — convergence stopping rules address
- **PR57** (ask explanation before fix) — elicitation protocol addresses
- **PR58** (which version?) — spec versioning addresses
- **PR76** (kill switch) — convergence loop max iterations addresses

### Summary: PA Thickening Roadmap

| ID | Theme | Items | Priority | Effort | Key Deliverable |
|----|-------|-------|----------|--------|-----------------|
| AL-001 | Agent Security Hardening | 10 PA items | High | Medium | TM spec + DAR spec + adapter-conformance updates |
| AL-002 | AI-Generated Code Testing | 11 PA items | High | Medium | TDD spec + execution-spec + code-craftsmanship updates |
| AL-003 | Agent Readiness & Delegation | 10 PA items | Medium | Medium | Tool-governance + getting-started + WDD updates |
| AL-004 | Knowledge Currency | 6 PA items | Medium | Low | DKK template + getting-started updates |
| AL-005 | Process & Workflow Hardening | 12 PA items | Medium | Medium | Multiple spec + playbook updates |
| AL-006 | Enterprise Integration | 9 PA items | Medium | Low | Adapter-conformance + governance-model updates |
| AL-007 | Memory Architecture | 8 PA items | Low | Medium | New guidance doc + philosophy.md update |
| AL-008 | Organizational AI Alignment | 27 PA items | Low | Low | Philosophy.md + getting-started updates |

**Total:** 8 thickening work packages covering 93 actionable PA items. 24 PA items require no action (structural). Combined with 12 GAP items (AG-001 through AG-012) and 6 proposed framework items (FR-014 through FR-019), the full alignment improvement backlog contains **26 work items**.

---

## Methodology Notes

### Assessment Parameters
- **Scope:** AIEOS framework design + construction process (aieos-console as case study)
- **Granularity:** Every individual P/PA/PR item scored
- **Scale:** 4-point (FE / PA / GAP / N/A)
- **Conservative scoring:** PA preferred over FE when evidence is circumstantial; GAP preferred over N/A when AIEOS could reasonably address the concern

### Assessor Bias Acknowledgment
AIEOS was designed and built by the assessor. This creates inherent positive bias. Mitigations applied:
- FE requires a citable file path — "implied by design" is insufficient
- PA preferred over FE when evidence is indirect or structural rather than explicit
- GAP preferred over N/A for items AIEOS could reasonably address
- Evidence channel codes required for every score

### Limitations
- Assessment reflects AIEOS state as of 2026-03-24
- AI-Native SDLC v3.1 was extracted from .docx; table formatting may have been lost
- Some practices sections (3.19-3.25) contain items highly specific to Kubernetes/GitOps platform engineering — scored N/A where clearly out of AIEOS governance domain
- The document numbers P1-P158 but practices skip PR88-PR96 — total scored items may be less than 335

### Source Document
AI-Native SDLC: Principles, Patterns & Practices v3.1 (March 2026). 45 sources, 158 Principles, 66 Patterns, 111 Practices, 39 Clusters. Author: Todd (curated with Claude).
