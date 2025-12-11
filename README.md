
# CHP Feasibility & Financial Model (Streamlit)

A web-based model to evaluate Combined Heat and Power (CHP) projects using manufacturer engine specs (CAT, Jenbacher, MTU, MAN, Cummins) and EPA methods for total system efficiency. Outputs include IRR, NPV, simple/discounted payback, annual cash-flow schedules, and exportable reports.

## Features
- Engine catalog across major OEMs
- Electrical & thermal efficiency inputs (HHV default)
- Tariff, fuel price, CapEx, O&M, IRA §48 ITC toggles
- IRR, NPV, payback, total efficiency
- Word report export (tables + chart)

## Methodology & References
- **EPA CHP efficiency methods** (total system efficiency): https://www.epa.gov/chp/methods-calculating-chp-efficiency
- **Caterpillar G3512H (CHP1500) & G3520H** specs: 
  - https://www.cat.com/en_GB/products/new/power-systems/electric-power/gas-generator-sets/113841.html
  - https://s7d2.scene7.com/is/content/Caterpillar/CM20190904-a8775-29c11
- **INNIO Jenbacher J620** (Type 6): https://www.jenbacher.com/en/gas-engines/type-6/j620/
- **MTU Series 4000**: 
  - https://www.mtu-solutions.com/eu/en/applications/power-generation/power-generation-products/gas-generator-sets/natural-gas-generator-sets.html
  - https://www.curtispowersolutions.com/specs-mtu-continuous-gas-gensets
- **MAN Engines**:
  - 51/60G brochure: https://studylib.net/doc/26051374/man-v51-60g-eng
  - E3262 overview: https://www.man.eu/engines/en/products/power-generation/gas/man-motor-e3262.html
  - E3268 datasheet: https://www.gasengineexchange.com/landing/file/MAN%20E3268%20gas%20engine%20CHP.pdf
  - Portfolio: https://martinenergygroup.com/wp-content/uploads/2019/01/Power_Gas_EN_150927_web-MAN.pdf
- **Cummins**:
  - HSK78G: https://www.cummins.com/sites/default/files/2019-08/Spec-Sheet-HSK78G-50Hz_2.pdf
  - C1000 N6C: https://www.cummins.com/sites/default/files/2020-02/C1000N6C%20-%20D-6203.pdf
  - C1400 N6C: https://www.cumminsperu.pe/uploads/shares/DATA_SHEETS/DATA_SHEET_GAS_NATURAL/C1400N6C.pdf
  - Portfolio: https://www.cummins.com/na/sales-and-service/natural-gas-gensets
- **IRA §48 ITC** overview (business incentives): https://www.irs.gov/pub/irs-pdf/p5886.pdf

> Note: Efficiency bases (HHV/LHV) vary by manufacturer. This app assumes HHV for consistency in total system efficiency; you can toggle basis and adjust inputs per site data.

## Run Locally
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
