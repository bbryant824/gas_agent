"""
Authoritative reference sources for HMIS chemical gas data.
Used to prioritize web searches from trusted domains.
"""

# Tier 1: Gas supplier SDS/technical data (most specific and reliable)
GAS_SUPPLIERS = [
    "airliquide.com",
    "airproducts.com",  # Air Liquide subsidiary
    "sigmaaldrich.com",  # Merck
    "merckmillipore.com",
    "mathesongas.com",
    "linde.com",
    "lindeus.com",
    "praxair.com",  # Now part of Linde
]

# Tier 2: Safety standards organizations (authoritative classifications)
SAFETY_STANDARDS = [
    "osha.gov",  # OSHA SDS database
    "cdc.gov",  # NIOSH pocket guide
    "nfpa.org",  # National Fire Protection Association
    "unece.org",  # GHS (Global Harmonized System)
    "cganet.com",  # Compressed Gas Association
]

# Tier 3: Regulatory and code bodies (building/fire codes)
REGULATORY_BODIES = [
    "iccsafe.org",  # IBC/IFC (International Building/Fire Code)
    "nfpa.org",
    "epa.gov",
    "echa.europa.eu",  # European Chemicals Agency
]

# Combined list for convenience (order = priority)
ALL_TRUSTED_DOMAINS = GAS_SUPPLIERS + SAFETY_STANDARDS + REGULATORY_BODIES

# Search strategy: try domains in tiers
SEARCH_TIERS = [
    ("suppliers", GAS_SUPPLIERS),
    ("standards", SAFETY_STANDARDS),
    ("regulatory", REGULATORY_BODIES),
    ("all_trusted", ALL_TRUSTED_DOMAINS),
    ("open_web", None),  # Fallback to unrestricted search
]


def get_domains_for_field(field_name: str) -> list[str] | None:
    """
    Return prioritized domain list based on field type.
    Returns None for open web search.
    """
    # Physical/chemical properties → suppliers (they have detailed SDS)
    physical_properties = {
        "cas_number", "boiling_point_c", "freeze_melt_point_c", "flash_point",
        "vapor_pressure_bar", "viscosity_cp", "specific_gravity", "appearance",
        "physical_form", "ph_value"
    }
    
    # Safety/hazard classifications → standards organizations
    safety_fields = {
        "hazardous_chemical", "hazard_class", "flammability", "reactivity",
        "special", "ghs05_corrosive", "ghs08_harmful_health", "ghs07_harmful",
        "ghs04_compressed", "ghs09_environmental", "ghs03_oxidizing",
        "ghs06_toxic", "ghs02_flammable", "ghs01_explosive",
        "hazardous_statement", "fire_extinguishing_media"
    }
    
    # Building/facility codes → regulatory bodies
    facility_fields = {
        "exhausted_enclosure", "coaxal_line_dc", "gas_detection_gds",
        "lss_shutdown", "design_specialities", "exhaust_dispense",
        "exhaust_distribution", "purge_vent", "purge_panel_dispense",
        "purge_panel_distribution", "gb_fire_code_class"
    }
    
    if field_name in physical_properties:
        return GAS_SUPPLIERS + SAFETY_STANDARDS
    elif field_name in safety_fields:
        return SAFETY_STANDARDS + GAS_SUPPLIERS
    elif field_name in facility_fields:
        return REGULATORY_BODIES + GAS_SUPPLIERS
    else:
        # Generic: try all trusted sources
        return ALL_TRUSTED_DOMAINS
