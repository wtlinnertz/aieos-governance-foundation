Feature: Escalation Paths
  Escalation paths move work upstream when downstream evidence reveals issues.
  All escalation paths must create new initiative cycles, not patch existing frozen artifacts.

  Scenario: T1 - SEV1/2 incident with code defect escalates to EEK
    Given the dependency graph is loaded
    Then an escalation edge exists from "RRK:IR" to "EEK:KER"

  Scenario: T2 - Recurring reliability pattern escalates to PIK
    Given the dependency graph is loaded
    Then an escalation edge exists from "RRK:RHR" to "PIK:WCR"

  Scenario: T3 - Rollback caused by code defect escalates to EEK
    Given the dependency graph is loaded
    Then an escalation edge exists from "REK:RR" to "EEK:KER"

  Scenario: T4 - Rollback caused by wrong feature escalates to PIK
    Given the dependency graph is loaded
    Then an escalation edge exists from "REK:RR" to "PIK:WCR"

  Scenario: T5 - SEV1/2 requiring structured diagnosis escalates to ODK
    Given the dependency graph is loaded
    Then an escalation edge exists from "RRK:IR" to "ODK:DCR"

  Scenario: T6 - Evolution signal re-discover escalates to PIK
    Given the dependency graph is loaded
    Then an escalation edge exists from "IEK:ES" to "PIK:WCR"

  Scenario: Escalation edges do not create forward cycles
    Given the dependency graph is loaded
    When escalation edges are removed
    Then the remaining graph is a DAG
