Feature: Re-Entry Protocols
  When frozen artifacts must change, re-entry protocols govern how changes cascade.

  Scenario: QAK FAIL returns to EEK
    Given the dependency graph is loaded
    Then a path exists from "EEK:ORD" to "QAK:QGR"
    And an escalation path exists for QAK FAIL back to EEK

  Scenario: Cross-kit re-entry from PIK to EEK
    Given the dependency graph is loaded
    Then a path exists from "PIK:DPRD" to "EEK:PRD"

  Scenario: Path selection is immutable
    Given the preset "New Feature" is loaded
    Then the entry point is "PIK:WCR"
    And "EEK:PRD" is a required artifact

  Scenario: Separate generation and validation sessions
    Given the flow validation rules are loaded
    Then rule 8 states "Separate generation and validation sessions"
