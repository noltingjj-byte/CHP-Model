
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class EngineModel:
    oem: str
    family: str
    model_name: str
    rated_power_kw: float             # nominal continuous kW at site frequency
    electrical_efficiency_pct: float  # assumed HHV unless noted (UI toggle available)
    thermal_output_kw: Optional[float]
    frequency_hz: int
    voltage_options: List[str]
    fuel_type: str
    reference_url: str
    notes: str

# ---------------------------
# Caterpillar
# Sources:
# - CAT CHP1500 (G3512H) page: ~1.49 MW, max electrical efficiency ~42.5%  https://www.cat.com/en_GB/products/new/power-systems/electric-power/gas-generator-sets/113841.html
# - G3520H Scene7 datasheet: configurations, efficiency options  https://s7d2.scene7.com/is/content/Caterpillar/CM20190904-a8775-29c11
# ---------------------------
def cat_models() -> List[EngineModel]:
    return [
        EngineModel(
            oem="Caterpillar",
            family="G3512H / CHP1500",
            model_name="G3512H",
            rated_power_kw=1490.0,
            electrical_efficiency_pct=42.5,  # CAT cites max electrical efficiency ~42.5%
            thermal_output_kw=1490.0 * 0.436,  # illustrative pack thermal eff × power
            frequency_hz=60,
            voltage_options=["4.16 kV"],
            fuel_type="Natural Gas",
            reference_url="https://www.cat.com/en_GB/products/new/power-systems/electric-power/gas-generator-sets/113841.html",
            notes="CHP1500 standardized enclosure; combined efficiency cited by Caterpillar."
        ),
        EngineModel(
            oem="Caterpillar",
            family="G3520H",
            model_name="G3520H",
            rated_power_kw=2476.0,  # representative within brochure range
            electrical_efficiency_pct=43.5,  # representative high-efficiency config; confirm HHV/LHV on site
            thermal_output_kw=None,
            frequency_hz=60,
            voltage_options=["4.16 kV"],
            fuel_type="Natural Gas",
            reference_url="https://s7d2.scene7.com/is/content/Caterpillar/CM20190904-a8775-29c11",
            notes="Multiple configurations (fuel tolerant vs. high efficiency); check emissions and ambient corrections."
        ),
    ]

# ---------------------------
# INNIO Jenbacher (Type 6)
# Source: J620 product page (electrical output up to ~3.36 MW; up to ~45.9% electrical efficiency)  https://www.jenbacher.com/en/gas-engines/type-6/j620/
# ---------------------------
def jenbacher_models() -> List[EngineModel]:
    return [
        EngineModel(
            oem="INNIO Jenbacher",
            family="Type 6",
            model_name="J620",
            rated_power_kw=3360.0,            # top-of-range for quick comparisons
            electrical_efficiency_pct=45.9,   # “up to 45.9%” (50 Hz)
            thermal_output_kw=None,
            frequency_hz=50,
            voltage_options=["6.3 kV","10.5 kV","11 kV","15 kV"],
            fuel_type="Natural Gas / Biogas",
            reference_url="https://www.jenbacher.com/en/gas-engines/type-6/j620/",
            notes="Electrical output up to ~3.36 MW; electrical efficiency up to ~45.9% (50 Hz). Confirm variant and ambient."
        ),
        EngineModel(
            oem="INNIO Jenbacher",
            family="Type 6",
            model_name="J620 (60 Hz)",
            rated_power_kw=3350.0,
            electrical_efficiency_pct=45.0,   # “up to 45.0%” at 60 Hz variants
            thermal_output_kw=None,
            frequency_hz=60,
            voltage_options=["6.3 kV","10.5 kV","11 kV","15 kV"],
            fuel_type="Natural Gas / Biogas",
            reference_url="https://www.jenbacher.com/en/gas-engines/type-6/j620/",
            notes="60 Hz variant; electrical efficiency up to ~45.0% depending on model."
        ),
    ]

# ---------------------------
# MTU / Rolls-Royce (Series 4000)
# Sources:
# - MTU natural gas gensets overview (250–2535 kW, CHP/CHPC)  https://www.mtu-solutions.com/eu/en/applications/power-generation/power-generation-products/gas-generator-sets/natural-gas-generator-sets.html
# - Distributor datasheets (Curtis Power)  https://www.curtispowersolutions.com/specs-mtu-continuous-gas-gensets
# ---------------------------
def mtu_models() -> List[EngineModel]:
    return [
        EngineModel(
            oem="MTU / Rolls-Royce",
            family="Series 4000",
            model_name="16V4000 (60 Hz)",
            rated_power_kw=2514.0,            # upper end of 60 Hz range
            electrical_efficiency_pct=41.5,   # representative; confirm per latest datasheet
            thermal_output_kw=None,
            frequency_hz=60,
            voltage_options=["480 V","4.16 kV"],
            fuel_type="Natural Gas",
            reference_url="https://www.mtu-solutions.com/eu/en/applications/power-generation/power-generation-products/gas-generator-sets/natural-gas-generator-sets.html",
            notes="CHP/CHPC capable; distributor literature cites overall CHP efficiency up to ~91.9%."
        ),
        EngineModel(
            oem="MTU / Rolls-Royce",
            family="Series 4000",
            model_name="12V4000 (60 Hz)",
            rated_power_kw=2010.0,            # representative mid-range
            electrical_efficiency_pct=42.0,   # representative; verify for your node
            thermal_output_kw=None,
            frequency_hz=60,
            voltage_options=["480 V","4.16 kV"],
            fuel_type="Natural Gas",
            reference_url="https://www.curtispowersolutions.com/specs-mtu-continuous-gas-gensets",
            notes="Curtis Power specs provide model datasheets; confirm electrical efficiency and heat balances."
        ),
    ]

# ---------------------------
# MAN Energy Solutions
# Sources:
# - MAN V51/60G brochure (~50% electrical; up to ~95% total efficiency CHP)  https://studylib.net/doc/26051374/man-v51-60g-eng
# - MAN E3262 overview  https://www.man.eu/engines/en/products/power-generation/gas/man-motor-e3262.html
# - MAN E3268 datasheet (CHP/COP variants)  https://www.gasengineexchange.com/landing/file/MAN%20E3268%20gas%20engine%20CHP.pdf
# - MAN portfolio brochure (E0834/E0836/E2676/E3268/E3262)  https://martinenergygroup.com/wp-content/uploads/2019/01/Power_Gas_EN_150927_web-MAN.pdf
# ---------------------------
def man_models() -> List[EngineModel]:
    return [
        EngineModel(
            oem="MAN Energy Solutions",
            family="51/60G",
            model_name="18V51/60G (2-stage TC)",
            rated_power_kw=20700.0,           # brochure shows up to ~20,700 kWm; adjust to kWe with alternator efficiency if needed
            electrical_efficiency_pct=50.0,   # “~50% in single cycle; up to ~95% total in CHP” (representative)
            thermal_output_kw=None,
            frequency_hz=50,
            voltage_options=["Medium voltage (site-specific)"],
            fuel_type="Natural Gas (H2-blend capable variants)",
            reference_url="https://studylib.net/doc/26051374/man-v51-60g-eng",
            notes="High-efficiency large engine; adjust kWe vs. kWm per alternator; confirm local site configuration."
        ),
        EngineModel(
            oem="MAN Engines",
            family="E3262",
            model_name="E3262 LE232 (Natural Gas)",
            rated_power_kw=550.0,             # representative mech output; adjust electrical as needed
            electrical_efficiency_pct=39.6,   # representative; verify per site datasheet
            thermal_output_kw=None,
            frequency_hz=50,
            voltage_options=["400 V / MV (site-specific)"],
            fuel_type="Natural Gas",
            reference_url="https://www.man.eu/engines/en/products/power-generation/gas/man-motor-e3262.html",
            notes="12‑cyl forced induction variant; CHP total efficiency reported ~93.6% in literature (verify)."
        ),
        EngineModel(
            oem="MAN Engines",
            family="E3268",
            model_name="E3268 (8V)",
            rated_power_kw=390.0,
            electrical_efficiency_pct=39.0,   # representative; confirm per node
            thermal_output_kw=None,
            frequency_hz=60,
            voltage_options=["480 V / MV (site-specific)"],
            fuel_type="Natural Gas / Special Gases",
            reference_url="https://www.gasengineexchange.com/landing/file/MAN%20E3268%20gas%20engine%20CHP.pdf",
            notes="Datasheet covers COP/CHP variants; verify local fuel HHV/LHV and heat recovery configuration."
        ),
        EngineModel(
            oem="MAN Engines",
            family="E2676",
            model_name="E2676 (6L)",
            rated_power_kw=220.0,
            electrical_efficiency_pct=38.0,   # representative; confirm per node
            thermal_output_kw=None,
            frequency_hz=50,
            voltage_options=["400 V / MV"],
            fuel_type="Natural Gas / Biogas",
            reference_url="https://martinenergygroup.com/wp-content/uploads/2019/01/Power_Gas_EN_150927_web-MAN.pdf",
            notes="Brochure summarizes CHP suitability and outputs for E‑series engines."
        ),
    ]

# ---------------------------
# Cummins Gas Gensets
# Sources:
# - HSK78G spec sheet (1.6–2.0 MW)  https://www.cummins.com/sites/default/files/2019-08/Spec-Sheet-HSK78G-50Hz_2.pdf
# - C1000 N6C / QSK60G datasheet  https://www.cummins.com/sites/default/files/2020-02/C1000N6C%20-%20D-6203.pdf
# - C1400 N6C datasheet  https://www.cumminsperu.pe/uploads/shares/DATA_SHEETS/DATA_SHEET_GAS_NATURAL/C1400N6C.pdf
# - Portfolio overview  https://www.cummins.com/na/sales-and-service/natural-gas-gensets
# ---------------------------
def cummins_models() -> List[EngineModel]:
    return [
        EngineModel(
            oem="Cummins",
            family="HSK78G",
            model_name="C1600 N5CD (50 Hz) / C1600 N6CD (60 Hz)",
            rated_power_kw=1600.0,            # series spans 1600–2000 kW
            electrical_efficiency_pct=41.0,   # datasheet example shows ~41% electrical efficiency (representative)
            thermal_output_kw=None,
            frequency_hz=60,
            voltage_options=["480 V","4.16 kV","MV (per alternator)"],
            fuel_type="Natural Gas (lean-burn)",
            reference_url="https://www.cummins.com/sites/default/files/2019-08/Spec-Sheet-HSK78G-50Hz_2.pdf",
            notes="Lean‑burn with detailed heat balance and emissions; multiple models 1.6–2.0 MW."
        ),
        EngineModel(
            oem="Cummins",
            family="QSK60G",
            model_name="C1000 N6C (60 Hz)",
            rated_power_kw=1000.0,
            electrical_efficiency_pct=41.0,   # example table shows ~41% at 100% load (representative)
            thermal_output_kw=None,
            frequency_hz=60,
            voltage_options=["480 V","4.16 kV"],
            fuel_type="Natural Gas (lean-burn)",
            reference_url="https://www.cummins.com/sites/default/files/2020-02/C1000N6C%20-%20D-6203.pdf",
            notes="Data sheet provides fuel consumption, electrical efficiency, and heat balance; NSPS variants exist."
        ),
        EngineModel(
            oem="Cummins",
            family="QSK60G",
            model_name="C1400 N6C (60 Hz)",
            rated_power_kw=1400.0,
            electrical_efficiency_pct=40.0,   # representative; confirm per alternator & load point
            thermal_output_kw=None,
            frequency_hz=60,
            voltage_options=["480 V","4.16 kV"],
            fuel_type="Natural Gas (lean-burn)",
            reference_url="https://www.cumminsperu.pe/uploads/shares/DATA_SHEETS/DATA_SHEET_GAS_NATURAL/C1400N6C.pdf",
            notes="Spec sheet outlines emissions options (0.7–1.0 g/hp-hr NOx) and CHP applicability."
        ),
        EngineModel(
            oem="Cummins",
            family="Portfolio Overview",
            model_name="Natural Gas Gensets (55–2000 kW)",
            rated_power_kw=1000.0,            # placeholder mid-range for overview entry
            electrical_efficiency_pct=40.0,   # portfolio overview; use model-specific sheets for exact values
            thermal_output_kw=None,
            frequency_hz=60,
            voltage_options=["480 V","4.16 kV","MV"],
            fuel_type="Natural Gas / Dual Fuel",
            reference_url="https://www.cummins.com/na/sales-and-service/natural-gas-gensets",
            notes="Portfolio page—use specific datasheets for performance; HSK/QSK lines cover 1–2 MW nodes."
        ),
    ]

# ---------------------------
# Aggregate helper
# ---------------------------
def all_models() -> List[EngineModel]:
    """Return all engines across OEMs."""
    return cat_models() + jenbacher_models() + mtu_models() + man_models() + cummins_models()
