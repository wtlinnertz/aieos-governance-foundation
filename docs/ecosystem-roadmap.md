# AIEOS system Roadmap

This document captures the adjacent projects identified as high-value additions to the AIEOS system. AIEOS itself is a governance framework (all Markdown, no runtime). These projects would make that governance executable, observable, and measurable at organizational scale.

**Origin:** An "AIEOS Implementation Master Plan" proposed making AIEOS a software platform. That was rejected as architecturally incompatible (governance framework, not runtime system). Five ideas were extracted and implemented as governance enhancements (WS-1 through WS-5, 2026-03-16). The remaining ideas, plus newly identified gaps, form this roadmap.

**Relationship to AIEOS:** AIEOS defines *what* good looks like (specs, hard gates, decision tables). These projects *execute, observe, and measure* that definition. AIEOS remains the source of truth; system projects are consumers.

**Naming Convention:** AIEOS governance units use `aieos-{descriptor}-kit` (e.g., `aieos-peer-review-kit`). system software components use `aieos-{descriptor}` without the `-kit` suffix. The presence or absence of `-kit` distinguishes governance Markdown from software projects at a glance.

| Component | Repository | Type |
|-----------|-----------|------|
| Schema | `aieos-schema` | Software — machine-readable spec contracts |
| Evaluation Engine | `aieos-evaluation-engine` | Software — runtime governance enforcement |
| Artifact Store | `aieos-artifact-store` | Software — cross-initiative artifact indexing |
| Governance Analytics | `aieos-governance-analytics` | Software — cross-initiative intelligence |
| Compliance Reporter | `aieos-compliance-reporter` | Software — automated audit packages |
| System Twin | `aieos-system-twin` | Software — live system topology graph |
| Playground | `aieos-playground` | Software — interactive learning environment |
| Engineer Impact | `aieos-engineer-impact` | Documentation — quarterly engineer impact assessment framework |
| Agent Harness | `aieos-agent-harness` | Software — pluggable multi-agent orchestration engine |

---

## system map

```
                    ┌─────────────────────────────────┐
                    │   AIEOS Governance Framework     │
                    │   (what exists today - Markdown)  │
                    └──────────┬──────────────────────┘
                               │
                    ┌──────────▼──────────┐
                    │    AIEOS Schema     │ ◄── strengthens the framework itself
                    │  (machine-readable  │     (deeper Tier 2 tests, drift
                    │   spec contract)    │      detection, consistency checks)
                    └──────────┬──────────┘
                               │ unlocks
          ┌────────────────────┼────────────────────────┐
          ▼                    ▼                         ▼
   ┌──────────────┐    ┌──────────────┐    ┌──────────────────┐
   │  Evaluation   │    │ System Twin  │    │  Gov Analytics   │
   │  Engine       │◄──►│ (observe)    │───►│  (learn)         │
   │  (enforce)    │    └──────┬───────┘    └────────┬─────────┘
   └──────┬───────┘           │                      │
          │                   ▼                      ▼
          ▼            ┌──────────────┐    ┌──────────────────┐
   ┌──────────────┐    │ Artifact     │    │ Compliance       │
   │ Adapter SDK  │    │ Store        │    │ Reporter         │
   │ (integrate)  │    │ (index)      │    │ (audit)          │
   └──────────────┘    └──────────────┘    └──────────────────┘
```

Schema has a dual role: it strengthens the existing AIEOS framework (deeper testing, drift detection) AND unlocks all downstream system projects (machine-consumable specs).

---

## Critical path (Priority order)

### 1. AIEOS schema (`aieos-schema`)

**What:** A machine-readable format (YAML or JSON) that coexists alongside Markdown specs. Each spec's hard gates, required sections, and content rules become parseable by automated systems.

**Why first:** Schema serves two distinct purposes — it strengthens the existing AIEOS framework *and* unlocks the system projects. It's the keystone for both.

#### Value to the existing framework (Before any system project)

Today, AIEOS specs are Markdown prose. The four-file system works because AI reads the prose and applies judgment. But this creates gaps that Schema closes:

**Problem 1: Tier 2 tests can only verify structure, not semantics.**

The current test suite validates that a spec file exists and has a version field. It cannot validate what's *inside* the spec — how many hard gates, what sections are required, what field constraints apply. This means a spec could silently lose a hard gate (editing error, merge conflict) and no test would catch it.

With Schema: Tier 2 tests validate spec *content*. "prr-spec declares exactly 5 hard gates: lens_coverage, finding_actionability, conflict_surfacing, artifact_traceability, disposition_justified." A test fails if a gate is renamed, removed, or added without updating the schema.

**Problem 2: Template/spec drift is undetectable.**

A spec might require 7 sections, but the template could have 6 (or 8). Today, only a human reading both files side-by-side can catch the mismatch. The sherpa integration tests exercise full flows, but they run against one scenario — they don't systematically verify spec-template alignment across all 40+ artifact types.

With Schema: A Tier 2 test validates that every required section declared in the schema has a corresponding heading in the template. Drift is caught at the structural level, not the behavioral level.

**Problem 3: Validator/spec drift is undetectable.**

A validator prompt lists the gates it evaluates. If the spec renames a gate (e.g., `failure_mode_analysis` → `failure_mode_identification` as we did in WS-1), the validator prompt must be manually updated. Nothing enforces this.

With Schema: The validator references gate names from the schema. A test validates that every gate in the schema appears in the validator's evaluation procedure.

**Problem 4: Prompt self-review checklists can drift from specs.**

Generation prompts include a self-review checklist that's supposed to mirror the spec's hard gates. If a gate is added to the spec, the prompt checklist must be updated separately. Nothing enforces alignment.

With Schema: A test validates that the prompt's self-review checklist covers every hard gate declared in the schema.

**Problem 5: `framework.py` is manually maintained and can drift.**

The test model (`framework.py`) lists artifacts per kit, dependency edges, and preset definitions. These are manually synchronized with the actual kit specs. If a new artifact type is added to a kit (like SMR or RSA), `framework.py` must be updated separately.

With Schema: `framework.py` could be *generated* from schema files, or at minimum, a Tier 2 test could validate that `framework.py`'s artifact list matches the schemas that actually exist in each kit.

**Problem 6: AI interpretation variance.**

Different AI sessions may interpret the same Markdown spec differently. One validator session might accept "High" as matching "high" (the spec says "critical, high, medium, low" in prose). Schema makes the allowed values explicit and enumerated, reducing interpretation variance.

**Problem 7: Cross-file consistency checks require reading prose.**

To verify that a PRK lens spec's review points match the prr-spec's Review Point Mapping table, you currently need to read both Markdown files and compare. With Schema, both files declare their review point data in a parseable format, and a test validates consistency.

#### Concrete tier 2 test gains

With Schema in place, these tests become possible without any system project:

| Test | What it validates |
|------|-------------------|
| `test_schema_hard_gate_count` | Each schema declares the same number of hard gates as its Markdown spec |
| `test_template_sections_match_schema` | Every required section in the schema has a heading in the template |
| `test_validator_covers_all_gates` | Every hard gate in the schema is evaluated in the validator |
| `test_prompt_checklist_covers_gates` | The prompt's self-review checklist covers every schema gate |
| `test_framework_py_matches_schemas` | `framework.py` artifact lists match actual schema files per kit |
| `test_prk_review_points_consistent` | Lens specs' review points match the prr-spec schema's mapping table |
| `test_field_enum_values` | Template fields that have enumerated values (status, severity, criticality) match schema definitions |
| `test_provenance_fields_match_schema` | Document Control provenance fields match the schema's required provenance list |

This is 8+ new tests that validate *semantic correctness*, not just structural existence. The existing 90 tests verify the framework's skeleton; these would verify its muscles.

#### Value to system projects (After schema exists)

Everything downstream needs machine-readable specs to avoid building custom parsers:

- **Engine** consumes schemas to know what gates to evaluate, what sections to check, what fields to validate — without custom logic per artifact type
- **Artifact Store** uses schemas to parse artifact fields for indexing — service name, status, upstream references become queryable fields, not grep patterns
- **Analytics** uses schemas to normalize findings across artifact types — "how many hard gate failures across all QGRs this quarter?" requires knowing what a QGR's gates are
- **Compliance Reporter** uses schemas to map artifact sections to regulatory controls — "which AIEOS field satisfies SOC2 CC6.1?" requires knowing what fields exist

Building the Engine without Schema means building artifact-type-specific parsers for every spec — then rebuilding them when specs change. Schema makes the Engine generic.

#### Scope

- Schema format definition for specs (hard gates, required sections, content rules, field enumerations)
- Schema format for templates (required fields, field types, provenance requirements)
- Schema format for validator output (formalize the existing JSON contract)
- Schema format for tool specs (preconditions, postconditions, hard gates)
- Sync mechanism: Schema ↔ Markdown spec (one is generated from the other, or both are maintained with a consistency test)
- ~40 schema definitions (one per spec across all 15 kits plus governance-foundation tools)

**Size estimate:** Small-medium project. The format design is the hard part; the individual schemas are mechanical once the format is defined.

**Relationship to AIEOS:** Schema files would live alongside specs in each kit (e.g., `docs/specs/prd-spec.yaml` next to `prd-spec.md`). The governance model would need a new section on schema governance — versioning, sync with Markdown specs, and the rule that Schema and Markdown must agree (with a Tier 2 test enforcing it).

---

### 2. AIEOS evaluation engine (`aieos-evaluation-engine`)

**What:** A runtime system that consumes AIEOS schemas as evaluation rules, wraps existing tools (SAST, container scan, linters, test runners) via an Adapter SDK, and produces evidence in AIEOS normalized format.

**Origin:** Combines the Lens Engine concept (original plan §7) and Tool Adapter Specification (original plan §16). Filtered to remove autonomous promotion — the Evaluation Engine *produces evidence*, it doesn't *make deployment decisions*.

#### Value to the existing framework

Today, every AIEOS validation is performed by an AI session reading a spec and applying judgment. This works but has limitations:

**Problem 1: Evidence collection is manual.** When the sherpa generates a QGR (Quality Gate Record), it needs test results, coverage data, and security scan findings. Today, the human gathers this evidence and pastes it into the session. The Engine automates this — it runs the tools and produces normalized evidence that feeds directly into artifact generation.

**Problem 2: Validation is AI-interpreted, not deterministic.** Two different AI sessions may evaluate the same artifact against the same spec and reach different conclusions. The Engine provides deterministic checks for the subset of hard gates that are mechanically verifiable (field presence, format compliance, enumeration values), reserving AI judgment for semantic evaluation only.

**Problem 3: Tool governance has no runtime enforcement.** AIEOS has `tool-governance-spec.md` and `docs/bindings/` but these are documentation — nothing prevents a team from skipping the governed tool and using an ungoverned alternative. The Engine makes tool governance executable: if a spec requires a security scan, the Engine invokes the bound adapter.

**Problem 4: The sherpa can't observe real artifacts.** The sherpa generates and validates Markdown documents, but it can't run Semgrep against actual code, Trivy against a container, or pytest against a test suite. The Engine bridges this gap — it operates on real software artifacts and translates results into AIEOS evidence format.

#### Relationships to other system components

| Component | Relationship |
|-----------|-------------|
| **Schema** | Engine consumes schemas to know what gates to evaluate per artifact type. Without Schema, the Engine needs custom logic per spec. With Schema, it's generic. |
| **Adapter SDK** | Part of the Engine project. Adapters are how the Engine connects to external tools. Each adapter wraps one tool (Semgrep, Trivy, ESLint) and normalizes its output to AIEOS evidence format. |
| **Artifact Store** | Engine produces evidence artifacts that the Store indexes. Engine can also query the Store for upstream artifacts when evaluating downstream ones (e.g., "does this ORD reference a frozen SAD?"). |
| **Analytics** | Engine produces structured evaluation results (timestamps, gate results, finding counts) that Analytics mines for patterns. Engine is the primary data producer for Analytics. |
| **Twin** | Engine queries the Twin for real-time system context during evaluation. "Is this service currently healthy?" "What depends on it?" Twin provides the blast radius context that the RSA needs. |
| **Compliance Reporter** | Engine produces the evidence artifacts (SAR, DAR, QGR) that the Compliance Reporter assembles into audit packages. Automated evidence collection means compliance packages are always current. |
| **Playground** | Engine could power the Playground's "real feedback" mode — instead of simulated validation, the Playground runs actual Engine checks against practice artifacts. |
| **AIEOS Framework** | The Engine is governed by AIEOS. AIEOS `tool-governance-spec.md` governs the Engine itself. Each adapter has a bindings file in the consuming kit. The Engine doesn't replace the sherpa — it automates evidence collection that the sherpa and human currently do manually. |

#### Scope

**Engine:**
- Artifact detection (PR opened, build completed, container pushed, deploy triggered)
- Schema-driven evaluation routing (artifact type → applicable specs → required gates)
- Tool invocation via adapter interface
- Result normalization to AIEOS findings format
- Policy evaluation (hard gate pass/fail → decision outcome per taxonomy)
- Evidence artifact production (feeds into QGR, RSA, SAR workflows)

**Adapter SDK:**
- Three-method interface: `configure()`, `execute()`, `normalize()`
- Reference adapters for common tools (Semgrep, Trivy, ESLint, pytest, SonarQube)
- Evidence schema matching AIEOS validator JSON output format
- Adapter testing harness (given this input, expect this normalized output)

---

### 3. AIEOS artifact store (`aieos-artifact-store`)

**What:** An indexing and query layer over AIEOS artifacts across all initiatives. Enables search, lineage tracing, cross-referencing, and dependency analysis.

#### Value to the existing framework

Today, AIEOS artifacts are Markdown files in git directories. The ER (Engagement Record) serves as the per-initiative index. This works for small scale but creates real problems:

**Problem 1: Cross-initiative queries are impossible.** "Show me every SAD that references Kafka" requires grepping across dozens of project directories. "Which initiatives had PRK findings about blast radius?" requires reading every PRR manually.

**Problem 2: Impact analysis is manual.** When a frozen ISPEC changes (new version), the impact analysis question is "which initiatives reference this ISPEC?" Today, that requires searching every ER across every project. The Store makes this a query.

**Problem 3: The sherpa loses context between sessions.** When the sherpa resumes an initiative, it reads the ER and local artifacts. But it can't see related initiatives — "the team's last three SADs all failed the security lens on first pass" is organizational knowledge that no single ER contains.

**Problem 4: Artifact reuse tracking doesn't exist.** The RCF (Release Context File) is designed to be reusable across initiatives. But there's no way to know how many initiatives currently reference a given RCF, or what happens if the RCF is updated.

**Problem 5: The healthcheck can't verify cross-initiative consistency.** Healthcheck playbook Scope B checks individual initiatives. But "does every initiative using ISPEC-PLATFORM-001 have a compatible EM?" is a cross-initiative consistency question that requires indexing.

#### Relationships to other system components

| Component | Relationship |
|-----------|-------------|
| **Schema** | Store uses schemas to parse artifact fields for structured indexing. Without Schema, the Store does text search only. With Schema, it understands that an ORD's §2 contains deployment evidence with specific field types, making field-level queries possible. |
| **Engine** | Engine produces evidence artifacts that the Store indexes. Engine also queries the Store for upstream dependencies during evaluation ("is the SAD referenced by this TDD actually frozen?"). |
| **Analytics** | Analytics is the primary consumer of the Store. Every Analytics query runs against the Store's index. Without the Store, Analytics would need to parse raw Markdown files on every query. |
| **Twin** | Twin provides live deployment state; Store provides governed artifact state. Together they answer "what was planned (Store: RP) vs what is running (Twin: deployment state) vs what was recorded (Store: RR)." |
| **Compliance Reporter** | Reporter queries the Store for all evidence artifacts within an audit scope. Store's lineage tracing enables the Reporter to follow evidence chains (CER → SAR → TM → SAD → PRD). |
| **Playground** | Playground could query the Store for real examples to use as reference material during training ("show me a well-formed SAD from a completed initiative"). |
| **AIEOS Framework** | Store indexes what AIEOS produces but doesn't govern anything. The ER is the per-initiative index; the Store is the cross-initiative index. Store could also index the framework itself — "which kits reference this governance model section?" — enabling framework maintenance queries. |

#### Scope

- Index all AIEOS artifacts across all initiatives (parse artifact IDs, cross-references, frozen status, timestamps)
- Lineage queries: "What DPRD produced this ORD?" (upstream trace) and "What TDDs were generated from this SAD?" (downstream trace)
- Full-text search scoped by kit, layer, initiative, date range, or artifact type
- Schema-aware field extraction (structured queries on artifact content)
- Dependency queries: "Which frozen artifacts reference ISPEC-CONSOLE-001?"
- Artifact reuse tracking: "How many initiatives reference RCF-ORG-001?"

---

### 4. AIEOS governance analytics (`aieos-governance-analytics`)

**What:** Cross-initiative intelligence derived from artifact data. Pattern detection, bottleneck identification, governance effectiveness measurement, and predictive signals.

#### Value to the existing framework

AIEOS already has a per-initiative learning loop: IEK (Layer 7) synthesizes RHR data into Evolution Signals that feed back to PIK. But there's no cross-initiative learning — and the most valuable insights come from patterns across initiatives, not within a single one.

**Problem 1: No way to measure whether AIEOS is helping.** An organization adopts AIEOS and follows the process. A year later: "Has our incident rate decreased? Are our releases safer? Are we moving faster or slower?" Without Analytics, these questions require manual data collection from dozens of ERs.

**Problem 2: Framework improvement is anecdotal.** Today, framework changes come from findings logged during individual initiatives (like the 10 findings from ER-CONSOLE-001). But systematic patterns — "80% of first-pass PFDs fail the scope_bounded gate" — are invisible because nobody is aggregating validator results across initiatives.

**Problem 3: IEK can't see cross-initiative patterns.** IEK processes RHRs for one service. But "services built with Architecture Pattern X have 3x the incident rate of Pattern Y" requires data from multiple initiatives. That's an Analytics insight, not an IEK insight.

**Problem 4: The sherpa can't learn from organizational history.** When the sherpa guides a new P1 initiative, it follows the playbook. But it can't say "based on your organization's last 10 P1 initiatives, the most common failure point is the SAD→TDD transition — here's what to watch for." That requires cross-initiative data.

**Problem 5: Preset optimization is guesswork.** The 5 presets (P1-P5) define which kits and artifacts are required vs optional. But are they right? Maybe P2 Enhancements should require QAK based on historical rollback data. Analytics provides the evidence for preset tuning.

#### Relationships to other system components

| Component | Relationship |
|-----------|-------------|
| **Schema** | Analytics uses schemas to normalize data across artifact types. "Hard gate failure rate" requires knowing what gates each artifact type has — that's in the schema. |
| **Engine** | Engine is the primary data producer for Analytics. Every Engine evaluation generates timestamped, structured results (gate pass/fail, finding counts, tool execution time) that Analytics aggregates. |
| **Artifact Store** | Analytics queries run against the Store. Store provides the indexed data; Analytics provides the intelligence layer on top. |
| **Twin** | Twin provides runtime data (incidents, deployments, SLO metrics) that Analytics correlates with governance data (artifact quality, review findings). "Do initiatives with more PRK findings have fewer production incidents?" requires both. |
| **Compliance Reporter** | Analytics can measure compliance posture trends: "compliance gap count is decreasing quarter over quarter." Reporter handles individual audits; Analytics tracks the path. |
| **Playground** | Analytics identifies which governance steps teams struggle with most, informing Playground scenario design ("teams need more practice with SAD→TDD transitions"). |
| **AIEOS Framework** | Analytics is the feedback mechanism that AIEOS currently lacks at the framework level. IEK provides per-initiative feedback. Analytics provides framework-level feedback: "this spec is too strict," "this prompt consistently produces artifacts that fail gate X," "this preset should require SCK." Analytics findings would be the primary input to framework revision decisions. |

#### Scope

- **Pattern detection:** "Initiatives that skip SSK have 3x the rollback rate."
- **Process bottleneck identification:** "Average time between ORD freeze and RER freeze is 12 days."
- **Governance effectiveness:** "Since adding the observability lens, monitoring gaps decreased 40%."
- **Predictive signals:** "This initiative's pattern matches 3 prior initiatives that required redesign."
- **Framework improvement signals:** "Gate X fails on 80% of first attempts — the spec or prompt needs revision."
- **Preset optimization:** "P2 initiatives that skip QAK have 2x the rollback rate — recommend making QAK required for P2."

---

### 5. AIEOS compliance reporter (`aieos-compliance-reporter`)

**What:** Automated assembly of audit-ready evidence packages from AIEOS artifacts, mapped to regulatory control frameworks.

#### Value to the existing framework

AIEOS already produces all the evidence an auditor needs — CERs, SARs, DARs, QGRs, PRRs, RRs. SCK (Layer 10) is specifically designed for compliance evidence. But the evidence is scattered across dozens of artifacts per initiative, across multiple initiatives per system.

**Problem 1: Audit preparation is a fire drill.** When an auditor asks "show me evidence that your deployment process includes security review," someone manually searches through ERs, finds the relevant SARs and PRRs, and assembles a package. This takes days and happens under time pressure.

**Problem 2: Control mapping is in someone's head.** The mapping from "SOC2 CC6.1 (Logical and Physical Access Controls)" to "AIEOS artifacts: SAR §3 + CER §2 + EM §4" is tribal knowledge. If that person leaves, the mapping is lost.

**Problem 3: Gap detection is reactive.** Organizations discover compliance gaps during audits, not before them. AIEOS produces the evidence, but nobody is continuously checking "do we have evidence for every required control?"

**Problem 4: Multi-initiative compliance is fragmented.** A system may span multiple AIEOS initiatives (initial build, enhancement, performance fix). The compliance evidence for that system is spread across multiple ERs. Assembling the complete evidence chain requires tracing across initiatives.

#### Relationships to other system components

| Component | Relationship |
|-----------|-------------|
| **Schema** | Reporter uses schemas to identify which artifact sections map to which regulatory controls. Schema makes the mapping maintainable — when a spec adds a new section, the control mapping can be updated. |
| **Engine** | Engine ensures evidence artifacts (SAR, DAR, QGR) are always produced when required. Without Engine, evidence collection depends on human discipline. With Engine, evidence is automatically generated and the Reporter can guarantee completeness. |
| **Artifact Store** | Reporter queries the Store for all evidence artifacts within an audit scope. Store's lineage tracing enables evidence chain assembly (CER → SAR → TM → SAD → PRD). |
| **Analytics** | Analytics tracks compliance posture trends over time. Reporter handles point-in-time audits; Analytics measures path ("our SOC2 coverage has improved from 72% to 94% over 6 months"). |
| **Twin** | Twin provides the system inventory that scopes the audit. "Which systems are in scope for PCI-DSS?" requires knowing what's running — that's the Twin's live topology. |
| **Playground** | Reporter's control-to-artifact mapping could be used in Playground scenarios to teach teams *why* each artifact matters for compliance ("skipping the DAR means we can't satisfy CC6.8"). |
| **AIEOS Framework** | SCK (Layer 10) produces the evidence; Reporter assembles it. The CER spec already defines what evidence looks like. Reporter adds the external dimension — mapping AIEOS's internal evidence structure to external regulatory control frameworks. This could inform SCK spec improvements: "auditors consistently ask for X, but no AIEOS artifact covers it — add a gate to the CER spec." |

#### Scope

- Accept audit scope (regulation, date range, systems)
- Query Artifact Store for relevant evidence artifacts
- Control-to-evidence mapping: which AIEOS artifacts satisfy which regulatory controls
- Gap analysis: "Control X.Y requires encryption-at-rest evidence — no DAR covers this"
- Package generation: structured audit package with table of contents, control matrix, and linked evidence
- Continuous compliance state: dashboard showing current coverage vs. control requirements
- Regulatory frameworks to target first: SOC2 Type II, ISO 27001, GDPR (Article 25/32), PCI-DSS, HIPAA

---

### 6. AIEOS system twin (`aieos-system-twin`)

**What:** An event-sourced system model that tracks service topology, dependencies, and deployments in real time.

**Origin:** Original plan §9 (SDLC Digital Twin). Filtered to remove vendor-specific prescriptions (Neo4j, Kafka). The entity model is valuable; the implementation is a tool binding.

#### Value to the existing framework

AIEOS governs the decision process but has limited visibility into what's actually running. The SMR (System Model Record, built in WS-2) captures a point-in-time snapshot of system topology. But snapshots go stale.

**Problem 1: The SMR is manually assembled.** Someone must inventory services, map dependencies, and check deployment versions. This is labor-intensive and the SMR is outdated the moment a new deployment occurs.

**Problem 2: Blast radius assessment during release planning is guesswork.** When the RSA (Release Safety Assessment) asks "what's the deployment risk?" the answer depends on knowing what else is running and what depends on the service being released. Today, this is assessed from memory and the SMR snapshot.

**Problem 3: Incident context requires archaeology.** When ODK investigates a production incident, the first question is "what changed recently and what depends on the affected service?" Today, the DCR (Diagnostic Context Record) is assembled from deployment logs and tribal knowledge. The Twin provides this instantly.

**Problem 4: Environment drift is invisible.** The EM (Environment Matrix) defines what environments should look like. But nobody is continuously checking whether the actual deployment state matches the EM. The Twin provides the live state that the EM can be validated against.

#### Relationships to other system components

| Component | Relationship |
|-----------|-------------|
| **Schema** | Twin uses the SMR schema to know what entity relationships to track (services, dependencies, environments). Schema ensures Twin's data model stays aligned with AIEOS's governed model. |
| **Engine** | Engine queries the Twin for real-time context during evaluation. "Is this service's dependency healthy?" "What's the current deployment version in staging?" Twin provides the runtime context that makes Engine evaluations aware of live system state. |
| **Artifact Store** | Store holds governed artifacts (what was planned); Twin holds live state (what is running). Together they enable drift detection: "the RP said deploy to 3 environments, but the Twin shows only 2 have the new version." |
| **Analytics** | Twin provides the runtime data (incidents, deployments, SLO metrics) that Analytics correlates with governance data. "Do services with higher PRK scores have fewer incidents?" requires both Analytics (PRK data from Store) and Twin (incident data from live systems). |
| **Compliance Reporter** | Twin provides the system inventory that scopes audits. "Which systems are in scope?" requires knowing what's running. Twin also enables continuous compliance monitoring: "is the production environment still compliant with the EM's security group rules?" |
| **Playground** | Twin could provide realistic system topologies for Playground scenarios, so trainees practice with real-world complexity rather than toy examples. |
| **AIEOS Framework** | Twin feeds the SMR — the governed snapshot of what the Twin tracks in real time. Currently SMR is manually assembled; Twin would make SMR generation near-automatic (Twin snapshot → SMR artifact → validate → freeze). Twin also provides context to the sherpa: "before we plan this release, here's what's currently running and what depends on it." |

#### Scope

- Event-sourced topology: services, dependencies, deployments, config changes
- Real-time dependency graph (what depends on what right now)
- Blast radius analysis (if service X fails, what's affected?)
- Automated SMR generation from live state (Twin snapshot → SMR artifact)
- Deployment history per service per environment
- Change correlation (deployment X happened, then incident Y — related?)
- Environment drift detection (live state vs. EM definition)

**Why deferred to #6:** High infrastructure cost (event store + graph DB + materialization layer). The SMR covers the snapshot use case adequately. The Twin's value multiplies when the Engine and Store exist — without them, the Twin is an isolated operational tool rather than an integrated part of the governance system.

---

### 7. AIEOS playground (`aieos-playground`)

**What:** An interactive learning environment where teams practice AIEOS flows with simulated scenarios.

#### Value to the existing framework

AIEOS has a steep learning curve — 15 layers, 40+ artifact types, decision tables, presets, convergence loops. The sherpa helps during real work, but real work has real consequences. Teams need a way to build muscle memory without risk.

**Problem 1: First initiatives are expensive learning exercises.** The first time a team runs a P1 flow, they make predictable mistakes — freezing too early, skipping utility prompts, not maintaining the ER. These mistakes cost rework. A practice environment would move the learning curve before the first real initiative.

**Problem 2: The sherpa integration tests prove behavior but don't teach it.** The test fixtures show what correct sherpa behavior looks like, but they're not designed for human consumption. The Playground would turn test fixtures into guided learning experiences.

**Problem 3: Cross-cutting kit adoption is poorly understood.** Teams consistently under-adopt cross-cutting kits (QAK, SCK, PRK) because they don't understand when and why to use them. A Playground scenario that shows "here's what happens when you skip SCK and discover a vulnerability in production" would build intuition.

**Problem 4: New team members can't practice decision junctions.** The navigation map has 28 decision junctions. In real work, a team might encounter 5-8 of them. The Playground would expose all junction types with practice scenarios.

#### Relationships to other system components

| Component | Relationship |
|-----------|-------------|
| **Schema** | Playground uses schemas to validate practice artifacts in real time. When a trainee generates a draft SAD, the Playground checks it against the SAD schema immediately — "you're missing the Layer Assignment table." This is faster feedback than waiting for a validator session. |
| **Engine** | Engine could power the Playground's "real feedback" mode. Instead of simulated validation ("this would pass"), the Playground runs actual Engine checks against practice artifacts, providing realistic feedback with real tools. |
| **Artifact Store** | Store provides real examples for reference during training. "Here's a well-formed SAD from a completed initiative" is more valuable than the template alone. Store also tracks practice history across trainees. |
| **Analytics** | Analytics identifies which governance steps teams struggle with most, directly informing Playground scenario priorities. "80% of first-pass PFDs fail scope_bounded — create a PFD practice scenario focused on scoping." |
| **Twin** | Twin provides realistic system topologies for advanced scenarios. Instead of practicing against toy "TODO app" examples, trainees practice against real (anonymized) system graphs from the Twin. |
| **Compliance Reporter** | Reporter's control-to-artifact mapping enriches Playground scenarios for compliance presets (P3). Trainees learn which artifacts satisfy which controls, building compliance intuition alongside governance skills. |
| **AIEOS Framework** | Playground consumes the framework (specs, templates, playbooks, navigation map) but doesn't modify it. It reads the same files the sherpa reads. The integration test fixtures (`tests/integration/fixtures/`) already have 10 scenarios that could bootstrap the Playground's initial content. Playground usage data (which scenarios fail most, where trainees get stuck) feeds back as framework usability signals. |

#### Scope

- Pre-built scenarios per preset (P1-P5) with branching paths
- Simulated initiatives where teams practice the full flow
- Immediate feedback on governance violations ("you tried to generate a TDD without freezing the SAD")
- Guided tutorials: "Walk through a P2 Enhancement in 30 minutes"
- Sandboxed environment (mistakes don't affect real projects)
- Progress tracking (which flows has this person practiced?)
- Reference artifact library (real examples from the Store, anonymized)

**Bootstrap opportunity:** The integration test fixtures already have 10 scenarios with pre-scripted interactions. The Playground could reuse these as interactive tutorials.

**Why #7:** Independent of the critical path — can be built at any point. But its value increases as other system components come online (Engine for real validation, Store for real examples, Analytics for scenario prioritization).

---

## Dependency graph

```
AIEOS Framework (exists)
    │
    ▼
AIEOS Schema ──────────────────────────────────┐
    │ │                                          │
    │ └──► AIEOS Framework (strengthened)         │
    │      (deeper Tier 2 tests, drift            │
    │       detection, consistency checks)         │
    │                                              │
    ▼                                              ▼
Evaluation Engine + Adapter SDK         Artifact Store
    │                                      │          │
    ▼                                      ▼          ▼
System Twin ◄──────────────────── Governance Analytics  Compliance Reporter
                                      │
                                      ▼
                              (feedback → AIEOS Framework improvement)

Playground (independent — can be built at any point)
```

Schema delivers value in two phases:
1. **Immediate** (no system projects needed): deeper Tier 2 tests, spec/template/validator drift detection, `framework.py` consistency validation
2. **Enabling** (unlocks system): machine-readable specs for Engine, Store, Analytics, and Compliance Reporter

---

## Integration flows

32 integration points connecting the 15 AIEOS kits and 7 system modules. Organized by direction: what kits send to modules, what modules send back to kits, and what modules exchange with each other.

### Kit → module flows (Kits produce, modules consume)

Every kit produces frozen Markdown artifacts. The modules consume them for different purposes.

| # | Flow | Source Kit(s) | Target Module | What Flows | Trigger |
|---|------|--------------|---------------|------------|---------|
| K1 | All artifacts → indexing | All 15 kits | `aieos-artifact-store` | Every frozen artifact (DPRD, SAD, TDD, ORD, RR, RHR, PMR, QGR, PRR, SMR, RSA, etc.) | On artifact freeze |
| K2 | All specs → machine-readable contracts | All 15 kits + governance-foundation | `aieos-schema` | Spec Markdown files parsed into YAML/JSON schemas | On spec creation or change |
| K3 | Real software artifacts → evaluation | EEK (Layer 4) — the actual software being built | `aieos-evaluation-engine` | Source code, container images, test suites, dependency manifests | On PR open, build complete, or deploy trigger |
| K4 | Security evaluation scope | SCK (Layer 10) — TM and SAR specs | `aieos-evaluation-engine` | Threat categories to scan for; security check requirements | Engine reads SCK schemas to determine what security adapters to invoke |
| K5 | Quality evaluation scope | QAK (Layer 9) — VP and QGR specs | `aieos-evaluation-engine` | Test scope definition; quality evidence requirements | Engine reads QAK schemas to determine what quality evidence to collect |
| K6 | Expected topology → drift baseline | PINFK (Layer 12) — EM and SMR definitions | `aieos-system-twin` | Environment definitions, service entity model | Twin aligns data model to PINFK schemas; detects drift between EM (expected) and Twin (actual) |
| K7 | Operational health data | RRK (Layer 6) — SRP and IR | `aieos-system-twin` | SLO targets from SRP; incident records | Twin tracks service health against SLO targets; correlates incidents with topology |
| K8 | Compliance evidence | SCK (Layer 10) — frozen CER, SAR, DAR | `aieos-compliance-reporter` | Compliance evidence artifacts | Reporter maps to regulatory control frameworks |
| K9 | Review lens definitions | PRK (Layer 14) — lens specs | `aieos-evaluation-engine` | Lens evaluation categories and hard gates | Engine automates the deterministic subset of lens checks (field presence, format compliance) |
| K10 | Framework files → training content | All 15 kits | `aieos-playground` | Playbooks, specs, templates, navigation map, integration test fixtures | Playground reads framework files to build interactive training scenarios |

### Module → kit flows (Modules produce, kits consume)

Modules feed evidence, intelligence, and live state back into the governance process. Humans remain the decision-makers — modules produce inputs, not decisions.

| # | Flow | Source Module | Target Kit(s) | What Flows | How Kit Uses It |
|---|------|-------------|---------------|------------|-----------------|
| M1 | Schema files → all kits | `aieos-schema` | All 15 kits | YAML/JSON schema files alongside Markdown specs | Tier 2 tests validate spec/template/validator consistency; Engine and Store consume for automation |
| M2 | Quality evidence → QAK | `aieos-evaluation-engine` | QAK (Layer 9) | Test results, coverage data, quality metrics in AIEOS evidence format | Feeds QGR generation — sherpa uses Engine evidence instead of manually-collected data |
| M3 | Security evidence → SCK | `aieos-evaluation-engine` | SCK (Layer 10) | SAST findings, container scan results, dependency audit data | Feeds SAR and DAR generation — automated security evidence collection |
| M4 | Risk evidence → REK | `aieos-evaluation-engine` | REK (Layer 5) | Aggregated risk data from QAK and SCK evaluations | Feeds RSA generation — quality, security, and deployment risk dimensions populated from Engine evidence |
| M5 | Live topology → REK | `aieos-system-twin` | REK (Layer 5) | Dependency graph, blast radius analysis | RSA §4 deployment risk classification; RP §2 deployment planning uses real dependency data |
| M6 | Incident context → ODK | `aieos-system-twin` | ODK (Layer 8) | Recent changes, affected dependencies, topology at time of incident | DCR and INR investigation context — replaces manual archaeology ("what changed? what depends on this?") |
| M7 | Live health → RRK | `aieos-system-twin` | RRK (Layer 6) | Service health status, deployment state, SLO current values | RHR health picture; SRP revision triggers when infrastructure changes are detected |
| M8 | Automated SMR → PINFK | `aieos-system-twin` | PINFK (Layer 12) | Twin snapshot materialized as SMR artifact | Replaces manual SMR assembly: Twin snapshot → SMR draft → validate → freeze |
| M9 | Cross-initiative context → IEK | `aieos-artifact-store` | IEK (Layer 7) | Artifact data from related initiatives | Supplements per-initiative RHR data with organizational patterns for richer Evolution Signals |
| M10 | Framework improvement signals → governance-foundation | `aieos-governance-analytics` | governance-foundation | "Gate X fails 80% on first pass"; "P2 initiatives that skip QAK have 2x rollback rate" | Humans evaluate insights and apply spec, prompt, or preset changes through normal governance process |
| M11 | Compliance gaps → SCK | `aieos-compliance-reporter` | SCK (Layer 10) | "Control X.Y has no covering evidence artifact" | Informs CER scope — identifies what compliance evidence needs to be produced in the next initiative cycle |

### Module → module flows (system internal)

| # | Flow | Source | Target | What Flows | Contract |
|---|------|--------|--------|------------|----------|
| I1 | Spec contracts → evaluation rules | `aieos-schema` | `aieos-evaluation-engine` | Schema files defining gates, sections, field types | Schema YAML/JSON format |
| I2 | Spec contracts → index structure | `aieos-schema` | `aieos-artifact-store` | Schema files defining how to parse artifact fields | Schema YAML/JSON format |
| I3 | Spec contracts → data model | `aieos-schema` | `aieos-system-twin` | SMR schema defining entity relationships | Schema YAML/JSON format |
| I4 | Evidence → indexing | `aieos-evaluation-engine` | `aieos-artifact-store` | Evaluation results in AIEOS validator JSON format | AIEOS validator JSON schema |
| I5 | Upstream status → evaluation context | `aieos-artifact-store` | `aieos-evaluation-engine` | "Is the SAD this TDD references frozen?" | Store query API |
| I6 | Indexed data → intelligence | `aieos-artifact-store` | `aieos-governance-analytics` | Cross-initiative artifact data, finding aggregations | Store query API |
| I7 | Indexed data → audit assembly | `aieos-artifact-store` | `aieos-compliance-reporter` | Evidence artifacts within audit scope, lineage chains | Store query API |
| I8 | Runtime context → evaluation | `aieos-system-twin` | `aieos-evaluation-engine` | Live topology, service health, deployment state | Twin state query API |
| I9 | Topology changes → indexing | `aieos-system-twin` | `aieos-artifact-store` | Deployment events as indexable state changes | Twin event format |
| I10 | Scenario prioritization → training | `aieos-governance-analytics` | `aieos-playground` | "Teams struggle most with SAD→TDD transition" | Analytics insight format |
| I11 | Reference artifacts → training | `aieos-artifact-store` | `aieos-playground` | Well-formed artifacts from completed initiatives as examples | Store query API |

### Flow diagram

```
                                    ┌──────────────────────┐
                                    │  AIEOS Governance     │
                                    │  Framework (15 kits)  │
                                    └──────┬──┬────────────┘
                              K2 (specs)   │  │   M1 (schemas back to kits)
                                    ┌──────▼──▼────────────┐
                                    │   aieos-schema        │
                                    └──┬─────┬──────────┬──┘
                                I1    │  I2  │       I3 │
                    ┌─────────────────▼─┐  ┌─▼────────┐ │ ┌──────────────┐
    K3,K4,K5,K9 ──►│  aieos-evaluation │  │  aieos-  │ │ │    aieos-    │
    (code, specs)   │  -engine          │  │  artifact│ │ │    system-   │◄── External
                    │                   │  │  -store  │ └►│    twin      │    systems
    M2,M3,M4 ◄─────│  (evidence out)   │  │          │   │              │    (CI/CD,
                    └──┬──────────▲─────┘  └─┬──┬──┬──┘   └──┬──┬──┬───┘    K8s)
                       │I4     I5│  I8       │  │  │      M5 │  │  │
                       │  ┌──────┘    ┌──────┘  │  │  ┌──────┘  │  │
                       │  │           │    I6   │  │  │     M6  │  │
                       ▼  │           │  ┌──────┘  │  │  ┌──────┘  │M8
                    ┌─────┘           │  │    I7   │  │  │     M7  │
                    │                 │  │  ┌──────┘  │  │  ┌──────┘
                    │              ┌──▼──▼──▼──┐   ┌──▼──▼──▼──────┐
                    │         I10  │  aieos-   │   │   PINFK,      │
                    │        ┌────►│  gov-     │   │   RRK, ODK,   │
                    │        │    │  analytics │   │   REK (kits)  │
                    │        │    └────────────┘   └───────────────┘
                    │        │    ┌────────────┐
                    │        │    │  aieos-     │
                    │        │    │  compliance │
                    │        │    │  -reporter  │
                    │        │    └──────┬──────┘
                    │        │       M11 │
                    │   I11  │    ┌──────▼──────┐
                    └────────┴───►│   aieos-    │
                                 │   playground │
                                 └──────────────┘
```

### Flow inventory summary

| Direction | Count | Examples |
|-----------|-------|---------|
| Kit → Module | 10 | Frozen artifacts → Store, source code → Engine, lens specs → Engine, EM → Twin |
| Module → Kit | 11 | Engine evidence → QAK/SCK/REK, Twin topology → REK/ODK/RRK, Analytics insights → governance-foundation |
| Module → Module | 11 | Schema → Engine/Store/Twin, Engine → Store, Store → Analytics/Reporter, Twin → Engine |
| **Total** | **32** | |

### Kit-Level flow summary

Which kits interact with which modules, and in what direction:

| Kit | Sends To | Receives From |
|-----|----------|---------------|
| **governance-foundation** | Schema (K2: specs) | Schema (M1: schema files), Analytics (M10: improvement signals) |
| **PIK (L2)** | Store (K1: frozen artifacts), Playground (K10: playbook) | Schema (M1) |
| **SSK (L3)** | Store (K1: frozen artifacts) | Schema (M1) |
| **EEK (L4)** | Store (K1: frozen artifacts), Engine (K3: source code + containers) | Schema (M1) |
| **REK (L5)** | Store (K1: frozen artifacts) | Schema (M1), Engine (M4: risk evidence for RSA), Twin (M5: blast radius for RSA/RP) |
| **RRK (L6)** | Store (K1: frozen artifacts), Twin (K7: SLO targets + incidents) | Schema (M1), Twin (M7: live health for RHR) |
| **IEK (L7)** | Store (K1: frozen ES) | Schema (M1), Store (M9: cross-initiative context) |
| **ODK (L8)** | Store (K1: frozen artifacts) | Schema (M1), Twin (M6: incident context) |
| **QAK (L9)** | Store (K1: frozen artifacts), Engine (K5: quality scope) | Schema (M1), Engine (M2: quality evidence for QGR) |
| **SCK (L10)** | Store (K1: frozen artifacts), Engine (K4: security scope), Reporter (K8: compliance evidence) | Schema (M1), Engine (M3: security evidence for SAR/DAR), Reporter (M11: gap analysis) |
| **DCK (L11)** | Store (K1: frozen artifacts) | Schema (M1) |
| **PINFK (L12)** | Store (K1: frozen artifacts), Twin (K6: EM/SMR definitions) | Schema (M1), Twin (M8: automated SMR) |
| **DKK (L13)** | Store (K1: frozen artifacts) | Schema (M1) |
| **PRK (L14)** | Store (K1: frozen artifacts), Engine (K9: lens specs) | Schema (M1) |
| **BPK (L15)** | Store (K1: frozen artifacts) | Schema (M1) |

---

## Operational layer: lenses, tools, and skills

The integration flows above show data moving between kits and modules. But data doesn't move itself — **lenses**, **tools**, and **skills** are the mechanisms that do the actual work. They form a third architectural layer that bridges governance (source of truth) and system (runtime infrastructure).

```
┌──────────────────────────────────────────────────────┐
│  OPERATIONAL LAYER (how work gets done)              │
│                                                      │
│  Sherpa (skill) ─── orchestrates everything          │
│  ├── invokes Tools (router, position-check, etc.)    │
│  ├── triggers Lenses (security, reliability, etc.)   │
│  ├── queries Modules (Engine, Store, Twin)            │
│  └── surfaces Analytics insights                     │
│                                                      │
│  Tools ─── governed capabilities                     │
│  ├── invoked by Sherpa (AI sessions)                 │
│  ├── invoked by Engine (programmatic, deterministic) │
│  └── output indexed by Store                         │
│                                                      │
│  Lenses ─── evaluation perspectives                  │
│  ├── pre-populated by Engine evidence                │
│  ├── findings indexed by Store                       │
│  └── finding patterns analyzed by Analytics          │
├──────────────────────────────────────────────────────┤
│  ECOSYSTEM LAYER (runtime infrastructure)            │
│                                                      │
│  Schema ── Engine ── Store ── Analytics              │
│                      Twin ── Reporter ── Playground  │
├──────────────────────────────────────────────────────┤
│  GOVERNANCE LAYER (source of truth)                  │
│                                                      │
│  15 Kits ── governance-foundation ── specs           │
│  playbooks ── navigation map ── decision tables      │
└──────────────────────────────────────────────────────┘
```

The governance layer defines *what*. The system layer provides *infrastructure*. The operational layer is *how work actually happens* — and it's the layer that touches both.

### Lenses (12 PRK review lenses)

Currently: Each lens runs as an independent AI session. The AI reads the artifact, reads the lens spec, applies judgment, produces findings. Human provides the artifact; AI evaluates it.

With the system, lenses gain three integration points:

#### L-1: evidence pre-Population (Engine → lenses)

Today the security lens reads a SAD and makes judgments based on prose descriptions of security measures. With Engine, the security lens receives *actual* SAST/DAST findings from the Semgrep adapter alongside the artifact. The lens still applies semantic judgment — but it's evaluating real evidence, not just descriptions of intent.

| Lens | Engine Evidence That Pre-Populates It |
|------|--------------------------------------|
| Security | SAST findings (Semgrep), container scan results (Trivy), dependency vulnerabilities (Snyk) |
| Reliability | Unit/integration test results, chaos test outcomes, health check verification |
| Resilience | Chaos engineering results, multi-failure scenario test outcomes |
| Performance | Load test metrics, profiling data, resource utilization measurements |
| Observability | Log output verification, metric emission checks, alert fire tests |
| Compliance | License audit results (FOSSA), policy-as-code evaluation, CIS benchmark scans |
| Cost | Cloud cost estimates, resource allocation data |
| Operability | Deployment dry-run results, rollback verification, runbook validation |

Lenses that are purely design-evaluative (maintainability, devex, business-value, accessibility) gain less from Engine evidence — they primarily evaluate artifact content, not tool output. They benefit more from Store context (L-3).

#### L-2: deterministic pre-Screening (Engine → lenses)

Some lens checks are mechanical: "does this SAD have a section on authentication?" is field-presence, not judgment. Engine runs the deterministic subset via Schema (section headings, required fields, enumerated values) and passes results to the AI lens session as pre-screened gates. The AI focuses on semantic evaluation where it adds unique value.

| Check Type | Engine Handles (Deterministic) | AI Handles (Semantic) |
|-----------|-------------------------------|----------------------|
| Field presence | "§4 Security section exists" | "The security measures described in §4 are appropriate for the threat model" |
| Format compliance | "All findings have severity: critical/high/medium/low" | "The severity classifications are consistent with the impact described" |
| Enumeration values | "Deployment strategy is one of: canary, blue-green, rolling, direct-full" | "The chosen deployment strategy is appropriate for the risk level" |
| Cross-reference integrity | "The TDD references SAD-CONSOLE-001 which exists and is frozen" | "The TDD's design choices are architecturally consistent with the referenced SAD" |

This split preserves the AIEOS principle that validators (and lenses) judge — but acknowledges that some judgment is mechanical and some requires AI reasoning.

#### L-3: finding pattern analysis (Store + analytics → lens improvement)

"The security lens flags missing rate limiting on 70% of SADs" is a cross-initiative insight that individual lens sessions can't see. This flow works through Analytics:

1. Every PRR's per-lens findings are indexed by Store (finding text, severity, location, lens name, artifact type)
2. Analytics queries Store for cross-initiative finding patterns
3. Patterns inform lens improvement: "if 70% of SADs fail this check, either the SAD prompt needs to emphasize rate limiting, or the security lens spec needs to make it a named evaluation category rather than an implicit check"
4. Humans evaluate the Analytics insight and update the lens spec/prompt through normal governance process

### Tools (Governed capabilities)

Currently: Tools are invoked by the sherpa during guided sessions or by humans following playbooks. Each tool's four-file set defines what it does (spec), outputs (template), how to invoke it (prompt), and how to judge its output (validator). Framework-level tools: initiative-router, position-check, decision-router, handoff-navigator, dependency-check, spec-lookup. Kit-level tools: BAT (EEK), 12 review lenses (PRK).

With the system, tools gain four integration points:

#### T-1: machine-Readable tool contracts (Schema → tools)

Today, tool specs are Markdown prose. Schema gives tool specs machine-readable contracts — preconditions, postconditions, hard gates, input/output fields become parseable. This means the Engine can understand tool requirements programmatically rather than requiring an AI session to interpret prose.

| Tool Spec Field | Currently | With Schema |
|----------------|-----------|-------------|
| Preconditions | "The artifact under review has passed its own validator" | `preconditions: [{type: "artifact_status", value: "validated"}]` |
| Hard gates | Markdown table with gate names and rules | `hard_gates: [{name: "artifact_scoped", rule: "..."}]` |
| Input fields | Markdown table with field/required/description | `inputs: [{name: "artifact", required: true, type: "artifact_reference"}]` |
| Output format | "conforming to {tool}-template.md" | `output_schema: "review-security-template.yaml"` |

#### T-2: programmatic tool invocation (Engine → tools)

Tools like dependency-check and spec-lookup currently require an AI session. Engine could invoke them as automated checks:

| Tool | Current Invocation | Engine Invocation |
|------|-------------------|-------------------|
| dependency-check | Sherpa reads the tool prompt, evaluates dependencies, produces findings | Engine runs adapter (npm audit, pip-audit, trivy fs), normalizes output to dependency-check template format |
| spec-lookup | Sherpa reads the navigation map and finds the relevant spec | Engine queries Schema index directly — no AI session needed |
| position-check | Sherpa reads ER + artifact directory + navigation map | Engine queries Store (artifact inventory) + Twin (live state) + navigation map schema — produces richer position report |
| BAT (Build Acceptance Test) | Sherpa evaluates work group output against acceptance criteria | Engine runs automated test suites via adapter, pre-populates BAT with pass/fail evidence |

Not all tools benefit from programmatic invocation. Decision-router and initiative-router require human context (user intent, organizational knowledge) that the Engine doesn't have — these remain sherpa-invoked.

#### T-3: ground-Truth enrichment (Store + twin → tools)

The position-check tool currently reads the ER and artifact directory for ground truth. With Store and Twin, ground truth becomes richer:

| Ground Truth Source | Current | With system |
|--------------------|---------|---------------|
| Artifact inventory | Local filesystem: `docs/sdlc/*.md` | Store: all artifacts across all initiatives, with lineage and cross-references |
| Artifact status | ER §N artifact table | Store: verified against actual file content, with timestamp of last freeze |
| Deployment state | Not available | Twin: what's running where, what version, when deployed |
| Related initiatives | Not available | Store: other initiatives touching the same services, with their current position |
| Health signals | Rule-based (WS-5 heuristics) | Analytics: data-driven signals based on cross-initiative patterns |

Position-check evolves from "you are HERE in this initiative" to "you are HERE in context of everything your organization is doing."

#### T-4: tool output indexing (Tools → store)

Tool outputs (routing records, position-check reports, BAT results, handoff records) are currently ephemeral — they exist in the session transcript but aren't systematically captured. Store indexes tool outputs, making them queryable:

| Query | What It Reveals |
|-------|----------------|
| "How many BAT escalations has this team triggered?" | Engineering execution patterns — frequent BAT escalations may indicate WDD quality issues |
| "Which initiatives had ambiguous routing requiring clarifying questions?" | Intake quality patterns — ambiguous routing suggests PIK intake forms need improvement |
| "What's the average position-check anomaly count across initiatives?" | Framework health — high anomaly counts indicate systematic process gaps |
| "How often does handoff-navigator find missing exit conditions?" | Kit boundary quality — frequent failures suggest playbook or entry-from file gaps |

### Skills (The sherpa)

Currently: The sherpa is the sole user-facing interface to AIEOS. It reads framework files, guides users through decision tables, generates artifacts, validates them, maintains the ER. It operates entirely within the governance layer.

With the system, the sherpa becomes the **orchestration control plane** that coordinates across all three layers:

#### S-1: evidence-Informed artifact generation (Engine → sherpa)

Today when the sherpa generates an RSA, it asks the human for quality and security evidence. With Engine:

```
Current:  Human collects evidence → pastes into session → sherpa generates RSA
With Engine: Sherpa queries Engine → Engine returns evidence → sherpa pre-populates RSA → human reviews
```

| Artifact | Current Evidence Source | Engine Evidence Source |
|----------|----------------------|----------------------|
| QGR | Human provides test results | Engine provides test runner adapter output + coverage metrics |
| SAR | Human describes security measures | Engine provides SAST/DAST adapter findings |
| DAR | Human provides dependency list | Engine provides dependency audit adapter results |
| RSA | Human summarizes QGR + SAR findings | Engine provides aggregated risk data from all adapters |
| RHR | Human provides SLO metrics | Engine provides monitoring adapter data |

The sherpa's generation prompts don't change — they still reference the spec and template. What changes is the *input quality*. Instead of "tell me about your security posture," the sherpa says "the Engine found 3 high-severity SAST findings and 0 critical dependency vulnerabilities — I'll incorporate these into the SAR."

#### S-2: cross-Initiative awareness (Store → sherpa)

Today the sherpa sees only the current initiative's ER and artifacts. With Store:

```
Current:  Sherpa reads local ER + docs/sdlc/ → generates artifacts in isolation
With Store: Sherpa queries Store → gains organizational context → generates artifacts with awareness
```

| Sherpa Capability | Current | With Store |
|-------------------|---------|------------|
| Health dashboard (WS-5) | Rule-based: "SCK trigger was met 3 artifacts ago" | Data-driven: "3 prior initiatives with similar SADs all needed SCK — your team's rollback rate without SCK is 2x" |
| Utility prompt offers | "There's an optional stress test" | "The assumption stress test found issues in 4 of your team's last 6 initiatives — strongly recommend running it" |
| Kit transition explanation | "We're moving from PIK to EEK" | "We're moving from PIK to EEK. Your team's last P1 initiative spent 60% of its time in EEK — the SAD→TDD transition was the bottleneck" |
| Artifact generation | Template-driven only | Template + reference: "here's how a similar initiative structured their SAD §3" (from Store) |

#### S-3: live context (Twin → sherpa)

Today the sherpa generates infrastructure artifacts from human-provided descriptions. With Twin:

```
Current:  Human describes system topology → sherpa generates SMR
With Twin: Sherpa queries Twin → Twin returns live topology → sherpa generates SMR from real data
```

| Sherpa Task | Current | With Twin |
|------------|---------|-----------|
| SMR generation | "Tell me about your services and dependencies" | "The Twin shows 5 services with 8 dependencies — let me draft the SMR" |
| RSA blast radius | "What depends on this service?" | "The Twin shows 3 upstream consumers — deployment risk is moderate" |
| ODK incident context | "What changed recently?" | "The Twin shows a deployment 2 hours before the incident to service X, which service Y depends on" |
| RHR health picture | "How are SLOs?" | "The Twin shows SLO compliance at 99.2% with a burn rate trend that will breach error budget in 4 days" |

#### S-4: data-Driven recommendations (Analytics → sherpa)

Today the sherpa recommends presets and kit adoption based on navigation map decision tables. With Analytics:

```
Current:  Sherpa cites decision table: "J-EEK-PATH says Path A because you have a frozen DPRD"
With Analytics: Sherpa cites decision table + evidence: "J-EEK-PATH says Path A, and Analytics shows
                Path A initiatives with frozen DPRDs from full discovery have a 40% lower rework rate"
```

The Decision Explanation Protocol (WS-5) evolves from rule-citing to evidence-citing. The decision tables remain authoritative — Analytics provides supporting evidence, not overrides.

#### S-5: training mode (Playground → sherpa)

The sherpa skill could operate in two modes with identical behavior but different context:

| Mode | Environment | Artifacts | Consequences |
|------|-------------|-----------|-------------|
| Production | Real project directory | Real frozen artifacts affecting real initiatives | Full governance — freeze-before-promote, ER maintenance, cross-kit handoffs |
| Training | Playground sandbox | Practice artifacts in isolated directory | Safe to fail — governance rules enforced for learning but mistakes don't affect real work |

Same skill definition, same playbook adherence, same decision table routing. The Playground provides the sandboxed environment; the sherpa provides the guided experience. A trainee interacts with the sherpa identically in both modes — they learn the real process, not a simplified version.

#### S-6: schema-Accelerated validation (Schema → sherpa)

Today the sherpa generates an artifact and then validates via a separate AI session reading the spec. With Schema:

```
Current:  Generate artifact → separate AI session reads spec → evaluates all gates → PASS/FAIL
With Schema: Generate artifact → instant Schema check (structural) → flag structural issues immediately
             → separate AI session evaluates semantic gates only → PASS/FAIL
```

Structural validation (required sections present, field formats correct, enumeration values valid, cross-references resolve) happens instantly against the Schema. The heavier AI validation session focuses on semantic evaluation — is the content *meaningful*, not just *present*? This is a faster feedback loop: structural issues are caught in seconds, not after a full validation session.

### Operational layer flow summary

| Mechanism | Current Integration Points | system Integration Points | Total |
|-----------|---------------------------|------------------------------|-------|
| **Lenses** (12) | AI session reads spec + artifact | L-1 Engine evidence, L-2 deterministic pre-screening, L-3 Analytics patterns | +3 |
| **Tools** (18) | Sherpa invokes in AI sessions | T-1 Schema contracts, T-2 Engine invocation, T-3 Store+Twin enrichment, T-4 Store indexing | +4 |
| **Skills** (sherpa) | Reads framework files, guides humans | S-1 Engine evidence, S-2 Store context, S-3 Twin live state, S-4 Analytics insights, S-5 Playground training, S-6 Schema validation | +6 |
| **Total** | 3 mechanisms, framework-only | +13 system integration points | |

---

## Phased execution plan

The low-coupling design means components that share only the Schema contract can be built in parallel. Tracing the interface contract table produces three phases, not seven sequential steps.

### Phase 1: schema (Sequential — must be first)

```
┌──────────────┐
│ AIEOS Schema │
└──────────────┘
```

**Duration:** Smallest project in the system. The format design is the hard decision; individual schemas are mechanical.

**What blocks on this:** Engine, Store, Twin (for SMR schema alignment), Analytics (indirectly via Store), Reporter (indirectly via Store). Everything except Playground.

**Why it can't be parallelized:** Schema defines the contracts that Phase 2 components consume. Building Engine or Store without Schema means building custom parsers that will be thrown away when Schema arrives. The whole point of Schema is to avoid that waste.

**outputs:**
1. Schema format specification (the meta-schema — how specs are expressed as YAML/JSON)
2. ~40 individual schema files (one per spec across all kits)
3. Schema sync tests (Tier 2 tests validating Markdown ↔ Schema consistency)
4. Schema governance rules (added to the AIEOS governance model)

**Exit criteria:** All existing specs have corresponding schema files. Tier 2 tests validate semantic consistency (hard gate counts, template section alignment, validator gate coverage). Schema format is documented and stable enough for Phase 2 consumers to build against.

### Phase 2: engine + store + twin + playground (Parallel)

```
┌─────────────────────┐  ┌─────────────────┐  ┌──────────────┐  ┌──────────────┐
│ Evaluation Engine   │  │ Artifact Store  │  │ System Twin  │  │  Playground  │
│ + Adapter SDK       │  │                 │  │              │  │              │
└─────────────────────┘  └─────────────────┘  └──────────────┘  └──────────────┘
         │                        │                  │                │
    needs Schema            needs Schema        needs SMR         needs only
    (Phase 1)               (Phase 1)          schema concept     Framework
                                               (Phase 1)         (exists)
```

**Why these four can run in parallel:**

| Component | Upstream Dependency | Interface to Other Phase 2 Components |
|-----------|--------------------|-----------------------------------------|
| Engine | Schema (Phase 1) | Produces evidence in AIEOS validator JSON format — this format already exists today. Engine doesn't need Store to function; it writes evidence artifacts to the filesystem just like the sherpa does now. |
| Store | Schema (Phase 1) | Indexes artifacts from the filesystem. Doesn't need Engine — it can index the manually-produced artifacts that already exist from completed initiatives (e.g., aieos-console). |
| Twin | SMR schema concept (Phase 1) | Consumes deployment events from external systems (CI/CD, Kubernetes). Doesn't need Engine or Store — it builds the topology graph independently. |
| Playground | AIEOS Framework (exists) | Consumes specs, templates, playbooks, and integration test fixtures. Doesn't need any other system component. |

**The key insight:** Engine and Store are independent to *build* but more valuable *together*. Their interface is the AIEOS validator JSON format, which already exists. They agree on the contract up front (Schema's job, done in Phase 1), then each team builds to that contract without needing the other's code.

**Phase 2 integration point:** Once both Engine and Store are independently functional, connect them:
- Engine writes evidence artifacts → Store indexes them (this is just "Store indexes what's in the filesystem," which Store already does)
- Store provides upstream artifact status → Engine queries before evaluation ("is the SAD this TDD references actually frozen?")

This integration is additive — neither component changes its core; they just become aware of each other through the contracts.

**Twin integration point:** Once Twin and Engine are independently functional:
- Twin provides runtime context → Engine queries for blast radius during RSA evaluation
- Twin provides topology → Engine verifies deployment claims in ORD against live state

Again, additive — Twin and Engine each work alone; together they're smarter.

**Phase 2 outputs per component:**

| Component | Minimum Viable Deliverable |
|-----------|---------------------------|
| Engine | Schema-driven evaluation of one artifact type (e.g., SAD) using one adapter (e.g., markdownlint). Produces AIEOS validator JSON. Demonstrates: schema consumption, adapter invocation, evidence normalization. |
| Store | Index all artifacts from one completed initiative (e.g., aieos-console). Lineage query working ("what DPRD produced this ORD?"). Full-text search working. Demonstrates: schema-aware field extraction, cross-artifact lineage. |
| Twin | Topology graph for one service from deployment events. SMR auto-generation from Twin snapshot. Demonstrates: event ingestion, materialized topology, governed artifact output. |
| Playground | One interactive P5 scenario (simplest preset). Reuses integration test fixture. Immediate feedback on freeze-before-promote violations. Demonstrates: framework consumption, interactive guidance, governance rule enforcement in training context. |

**Phase 2 exit criteria:** Each component delivers its core value independently. Integration between components is demonstrated but not required for individual operation.

### Phase 3: analytics + reporter (Parallel, after store)

```
┌───────────────────────┐  ┌───────────────────────┐
│ Governance Analytics  │  │ Compliance Reporter   │
└───────────────────────┘  └───────────────────────┘
         │                       │
    needs Store             needs Store
    (Phase 2)               (Phase 2)
```

**Why these wait for Phase 2:** Both Analytics and Reporter are consumers of the Store's query API. They can't deliver meaningful value without indexed, queryable artifact data across multiple initiatives.

**Why these two can run in parallel:** Analytics and Reporter both consume the Store but don't consume each other. Analytics produces trend insights; Reporter produces audit packages. Different outputs, same input source, no dependency between them.

**Phase 3 outputs per component:**

| Component | Minimum Viable Deliverable |
|-----------|---------------------------|
| Analytics | One cross-initiative insight from Store data (e.g., "average time from ORD freeze to RER freeze across all initiatives"). Framework improvement signal for one spec (e.g., "gate X fails on N% of first attempts"). Demonstrates: Store query consumption, pattern detection, evidence-cited insights. |
| Reporter | One audit package for one regulation (e.g., SOC2 Type II) covering one system. Control-to-evidence mapping with gap analysis. Demonstrates: Store query consumption, control mapping, gap detection, package assembly. |

**Phase 3 exit criteria:** Analytics produces actionable framework improvement signals. Reporter produces an audit package that an auditor would accept.

### Phase 4: people & impact

| ID | Component | Repository | Type | Dependencies |
|----|-----------|-----------|------|-------------|
| **ECO-008** | Engineer Impact Framework | `aieos-engineer-impact` | Documentation — quarterly engineer impact assessment | None (standalone; optional ER §16 integration) |

**Why separate from Phase 1–3:** Phases 1–3 make governance *executable and observable* (software tooling). Phase 4 extends AIEOS into *people measurement* — a different domain. The Engineer Impact Framework is documentation (rubrics, templates, process guides), not software. It has no dependency on Schema, Engine, or Store.

**What ECO-008 delivers:**
- Two-tier assessment framework (Starter ~2hrs/quarter, Advanced ~8hrs/quarter)
- Four dimensions: Outcome-Driven Impact, Enablement Impact, Operational Excellence, Team Multiplier
- Contribution Factor rubric (0–1 scale), Complexity Factor rubric (1.0–1.7)
- Calibration meeting template and gaming detection checklist
- Optional AIEOS integration: ER §16 Impact Attribution captures contribution data at artifact freeze points; IEK ES/PES can consume this data for execution pattern analysis

**Phase 4 exit criteria:** One team completes a full quarterly assessment cycle using the templates.

### Phase 5: orchestrate & execute

| ID | Component | Repository | Type | Dependencies |
|----|-----------|-----------|------|-------------|
| **ECO-009** | Agent Harness | `aieos-agent-harness` | Software — pluggable multi-agent orchestration engine | ECO-001 (schema for artifact event contracts), INT-002 (adapter pattern proven) |

**Why a new phase:** Phases 1–3 make governance *observable and measurable*. Phase 4 extends into *people*. Phase 5 extends into *execution orchestration* — the runtime layer that binds AI providers and deterministic tools to AIEOS artifact lifecycle events. This is the most ambitious system project because it operates at the boundary between governance (Markdown, immutable) and execution (code, dynamic).

**What ECO-009 delivers:**

A pluggable orchestration engine that lets users bind different AI providers (and non-AI tools like SAST scanners) to artifact lifecycle events, while enforcing AIEOS invariants.

**Core components:**

1. **Lifecycle Binder** — Maps artifact lifecycle events to agent invocations. Events include `pre_generation`, `post_generation`, `pre_validation`, `post_validation`, `post_freeze`, and `on_failure`. Users configure which agents handle which events for which artifact types:
   ```yaml
   bindings:
     - event: pre_generation
       artifact_type: SAD
       agents: [architecture-context-builder]
     - event: post_generation
       artifact_type: SAD
       agents: [sad-validator]  # Runs in separate session (enforced)
     - event: post_freeze
       artifact_type: WDD
       agents: [github-issues-sync]  # Non-LLM adapter
   ```

2. **Routing Engine** — Four execution strategies, each governed:
   - **Parallel consensus** — Multiple agents evaluate the same artifact; configurable agreement threshold. Maps to PRK lens parallelism pattern. Outputs are independent (no shared context between parallel agents).
   - **Pipeline** — Sequential agent chain where output of one feeds the next. Maps to artifact dependency chains. Each step validates before passing downstream.
   - **Fallback** — Primary agent fails or is unavailable; secondary agent invoked with same inputs. **New to AIEOS** — requires new routing spec in tool-governance. Circuit breaker prevents repeated failures.
   - **Cost-aware** — Routes to different providers based on artifact risk level, complexity, or budget constraints. **New to AIEOS** — low-risk artifacts to cheaper models, high-risk to premium. Requires cost-tier classification per provider.

3. **Provider Adapter Layer** — Thin adapters implementing the AIEOS adapter conformance contract (`push()/verify()/health()`) extended for AI invocation:
   ```
   interface AgentAdapter {
     invoke(request: AgentRequest): Promise<AgentResponse>;
     health(): HealthStatus;         // ok | degraded | down
     capabilities(): Capability[];    // What this adapter can do
     costEstimate(request): Cost;     // Estimated cost for this invocation
   }
   ```
   Implementations: `AnthropicAdapter`, `OpenAIAdapter`, `AzureOpenAIAdapter`, `LocalLLMAdapter`, `ToolAdapter` (non-LLM: SAST, linters, dependency scanners).

4. **State Manager** — Reads and writes AIEOS state artifacts on disk (never in a database):
   - Reads: ER (current position, frozen artifacts), Sherpa Journal (decision history), frozen upstream artifacts (generation context)
   - Writes: ER state block updates (current position), Sherpa Journal entries (routing decisions, agent invocations, costs), validation results
   - Invariant: disk is the system of record. The harness may cache in memory for performance, but all authoritative state is files.

5. **Observability Layer** — Per-invocation metrics:
   - Token usage and cost (per agent, per artifact, per initiative)
   - Latency (generation time, validation time, total cycle time)
   - Provider health (availability, error rates, degradation events)
   - Quality signals (completeness scores over time, convergence iteration counts)
   - Cost anomaly detection (sudden cost spikes trigger alerts)

**AIEOS invariants enforced by the harness:**

| Invariant | How the harness enforces it |
|-----------|---------------------------|
| Generation/validation separation | Lifecycle binder never routes generation and validation to the same agent session. Separate `invoke()` calls with fresh context. |
| Freeze-before-promote | State manager checks upstream artifact status before invoking downstream generation. Blocks if upstream is not frozen. |
| Human freeze decision | Harness presents validation results to user. Never autonomously transitions artifact status from Validated → Frozen. |
| Bounded convergence | Convergence loop counter maintained by state manager. After 3 iterations of Remediate-and-Retry, harness escalates to human with full history. |
| Validators judge only | Validation agent responses are parsed into standardized JSON output. Non-conforming responses (suggestions, redesigns) are rejected. |
| Tool-agnostic policy | Provider-specific details live in adapter code, never in AIEOS specs/prompts/validators. The harness reads AIEOS governance as-is. |
| Disk-based state | All state changes written to ER + Sherpa Journal files. No hidden state in memory or database. |

**What the harness does NOT do:**
- Does not modify AIEOS governance files (specs, templates, prompts, validators)
- Does not make freeze decisions (presents results, human decides)
- Does not choose artifact types (follows the preset/flow defined in AIEOS)
- Does not replace the sherpa (the sherpa remains the conversational guide; the harness is the execution substrate)
- Does not maintain its own prompt library (uses AIEOS four-file prompts)

**Relationship to existing components:**
- **ECO-001 (Schema):** Harness consumes schema for artifact event contracts, gate enumeration, and input/output validation
- **ECO-002 (Evaluation Engine):** Complementary — Engine validates artifacts programmatically; Harness orchestrates the agents that generate and validate them. Engine could be a validator adapter in the harness.
- **ECO-003 (Artifact Store):** Harness queries Store for cross-initiative context before generation (existing sherpa integration point)
- **INT-002–005 (Adapters):** Existing adapters (GitHub Issues, GitHub Releases) become adapter implementations in the harness's provider layer
- **Sherpa:** Sherpa remains the user-facing guide. Harness operates underneath — when sherpa says "generate SAD," the harness routes to the configured agent, enforces separation, and returns results to sherpa for user presentation.

**Phase 5 exit criteria:**
1. At least 2 provider adapters working (e.g., Anthropic + OpenAI, or Anthropic + a SAST tool)
2. One complete artifact lifecycle (generate → validate → present for freeze) running through the harness
3. Fallback routing demonstrated (primary unavailable → secondary invoked → same result quality)
4. Cost and latency observability producing per-invocation metrics
5. All AIEOS invariants verified (generation/validation separation, human freeze, disk state, bounded convergence)

### Phase 2-3 enhancement: post-Integration capabilities

After Phase 2 components are independently functional and Phase 3 components exist, cross-component integration unlocks capabilities that no single component provides:

| Capability | Requires | What It Enables |
|-----------|----------|-----------------|
| Predictive initiative risk | Engine + Store + Analytics | "This initiative's artifact pattern matches 3 prior initiatives that required redesign" |
| Continuous compliance | Engine + Store + Reporter | Evidence is auto-collected (Engine), auto-indexed (Store), and continuously mapped to controls (Reporter). Audits become "pull the current report" not "assemble a package" |
| Context-aware evaluation | Engine + Twin | Engine checks ORD deployment claims against Twin's live state. RSA blast radius assessment uses real dependency data |
| Informed training | Store + Analytics + Playground | Playground scenarios prioritized by Analytics ("teams struggle most with SAD→TDD"). Reference artifacts from Store |
| Framework evolution | Analytics + Store + Humans | Analytics detects "80% of PFDs fail scope_bounded on first pass" → humans evaluate → spec revision → Schema updated → Engine enforces new rules. Full feedback loop |

These are not separate projects — they emerge from connecting Phase 2-3 components through their existing contracts.

### Timeline summary

```
Phase 1 ──►  Phase 2 (parallel) ─────────────────►  Phase 3 (parallel)

Schema       Eval Engine ─┐                            Gov Analytics
             Store       ─┤── integrate after each     Reporter
             Sys Twin    ─┤   delivers independently
             Playground   ┘
```

| Phase | Components | Parallelism | Depends On |
|-------|-----------|-------------|------------|
| 1 | Schema | Sequential (1 project) | AIEOS Framework (exists) |
| 2 | Eval Engine, Store, Sys Twin, Playground | 4 projects in parallel | Schema (Phase 1) |
| 3 | Gov Analytics, Reporter | 2 projects in parallel | Store (Phase 2) |
| 4 | Engineer Impact | Sequential (1 project) | None (standalone) |
| 5 | Agent Harness | Sequential (1 project) | Schema (Phase 1), INT-002 (adapter pattern) |
| 2-3+ | Cross-component integration | Incremental, as components mature | Multiple Phase 2-3 components |

**Total: 5 phases covering 9 projects, with up to 4 projects running in parallel.**

The original priority ranking (1-7 sequential) assumed each project had to complete before the next started. The phased plan recognizes that low coupling means independent buildability — the same architectural principle that makes the system maintainable also makes it parallelizable.

---

## Cross-Reference matrix

How every component relates to every other. Read rows as "how {row} relates to {column}."

|  | AIEOS Framework | Schema | Eval Engine | Store | Gov Analytics | Reporter | Sys Twin | Playground |
|--|----------------|--------|-------------|-------|---------------|----------|----------|------------|
| **AIEOS Framework** | — | Schema strengthens framework testing (drift detection, semantic validation) | Engine automates evidence collection the framework currently requires humans to do | Store indexes what the framework produces | Analytics measures whether the framework is effective | Reporter assembles framework evidence for auditors | Twin provides live state that SMR captures as snapshot | Playground teaches the framework |
| **Schema** | Lives alongside Markdown specs; governed by governance model | — | Engine consumes schemas as evaluation rules (generic, not per-artifact-type) | Store uses schemas for structured field extraction and indexing | Analytics uses schemas to normalize data across artifact types | Reporter uses schemas to map artifact sections to controls | Twin uses SMR schema to align its data model | Playground uses schemas for real-time practice artifact validation |
| **Engine** | Governed by tool-governance-spec; each adapter has a bindings file | Requires Schema to be generic | — | Produces evidence artifacts that Store indexes; queries Store for upstream dependencies | Primary data producer (timestamps, gate results, findings) | Ensures evidence artifacts are always produced (automated collection) | Queries Twin for runtime context during evaluation | Powers "real feedback" mode with actual tool checks |
| **Store** | Indexes framework artifacts; cross-initiative ER | Uses schemas for structured queries | Indexes Engine evidence; provides upstream context to Engine | — | Provides indexed data that Analytics queries | Provides evidence artifacts within audit scope; enables lineage tracing | Store = governed state; Twin = live state; together enable drift detection | Provides real artifact examples for training reference |
| **Analytics** | Feedback loop: framework-level improvement signals | Uses schemas to normalize cross-type data | Correlates Engine results across initiatives | Runs all queries against Store index | — | Tracks compliance posture trends over time | Correlates governance data (Store) with runtime data (Twin) | Identifies struggling areas to prioritize scenarios |
| **Reporter** | SCK produces evidence; Reporter assembles | Uses schemas for control-to-field mapping | Engine ensures evidence is always current | Queries Store for evidence within audit scope | Analytics tracks compliance path | — | Twin provides system inventory for audit scoping | Control mappings enrich compliance training scenarios |
| **Twin** | Feeds SMR (governed snapshot from live state) | Uses SMR schema for data model alignment | Provides runtime context to Engine evaluations | Complements Store (planned vs running vs recorded) | Provides runtime data for correlation with governance data | Provides system inventory for audit scoping | — | Provides realistic topologies for advanced scenarios |
| **Playground** | Consumes framework files; reuses integration test fixtures | Uses schemas for instant practice feedback | Uses Engine for realistic validation | Uses Store for reference examples | Informed by Analytics on what to prioritize | Uses control mappings for compliance scenarios | Uses topologies for realistic complexity | — |

---

## system design principles

### Overarching constraint: high cohesion, low coupling

The system must be a **coherent system**, not a collection of tools that happen to share a name. Coherence means every component serves a clear, focused purpose (high cohesion) while depending on other components only through narrow, well-defined interfaces (low coupling).

**High cohesion** means each component does one thing completely:

| Component | Single Responsibility | Violation Example (What NOT to Do) |
|-----------|----------------------|-------------------------------------|
| Schema | Machine-readable spec contracts | Schema that also contains evaluation logic (that's the Engine's job) |
| Engine | Evaluate artifacts against schemas using tools | Engine that also indexes results for search (that's the Store's job) |
| Store | Index and query artifacts across initiatives | Store that also computes trend analytics (that's Analytics' job) |
| Analytics | Derive cross-initiative intelligence from Store data | Analytics that also produces audit packages (that's the Reporter's job) |
| Reporter | Assemble audit-ready evidence packages | Reporter that also tracks live system state (that's the Twin's job) |
| Twin | Track live system topology and state | Twin that also enforces governance rules (that's the Engine's job) |
| Playground | Interactive learning environment | Playground that also governs real initiatives (that's the Framework's job) |

When a component starts absorbing adjacent responsibilities, it becomes harder to change, harder to test, and harder to adopt independently. The test for cohesion: *can you describe what this component does in one sentence without using "and"?*

**Low coupling** means components interact through contracts, not knowledge of internals:

| Interface | Contract | What Flows Through It |
|-----------|----------|----------------------|
| Framework → Schema | Schema format specification | Machine-readable spec definitions |
| Schema → Engine | Schema files (YAML/JSON) | Hard gates, required sections, field enumerations |
| Schema → Store | Schema files (YAML/JSON) | Field definitions for structured indexing |
| Engine → Store | Evidence artifact format (AIEOS validator JSON) | Evaluation results, findings, timestamps |
| Store → Analytics | Query API (search, lineage, aggregation) | Indexed artifact data |
| Store → Reporter | Query API (scoped by audit) | Evidence artifacts within audit scope |
| Twin → Engine | State query API (topology, health) | Current deployment state, dependency graph |
| Twin → Store | Event format (state changes) | Deployment events, topology changes |
| Analytics → Humans | Insight report format | Findings, recommendations, evidence citations |

Each arrow is a **contract**, not a function call into another component's internals. If the Store switches from PostgreSQL to Elasticsearch, the Analytics query API doesn't change. If the Engine switches from running adapters locally to invoking them via API, the Store still receives the same evidence format.

**The coupling test:** *Can you replace one component's implementation without modifying any other component's code?* If yes, coupling is low. If replacing the Store requires Engine changes, something crossed a boundary it shouldn't have.

**The coherence test across the system:** *Can someone new look at the component list and immediately understand what each one does and why it's separate?* If two components seem like they should be one, either the boundary is wrong or the naming is unclear. If one component seems like it should be two, it's absorbed a responsibility it shouldn't have.

This constraint is not aspirational — it's architectural. Every design decision, API boundary, and data flow should be evaluated against it. The system will evolve over years; components will be rebuilt, replaced, and extended. Low coupling means any component can be rebuilt without cascading changes. High cohesion means the rebuild is scoped and comprehensible.

---

The AIEOS governance framework is built on 9 design philosophies (see `philosophy.md`). These aren't just governance rules — they're engineering principles that apply whenever structured systems make decisions that affect software delivery. Each system component should inherit the applicable principles and, where the runtime context introduces new concerns, extend them.

### Principles that transfer directly

#### P1. structure enables speed (Philosophy §1)

**In the framework:** Structure is in the documents, not in gatekeepers.

**In the system:** Structure is in the schemas, not in custom parsers. Every system component should consume structured contracts (schemas, evidence format, query interfaces) rather than parsing prose or inferring structure from conventions. An Engine adapter that works by regex-parsing tool output is the system equivalent of a spec whose rules live in the prompt — it works until it doesn't, and when it breaks, the failure is silent.

| Component | Application |
|-----------|------------|
| Schema | Defines the structure contract. All other components inherit structure from it. |
| Engine | Schema-driven evaluation routing — not hardcoded per-artifact-type logic. Adding a new artifact type is configuration, not code. |
| Store | Schema-driven indexing — field extraction follows the schema, not custom parsers per artifact type. |
| Analytics | Schema-driven normalization — comparing findings across artifact types works because schemas define what "a finding" is for each type. |
| Twin | Entity model aligned with SMR schema — the Twin's data model is structured by governance, not invented independently. |

#### P2. AI-Native, not AI-Replaced (Philosophy §2)

**In the framework:** Every freeze point is a human decision. AI generates; humans approve.

**In the system:** Every *action* point is a human decision. Components produce evidence and recommendations; humans (or sherpa-guided humans) act on them. This is the principle that prevents the Engine from becoming an autonomous promotion system and prevents Analytics from auto-modifying specs.

| Component | Application |
|-----------|------------|
| Engine | Produces evidence artifacts and PASS/FAIL results. Does NOT auto-promote, auto-deploy, or auto-rollback. The Engine's output feeds into human decision workflows (RSA, QGR), not into deployment pipelines directly. |
| Analytics | Produces insights and recommendations ("this spec gate fails 80% of the time"). Does NOT auto-modify specs, auto-tune thresholds, or auto-change presets. Framework changes require human review. |
| Reporter | Produces audit packages and gap analysis. Does NOT auto-remediate gaps or auto-generate missing evidence. Humans decide how to address compliance gaps. |
| Twin | Produces system state and drift alerts. Does NOT auto-correct drift or auto-update the EM. Drift is a finding, not an auto-fix trigger. |
| Playground | Provides feedback during practice. Does NOT auto-advance trainees or certify competency. Learning assessment is human judgment. |

#### P3. explicit over implicit (Philosophy §3)

**In the framework:** Rules are in specs. Routing is in records. Missing information is marked.

**In the system:** Configuration is in schemas. Decisions are in audit logs. Failures are in structured error output. No system component should silently swallow errors, infer missing configuration, or make decisions without recording why.

| Component | Application |
|-----------|------------|
| Engine | Every evaluation decision is logged: which schema was used, which gates were checked, what the tool returned, what the normalized result was. Silent pass (skipping a gate because the adapter didn't return data for it) is not permitted — missing evidence is a finding, not an absence. |
| Store | Every index operation records what was parsed and what was skipped. If an artifact can't be parsed against its schema, the Store records the parse failure rather than silently omitting the artifact. |
| Analytics | Every insight cites its evidence: "rollback rate is 3x for SSK-skipping initiatives (N=12, date range 2026-01 to 2026-06, source: Store query Q-xxx)." Analytics never asserts a pattern without stating the sample, the query, and the confidence. |
| Reporter | Every control mapping is explicit: "SOC2 CC6.1 → SAR §3 (access control findings) + EM §4 (security groups)." No implicit coverage claims. Gaps are gaps, not "probably covered by..." |
| Twin | Every state change is an event with a source: "service X version changed from v2.1 to v2.3 at 2026-03-16T14:30Z, source: deployment event from ArgoCD." No "current state" without provenance of how it got there. |

#### P4. separation of concerns (Philosophy §4)

**In the framework:** The four-file system separates rules (spec), structure (template), generation behavior (prompt), and quality judgment (validator).

**In the system:** Each component has a clear, non-overlapping responsibility. No component should absorb another's concern. This is the cohesion dimension of the overarching High Cohesion, Low Coupling constraint — P4 provides the *why* (rule drift), the overarching constraint provides the *test* (can you describe it in one sentence without "and"?).

| Concern | Owner | NOT the job of |
|---------|-------|---------------|
| What the rules are | Schema (from AIEOS specs) | Engine doesn't define rules — it enforces them |
| Whether an artifact passes | Engine (deterministic checks) + AI validator (semantic checks) | Store doesn't judge quality — it indexes |
| What happened across initiatives | Store (indexing) + Analytics (intelligence) | Engine doesn't do cross-initiative analysis |
| What's running now | Twin | Store doesn't track live state; Twin doesn't track governed artifacts |
| Whether compliance is met | Reporter | Analytics doesn't produce audit packages; Reporter doesn't track trends |
| What should change in the framework | Humans, informed by Analytics | No component auto-modifies AIEOS specs, prompts, or validators |

The most important separation: **the Engine enforces rules but does not define them.** If the Engine team needs a stricter check, they propose a spec change through the normal AIEOS governance process — they don't add it as Engine-level logic. This prevents rule drift between the framework and its runtime enforcement.

#### P5. validators judge, not help (Philosophy §5)

**In the framework:** Validators produce PASS/FAIL with blocking issues. No suggestions, no redesign.

**In the system:** Every evaluation component (Engine, Analytics, Reporter) reports findings — it does not fix them.

| Component | Judges | Does NOT |
|-----------|--------|----------|
| Engine | "Gate X: FAIL. Finding: §3 missing required field 'Fallback'" | "Here's what §3 should say..." |
| Analytics | "Initiatives skipping SCK have 3x rollback rate (p<0.05)" | "Therefore, make SCK required for P2" (that's a human decision) |
| Reporter | "Gap: SOC2 CC6.8 has no covering evidence artifact" | "Generate a DAR to fill this gap" (that's a human + sherpa action) |
| Twin | "Drift: Production has v2.3 but EM specifies v2.1" | Auto-deploying v2.1 to fix the drift |

This principle prevents system components from becoming "helpful" in ways that obscure what actually needs human attention. A Reporter that auto-generates evidence to fill gaps is hiding compliance problems, not solving them.

#### P6. immutability is the source of reliability (Philosophy §6)

**In the framework:** Frozen artifacts are immutable. Changes go through re-entry.

**In the system:** Indexed data is append-only. Evaluations are immutable once recorded. Historical state is never overwritten.

| Component | Application |
|-----------|------------|
| Engine | An evaluation result, once recorded, is never modified. If a re-evaluation is needed (spec changed, tool upgraded), it produces a new evaluation with a reference to the previous one. Historical results remain for trend analysis. |
| Store | The Store indexes frozen artifacts. When an artifact is superseded (new version), the original index entry is retained with a "superseded by" reference. The Store never deletes index entries for frozen artifacts. |
| Analytics | Analytics insights are timestamped snapshots. When a new analysis runs, it produces a new snapshot — it doesn't modify the previous one. Trend analysis depends on comparing snapshots over time. |
| Twin | The Twin is event-sourced. Every state change is an appended event. The current state is a materialized view of the event stream. Historical state can always be reconstructed by replaying events to a point in time. |

#### P7. tool-Agnostic policy (Philosophy §7)

**In the framework:** Specs never reference vendor tools. Tool details live in bindings files.

**In the system:** Core component interfaces never reference vendor implementations. Integration details live in adapters and configuration.

| Component | Application |
|-----------|------------|
| Engine | Engine core knows about schemas, gates, and evidence format. It does NOT know about Semgrep, Trivy, or ESLint — those are adapters. Swapping a SAST tool means swapping an adapter, not modifying the Engine. |
| Store | Store interface is query-based (lineage, search, field extraction). Backend could be PostgreSQL, SQLite, Elasticsearch, or flat files — the Store's API doesn't change. |
| Twin | Twin interface is event-based (publish event, query state). Backend could be Kafka + Neo4j, or a simple event log + in-memory graph — the Twin's API doesn't change. |
| Reporter | Reporter knows about controls and evidence schemas. It does NOT know about specific audit platforms (Vanta, Drata, AuditBoard) — those are output format adapters. |
| Playground | Playground knows about AIEOS flows and schemas. It does NOT know about specific LMS platforms — those are integration adapters. |

#### P8. independent components, compatible system (Philosophy §8)

**In the framework:** Each kit is standalone. An organization can start with just one kit.

**In the system:** Each component is independently deployable. An organization can adopt Schema alone (for better testing), then add Engine later, then Store later — without requiring the full system on day one. This is the coupling dimension of the overarching High Cohesion, Low Coupling constraint — P8 provides the *why* (incremental adoption), the overarching constraint provides the *test* (can you replace one component without modifying another?).

| Adoption level | What you get |
|---------------|-------------|
| Schema only | Deeper Tier 2 tests, drift detection, consistency validation for the existing framework |
| Schema + Engine | Automated evidence collection, deterministic gate checks on real artifacts |
| Schema + Engine + Store | Cross-initiative search, lineage tracing, reuse tracking |
| Schema + Engine + Store + Analytics | Governance effectiveness measurement, framework improvement signals |
| Full system | All of the above plus compliance automation, live topology, and training |

No component should require another component to deliver its core value (except Schema, which everything requires). The Engine works without the Store — it just can't do cross-initiative queries. The Store works without the Twin — it just tracks governed artifacts, not live state. Each layer adds value on top of the previous one.

#### P9. adapt the edges, not the core (Philosophy §9)

**In the framework:** Core invariants (four-file system, freeze-before-promote, validators-as-gates) are non-negotiable. Kit-specific artifacts, principles, and tool bindings are customizable.

**In the system:** Core interfaces (schema format, evidence format, query API, event API) are non-negotiable. Adapters, backends, and UI are customizable.

| Core (don't change) | Edges (customize freely) |
|---------------------|------------------------|
| Schema format (how specs are expressed as machine-readable contracts) | Individual schema content (what gates a specific spec has) |
| Evidence format (how tool results are normalized) | Individual adapter logic (how Semgrep output becomes evidence) |
| Store query API (how artifacts are searched and traced) | Store backend (PostgreSQL, Elasticsearch, flat files) |
| Twin event format (how state changes are recorded) | Twin backend (Kafka, simple log, in-memory) |
| Analytics insight format (how findings are structured) | Analytics algorithms (what patterns to look for) |
| Reporter control mapping format (how controls map to evidence) | Individual control mappings (SOC2 CC6.1 → SAR §3) |

### Principles that extend for the system

The AIEOS framework operates in a single-session, single-initiative context. The system introduces new concerns — runtime operation, cross-initiative data, live systems — that require new principles built on the same philosophical foundation.

#### E1. evidence provenance is non-Negotiable

**Derived from:** Philosophy §3 (Explicit Over Implicit) + AI Transparency Principles §2 (AI Output Integrity)

**In the framework:** AI-generated artifacts must not present inferred information as established fact.

**Extended for system:** Every piece of evidence in the system must carry provenance: what produced it, when, from what inputs, using what tool version. An Engine evaluation without provenance is as untrustworthy as an AI-generated artifact without provenance.

This matters most for the Compliance Reporter — an audit package with evidence that can't be traced to its source is worthless. And for Analytics — an insight derived from data of unknown provenance is a guess, not an analysis.

#### E2. graceful degradation over hard dependencies

**Derived from:** Philosophy §8 (Independent Kits, Compatible System)

**New for system:** When a downstream component is unavailable, upstream components continue operating with reduced capability rather than failing entirely.

- If the Twin is down, the Engine still evaluates — it just can't provide blast radius context. The RSA notes "Twin unavailable — deployment risk assessed without live dependency data."
- If the Store is down, Analytics can't run — but the Engine and Twin continue independently.
- If the Engine is down, the sherpa workflow continues manually — the framework works without runtime enforcement, as it does today.

No component's outage should prevent software delivery. The system enhances the governance process; it must not become a bottleneck to it.

#### E3. framework authority is upstream

**Derived from:** Philosophy §4 (Separation of Concerns) + Philosophy §9 (Adapt Edges, Not Core)

**New for system:** The AIEOS governance framework is always the source of truth. system components consume the framework's rules — they never override, extend, or contradict them.

- If the Engine adds a check that isn't in any spec, that check is invalid — it must be proposed as a spec change first.
- If Analytics recommends a threshold change, the change goes through the governance process (human reviews, spec updated, schema updated, Engine picks up the new schema).
- If the Reporter identifies a compliance gap that requires a new artifact type, that artifact type is created in the framework first, then the Reporter maps to it.

The information flow is: Framework → Schema → Components. Never: Component → Schema → Framework. The feedback loop (Analytics → framework improvement) goes through humans, not through automated schema modification.

#### E4. cross-Initiative data requires consent and scoping

**New for system:** The Store, Analytics, and Reporter operate on data from multiple initiatives, potentially across teams. This introduces data governance concerns that single-initiative AIEOS doesn't have.

- The Store must respect access boundaries — a team's initiative artifacts are not automatically visible to other teams.
- Analytics aggregations must be scoped — "your team's rollback rate" vs "the organization's rollback rate" are different queries with different authorization requirements.
- The Reporter must scope audit packages to authorized systems — an auditor for System A should not see evidence from System B unless scoped.

This principle doesn't exist in AIEOS because the framework operates within a single project directory. The system operates across projects, which requires explicit data governance.

---

## What was explicitly rejected (Not in roadmap)

These ideas from the original Implementation Master Plan are not in the system roadmap because they conflict with AIEOS philosophy:

| Idea | Why Rejected |
|------|-------------|
| **Autonomous promotion** (no human trigger) | Violates philosophy §2: every freeze point is a human decision |
| **Six-layer architecture** replacing 15-layer model | Collapses governance precision built from real initiative experience |
| **Technology-specific core** (Kafka, Neo4j, FluxCD in core architecture) | Violates §7: tool-agnostic policy. These belong in bindings, not architecture. |
| **Risk scoring in validators** | Violates §5: validators produce PASS/FAIL only. Risk scoring belongs in the decision layer. |
| **AI-replaced decision making** | Violates §2: AI generates, humans approve. The Engine produces evidence; humans (or sherpa-guided humans) make decisions. |

---

## Risks, tradeoffs, and recommendations

### Strengths of this plan

**Schema delivers immediate, measurable value with minimal risk.** The existing test suite has 90 tests that verify structural correctness. Schema adds semantic correctness — spec/template drift, gate consistency, prompt alignment. These are real gaps we encountered during WS-1 (renaming `failure_mode_analysis` → `failure_mode_identification` required manually updating the prompt and validator). Schema catches that automatically. Measurable by: test count increase and drift detection rate.

**Low coupling means low commitment.** You don't have to build all 7 projects. Schema alone is valuable. Schema + Engine is valuable. You can stop at any phase and still have delivered something useful. The architecture was explicitly designed for independent deployability — the same principle that makes the system maintainable also means partial adoption isn't a waste.

**Compliance Reporter has a direct business case.** For regulated organizations, audit preparation costs real money — staff time, consultant fees, deadline pressure. AIEOS already produces the evidence (CER, SAR, DAR, QGR). The Reporter assembles it. Measurable by: hours spent on audit prep before vs. after.

**Engine solves a demonstrated problem.** The sherpa session for aieos-console required manually collecting test results, coverage data, and deployment evidence. The human gathered it and pasted it in. Engine automates this. Measurable by: time from code complete to QGR generated.

**The three-layer architecture is clean.** Governance (Markdown), system (runtime), and operational (lenses/tools/skills) each have clear boundaries and can evolve independently. No layer pollutes another.

### Risks and weaknesses

**Risk 1: The framework is validated by exactly one initiative.**

aieos-console is the only initiative that has gone through the full pipeline (PIK → EEK → REK). All 15 kits are built but most have never been exercised by a real project. We're designing system infrastructure for a governance framework with limited production mileage.

*Why this matters:* Schema, Engine, Store — they all assume specs are stable enough to formalize as machine-readable contracts. If running 5 more initiatives reveals that 30% of specs need major revision, every schema is wrong and every Engine rule is wrong.

*Severity:* **High.** This is the single biggest risk in the plan.

**Risk 2: 32 integration points create maintenance surface area.**

Each integration point is a contract between independent projects. When a spec changes, the cascade is: Markdown spec → Schema → Engine rules → Store indexing → Analytics normalization. That's 5 touchpoints for one spec change. Low coupling mitigates this (contracts, not internals), but doesn't eliminate it.

*Why this matters:* Framework evolution slows down as more system components depend on spec stability.

*Severity:* **Medium.** Manageable with Schema as the single source of machine-readable truth — but only if Schema versioning and backward compatibility are treated as first-class concerns.

**Risk 3: Analytics and Store require data that doesn't exist yet.**

"Initiatives that skip SSK have 3x the rollback rate" requires dozens of initiatives to be statistically meaningful. With one completed initiative, Analytics produces nothing useful. The Store indexing one initiative is a demo, not a capability.

*Why this matters:* These projects deliver value proportional to the number of initiatives using AIEOS. If adoption is slow, they sit idle.

*Severity:* **Medium.** Mitigated by the phased plan (these are Phase 3, not Phase 1), but still a real risk if adoption doesn't materialize.

**Risk 4: Twin is expensive for uncertain return.**

The SMR covers the snapshot use case. The Twin adds live topology, event sourcing, and real-time queries — requiring an event store, a graph database, and a materialization layer. That's real infrastructure cost and operational burden.

*Why this matters:* A team with 3 services doesn't need a graph database to know what depends on what. The Twin is justified only at meaningful system complexity (10+ services with non-trivial dependency graphs).

*Severity:* **Low-Medium.** Mitigated by deferral to Phase 2 and the SMR filling the gap.

**Risk 5: Sherpa-centric orchestration is a single-interface bet.**

The entire operational layer flows through the sherpa. If organizations want a different interface (web dashboard, CLI tool, Slack bot, IDE integration), the sherpa-centric design becomes a constraint.

*Why this matters:* The sherpa is Claude Code-specific. Organizations using different AI assistants or wanting non-AI interfaces need an alternative orchestration path.

*Severity:* **Low-Medium.** Mitigated by the fact that system modules have their own APIs — the sherpa is one consumer, not the only possible consumer. But the operational layer documentation currently assumes sherpa as the sole orchestrator.

**Risk 6: Premature infrastructure before product-market fit.**

The framework works today. Artifacts get generated, validated, and frozen. The system makes it *better* — but the question is whether the current pain points justify the investment, or whether the priority should be running more initiatives to find the real problems.

*Why this matters:* Building Schema for specs that will change significantly is premature optimization. Building Analytics for a single-initiative dataset is premature investment.

*Severity:* **Medium.** This is the core tension of the plan — architectural correctness vs. timing.

**Risk 7: No external demand signal.**

This system isn't being built in response to user demand. It's designed because the architecture suggests it. Design-forward approaches can produce elegant solutions to problems nobody has.

*Severity:* **Low-Medium.** Mitigated by the fact that each component addresses a real gap identified during aieos-console. But "identified during one initiative" is a thin signal.

### Will it make a meaningful and measurable improvement?

Yes — but the timing of value delivery depends on framework adoption.

| Improvement | Measurable? | When? | What It Requires |
|-------------|-------------|-------|------------------|
| Fewer drift bugs in framework | Yes — test count, drift detection rate | Immediately | Schema alone (Phase 1) |
| Faster evidence collection | Yes — time from code complete to QGR/SAR | After Engine exists | Schema + at least 2-3 adapters (Phase 2) |
| Cross-initiative search | Yes — query response time vs. manual grep | After Store exists | Multiple initiatives indexed (Phase 2 + adoption) |
| Governance effectiveness measurement | Yes — but requires statistical significance | After Analytics + maturity | 10-20+ initiatives across teams (Phase 3 + adoption) |
| Audit prep time reduction | Yes — hours before vs. after | After Reporter exists | Regulated industry adopter + SCK evidence (Phase 3) |
| Incident investigation speed | Yes — time to context assembly | After Twin exists | Production systems emitting deployment events (Phase 2) |
| Training time to competency | Yes — time for new member to run first solo initiative | After Playground exists | Enough adoption to have new team members (Phase 2) |

**Schema and Engine deliver measurable improvement quickly. Everything else requires organizational adoption at a scale that doesn't exist yet.**

### Recommendations: adoption-Gated execution

The phased plan is architecturally correct — the dependency graph and parallelism analysis are sound. But the *timing* should be driven by adoption milestones, not by the dependency graph alone.

#### Phase 0 (Before any system work): validate the framework

**Run 3-5 more initiatives through the existing framework.** Each initiative will surface framework findings (aieos-console surfaced 10). Those findings will stabilize the specs.

**Adoption milestone:** Two consecutive initiatives produce zero spec-level findings. This signals specs are stable enough to formalize as schemas.

*Why this matters:* Schema on unstable specs creates maintenance burden. Every schema revision cascades to every system consumer. Wait for stability.

#### Phase 1 (After specs stabilize): schema

Build Schema as designed. Immediate Tier 2 test improvements. No adoption dependency — Schema benefits the framework regardless of whether system modules are ever built.

**Adoption milestone for next phase:** Schema exists and Tier 2 tests validate spec/template/validator semantic consistency across all kits.

#### Phase 2 (After schema): engine first, others as justified

**Start with one adapter, not five.** Prove the concept with a single adapter (e.g., pytest for test evidence) feeding a single artifact (QGR). If that works, add adapters incrementally.

**Store:** Build when the third initiative starts producing artifacts. Before that, the Store indexes too little to justify itself.

**Twin:** Defer until there are production systems with complex enough topologies that the SMR snapshot approach becomes painful. The trigger: a team spends more than an hour assembling an SMR.

**Playground:** Defer until you know what people struggle with from real usage. The sherpa integration tests tell you what the *sherpa* struggles with. You need real users struggling to know what the *Playground* should teach.

**Adoption milestones:**
- Engine MVP: One adapter producing evidence that feeds one artifact type
- Store trigger: Third initiative starts (enough data to index)
- Twin trigger: Team reports SMR assembly taking >1 hour
- Playground trigger: Third team onboards to AIEOS (enough "new user" signal)

#### Phase 3 (After store + adoption): analytics and reporter

**Analytics:** Only after the Store has indexed 10+ initiatives across multiple teams. Before that, the sample size is too small for meaningful patterns.

**Reporter:** Only after an organization is actively undergoing audits and has SCK evidence artifacts. The first audit without the Reporter is the baseline measurement.

**Adoption milestones:**
- Analytics trigger: 10+ initiatives indexed in Store, across 3+ teams
- Reporter trigger: Organization has a scheduled audit and SCK evidence in Store

### Summary assessment

| Verdict | Detail |
|---------|--------|
| **Architecture** | Sound. Low coupling, high cohesion, clean layer separation, incremental adoption. |
| **Timing risk** | High. The framework needs more real-world mileage before system investment is justified. |
| **Recommendation** | Run more initiatives first. Build Schema when specs stabilize. Build Engine with one adapter as proof-of-concept. Gate everything else on adoption milestones. |
| **Measurable improvement** | Yes for Schema (immediate) and Engine (near-term). Uncertain for the rest until adoption exists. |
| **Biggest risk** | Building infrastructure for a framework that hasn't been validated at scale. |
| **Biggest opportunity** | If adoption materializes, the system turns AIEOS from "a process teams follow" into "an organizational capability that measures and improves itself." |

---

## Implementation notes

### WS-1 through WS-5 (Completed 2026-03-16)

Five ideas from the original plan were extracted and implemented as AIEOS governance enhancements:

| WS | What Was Implemented | Origin in Plan |
|----|---------------------|----------------|
| WS-1 | PRK lens expansion: Observability + Resilience (10→12 lenses) | Plan §5 lens catalog gaps |
| WS-2 | System Model Record (SMR) in PINFK | Plan §9 Digital Twin entity model (as governed snapshot) |
| WS-3 | Release Safety Assessment (RSA) in REK | Plan §11 Release Safety Artifact |
| WS-4 | Decision Outcome Taxonomy (6 outcomes) | Plan §8.1 Decision Outcomes |
| WS-5 | Sherpa cognitive enhancements (intent resolution, decision explanation, health dashboard) | Plan §12 Cognitive Control Plane |

These are governance framework changes (Markdown + test model). The system projects above are the runtime/tooling complement.
