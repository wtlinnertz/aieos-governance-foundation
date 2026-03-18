Feature: Decision Table Routing
  Every decision table in the navigation map must have corresponding edges in the
  dependency graph that implement its routing outcomes. The sherpa uses these tables
  to guide operators through junctions.

  # J-ENTRY-1: Framework Entry Point
  Scenario: J-ENTRY-1 route 1 — new work to PIK
    Given the dependency graph is loaded
    Then "PIK:WCR" is a valid entry point

  Scenario: J-ENTRY-1 route 2 — known problem to EEK
    Given the dependency graph is loaded
    Then "EEK:KER" is a valid entry point

  Scenario: J-ENTRY-1 route 3 — incident to ODK
    Given the dependency graph is loaded
    Then "ODK:DCR" is a valid entry point

  Scenario: J-ENTRY-1 route 4 — infra decision to PINFK
    Given the dependency graph is loaded
    Then "PINFK:PDR" is a valid entry point

  # J-ENTRY-2: Preset Selection
  Scenario: J-ENTRY-2 preset P1 starts at PIK
    Given the preset "New Feature" is loaded
    Then the entry point is "PIK:WCR"

  Scenario: J-ENTRY-2 preset P2 starts at EEK
    Given the preset "Enhancement" is loaded
    Then the entry point is "EEK:KER"

  Scenario: J-ENTRY-2 preset P4 starts at ODK
    Given the preset "Performance and Reliability Fix (incident)" is loaded
    Then the entry point is "ODK:DCR"

  Scenario: J-ENTRY-2 preset P5 starts at PIK
    Given the preset "Exploratory Research" is loaded
    Then the entry point is "PIK:WCR"

  # J-PIK-EL: EL Outcome Decision
  Scenario: J-PIK-EL proceed route reaches DPRD
    Given the dependency graph is loaded
    Then a path exists from "PIK:EL" to "PIK:DPRD"

  Scenario: J-PIK-EL pause terminates — no DPRD required for exploratory
    Given the preset "Exploratory Research" is loaded
    Then "PIK:DPRD" is not a required artifact

  # J-SSK-ENTRY: SSK Engagement Decision
  Scenario: J-SSK-ENTRY route 1 — skip SSK to EEK
    Given the dependency graph is loaded
    Then a path exists from "PIK:DPRD" to "EEK:PRD"

  Scenario: J-SSK-ENTRY route 2 — engage SSK
    Given the dependency graph is loaded
    Then a path exists from "PIK:DPRD" to "SSK:SOER"

  # J-SSK-ROUTE: Sourcing Decision Routing
  Scenario: J-SSK-ROUTE all decisions reach EEK
    Given the dependency graph is loaded
    Then a path exists from "SSK:SDR" to "EEK:PRD"

  # J-EEK-PATH: Path A vs Path B
  Scenario: J-EEK-PATH A — PIK DPRD flows to EEK PRD
    Given the dependency graph is loaded
    Then a path exists from "PIK:DPRD" to "EEK:PRD"

  Scenario: J-EEK-PATH B — KER gates PRD directly
    Given the dependency graph is loaded
    Then a path exists from "EEK:KER" to "EEK:PRD"

  # J-EEK-QAK: QAK Adoption Decision
  Scenario: J-EEK-QAK route 1 — adopt QAK
    Given the dependency graph is loaded
    Then a path exists from "EEK:ORD" to "QAK:QAER"

  Scenario: J-EEK-QAK route 2 — skip QAK to REK
    Given the dependency graph is loaded
    Then a path exists from "EEK:ORD" to "REK:RER"

  # J-QAK-DISPOSITION: QGR Disposition
  Scenario: J-QAK-DISPOSITION PASS routes to REK
    Given the dependency graph is loaded
    Then a path exists from "QAK:QGR" to "REK:RER"

  # J-REK-DISPOSITION: Release Disposition
  Scenario: J-REK-DISPOSITION success routes to RRK
    Given the dependency graph is loaded
    Then a path exists from "REK:RR" to "RRK:SRER"

  Scenario: J-REK-DISPOSITION rollback code defect escalates to EEK
    Given the dependency graph is loaded
    Then an escalation edge exists from "REK:RR" to "EEK:KER"

  Scenario: J-REK-DISPOSITION rollback wrong feature escalates to PIK
    Given the dependency graph is loaded
    Then an escalation edge exists from "REK:RR" to "PIK:WCR"

  # J-RRK-ESCALATION: Escalation Assessment
  Scenario: J-RRK-ESCALATION trigger 1 — code defect to EEK
    Given the dependency graph is loaded
    Then an escalation edge exists from "RRK:IR" to "EEK:KER"

  Scenario: J-RRK-ESCALATION trigger 2 — recurring pattern to PIK
    Given the dependency graph is loaded
    Then an escalation edge exists from "RRK:RHR" to "PIK:WCR"

  Scenario: J-RRK-ESCALATION trigger 5 — SEV to ODK
    Given the dependency graph is loaded
    Then an escalation edge exists from "RRK:IR" to "ODK:DCR"

  # J-IEK-SIGNAL: Re-Entry Signal
  Scenario: J-IEK-SIGNAL re-discover routes to PIK
    Given the dependency graph is loaded
    Then an escalation edge exists from "IEK:ES" to "PIK:WCR"

  # J-ODK-ESCALATION: ODK Escalation Assessment
  Scenario: J-ODK-ESCALATION code defect routes to EEK
    Given the dependency graph is loaded
    Then a path exists from "ODK:PMR" to "EEK:KER"

  # J-SCK-TIMING: SCK Timing for Compliance
  Scenario: J-SCK-TIMING compliance preset requires SCK
    Given the preset "Compliance and Regulatory" is loaded
    Then "SCK" is a required kit

  # J-REENTRY: Re-Entry Decision
  Scenario: J-REENTRY cross-kit re-entry path exists PIK to EEK
    Given the dependency graph is loaded
    Then a path exists from "PIK:DPRD" to "EEK:PRD"

  # Cross-cutting trigger edges
  Scenario: SCK triggers from SAD
    Given the dependency graph is loaded
    Then a path exists from "EEK:SAD" to "SCK:TM"

  Scenario: DCK triggers from TDD
    Given the dependency graph is loaded
    Then a path exists from "EEK:TDD" to "DCK:CSPEC"

  Scenario: DKK triggers from TDD
    Given the dependency graph is loaded
    Then a path exists from "EEK:TDD" to "DKK:ARR"

  Scenario: BPK triggers from SAD
    Given the dependency graph is loaded
    Then a path exists from "EEK:SAD" to "BPK:PIA"
