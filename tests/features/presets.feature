Feature: Initiative Presets
  The 5 initiative presets define complete artifact routing for common initiative types.
  Each preset must produce a valid flow through the framework.

  Scenario: New Feature preset starts at PIK
    Given the preset "New Feature" is loaded
    Then the entry point is "PIK:WCR"
    And "EEK" is a required kit
    And "REK" is a required kit

  Scenario: Enhancement preset starts at EEK Path B
    Given the preset "Enhancement" is loaded
    Then the entry point is "EEK:KER"
    And "PIK" is not a required kit

  Scenario: Compliance preset requires SCK
    Given the preset "Compliance and Regulatory" is loaded
    Then the entry point is "PIK:WCR"
    And "SCK" is a required kit
    And "SCK:CER" is a required artifact

  Scenario: Incident-triggered fix starts at ODK
    Given the preset "Performance and Reliability Fix (incident)" is loaded
    Then the entry point is "ODK:DCR"
    And "ODK" is a required kit
    And "EEK" is a required kit

  Scenario: Exploratory research can terminate at PIK
    Given the preset "Exploratory Research" is loaded
    Then the entry point is "PIK:WCR"
    And "REK" is not a required kit
    And "RRK" is not a required kit
