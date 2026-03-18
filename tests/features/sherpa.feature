Feature: Sherpa Awareness of New Capabilities
  The sherpa must be aware of the elicitation protocol, adversarial review lens,
  and briefing distillation tool so it can offer them at appropriate points.

  Scenario: Adversarial lens is optional at Architecture Review
    Given the preset "New Feature" is loaded
    Then "PRK" is not a required kit

  Scenario: SAD is reachable from PIK for adversarial review
    Given the dependency graph is loaded
    Then a path exists from "PIK:DPRD" to "EEK:SAD"

  Scenario: PRK trigger exists for SAD review
    Given the dependency graph is loaded
    Then a path exists from "EEK:SAD" to "PRK:PRR"

  Scenario: PRK trigger exists for TDD review
    Given the dependency graph is loaded
    Then a path exists from "EEK:TDD" to "PRK:PRR"

  Scenario: PRK trigger exists for ORD review
    Given the dependency graph is loaded
    Then a path exists from "EEK:ORD" to "PRK:PRR"

  Scenario: PRK trigger exists for RP review
    Given the dependency graph is loaded
    Then a path exists from "REK:RP" to "PRK:PRR"

  Scenario: PRK trigger exists for QGR review
    Given the dependency graph is loaded
    Then a path exists from "QAK:QGR" to "PRK:PRR"
