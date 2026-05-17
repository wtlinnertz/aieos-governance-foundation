# Your first AIEOS initiative

A step-by-step tutorial for creating your first governed initiative. By the end, you'll have produced real artifacts: structured documents that capture product intent, validate against quality gates, and prepare for engineering execution.

This tutorial uses the **P2 Enhancement** preset with a concrete example: adding dark mode to an existing web application.

For reference documentation (not a tutorial), see [getting-started.md](getting-started.md).

## Before you start (5 minutes)

### What is AIEOS?

AIEOS is a structured way to move from "I have an idea" to "this is ready to build" using a series of documents called artifacts. Each artifact captures one decision: what the problem is, what the requirements are, how the architecture works, what the test plan looks like. An AI assistant generates these artifacts from your answers, and each passes through quality checks (gates) before the next step. The result is a clear, auditable trail from idea to production.

### What you'll build

A governed set of artifacts for adding dark mode to a web application:

- Kit Entry Record (KER): proves this work is real, scoped, and approved
- Product Requirements Document (PRD): defines what "dark mode" means in measurable terms
- **Architecture Context File (ACF)** and **Solution Architecture Document (SAD)**: define how the system implements it

These are the first four artifacts in the engineering execution pipeline. The tutorial covers them in detail, then points you to the remaining steps.

### What you need

- An AI assistant with file access (e.g., Claude Code with the AIEOS framework directory available)
- The AIEOS framework directory on your machine
- A project directory where your artifacts will be created

### Time estimate

2-4 hours for the full walkthrough. Each part lists its own estimate so you can take breaks.

## Part 1: routing (10 minutes)

### Start the sherpa

Open your AI assistant and type:

```
/sherpa I want to add dark mode to our web app
```

The sherpa is an AI guide built into the AIEOS framework. It reads the framework's navigation map and helps you figure out where to start, what to do next, and whether you are on track.

### What the sherpa asks

The sherpa's first job is intent resolution: figuring out what kind of work this is. It'll ask questions like:

- "Does this capability exist today, or is it entirely new?"
- "Is the problem and solution well understood, or does it need discovery?"
- "Is this driven by a compliance mandate, an incident, or a product decision?"

### Your answers map to a preset

For dark mode, your answers will be something like:

- "This is an improvement to our existing app: we are adding a feature to the UI."
- "We know what we want: a theme toggle, system preference detection, and persistent preference."
- "This is a product decision, not compliance or incident-driven."

The sherpa maps this to Preset 2: Enhancement with EEK Path B (direct entry to the Engineering Execution Kit, no discovery). Path B is right when the team can state the problem, solution space, and acceptance criteria without discovery.

### What gets created

The sherpa creates your project scaffolding:

- A project directory for your initiative
- An Engagement Record (ER): a tracking document that follows your initiative across all layers
- A Sherpa Journal: a log of decisions, position checks, and routing choices

### Checkpoint

Verify you have:

- [ ] An Engagement Record with status "Active" and preset "P2 Enhancement"
- [ ] A sherpa journal with the routing decision logged

## Part 2: kit entry (10 minutes)

### What is KER?

The Kit Entry Record is a lightweight gate that must be completed before generating artifacts. It proves four things: the work is real (not speculative), scoped (not unbounded), prioritized (someone approved it), and has a clear entry path.

Think of it as the bouncer at the door: it keeps unvetted work from consuming engineering time.

### Fill in each section for dark mode

**Document Control:**
```
Record ID: KER-DARKMODE-001
Date: 2026-03-27
Initiated By: Your Name
Work Summary: Add light/dark/system theme support to the web application UI
```

**Classification Check:**
```
[x] No classification record: Justification: Enhancement to existing UI;
    scope is bounded and well-understood. No competing sourcing options.
```

You don't need a Work Classification Record (WCR) for a straightforward enhancement. The justification must be specific: "N/A" or "skipped" would fail the gate.

**Entry Path:**
```
[x] Path B: Direct Entry
    Work type: Other: Enhancement
    Problem statement: Users cannot customize visual appearance, causing
    accessibility issues in low-light environments.
```

Path B means you are entering the Engineering Execution Kit directly, without running the Product Intelligence Kit's discovery process first.

**Priority:**
```
Priority justification: Approved in sprint planning 2026-Q1. Accessibility
improvement aligns with Q1 UX objectives.
```

**Scope:**
```
In scope: Theme toggle component, CSS variable system, system preference
detection, preference persistence.

Out of scope: Custom color palettes, per-user theme creation,
per-element theming, animated transitions between themes.
```

The out-of-scope list is just as important as the in-scope list. It prevents scope creep before it starts.

### Validate

Run the KER through the validator. It checks 5 hard gates:

| Gate | What it checks | Dark mode result |
|------|---------------|-----------------|
| `document_control` | All metadata fields present and formatted | PASS: ID, date, author, summary all present |
| `classification_check` | Either a WCR reference or a specific justification | PASS: justification explains why WCR is unnecessary |
| `path_selected` | Exactly one entry path selected with required fields | PASS: Path B selected with problem statement |
| `priority_on_record` | Priority justification is specific, not generic | PASS: references sprint planning and Q1 objectives |
| `scope_bounded` | Both in-scope and out-of-scope are stated | PASS: 4 items in, 4 items out |

### Freeze

When all 5 gates pass, the KER is frozen. Freezing means the document is now immutable: it becomes the official record that downstream artifacts depend on. If you need to change a frozen artifact later, there's a formal process (impact analysis and re-entry).

### Checkpoint

- [ ] KER-DARKMODE-001 frozen with all 5 gates passing
- [ ] Engagement Record updated with KER artifact ID

## Part 3: product requirements (20 minutes)

### What does the PRD do?

The PRD turns "add dark mode" into structured, measurable requirements. It defines what to build and why, not how. Architecture and implementation decisions come later, in separate artifacts. This separation prevents solution bias from contaminating the problem definition.

### Product brief: the sherpa asks questions

For Path B, the sherpa collects your input through a **Product Brief**: an intake form that captures the raw information needed to generate a PRD. The sherpa will walk you through each section with targeted questions.

**Problem Statement:**

Sherpa asks: "What problem are you solving, and who experiences it?"

Your answer: "Users cannot customize the visual appearance of our web app. This causes accessibility issues for users in low-light environments and does not meet modern UX expectations. We have received 47 support tickets about eye strain in the last quarter."

**Goals:**

Sherpa asks: "What does success look like? How will you measure it?"

Your answer:
- "G-1: Support light, dark, and system-preference themes with less than 100ms switching time."
- "G-2: Reduce eye-strain support tickets by 60% within 90 days of release."

**Non-Goals:**

Sherpa asks: "What is explicitly excluded from this work?"

Your answer: "Custom color palettes, per-element theming, animated transitions between themes, third-party theme marketplace."

**Requirements:**

Sherpa asks: "What must the system do? Be specific: each requirement gets an ID."

Your answer:
- "FR-1: Theme toggle in the settings panel. Acceptance: user can switch between light, dark, and system modes."
- "FR-2: System preference detection. Acceptance: app defaults to the OS theme on first visit."
- "FR-3: Persist preference in localStorage. Acceptance: theme survives browser restart."
- "NFR-1: Theme switch completes in under 100ms with no visible flash of unstyled content."

**Constraints:**

Sherpa asks: "What hard guardrails must the solution respect?"

Your answer: "Must work with existing Tailwind CSS setup. No new runtime dependencies. Must not break existing component tests."

### PRD generated

The sherpa generates a full PRD from your Product Brief answers. The PRD follows a fixed template with 12 required sections (Document Control through Freeze Declaration). You review it, correct any misinterpretations, and validate.

### Validation: the 6 gates explained

The PRD validator checks 6 hard gates. Here is what each one means for your dark mode PRD:

| Gate | What it checks | Dark mode example |
|------|---------------|------------------|
| `problem_definition` | Clear problem, identified users, rationale for "why now" | "Users cannot customize..." with 47 support tickets as rationale. PASS. |
| `goals` | Goals are measurable outcomes, not vague aspirations | "G-1: <100ms switching" is measurable. "Make it look better" would FAIL. |
| `scope` | Non-goals stated, boundaries clear | "Custom palettes" excluded explicitly. PASS. |
| `requirements` | Each requirement has an ID and acceptance criteria | FR-1, FR-2, FR-3, NFR-1 all have IDs and criteria. PASS. |
| `constraints` | Specific, enforceable guardrails | "Tailwind CSS, no new dependencies" is specific. "Must be performant" would FAIL. |
| `readiness` | No unresolved blocking questions | Open questions section is empty or non-blocking. PASS. |

### What happens on FAIL

If any gate fails, the validator returns a FAIL status with a description of the issue and its location in the document. The sherpa explains what went wrong in plain language and helps you fix it.

Example: if your problem statement said "make the UI better" instead of identifying a specific problem and affected users, the `problem_definition` gate would FAIL. The validator would report:

```json
{
  "status": "FAIL",
  "hard_gates": { "problem_definition": "FAIL" },
  "blocking_issues": [{
    "gate": "problem_definition",
    "description": "No specific problem identified. No users named.",
    "location": "§2 Problem Statement"
  }]
}
```

You fix the problem statement, regenerate or edit the PRD, and validate again. The framework allows up to 3 automatic retry attempts (a convergence loop) before escalating for human review.

### Freeze PRD

When all 6 gates pass, freeze the PRD. It is now the official requirements document that architecture will be built against.

### Checkpoint

- [ ] PRD-DARKMODE-001 frozen with all 6 gates passing
- [ ] Engagement Record updated with PRD artifact ID
- [ ] 2 frozen artifacts total (KER + PRD)

## Part 4: architecture (20 minutes)

### ACF intake

The next step is the Architecture Context File (ACF): an intake form where you provide the technical constraints and organizational standards that architecture must respect. The sherpa asks:

- "What is your tech stack?" React 18, Tailwind CSS 3.x, Vite build system
- "What are your deployment constraints?" Static hosting, CDN-cached assets
- "What persistence options are available?" localStorage for client-side, no server-side user preferences yet
- "Are there organizational standards?" Component library uses Tailwind utility classes; no CSS-in-JS

The ACF captures these answers in a structured format and is validated and frozen.

### SAD generation

With the frozen PRD and ACF, the sherpa generates the Solution Architecture Document (SAD). For dark mode, this might include:

- ThemeProvider component: React context provider managing current theme state
- CSS variable system: Theme tokens as CSS custom properties, switched by a data attribute on the root element
- Storage adapter: Abstraction over localStorage for persistence, enabling future server-side migration
- System preference listener: `prefers-color-scheme` media query listener that updates theme on OS change

### Key architecture decisions

The SAD documents decisions with rationale: not just what was chosen, but why alternatives were rejected:

- CSS variables vs. class toggling: CSS variables enable runtime switching without re-rendering the component tree. Class toggling would require Tailwind's `dark:` variant on every element.
- localStorage vs. server-side: localStorage chosen for simplicity and offline support. Server-side persistence listed as a future enhancement (out of scope per PRD).

### Validation

The SAD validator checks its own set of hard gates, including:

- `component_inventory`: Every component is listed with its responsibility
- `decision_rationale`: Every architectural decision has a stated rationale
- `failure_modes`: The document identifies what happens when things go wrong (e.g., localStorage unavailable, system preference API unsupported)

### Freeze ACF + SAD

Per the flow reference, ACF and SAD can be frozen in parallel once both pass validation.

### Checkpoint

- [ ] ACF-DARKMODE-001 frozen
- [ ] SAD-DARKMODE-001 frozen
- [ ] Engagement Record updated with ACF and SAD artifact IDs
- [ ] 4 frozen artifacts total (KER, PRD, ACF, SAD)

## Part 5: what's next (5 minutes)

### Remaining EEK artifacts

You've completed the first four artifacts in the Engineering Execution Kit. The remaining EEK artifacts follow the same pattern: intake, generation, validation, and freeze.

1. **DCF** (Design Context File): design standards, component patterns, and code conventions
2. **TDD** (Technical Design Document): translates architecture into implementation-level design
3. **WDD** (Work Decomposition Document): breaks TDD into work items with acceptance criteria
4. **Execution Plan**: orders work items and defines implementation sequence
5. **Code execution**: tests, implementation, and review for each work item
6. **ORD** (Operational Readiness Document): proves the system is ready for release

### After EEK: cross-cutting decisions

Once the ORD is frozen, you decide which cross-cutting kits apply:

- **QAK** (Quality Assurance Kit): Do you need a formal testing gate before release? Optional for enhancements.
- **DKK** (Documentation & Knowledge Kit): Does dark mode change user-visible behavior that needs docs?
- **SCK** (Security & Compliance Kit): Does dark mode touch security-sensitive paths? Probably not for a UI theme.

### Then: release through feedback

- **REK** (Release & Exposure Kit): governs release process, rollout plan, and release record
- **RRK** (Reliability & Resilience Kit): monitors the release in production, tracks SLOs
- **IEK** (Insight & Evolution Kit): captures what you learned and feeds it back into future planning

### How to resume

If you step away and come back later, tell the sherpa:

```
/sherpa Resume my dark-mode initiative
```

The sherpa reads your Engagement Record and artifacts to determine exactly where you left off. It doesn't rely on memory.

### Where to get help

- [getting-started.md](getting-started.md): reference guide organized by scenario
- Each kit's `docs/playbook.md`: per-artifact detail and process definition
- [initiative-presets.md](initiative-presets.md): the 5 golden paths with full artifact sequences
- `aieos-governance-foundation/examples/taskflow-full-flow/`: a complete worked example across multiple kits

---

## Appendix a: common questions

**"What if I get stuck?"**
Ask the sherpa: `/sherpa Where am I?` The sherpa runs a position check by reading your files, not memory, and tells you exactly which artifact is next and what it needs.

**"What if a gate keeps failing?"**
The framework runs a convergence loop: up to 3 automatic attempts to fix the issue based on feedback. If it still fails after 3 attempts, the issue escalates for human review. The validator tells you exactly which gate failed and where in the document.

**"Can I skip artifacts?"**
No. Freeze-before-promote is a non-negotiable rule. Each artifact depends on the one before it being frozen. Skipping creates gaps that compound downstream: a PRD without a KER means unvetted work enters the pipeline; a SAD without a frozen PRD means architecture built on unstable requirements.

**"Can I change a frozen artifact?"**
Yes, but through a formal process. You run impact analysis to identify affected downstream artifacts, then follow the re-entry protocol. This is intentionally deliberate: it prevents casual changes from silently breaking downstream work.

**"How long does a full initiative take?"**
For a P2 Enhancement like dark mode: 8-20 hours depending on complexity, spread across sessions. The EEK phase (KER through ORD) is typically 4-10 hours. Release and monitoring add another 4-10 hours.

**"What if I'm not technical?"**
The sherpa explains everything in plain language. You provide domain knowledge (what the problem is, who it affects, what success looks like). The AI handles structural formatting, gate checking, and artifact generation. Many artifacts (like KER, Product Brief, and PRD) are primarily product decisions.

## Appendix b: all 5 presets at a glance

**P1: New Feature**: Use when building a capability that doesn't exist today. Starts at PIK (Layer 2) with full discovery: problem framing, value hypothesis, assumption testing, and experiment log before engineering. Produces 15-20+ artifacts across all layers. Typical time: 20-40 hours.

**P2: Enhancement**: Use when improving an existing capability where the problem and solution are well understood. Starts at EEK (Layer 4, Path B), skipping discovery. Produces 8-12 artifacts in EEK plus release artifacts. Typical time: 8-20 hours. This is the preset used in this tutorial.

**P3: Compliance and Regulatory**: Use when work is driven by an external mandate (regulation, audit finding, legal obligation). Starts at PIK with compliance-specific intake. SCK artifacts are required, not optional. Produces 15-20+ artifacts with compliance evidence throughout. Typical time: 20-40 hours.

**P4: Performance and Reliability Fix**: Use when fixing a performance issue, SLO violation, or reliability problem. Entry point varies: incident-triggered at ODK (Layer 8), RHR-triggered at RRK (Layer 6), proactive at PIK. Produces 8-15 artifacts depending on trigger. Typical time: 8-20 hours.

**P5: Exploratory Research**: Use when investigating whether a capability is worth building. Starts at PIK with open-ended discovery. May end at the Experiment Log with a "no build" conclusion (that's a valid outcome). Produces 5-8 PIK artifacts; downstream kits only if research leads to build decision. Typical time: 10-20 hours.

## Appendix c: glossary

**Artifact**: A structured document capturing a specific decision or piece of knowledge. Examples: PRD (requirements), SAD (architecture), WDD (work breakdown). Each artifact follows a fixed template and passes through quality gates before use downstream.

**Freeze**: Making an artifact immutable. Once frozen, it becomes the official record that downstream artifacts depend on. Changes require formal impact analysis and re-entry.

**Gate**: A specific quality check that an artifact must pass during validation. Each gate evaluates one aspect (e.g., "are goals measurable?" or "is scope bounded?").

**Hard gate**: A gate where failure means the entire artifact fails validation. No partial credit: every hard gate must pass for the artifact to be frozen.

**Validator**: The quality judge for an artifact type. It evaluates the artifact against hard gates in the spec and produces PASS or FAIL. Validators judge only; they never suggest improvements.

**Kit**: A self-contained package governing one organizational layer. Each kit contains specs, templates, prompts, and validators for its artifact types, plus a playbook defining the process. Example: the Engineering Execution Kit (EEK) governs Layer 4.

**Layer**: One level in the AIEOS framework. Layers are numbered 1-15 and fall into three categories: pipeline layers (sequential value delivery), operational track (reactive incident response), and cross-cutting governance (quality, security, documentation).

**Preset**: A predefined path through the framework for a common initiative type. There are 5 presets: New Feature, Enhancement, Compliance, Performance Fix, and Exploratory. Each specifies which kits and artifacts are required vs. optional.

**Engagement Record (ER)**: A tracking document following an initiative across all layers. Records which artifacts are frozen, which gates have passed, and key decisions made. The single source of truth for "where is this initiative?"

**Sherpa journal**: A log maintained by the AI sherpa recording routing decisions, position checks, and navigation choices. Unlike the ER (which tracks artifacts), the journal tracks conversation and reasoning.

**Convergence loop**: An automatic retry mechanism for failed validation. When an artifact fails a gate, the sherpa attempts to fix the issue and re-validate, up to 3 times. If it still fails, the issue escalates for human review.

**Cross-cutting kit**: A kit operating across multiple pipeline layers rather than at a single point. Examples: SCK (security) can trigger after architecture or after code; DKK (documentation) triggers after design or after release.

**Four-file system**: The structural rule that every artifact type has exactly 4 governing files: a spec (rules), template (structure), prompt (AI generation behavior), and validator (judgment criteria). This separation ensures rules live in one place and are never duplicated.

**Spec**: The authoritative source of rules for an artifact type. Defines required sections, content rules, and hard gates. Prompts and validators reference the spec; they never define their own rules.

**Template**: The structural skeleton for an artifact. Defines sections and their order. When generating an artifact, the AI fills in the template according to the spec's rules.

**Prompt**: The behavioral instructions for AI artifact generation. Tells the AI how to behave when generating a specific artifact type: what inputs to use, what tone to adopt, what to avoid. References the spec; never inlines rules.
