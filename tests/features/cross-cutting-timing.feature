Feature: Cross-Cutting Kit Timing
  Cross-cutting kits activate at specific trigger points in the pipeline.
  The sherpa must know when to activate each one and not activate them too early.

  # SCK triggers from SAD
  Scenario: SCK activates after SAD freeze
    Given the dependency graph is loaded
    Then a path exists from "EEK:SAD" to "SCK:TM"

  Scenario: SCK TM feeds SAR
    Given the dependency graph is loaded
    Then a path exists from "SCK:TM" to "SCK:SAR"

  # DCK triggers from TDD
  Scenario: DCK activates after TDD freeze
    Given the dependency graph is loaded
    Then a path exists from "EEK:TDD" to "DCK:CSPEC"
    And a path exists from "EEK:TDD" to "DCK:DSR"

  # DCK FFLR triggers from REK
  Scenario: DCK FFLR activates after RR freeze
    Given the dependency graph is loaded
    Then a path exists from "REK:RR" to "DCK:FFLR"

  # DKK triggers from TDD and REK
  Scenario: DKK ARR activates after TDD freeze
    Given the dependency graph is loaded
    Then a path exists from "EEK:TDD" to "DKK:ARR"

  Scenario: DKK UDR activates after RR freeze
    Given the dependency graph is loaded
    Then a path exists from "REK:RR" to "DKK:UDR"

  Scenario: DKK SKA activates after RR or PMR freeze
    Given the dependency graph is loaded
    Then a path exists from "REK:RR" to "DKK:SKA"

  Scenario: DKK SKA also activates from ODK PMR
    Given the dependency graph is loaded
    Then a path exists from "ODK:PMR" to "DKK:SKA"

  # BPK triggers from SAD or TDD
  Scenario: BPK activates after SAD freeze
    Given the dependency graph is loaded
    Then a path exists from "EEK:SAD" to "BPK:PIA"

  Scenario: BPK also activates from TDD
    Given the dependency graph is loaded
    Then a path exists from "EEK:TDD" to "BPK:PIA"

  # PRK triggers at review points
  Scenario: PRK activates for all pipeline review points
    Given the dependency graph is loaded
    Then a path exists from "PIK:DPRD" to "PRK:PRR"
    And a path exists from "EEK:SAD" to "PRK:PRR"
    And a path exists from "EEK:TDD" to "PRK:PRR"
    And a path exists from "EEK:ORD" to "PRK:PRR"
    And a path exists from "QAK:QGR" to "PRK:PRR"
    And a path exists from "REK:RP" to "PRK:PRR"
    And a path exists from "RRK:RHR" to "PRK:PRR"
    And a path exists from "ODK:PMR" to "PRK:PRR"

  # Compliance preset ordering
  Scenario: Compliance preset requires SCK before QAK
    Given the preset "Compliance and Regulatory" is loaded
    Then "SCK" is a required kit
    And "QAK" is a required kit

  # New Feature preset includes all cross-cutting kits
  Scenario: New Feature preset includes cross-cutting kits
    Given the preset "New Feature" is loaded
    Then "QAK" is a required kit
    And "SCK" is a required kit
    And "DCK" is a required kit
    And "PINFK" is a required kit
    And "DKK" is a required kit
