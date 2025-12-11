
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

st.sidebar.header("Engine & Site Inputs")

# Rated power override for wide kW flexibility
power_kw = st.sidebar.number_input("Rated power (kW)", 200.0, 25000.0, float(m.rated_power_kw), 10.0)

# Efficiency basis (HHV default for consistency with EPA total system calc)
eff_basis = st.sidebar.selectbox("Efficiency basis", ["HHV","LHV"], index=0)
elec_eff_pct = st.sidebar.number_input("Electrical efficiency (%)", 25.0, 55.0, float(m.electrical_efficiency_pct), 0.1)

# Thermal: fixed output (kW) or efficiency (% of fuel)
use_fixed_thermal = st.sidebar.checkbox("Use thermal output (kW)", value=(m.thermal_output_kw is not None))
therm_output_kw = st.sidebar.number_input("Thermal output (kW)", 0.0, 25000.0, float(m.thermal_output_kw or 0.0), 10.0) if use_fixed_thermal else 0.0
therm_eff_pct = st.sidebar.number_input("Thermal efficiency (% of fuel)", 0.0, 60.0, 43.6, 0.1) if not use_fixed_thermal else 0.0

cap_factor = st.sidebar.slider("Capacity factor", 0.0, 1.0, 0.90, 0.01)

tariff_elec = st.sidebar.number_input("Avoided electricity ($/kWh)", 0.00, 0.75, 0.10, 0.01)
tariff_therm = st.sidebar.number_input("Thermal value ($/MMBtu)", 0.00, 40.00, 8.00, 0.10)
gas_price = st.sidebar.number_input("Gas price ($/MMBtu)", 0.00, 40.00, 5.00, 0.10)

om_fixed = st.sidebar.number_input("Fixed O&M ($/yr)", 0.0, 5_000_000.0, 50_000.0, 1000.0)
om_var = st.sidebar.number_input("Variable O&M ($/kWh)", 0.00, 0.20, 0.003, 0.001)

capex = st.sidebar.number_input("CapEx ($)", 0.0, 100_000_000.0, 3_000_000.0, 10_000.0)
itc_pct = st.sidebar.slider("IRA §48 ITC (%)", 0.0, 40.0, 30.0, 1.0) / 100.0

years = st.sidebar.slider("Project life (years)", 5, 30, 20)
debt = st.sidebar.slider("Debt fraction", 0.0, 0.9, 0.60, 0.05)
interest = st.sidebar.slider("Debt interest (real)", 0.0, 0.20, 0.07, 0.005)
term = st.sidebar.slider("Debt term (years)", 0, 25, 10)
tax_rate = st.sidebar.slider("Tax rate", 0.0, 0.50, 0.25, 0.01)

params = dict(
    power_kw=power_kw,
    cap_factor=cap_factor,
    elec_eff_pct=elec_eff_pct,
    therm_output_kw=therm_output_kw if use_fixed_thermal else 0.0,
    therm_eff_pct=therm_eff_pct if not use_fixed_thermal else 0.0,
    hh_basis=eff_basis,
    tariff_elec=tariff_elec,
    tariff_therm=tariff_therm,
    gas_price_per_mmbtu=gas_price,
    capex=capex,
    itc_pct=itc_pct,
    om_fixed=om_fixed,
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
