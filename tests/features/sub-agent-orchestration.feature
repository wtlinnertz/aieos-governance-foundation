Feature: Sub-Agent Orchestration
  The framework supports parallel execution patterns. The sherpa must understand
  when parallelism is allowed and when sequential ordering is required.

  # PRK lens parallelism — all lenses are independent
  Scenario: PRK lenses are independent (no lens-to-lens dependency)
    Given the dependency graph is loaded
    Then a path exists from "EEK:SAD" to "PRK:PRR"

  # EEK parallelism — ACF and SAD can run in parallel after PRD
  Scenario: EEK ACF and SAD both depend on PRD
    Given the dependency graph is loaded
    Then a path exists from "EEK:PRD" to "EEK:ACF"
    And a path exists from "EEK:PRD" to "EEK:SAD"

  # EEK sequential — TDD requires both SAD and ACF
  Scenario: EEK TDD requires both SAD and ACF frozen
    Given the dependency graph is loaded
    Then a path exists from "EEK:ACF" to "EEK:TDD"
    And a path exists from "EEK:SAD" to "EEK:TDD"

  # Cross-cutting kits are independent of each other
  Scenario: Cross-cutting kits do not block each other
    Given the dependency graph is loaded
    Then "SCK:TM" does not block "DCK:CSPEC"
    And "DCK:CSPEC" does not block "DKK:ARR"
    And "DKK:ARR" does not block "BPK:PIA"

  # WDD to ORD is sequential
  Scenario: ORD requires WDD frozen
    Given the dependency graph is loaded
    Then a path exists from "EEK:WDD" to "EEK:ORD"
