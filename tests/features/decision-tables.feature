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

  # J-PIK-WCR: Work Classification Routing
  Scenario: J-PIK-WCR route 1/2 — full or targeted discovery routes to intake
    Given the dependency graph is loaded
    Then a path exists from "PIK:WCR" to "PIK:PFD"

  Scenario: J-PIK-WCR route 3 — no discovery routes to EEK
    Given the dependency graph is loaded
    Then a path exists from "PIK:WCR" to "PIK:PFD"
    And a path exists from "EEK:KER" to "EEK:PRD"

  # J-PIK-PIVOT: Pivot Pattern Selection
  Scenario: J-PIK-PIVOT pattern 1 — problem reframe re-enters at PFD
    Given the dependency graph is loaded
    Then a path exists from "PIK:EL" to "PIK:DPRD"
    And a path exists from "PIK:PFD" to "PIK:VH"

  Scenario: J-PIK-PIVOT pattern 2 — hypothesis revision re-enters at VH
    Given the dependency graph is loaded
    Then a path exists from "PIK:VH" to "PIK:AR"

  Scenario: J-PIK-PIVOT all patterns cascade to DPRD
    Given the dependency graph is loaded
    Then a path exists from "PIK:PFD" to "PIK:DPRD"
    And a path exists from "PIK:VH" to "PIK:DPRD"

  # J-EEK-BAT: BAT Outcome
  Scenario: J-EEK-BAT pass continues to next work group
    Given the dependency graph is loaded
    Then a path exists from "EEK:WDD" to "EEK:ORD"

  Scenario: J-EEK-BAT execution path through WDD to ORD
    Given the dependency graph is loaded
    Then a path exists from "EEK:TDD" to "EEK:WDD"
    And a path exists from "EEK:WDD" to "EEK:ORD"

  # J-REK-RCF: RCF Reuse Decision
  Scenario: J-REK-RCF new RCF routes through RCF generation
    Given the dependency graph is loaded
    Then a path exists from "REK:RER" to "REK:RCF"

  Scenario: J-REK-RCF route reaches RP regardless
    Given the dependency graph is loaded
    Then a path exists from "REK:RCF" to "REK:RP"

  # J-ODK-RB: Runbook Decision
  Scenario: J-ODK-RB routes from PMR to escalation
    Given the dependency graph is loaded
    Then a path exists from "ODK:INR" to "ODK:PMR"

  # J-RRK-SRP-REVISION: SRP Revision
  Scenario: J-RRK-SRP-REVISION SRP depends on SRER
    Given the dependency graph is loaded
    Then a path exists from "RRK:SRER" to "RRK:SRP"

  # J-ENTRY-1: SDK entry point (was missing)
  Scenario: J-ENTRY-1 route 5 — strategic bet to SDK
    Given the dependency graph is loaded
    Then a path exists from "SDK:SBR" to "SDK:PPR"
    And a path exists from "SDK:PPR" to "PIK:WCR"

  # Boundary contract: QAK receives full EEK context
  Scenario: QAK reachable from EEK ORD
    Given the dependency graph is loaded
    Then a path exists from "EEK:ORD" to "QAK:QAER"

  # Boundary contract: IEK requires RHR
  Scenario: IEK reachable from RRK RHR
    Given the dependency graph is loaded
    Then a path exists from "RRK:RHR" to "IEK:ES"

  # BPK completion path
  Scenario: BPK PIA cascades to TP and RC
    Given the dependency graph is loaded
    Then a path exists from "BPK:PIA" to "BPK:TP"
    And a path exists from "BPK:TP" to "BPK:RC"

  # Alternative cross-cutting trigger paths
  Scenario: BPK also triggers from TDD
    Given the dependency graph is loaded
    Then a path exists from "EEK:TDD" to "BPK:PIA"

  Scenario: DKK SKA triggers from ODK PMR
    Given the dependency graph is loaded
    Then a path exists from "ODK:PMR" to "DKK:SKA"

  # EEK execution-phase reachability
  Scenario: EEK full execution path reachable
    Given the dependency graph is loaded
    Then a path exists from "EEK:PRD" to "EEK:ACF"
    And a path exists from "EEK:ACF" to "EEK:TDD"
    And a path exists from "EEK:TDD" to "EEK:WDD"
    And a path exists from "EEK:WDD" to "EEK:ORD"

  Scenario: EEK DCF parallel path exists
    Given the dependency graph is loaded
    Then a path exists from "EEK:ACF" to "EEK:DCF"
    And a path exists from "EEK:DCF" to "EEK:WDD"

  # Full pipeline reachability
  Scenario: Full P1 pipeline PIK through IEK is reachable
    Given the dependency graph is loaded
    Then a path exists from "PIK:WCR" to "PIK:DPRD"
    And a path exists from "PIK:DPRD" to "EEK:PRD"
    And a path exists from "EEK:ORD" to "QAK:QAER"
    And a path exists from "QAK:QGR" to "REK:RER"
    And a path exists from "REK:RR" to "RRK:SRER"
    And a path exists from "RRK:RHR" to "IEK:ES"
