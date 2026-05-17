# TERMS

This document defines common terms used throughout the **aieos-governance-foundation** repository.
These definitions are intentionally **tool-agnostic**, **employer-neutral**, and **AI-friendly**.

---

## Core concepts

### AIEOS (AI-Enabled operating system)
A governance framework for building AI-native software organizations. AIEOS defines how kits are structured, how artifacts are produced and validated, and how kits connect across layers. It is a process operating system — not a software platform.

---

### Kit
A governed collection of specs, templates, prompts, and validators that manages one layer of the AIEOS system. Each kit is a self-contained repository with a defined artifact flow, playbook, and boundary contracts.

---

### Layer
A distinct phase of the value-delivery lifecycle. AIEOS organizes software delivery into eight layers, each governed by a kit. Layers run top-down for value delivery and bottom-up for learning.

---

### Governance model
The complete set of structural rules, taxonomy, and invariants that all AIEOS kits follow. The canonical authority is `governance-model.md` in this repository. Kit copies are synchronized from this source.

---

### Artifact
A persisted document produced at a specific stage of the SDLC. Artifacts are promoted, not rewritten, as work progresses downstream. Each artifact type is governed by a spec, template, prompt, and validator.

---

### Artifact promotion
The formal progression of an artifact to the next stage after passing validation. Once promoted, an artifact is considered frozen.

---

### Freeze
A state indicating an artifact is approved and may not be reinterpreted, expanded, or redesigned by downstream artifacts without explicit re-entry.

---

### Spec
The content rules and hard gates for an artifact type. Specs are the source of truth — prompts and validators reference specs, never inline rules.

---

### Template
The structural scaffold for an artifact. Templates define section order and required fields. They do not contain content rules — those live in the spec.

---

### Prompt
AI generation instructions for an artifact type. Prompts reference the spec and template. They include input confirmation, generation steps, and a self-review checklist.

---

### Validator
A strict, non-prescriptive quality gate that evaluates whether an artifact satisfies its spec's hard gates. Validators judge — they do not help, suggest, or redesign.

---

### Hard gate
A binary pass/fail criterion in a spec that an artifact must satisfy to be promoted. Hard gates are non-negotiable.

---

### Engagement record (ER)
A project-level artifact that spans all kit layers. It maintains an index of every artifact ID, outcome, and key decision for one initiative. ERs serve as episodic memory and portfolio synthesis inputs.

---

### Portfolio evolution signal (PES)
A cross-initiative synthesis artifact produced by the Insight & Evolution Kit. Synthesizes patterns from multiple Engagement Records and generates improvement proposals for governing files.

---

## Kit layer reference

| Layer | Question | Kit |
|-------|----------|-----|
| 1 | What are we trying to achieve? | Strategic Direction *(planned)* |
| 2 | What should we build and why? | Product Intelligence |
| 3 | What do we work on next and when? | Flow Control *(planned)* |
| 4 | How do we build it correctly? | Engineering Execution |
| 5 | How do we ship it safely? | Release & Exposure |
| 6 | How do we keep it running? | Reliability & Resilience |
| 7 | What did we learn and what changes? | Insight & Evolution |
| 8 | How do we diagnose and resolve failures? | Operational Diagnostics |

---

## Governance roles

### Kit maintainer
The person or team responsible for a kit repository. Responsible for keeping `governance-model.md` in sync with this repo and for validating kit compliance.

### Canonical authority
This repository (`aieos-governance-foundation`). When the governance model changes, this repo is updated first. Kit copies are updated to match.

---

## Notes

- These terms are intentionally generic.
- No terminology implies a specific employer, vendor, or tool.
- Examples in this repository use placeholder names and neutral contexts.
