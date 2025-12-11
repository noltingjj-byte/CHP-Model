
import math

def irr(cashflows, guess=0.1, max_iter=100, tol=1e-6):
    """Compute IRR via Newton-Raphson."""
    r = guess
    for _ in range(max_iter):
        npv = sum(cf / ((1 + r) ** i) for i, cf in enumerate(cashflows))
        dnpv = sum(-i * cf / ((1 + r) ** (i + 1)) for i, cf in enumerate(cashflows))
        if abs(dnpv) < 1e-14:
            break
        r_new = r - npv / dnpv
        if abs(r_new - r) < tol:
            return r_new
        r = r_new
    return r

def npv(rate, cashflows):
    return sum(cf / ((1 + rate) ** i) for i, cf in enumerate(cashflows))

def simple_payback(cashflows):
    cum = 0.0
    for i, cf in enumerate(cashflows):
        cum += cf
        if cum >= 0:
            return i
    return None

def discounted_payback(rate, cashflows):
    cum = 0.0
    for i, cf in enumerate(cashflows):
        cum += cf / ((1 + rate) ** i)
        if cum >= 0:
            return i
    return None

def annual_schedule(params):
    """
    Core model for energy + cash flows (annual).
    params keys:
      power_kw, cap_factor, elec_eff_pct, therm_output_kw OR therm_eff_pct,
      hh_basis ('HHV'/'LHV'), tariff_elec, tariff_therm, gas_price_per_mmbtu,
      capex, itc_pct, om_fixed, om_var_per_kwh, years, debt, interest, term, tax_rate
    """
    hrs = 8760 * params['cap_factor']
    elec_kwh = params['power_kw'] * hrs

    # Electrical efficiency fraction (HHV basis by default)
    elec_eff_frac = params['elec_eff_pct'] / 100.0

    # kWh → MMBtu (HHV)
    kwh_to_mmbtu = 0.003412

    # Fuel input (MMBtu) based on electrical efficiency
    fuel_mmbtu_total = elec_kwh * (kwh_to_mmbtu / elec_eff_frac)

    # Useful thermal energy (MMBtu)
    if params.get('therm_output_kw'):
        therm_mmbtu = params['therm_output_kw'] * hrs * kwh_to_mmbtu
        therm_eff_frac = therm_mmbtu / fuel_mmbtu_total if fuel_mmbtu_total > 0 else 0.0
    else:
        therm_eff_frac = (params.get('therm_eff_pct', 0.0) / 100.0)
        therm_mmbtu = fuel_mmbtu_total * therm_eff_frac

    # Total system efficiency (EPA definition)
    # EPA reference: CHP total system efficiency is (We + Qth) / Qfuel.
    total_eff = (elec_kwh * kwh_to_mmbtu + therm_mmbtu) / fuel_mmbtu_total if fuel_mmbtu_total > 0 else 0.0

    # Value streams
    rev_elec = elec_kwh * params['tariff_elec']
    rev_therm = therm_mmbtu * params['tariff_therm']

    # Fuel & O&M
    fuel_cost = fuel_mmbtu_total * params['gas_price_per_mmbtu']
    om_cost = params['om_fixed'] + params['om_var_per_kwh'] * elec_kwh

    # CapEx net of ITC (IRA §48)
    capex_net = params['capex'] * (1 - params['itc_pct'])

    # Debt service (level payment)
    debt_amt = params['debt'] * capex_net
    equity_amt = (1 - params['debt']) * capex_net
    ann = 0.0
    if debt_amt > 0 and params['term'] > 0 and params['interest'] > 0:
        i = params['interest']
        n = params['term']
        ann = debt_amt * (i * (1 + i) ** n) / ((1 + i) ** n - 1)

    schedule, cashflows = [], []

    # Year 0
    schedule.append({
        'year': 0, 'elec_kwh': 0, 'therm_mmbtu': 0, 'fuel_mmbtu': 0,
        'rev_elec': 0, 'rev_therm': 0, 'fuel_cost': 0, 'om_cost': 0,
        'debt_service': 0, 'tax': 0, 'net_cf': -capex_net, 'total_eff': total_eff
    })
    cashflows.append(-capex_net)

    for y in range(1, params['years'] + 1):
        gross = rev_elec + rev_therm
        op_costs = fuel_cost + om_cost
        ebitda = gross - op_costs
        tax = max(0.0, (ebitda - ann)) * params['tax_rate']  # simplified tax
        net = ebitda - ann - tax
        schedule.append({
            'year': y, 'elec_kwh': elec_kwh, 'therm_mmbtu': therm_mmbtu,
            'fuel_mmbtu': fuel_mmbtu_total, 'rev_elec': rev_elec,
            'rev_therm': rev_therm, 'fuel_cost': fuel_cost, 'om_cost': om_cost,
            'debt_service': ann, 'tax': tax, 'net_cf': net, 'total_eff': total_eff
        })
        cashflows.append(net)

    return schedule, cashflows, total_eff
