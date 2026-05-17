# ANONYMIZATION

This document defines the **mandatory anonymization rules** for all content in the **aieos-governance-foundation** repository.

The goal is to ensure this repository remains:
- Publicly shareable
- Employer-neutral
- Tool-agnostic
- Safe for reuse and contribution
- Suitable for AI-assisted generation and validation

These rules apply to **all files**, including governance model text, examples, diagrams, and documentation.

---

## Core rule

> **No content may reference a real employer, internal system, or proprietary environment.**

If there is any doubt, **anonymize**.

---

## Prohibited content (Must NOT appear)

The following must never appear in this repository:

### Employer & organization identifiers
- Company names (current or former)
- Business unit names
- Internal team names
- Employer-specific acronyms
- Internal program or initiative names

---

### Internal systems & tooling
- Internal platform names
- Proprietary service names
- Internal dashboards or portals
- Internal CI/CD system names
- Internal ticketing or change-management systems
- Internal observability or logging system names

---

### Identifiers & metadata
- Internal URLs or domains
- IP addresses (internal or external)
- Email addresses
- Usernames or personal names
- Ticket IDs or prefixes
- Incident numbers
- Change request IDs
- Cluster names or environment identifiers tied to a real org

---

### Configuration & secrets
- API keys or tokens (even redacted)
- Certificates
- Credentials
- Environment-specific secrets
- Real account, subscription, or tenant IDs

---

### Logs, screenshots, and output
- Screenshots containing identifiers
- Logs with timestamps, IDs, or hostnames tied to a real environment
- Command output revealing environment details

---

## Required anonymization patterns

When examples require realism, use **explicit placeholders**.

### Approved placeholder conventions

Use ALL CAPS placeholders consistently:

- `ORG_NAME`
- `TEAM_NAME`
- `SERVICE_NAME`
- `SYSTEM_NAME`
- `REPO_NAME`
- `CLUSTER_NAME`
- `ENV_NAME`
- `PIPELINE_NAME`
- `USER_NAME`

---

### Domains & uRLs
Use:
- `example.com`
- `api.example.com`
- `git.example.com`

Never use:
- Real company domains
- Personal domains

---

### Environments
Use generic names only:
- `dev`
- `test`
- `preprod`
- `prod`

Avoid:
- Internally meaningful environment names
- Region- or datacenter-specific labels

---

### Cloud & platform references
Allowed:
- Generic cloud provider references (e.g., "a managed Kubernetes cluster")
- Open-source project names

Avoid:
- Internal landing zones
- Account naming schemes
- Tenant identifiers
