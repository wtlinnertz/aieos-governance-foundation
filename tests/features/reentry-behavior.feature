Feature: Re-Entry Protocol Behavior
  When frozen artifacts must change, re-entry protocols govern the cascade.
  The sherpa must understand material vs non-material changes and cross-kit impacts.

  # Material change within EEK cascades downstream
  Scenario: SAD change cascades to TDD
    Given the dependency graph is loaded
    Then a path exists from "EEK:SAD" to "EEK:TDD"

  Scenario: TDD change cascades to WDD
    Given the dependency graph is loaded
    Then a path exists from "EEK:TDD" to "EEK:WDD"

  Scenario: WDD change cascades to ORD
    Given the dependency graph is loaded
    Then a path exists from "EEK:WDD" to "EEK:ORD"

  # Cross-kit re-entry — DPRD change affects EEK
  Scenario: DPRD change reaches EEK PRD
    Given the dependency graph is loaded
    Then a path exists from "PIK:DPRD" to "EEK:PRD"

  # QAK FAIL returns to EEK for remediation
  Scenario: QAK FAIL path returns to EEK ORD
    Given the dependency graph is loaded
    Then an escalation path exists for QAK FAIL back to EEK

  # REK rollback returns to appropriate upstream kit
  Scenario: REK code defect rollback returns to EEK
    Given the dependency graph is loaded
    Then an escalation edge exists from "REK:RR" to "EEK:KER"

  Scenario: REK wrong feature rollback returns to PIK
    Given the dependency graph is loaded
    Then an escalation edge exists from "REK:RR" to "PIK:WCR"

  # Full pipeline is a DAG (no cycles when escalations removed)
  Scenario: Pipeline without escalations has no cycles
    Given the dependency graph is loaded
    When escalation edges are removed
    Then the remaining graph is a DAG
