# AIEOS Canonical Findings Schemas v1

Maps every findings-producing action in `taxonomy/actions-v1.md` to the canonical schema adapters must emit. Upstream versions are pinned. Never reference "latest."

Schema files live under `findings/schemas/<name>.schema.json`. Each schema is valid JSON Schema Draft 2020-12 and has a trivially valid example at `findings/schemas/examples/<name>.valid.json` and a trivially invalid example at `findings/schemas/examples/<name>.invalid.json`.

Non-findings actions (`build.artifact`, `sbom.verify`, `publish.*`, `deploy.*`, `verify.*`) produce evidence that is not structured findings (artifact references, commit SHAs, pass/fail observations). Their evidence shape is defined on the action entry in `taxonomy/actions-v1.md`.

---

## Canonical schema roster

Five schemas serve all thirteen findings-producing actions.

| Schema file | Canonical for | Upstream | Version pin |
|---|---|---|---|
| `findings/schemas/sarif-2.1.0.schema.json` | `security.sast`, `security.dast`, `security.secret-scan` | OASIS SARIF | 2.1.0 |
| `findings/schemas/cyclonedx-1.6-findings.schema.json` | `security.sca`, `security.container-scan`, `security.license-scan` | OWASP CycloneDX vulnerability findings (CVSS 3.1 scored) | 1.6 |
| `findings/schemas/cyclonedx-1.6-sbom.schema.json` | `sbom.generate` (primary) | OWASP CycloneDX SBOM | 1.6 |
| `findings/schemas/junit-xml.schema.json` | `test.unit`, `test.integration`, `test.contract`, `test.e2e` | JUnit 4-compatible test report (JSON-encoded) | JUnit 4 structure |
| `findings/schemas/oci-signing-bundle.schema.json` | `sign.artifact`, `sign.attestation` | Sigstore Bundle | v0.3 (`application/vnd.dev.sigstore.bundle.v0.3+json`) |

`sbom.generate` also accepts SPDX 2.3 as an alternative format. A dedicated SPDX schema is not included in v1; adapters that emit SPDX must declare that format in their attestation and attach a tool-produced SPDX document as evidence alongside the CycloneDX primary. A standalone SPDX schema is a v1.1 item.

---

## Per-action mapping

Each row carries: action identifier, upstream schema + version, AIEOS extension points (fields AIEOS adds or constrains beyond upstream), minimal example snippet (5–10 lines showing the smallest valid document).

### Test.unit / test.integration / test.contract / test.e2e

- **Upstream:** JUnit 4 test-report structure, canonically encoded as JSON (`testsuites` root with nested `testsuite` and `testcase` entries).
- **Version pin:** JUnit 4 structure; JSON encoding defined in `findings/schemas/junit-xml.schema.json`.
- **AIEOS extension points:** none. Adapters that want to attach raw JUnit XML do so as an evidence artifact alongside the canonical JSON findings; the schema does not describe the XML form.
- **Minimal example:**

```json
{
  "name": "unit",
  "tests": 1,
  "failures": 0,
  "errors": 0,
  "testsuite": [
    {
      "name": "smoke",
      "tests": 1,
      "failures": 0,
      "errors": 0,
      "testcase": [
        { "name": "test_one", "classname": "smoke.test_one", "time": 0.002 }
      ]
    }
  ]
}
```

### Security.sast / security.dast / security.secret-scan

- **Upstream:** OASIS SARIF (Static Analysis Results Interchange Format).
- **Version pin:** 2.1.0.
- **AIEOS extension points:** AIEOS requires `runs[].tool.driver.name`, `runs[].tool.driver.version`, and `runs[].results[].level` (SARIF allows level to be omitted — AIEOS requires it so criteria can threshold by level without reinferring). Other SARIF fields remain optional.
- **Minimal example:**

```json
{
  "version": "2.1.0",
  "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
  "runs": [
    {
      "tool": { "driver": { "name": "example-sast", "version": "1.0.0" } },
      "results": []
    }
  ]
}
```

### Security.sca / security.container-scan / security.license-scan

- **Upstream:** OWASP CycloneDX vulnerability findings (CVSS 3.1 scored).
- **Version pin:** CycloneDX 1.6.
- **AIEOS extension points:** AIEOS requires each vulnerability finding carry at least one `ratings` entry with `method: "CVSSv31"` and a numeric `score`. License findings report `score: 0.0` with a severity class describing the policy decision. The severity-class vocabulary is SARIF-aligned (`none`, `info`, `low`, `medium`, `high`, `critical`) so consumers can compare thresholds across findings streams.
- **Minimal example:**

```json
{
  "bomFormat": "CycloneDX",
  "specVersion": "1.6",
  "vulnerabilities": [
    {
      "id": "CVE-2024-00001",
      "source": { "name": "nvd" },
      "ratings": [
        { "method": "CVSSv31", "score": 7.5, "severity": "high" }
      ],
      "affects": [ { "ref": "pkg:npm/example@1.0.0" } ]
    }
  ]
}
```

### Sbom.generate

- **Upstream:** OWASP CycloneDX SBOM (primary).
- **Version pin:** CycloneDX 1.6 (primary). SPDX 2.3 accepted as alternative without a standalone schema in v1.
- **AIEOS extension points:** AIEOS requires each `components[]` entry carry `bom-ref`, `type`, `name`, and `version`. `purl` is strongly recommended but not required (some internal components cannot be packaged).
- **Minimal example:**

```json
{
  "bomFormat": "CycloneDX",
  "specVersion": "1.6",
  "components": [
    {
      "bom-ref": "pkg:npm/example@1.0.0",
      "type": "library",
      "name": "example",
      "version": "1.0.0"
    }
  ]
}
```

### Sign.artifact / sign.attestation

- **Upstream:** Sigstore Bundle.
- **Version pin:** `v0.3` (media type `application/vnd.dev.sigstore.bundle.v0.3+json`).
- **AIEOS extension points:** AIEOS requires `mediaType` match the pinned media type exactly and `verificationMaterial` be present. Either `messageSignature` (for `sign.artifact` — signing an OCI image) or `dsseEnvelope` (for `sign.attestation` — signing an in-toto statement) must be present; both may not be absent.
- **Minimal example:**

```json
{
  "mediaType": "application/vnd.dev.sigstore.bundle.v0.3+json",
  "verificationMaterial": {
    "publicKey": { "hint": "abc123" },
    "tlogEntries": []
  },
  "messageSignature": {
    "messageDigest": { "algorithm": "SHA2_256", "digest": "deadbeef" },
    "signature": "MEUCIQ..."
  }
}
```

---

## Schema subset rationale

SARIF 2.1.0 and CycloneDX 1.6 each run to tens of thousands of lines of upstream JSON Schema. AIEOS ships a **subset** of each that covers the fields adapters must emit, plus the AIEOS extension-point constraints above.

Excluded from the AIEOS subsets:

- **SARIF:** `externalizedProperties`, `invocations`, `conversion`, `thirdPartySuppressions`, `versionControlProvenance`, deep `logicalLocations`, `runs[].taxonomies`, detailed `graph` representations. Adapters may emit these; AIEOS validators do not reject on their presence.
- **CycloneDX findings:** `services`, `compositions`, `formulation`, `annotations`, detailed `analysis`/`workaround`/`advisories` fields. Adapters may emit these; AIEOS validators do not reject on their presence.
- **CycloneDX SBOM:** deep `properties`, `externalReferences`, `pedigree`, `compositions`, `formulation`. Adapters may emit these.

The subset approach is explicit and deliberate: the frozen AIEOS schema defines *what adapters must guarantee*, not the full upstream surface. Adapters that emit a richer superset are valid; validators ignore fields the subset does not constrain.

Adapters that want to claim full upstream conformance should attach the upstream schema version in an `AdapterResult.evidence` artifact and document the claim in their `MAPPING.md`.

---

## Testing

Every schema in `findings/schemas/` is exercised by `findings/schemas/validate.py`:

- Valid example must validate (exit 0).
- Invalid example must fail validation (exit non-zero).
- Schema itself must parse as JSON Schema Draft 2020-12.

Run:

```bash
python3 findings/schemas/validate.py
```

CI runs this check on every PR that touches `findings/` (to be wired up in a later milestone).
