"""
Structured schema for HMIS chemical gas table.
Maps Excel columns to normalized field names for LLM and web search.
"""

from typing import Optional

from pydantic import BaseModel, Field


# Column index → (schema field name, human description for LLM prompts)
HMIS_COLUMN_SPEC = [
    (0, "row_index", "Row number"),
    (1, "sub_system_filter_formula", "Sub-system filter list (chemical formula)"),
    (2, "chemical_name", "Chemical name"),
    (3, "sub_system_formula_2", "Sub-system chemical formula (alternate)"),
    (4, "source_location_typ", "Source location (typical)"),
    (5, "concentration", "Concentration"),
    (6, "cas_number", "CAS registry number"),
    (7, "hazardous_chemical", "Hazardous chemical (Y/N or classification)"),
    (8, "hazard_class", "Hazard class"),
    (9, "flammability", "Flammability rating"),
    (10, "reactivity", "Reactivity rating"),
    (11, "special", "Special hazards"),
    (12, "other", "Other hazards"),
    (13, "typ_rfo_id_in", "Typical RFO (ID in.)"),
    (14, "exhausted_enclosure", "Exhausted enclosure requirement"),
    (15, "coaxal_line_dc", "Coaxal line (DC)"),
    (16, "gas_detection_gds", "Gas detection (GDS)"),
    (17, "lss_shutdown", "LSS shutdown"),
    (18, "physical_form", "Physical form: Compressed Gas (CG) / Liquefied Gas (LG)"),
    (19, "design_specialities", "Design specialities"),
    (20, "fire_extinguishing_media", "Fire extinguishing media"),
    (21, "appearance", "Appearance"),
    (22, "vapor_pressure_bar", "Vapor pressure (bar); H2O = 0.023 bar @ 20°C"),
    (23, "viscosity_cp", "Viscosity (cP); H2O = 1 @ 20°C"),
    (24, "specific_gravity", "Specific gravity; H2O = 1 @ 4°C"),
    (25, "boiling_point_c", "Boiling point (°C)"),
    (26, "freeze_melt_point_c", "Freezing / melting point (°C)"),
    (27, "flash_point", "Flash point"),
    (28, "ph_value", "pH value"),
    (29, "ghs05_corrosive", "GHS05 Corrosive"),
    (30, "ghs08_harmful_health", "GHS08 Harmful for health"),
    (31, "ghs07_harmful", "GHS07 Harmful"),
    (32, "ghs04_compressed", "GHS04 Compressed gas"),
    (33, "ghs09_environmental", "GHS09 Dangerous for environment"),
    (34, "ghs03_oxidizing", "GHS03 Oxidizing"),
    (35, "ghs06_toxic", "GHS06 Toxic"),
    (36, "ghs02_flammable", "GHS02 Flammable"),
    (37, "ghs01_explosive", "GHS01 Explosive"),
    (38, "hazardous_statement", "Hazardous statement (H-phrase)"),
    (39, "exhaust_dispense", "Exhaust dispense"),
    (40, "exhaust_distribution", "Exhaust distribution"),
    (41, "purge_vent", "Purge vent"),
    (42, "purge_panel_dispense", "Purge panel dispense"),
    (43, "purge_panel_distribution", "Purge panel distribution"),
    (44, "non_hpm", "NON HPM"),
    (45, "gb_fire_code_class", "(GB) Fire code class"),
    (46, "col_46", "Reserved column"),
]

COLUMN_INDEX_TO_FIELD: dict[int, str] = {idx: name for idx, name, _ in HMIS_COLUMN_SPEC}
FIELD_TO_DESCRIPTION: dict[str, str] = {name: desc for _, name, desc in HMIS_COLUMN_SPEC}


class HMISGasRecord(BaseModel):
    """One row of the HMIS chemical gas table. All fields optional for sparse Excel data."""

    model_config = {"extra": "forbid", "str_strip_whitespace": True}

    row_index: Optional[str] = Field(None, description="Row number")
    sub_system_filter_formula: Optional[str] = Field(None, description="Sub-system filter list (chemical formula)")
    chemical_name: Optional[str] = Field(None, description="Chemical name")
    sub_system_formula_2: Optional[str] = Field(None, description="Sub-system chemical formula (alternate)")
    source_location_typ: Optional[str] = Field(None, description="Source location (typical)")
    concentration: Optional[str] = Field(None, description="Concentration")
    cas_number: Optional[str] = Field(None, description="CAS registry number")
    hazardous_chemical: Optional[str] = Field(None, description="Hazardous chemical (Y/N or classification)")
    hazard_class: Optional[str] = Field(None, description="Hazard class")
    flammability: Optional[str] = Field(None, description="Flammability rating")
    reactivity: Optional[str] = Field(None, description="Reactivity rating")
    special: Optional[str] = Field(None, description="Special hazards")
    other: Optional[str] = Field(None, description="Other hazards")
    typ_rfo_id_in: Optional[str] = Field(None, description="Typical RFO (ID in.)")
    exhausted_enclosure: Optional[str] = Field(None, description="Exhausted enclosure requirement")
    coaxal_line_dc: Optional[str] = Field(None, description="Coaxal line (DC)")
    gas_detection_gds: Optional[str] = Field(None, description="Gas detection (GDS)")
    lss_shutdown: Optional[str] = Field(None, description="LSS shutdown")
    physical_form: Optional[str] = Field(None, description="Physical form: CG/LG")
    design_specialities: Optional[str] = Field(None, description="Design specialities")
    fire_extinguishing_media: Optional[str] = Field(None, description="Fire extinguishing media")
    appearance: Optional[str] = Field(None, description="Appearance")
    vapor_pressure_bar: Optional[str] = Field(None, description="Vapor pressure (bar)")
    viscosity_cp: Optional[str] = Field(None, description="Viscosity (cP)")
    specific_gravity: Optional[str] = Field(None, description="Specific gravity")
    boiling_point_c: Optional[str] = Field(None, description="Boiling point (°C)")
    freeze_melt_point_c: Optional[str] = Field(None, description="Freezing / melting point (°C)")
    flash_point: Optional[str] = Field(None, description="Flash point")
    ph_value: Optional[str] = Field(None, description="pH value")
    ghs05_corrosive: Optional[str] = Field(None, description="GHS05 Corrosive")
    ghs08_harmful_health: Optional[str] = Field(None, description="GHS08 Harmful for health")
    ghs07_harmful: Optional[str] = Field(None, description="GHS07 Harmful")
    ghs04_compressed: Optional[str] = Field(None, description="GHS04 Compressed gas")
    ghs09_environmental: Optional[str] = Field(None, description="GHS09 Dangerous for environment")
    ghs03_oxidizing: Optional[str] = Field(None, description="GHS03 Oxidizing")
    ghs06_toxic: Optional[str] = Field(None, description="GHS06 Toxic")
    ghs02_flammable: Optional[str] = Field(None, description="GHS02 Flammable")
    ghs01_explosive: Optional[str] = Field(None, description="GHS01 Explosive")
    hazardous_statement: Optional[str] = Field(None, description="Hazardous statement (H-phrase)")
    exhaust_dispense: Optional[str] = Field(None, description="Exhaust dispense")
    exhaust_distribution: Optional[str] = Field(None, description="Exhaust distribution")
    purge_vent: Optional[str] = Field(None, description="Purge vent")
    purge_panel_dispense: Optional[str] = Field(None, description="Purge panel dispense")
    purge_panel_distribution: Optional[str] = Field(None, description="Purge panel distribution")
    non_hpm: Optional[str] = Field(None, description="NON HPM")
    gb_fire_code_class: Optional[str] = Field(None, description="(GB) Fire code class")
    col_46: Optional[str] = Field(None, description="Reserved column")


def get_empty_field_names(record: HMISGasRecord) -> list[str]:
    """Return field names whose value is None or empty string."""
    return [
        k
        for k, v in record.model_dump().items()
        if v is None or (isinstance(v, str) and not v.strip())
    ]


def get_filled_field_names(record: HMISGasRecord) -> list[str]:
    """Return field names that have a non-empty value."""
    return [
        k
        for k, v in record.model_dump().items()
        if v is not None and (not isinstance(v, str) or v.strip())
    ]
