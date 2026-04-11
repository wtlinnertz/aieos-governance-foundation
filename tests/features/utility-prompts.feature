Feature: Utility Prompt Availability
  The sherpa must be aware of utility prompts in each kit and offer them at
  appropriate points in the artifact flow.

  # PIK utility prompts
  Scenario: PIK assumption stress test available before EL
    Given the dependency graph is loaded
    Then a path exists from "PIK:AR" to "PIK:EL"

  Scenario: PIK discovery artifacts reachable from WCR
    Given the dependency graph is loaded
    Then a path exists from "PIK:WCR" to "PIK:PFD"
    And a path exists from "PIK:PFD" to "PIK:VH"
    And a path exists from "PIK:VH" to "PIK:AR"

  # EEK utility prompts
  Scenario: EEK codebase analysis available before ACF
    Given the dependency graph is loaded
    Then a path exists from "EEK:PRD" to "EEK:ACF"

  Scenario: EEK impact analysis available at frozen artifacts
    Given the dependency graph is loaded
    Then a path exists from "EEK:SAD" to "EEK:TDD"

  # REK utility prompts
  Scenario: REK rollout risk assessment available before RP execution
    Given the dependency graph is loaded
    Then a path exists from "REK:RSA" to "REK:RP"

  # RRK utility prompts
  Scenario: RRK SLO calibration available before SRP
    Given the dependency graph is loaded
    Then a path exists from "RRK:SRER" to "RRK:SRP"

  Scenario: RRK escalation assessment available at IR
    Given the dependency graph is loaded
    Then a path exists from "RRK:SRP" to "RRK:RHR"
