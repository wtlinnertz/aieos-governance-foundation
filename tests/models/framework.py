"""Data models for the AIEOS framework structure."""

from __future__ import annotations

from dataclasses import dataclass, field


# ─── Kit and Layer Registry ──────────────────────────────────────────────────

KIT_REGISTRY: dict[str, "KitInfo"] = {}


@dataclass
class KitInfo:
    """Static metadata about an AIEOS kit."""
    name: str            # e.g., "PIK"
    layer: int           # e.g., 2
    directory: str       # e.g., "aieos-product-intelligence-kit"
    full_name: str       # e.g., "Product Intelligence Kit"
    category: str        # "pipeline", "operational", "cross-cutting"


# The 13 built kits
KIT_REGISTRY = {
    "PIK":   KitInfo("PIK",   2,  "aieos-product-intelligence-kit",    "Product Intelligence Kit",       "pipeline"),
    "SSK":   KitInfo("SSK",   3,  "aieos-solution-sourcing-kit",       "Solution Sourcing Kit",          "pipeline"),
    "EEK":   KitInfo("EEK",   4,  "aieos-engineering-execution-kit",   "Engineering Execution Kit",      "pipeline"),
    "REK":   KitInfo("REK",   5,  "aieos-release-exposure-kit",        "Release & Exposure Kit",         "pipeline"),
    "RRK":   KitInfo("RRK",   6,  "aieos-reliability-resilience-kit",  "Reliability & Resilience Kit",   "pipeline"),
    "IEK":   KitInfo("IEK",   7,  "aieos-insight-evolution-kit",       "Insight & Evolution Kit",        "pipeline"),
    "ODK":   KitInfo("ODK",   8,  "aieos-operational-diagnostics-kit", "Operational Diagnostics Kit",    "operational"),
    "QAK":   KitInfo("QAK",   9,  "aieos-quality-assurance-kit",       "Quality Assurance Kit",          "cross-cutting"),
    "SCK":   KitInfo("SCK",   10, "aieos-security-compliance-kit",     "Security & Compliance Kit",      "cross-cutting"),
    "DCK":   KitInfo("DCK",   11, "aieos-data-configuration-kit",      "Data & Configuration Kit",       "cross-cutting"),
    "PINFK": KitInfo("PINFK", 12, "aieos-platform-infrastructure-kit", "Platform & Infrastructure Kit",  "cross-cutting"),
    "DKK":   KitInfo("DKK",   13, "aieos-documentation-knowledge-kit", "Documentation & Knowledge Kit",  "cross-cutting"),
    "PRK":   KitInfo("PRK",   14, "aieos-peer-review-kit",             "Peer Review Kit",                "cross-cutting"),
}


# ─── Dependency Graph Edges ──────────────────────────────────────────────────
# Each tuple: (upstream_kit:artifact, downstream_kit:artifact, gate_type)
# gate_type: "freeze" = upstream must be frozen; "trigger" = trigger-based activation

DEPENDENCY_EDGES: list[tuple[str, str, str]] = [
    # Pipeline sequential dependencies
    ("PIK:DPRD",   "EEK:PRD",    "freeze"),    # Path A: DPRD → EEK (when SSK not engaged)

    # SSK (between PIK and EEK)
    ("PIK:DPRD",   "SSK:SOER",   "freeze"),    # DPRD → SSK entry
    ("SSK:SOER",   "SSK:VER",    "freeze"),
    ("SSK:VER",    "SSK:SDR",    "freeze"),
    ("SSK:SDR",    "EEK:PRD",    "freeze"),    # SDR → EEK (when SSK engaged)
    ("EEK:ORD",    "REK:RER",    "freeze"),    # ORD → REK entry
    ("EEK:ORD",    "QAK:QAER",   "freeze"),    # ORD → QAK entry
    ("QAK:QGR",    "REK:RER",    "freeze"),    # QGR gates REK (when QAK adopted)
    ("REK:RR",     "RRK:SRER",   "freeze"),    # RR → RRK entry
    ("RRK:RHR",    "IEK:ES",     "freeze"),    # 2+ RHRs → IEK

    # Within-kit sequential dependencies
    # PIK
    ("PIK:WCR",    "PIK:PFD",    "freeze"),
    ("PIK:PFD",    "PIK:VH",     "freeze"),
    ("PIK:VH",     "PIK:AR",     "freeze"),
    ("PIK:AR",     "PIK:EL",     "freeze"),
    ("PIK:EL",     "PIK:DPRD",   "freeze"),

    # EEK (KER is the entry gate for EEK)
    ("EEK:KER",    "EEK:PRD",    "freeze"),    # KER gates PRD
    # EEK (simplified — ACF/SAD can parallel, DCF/TDD can parallel)
    ("EEK:PRD",    "EEK:ACF",    "freeze"),
    ("EEK:PRD",    "EEK:SAD",    "freeze"),
    ("EEK:ACF",    "EEK:TDD",    "freeze"),
    ("EEK:SAD",    "EEK:TDD",    "freeze"),
    ("EEK:ACF",    "EEK:DCF",    "freeze"),
    ("EEK:SAD",    "EEK:DCF",    "freeze"),
    ("EEK:TDD",    "EEK:WDD",    "freeze"),
    ("EEK:DCF",    "EEK:WDD",    "freeze"),
    ("EEK:WDD",    "EEK:ORD",    "freeze"),

    # QAK
    ("QAK:QAER",   "QAK:VP",     "freeze"),
    ("QAK:VP",     "QAK:TCR",    "freeze"),
    ("QAK:TCR",    "QAK:QGR",    "freeze"),

    # REK
    ("REK:RER",    "REK:RCF",    "freeze"),
    ("REK:RCF",    "REK:RP",     "freeze"),
    ("REK:RP",     "REK:RR",     "freeze"),

    # RRK (SRP depends on SRER; RHR depends on SRP being active)
    ("RRK:SRER",   "RRK:SRP",    "freeze"),
    ("RRK:SRP",    "RRK:RHR",    "freeze"),    # RHR requires active SRP

    # ODK
    ("ODK:DCR",    "ODK:INR",    "freeze"),
    ("ODK:INR",    "ODK:PMR",    "freeze"),

    # PINFK (sequential: PDR → ISPEC → EM)
    ("PINFK:PDR",  "PINFK:ISPEC","freeze"),
    ("PINFK:ISPEC","PINFK:EM",   "freeze"),

    # SCK internal
    ("SCK:TM",     "SCK:SAR",    "freeze"),

    # Cross-cutting trigger points
    ("EEK:SAD",    "SCK:TM",     "trigger"),   # SAD frozen → TM
    ("EEK:ORD",    "SCK:DAR",    "trigger"),   # Code complete → DAR (dependency audit)
    ("EEK:ORD",    "SCK:CER",    "trigger"),   # Compliance mandate → CER
    ("EEK:TDD",    "DCK:CSPEC",  "trigger"),   # TDD frozen → CSPEC
    ("EEK:TDD",    "DCK:DSR",    "trigger"),   # TDD frozen → DSR
    ("EEK:TDD",    "DKK:ARR",    "trigger"),   # TDD frozen → ARR (early)
    ("REK:RR",     "DCK:FFLR",   "trigger"),   # RR frozen → FFLR
    ("REK:RR",     "DKK:UDR",    "trigger"),   # RR frozen → UDR
    ("REK:RR",     "DKK:SKA",    "trigger"),   # RR frozen → SKA
    ("ODK:PMR",    "DKK:SKA",    "trigger"),   # PMR frozen → SKA (alternative trigger)

    # PRK trigger points (peer review after validation, before freeze)
    ("PIK:DPRD",   "PRK:PRR",    "trigger"),   # DPRD validated → concept review
    ("EEK:SAD",    "PRK:PRR",    "trigger"),   # SAD validated → architecture review
    ("EEK:TDD",    "PRK:PRR",    "trigger"),   # TDD validated → technical design review
    ("EEK:WDD",    "PRK:PRR",    "trigger"),   # WDD validated → implementation readiness
    ("EEK:ORD",    "PRK:PRR",    "trigger"),   # ORD validated → code review
    ("QAK:QGR",    "PRK:PRR",    "trigger"),   # QGR validated → integration review
    ("REK:RP",     "PRK:PRR",    "trigger"),   # RP validated → operational readiness
    ("RRK:RHR",    "PRK:PRR",    "trigger"),   # RHR validated → post-deployment review
    ("ODK:PMR",    "PRK:PRR",    "trigger"),   # PMR validated → incident review

    # Cross-kit escalation transitions (forward-direction for preset flows)
    ("ODK:PMR",    "EEK:KER",    "trigger"),   # PMR corrective action → EEK (incident fix path)

    # Escalation paths (reverse direction)
    ("RRK:IR",     "EEK:KER",    "escalation"),  # T1: code defect
    ("RRK:RHR",    "PIK:WCR",    "escalation"),  # T2: recurring pattern
    ("REK:RR",     "EEK:KER",    "escalation"),  # T3: rollback code defect
    ("REK:RR",     "PIK:WCR",    "escalation"),  # T4: rollback wrong feature
    ("RRK:IR",     "ODK:DCR",    "escalation"),  # T5: SEV1/2 → ODK
    ("IEK:ES",     "PIK:WCR",    "escalation"),  # T6: re-discover signal
]


# ─── Entry Points ────────────────────────────────────────────────────────────

ENTRY_POINTS: list[str] = [
    "PIK:WCR",      # New work request
    "EEK:KER",      # Path B enhancement (direct entry)
    "ODK:DCR",      # Production incident
    "PINFK:PDR",    # Technology decision
]


# ─── Boundary Contracts ─────────────────────────────────────────────────────
# Maps: (downstream_kit, entry_file_suffix) → list of expected upstream artifacts

BOUNDARY_CONTRACTS: dict[tuple[str, str], list[str]] = {
    ("EEK",  "pik"):  ["DPRD"],
    ("SSK",  "pik"):  ["DPRD"],
    ("EEK",  "ssk"):  ["SDR"],
    ("QAK",  "eek"):  ["ORD", "SAD", "TDD", "ACF", "WDD"],
    ("REK",  "eek"):  ["ORD"],
    ("RRK",  "rek"):  ["RR"],
    ("IEK",  "rrk"):  ["RHR"],
    ("ODK",  "rrk"):  ["SRP"],  # recommended, not required
    ("SCK",  "eek"):  ["SAD"],
    ("DCK",  "eek"):  ["TDD"],
    ("PINFK","eek"):  ["SAD", "TDD"],
    ("DKK",  "eek"):  ["TDD"],
    ("DKK",  "rek"):  ["RR"],
    ("DKK",  "odk"):  ["PMR"],
    ("PIK",  "iek"):  ["ES"],
    ("PRK",  "pik"):  ["DPRD"],
    ("PRK",  "eek"):  ["SAD", "TDD", "WDD", "ORD"],
    ("PRK",  "qak"):  ["QGR"],
    ("PRK",  "rek"):  ["RP"],
    ("PRK",  "rrk"):  ["RHR"],
    ("PRK",  "odk"):  ["PMR"],
}


# ─── Preset Definitions ─────────────────────────────────────────────────────

@dataclass
class PresetDefinition:
    """An initiative preset with its required flow."""
    name: str
    entry_point: str           # e.g., "PIK:WCR"
    required_kits: list[str]   # e.g., ["PIK", "EEK", "REK"]
    required_artifacts: list[str]  # e.g., ["PIK:DPRD", "EEK:ORD", ...]
    optional_kits: list[str] = field(default_factory=list)


PRESET_DEFINITIONS: list[PresetDefinition] = [
    PresetDefinition(
        name="New Feature",
        entry_point="PIK:WCR",
        required_kits=["PIK", "EEK", "QAK", "SCK", "DCK", "PINFK", "DKK", "REK", "RRK", "IEK"],
        required_artifacts=[
            "PIK:WCR", "PIK:PFD", "PIK:VH", "PIK:AR", "PIK:EL", "PIK:DPRD",
            "EEK:PRD", "EEK:ACF", "EEK:SAD", "EEK:DCF", "EEK:TDD", "EEK:WDD", "EEK:ORD",
            "QAK:QAER", "QAK:VP", "QAK:TCR", "QAK:QGR",
            "SCK:TM", "SCK:SAR", "SCK:DAR",
            "DCK:CSPEC", "DCK:DSR",
            "PINFK:PDR", "PINFK:ISPEC", "PINFK:EM",
            "DKK:UDR", "DKK:ARR",
            "REK:RER", "REK:RCF", "REK:RP", "REK:RR",
            "RRK:SRER", "RRK:SRP", "RRK:RHR",
            "IEK:ES",
        ],
        optional_kits=["ODK", "SSK", "PRK"],
    ),
    PresetDefinition(
        name="Enhancement",
        entry_point="EEK:KER",
        required_kits=["EEK", "REK"],
        required_artifacts=[
            "EEK:PRD", "EEK:ACF", "EEK:SAD", "EEK:DCF", "EEK:TDD", "EEK:WDD", "EEK:ORD",
            "REK:RER", "REK:RP", "REK:RR",
        ],
        optional_kits=["PIK", "QAK", "SCK", "DCK", "DKK", "RRK", "IEK", "PRK"],
    ),
    PresetDefinition(
        name="Compliance and Regulatory",
        entry_point="PIK:WCR",
        required_kits=["PIK", "EEK", "SCK", "QAK", "REK", "RRK"],
        required_artifacts=[
            "PIK:WCR", "PIK:PFD", "PIK:AR", "PIK:DPRD",
            "EEK:PRD", "EEK:ACF", "EEK:SAD", "EEK:DCF", "EEK:TDD", "EEK:WDD", "EEK:ORD",
            "SCK:TM", "SCK:SAR", "SCK:CER", "SCK:DAR",
            "QAK:QAER", "QAK:VP", "QAK:TCR", "QAK:QGR",
            "REK:RER", "REK:RCF", "REK:RP", "REK:RR",
            "RRK:SRER", "RRK:SRP", "RRK:RHR",
        ],
        optional_kits=["IEK", "ODK", "SSK", "PRK"],
    ),
    PresetDefinition(
        name="Performance and Reliability Fix (incident)",
        entry_point="ODK:DCR",
        required_kits=["ODK", "EEK", "REK", "RRK"],
        required_artifacts=[
            "ODK:DCR", "ODK:INR", "ODK:PMR",
            "EEK:PRD", "EEK:TDD", "EEK:WDD", "EEK:ORD",
            "REK:RER", "REK:RP", "REK:RR",
            "RRK:RHR",
        ],
        optional_kits=["QAK", "SCK", "DKK", "PRK"],
    ),
    PresetDefinition(
        name="Exploratory Research",
        entry_point="PIK:WCR",
        required_kits=["PIK"],
        required_artifacts=[
            "PIK:WCR", "PIK:PFD", "PIK:VH", "PIK:AR", "PIK:EL",
        ],
        optional_kits=[],
    ),
]
