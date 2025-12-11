
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from catalog import all_models
from finance import annual_schedule, irr, npv, simple_payback, discounted_payback
from report import export_word

st.set_page_config(page_title="CHP Feasibility (Multi-OEM)", layout="wide")

st.title("Natural Gas CHP Feasibility & Financial Model")
st.caption("Efficiency per EPA CHP methods; OEM datasheets cited in the catalog for each model.")

# --- Load engine list across OEMs ---
models = all_models()
model_names = [f"{m.oem} {m.model_name} ({m.family})" for m in models]
sel = st.selectbox("Select engine model", model_names, index=0)
m = models[model_names.index(sel)]


# --- Sidebar organized into logical sections with tooltips (V0.2 + BTU/hr support) ---

st.sidebar.header("Inputs")

# Engine
with st.sidebar.expander("Engine", expanded=True):
    power_kw = st.number_input(
        "Rated power (kW)",
        min_value=200.0, max_value=25000.0, value=float(m.rated_power_kw), step=10.0,
        help="Override the catalog rated kW to test derating or alternate nodes."
    )
    eff_basis = st.selectbox(
        "Efficiency basis", ["HHV","LHV"], index=0,
        help="Most OEM datasheets publish LHV efficiency. Model assumes HHV by default for EPA-aligned total system comparisons."
    )
    elec_eff_pct = st.number_input(
        "Electrical efficiency (%)",
        min_value=25.0, max_value=55.0, value=float(m.electrical_efficiency_pct), step=0.1,
        help="Electrical efficiency at rated conditions. If catalog is LHV, approximate HHV by multiplying LHV by ~1.11 for pipeline NG (future V0.3: automated conversion)."
    )
    use_fixed_thermal = st.checkbox(
        "Use thermal output (BTU/hr) instead of thermal efficiency (%)",
        value=False,
        help=("Check to enter a fixed thermal output rate in BTU/hr. "
              "Uncheck to enter thermal efficiency (% of fuel input).")
    )
    if use_fixed_thermal:
        # NEW: BTU/hr input
        therm_output_btu_per_hr = st.number_input(
            "Thermal output (BTU/hr)",
            min_value=0.0, max_value=200_000_000.0, value=0.0, step=10_000.0,
            help=("Instantaneous useful heat recovery rate. The model converts BTU/hr × operating hours to "
                  "annual MMBtu (1 MMBtu = 1,000,000 BTU).")
        )
        therm_output_kw = 0.0   # not used in BTU/hr mode
        therm_eff_pct = 0.0
    else:
        therm_output_btu_per_hr = 0.0
        therm_output_kw = 0.0
        therm_eff_pct = st.number_input(
            "Thermal efficiency (% of fuel input)",
            min_value=0.0, max_value=60.0, value=43.6, step=0.1,
            help="Share of fuel input recovered as useful heat (CHP). Typical ranges 35–50% depending on engine and recovery design."
        )
    cap_factor = st.slider(
        "Capacity factor",
        min_value=0.0, max_value=1.0, value=0.90, step=0.01,
        help="Average annual operating fraction (hours/8760). 0.90 ≈ ~7,884 hours."
    )

# Tariffs & Fuel
with st.sidebar.expander("Tariffs & Fuel", expanded=True):
    tariff_elec = st.number_input(
        "Avoided electricity ($/kWh)",
        min_value=0.00, max_value=0.75, value=0.10, step=0.01,
        help="Blended or marginal energy rate you avoid buying from the grid."
    )
    tariff_therm = st.number_input(
        "Thermal value ($/MMBtu)",
        min_value=0.00, max_value=40.00, value=8.00, step=0.10,
        help=("Economic value per MMBtu of recovered heat (boiler displacement or thermal sales). "
              "Quick estimate if NG boiler: thermal value ≈ gas $/MMBtu ÷ boiler efficiency "
              "(e.g., $5 ÷ 0.80 ≈ $6.25/MMBtu).")
    )
    gas_price = st.number_input(
        "Natural gas price ($/MMBtu)",
        min_value=0.00, max_value=40.00, value=5.00, step=0.10,
        help="Delivered fuel price on HHV basis."
    )

# CapEx & O&M
with st.sidebar.expander("CapEx & O&M", expanded=True):
    capex = st.number_input(
        "CapEx ($)",
        min_value=0.0, max_value=100_000_000.0, value=3_000_000.0, step=10_000.0,
        help="Total installed cost before incentives."
    )
    om_fixed = st.number_input(
        "Fixed O&M ($/yr)",
        min_value=0.0, max_value=5_000_000.0, value=50_000.0, step=1_000.0,
        help="Annual fixed O&M (maintenance contracts, inspections, etc.)."
    )
    om_var = st.number_input(
        "Variable O&M ($/kWh)",
        min_value=0.00, max_value=0.20, value=0.003, step=0.001,
        help="Variable O&M per kWh generated (oil, consumables, overhauls allocated)."
    )

# Financing
with st.sidebar.expander("Financing", expanded=True):
    debt = st.slider(
        "Debt fraction",
        min_value=0.0, max_value=0.9, value=0.60, step=0.05,
        help=("Share of net project cost financed with debt. The remainder is equity. "
              "Debt and equity are calculated after ITC is applied.")
    )
    interest = st.slider(
        "Debt interest (real)",
        min_value=0.0, max_value=0.20, value=0.07, step=0.005,
        help="Real (post-inflation) interest rate on project debt."
    )
    term = st.slider(
        "Debt term (years)",
        min_value=0, max_value=25, value=10, step=1,
        help="Amortization term for the debt annuity payment."
    )
    tax_rate = st.slider(
        "Tax rate",
        min_value=0.0, max_value=0.50, value=0.25, step=0.01,
        help="Effective tax rate for simplified annual tax calc (V0.2 does not yet include depreciation shields)."
    )
    years = st.slider(
        "Project life (years)",
        min_value=5, max_value=30, value=20, step=1,
        help="Evaluation horizon for IRR/NPV/payback."
    )

# Policy
with st.sidebar.expander("Policy", expanded=True):
    itc_pct = st.slider(
        "IRA §48 ITC (%)",
        min_value=0.0, max_value=40.0, value=30.0, step=1.0,
        help=("Investment Tax Credit for CHP per IRA §48. Base        help=("Investment Tax Credit for CHP per IRA §48. Base 6%; up to 30% with prevailing wage "
              "and apprenticeship requirements. Additional bonuses may apply (domestic content, energy community).")



params = dict(
    power_kw=power_kw,
    cap_factor=cap_factor,
    elec_eff_pct=elec_eff_pct,
    therm_output_btu_per_hr=therm_output_btu_per_hr,  # NEW
    therm_output_kw=therm_output_kw,                  # legacy (unused if BTU/hr mode)
    therm_eff_pct=therm_eff_pct,
    hh_basis=eff_basis,
    tariff_elec=tariff_elec,
    tariff_therm=tariff_therm,
    gas_price_per_mmbtu=gas_price,
    capex=capex,
    itc_pct=itc_pct,
    om_fixed=    om_fixed=om_fixed,
    om_var_per_kwh=om_var,
    years=years,
    debt=debt,
    interest=interest,
    term=term,
    tax_rate=tax_rate

)

schedule, cf, total_eff = annual_schedule(params)

irr_val = irr(cf)
npv_rate = 0.10
npv_val = npv(npv_rate, cf)
pb = simple_payback(cf)
dpb = discounted_payback(npv_rate, cf)

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("IRR", f"{irr_val*100:0.1f}%")
col2.metric("NPV @10%", f"${npv_val:,.0f}")
col3.metric("Payback (yrs)", pb if pb is not None else ">life")
col4.metric("Disc. Payback (yrs)", dpb if dpb is not None else ">life")
col5.metric("Total Efficiency", f"{total_eff*100:0.1f}%")

# Table
df = pd.DataFrame(schedule)

# Chart
fig, ax = plt.subplots(figsize=(8,4))
ax.bar(df['year'], df['net_cf'], color="#2E86C1")
ax.set_title("Annual Cash Flow")
ax.set_xlabel("Year"); ax.set_ylabel("Net cash flow ($)")
st.pyplot(fig)
chart_path = "cashflow.png"
fig.savefig(chart_path, dpi=160, bbox_inches="tight")

st.subheader("Annual schedule")
st.dataframe(df[['year','rev_elec','rev_therm','fuel_cost','om_cost','debt_service','tax','net_cf']])

# Export report
if st.button("Export Word report"):
    kpis = {
        'engine_display': sel,
        'rated_power_kw': power_kw,
        'elec_eff_pct': elec_eff_pct,
        'total_eff_pct': total_eff*100,
        'itc_pct': itc_pct*100,
        'irr': irr_val,
        'npv_rate': npv_rate,
        'npv': npv_val,
        'payback': pb if pb is not None else -1,
        'disc_payback': dpb if dpb is not None else -1,
    }
    outfile = export_word(kpis, schedule, chart_path, outfile="CHP_Report.docx")
    st.success(f"Report saved: {outfile}")
    with open(outfile, "rb") as f:
        st.download_button("Download CHP_Report.docx", f, file_name="CHP_Report.docx")

